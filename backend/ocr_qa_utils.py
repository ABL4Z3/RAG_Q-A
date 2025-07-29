import os
import time
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import warnings
warnings.filterwarnings("ignore")

from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# ------------------------- #
# Configuration
# ------------------------- #

TESSERACT_PATH = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
POPPLER_PATH = r"C:\\Program Files\\poppler-24.08.0\\Library\\bin"
OPENAI_API_KEY = ""  # Use environment variable in production
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# ------------------------- #
# OCR Functions
# ------------------------- #

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
llm_cleaner = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

def ocr_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)

def ocr_pdf(pdf_path: str, dpi: int = 300) -> str:
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=POPPLER_PATH)
    full_text = []
    for page_num, image in enumerate(images):
        text = ocr_image(image)
        full_text.append(f"\n--- Page {page_num+1} ---\n{text.strip()}")
    return "\n".join(full_text)

def ocr_image_file(image_path: str) -> str:
    image = Image.open(image_path)
    return ocr_image(image)

def llm_ocr_text(text: str) -> str:
    prompt = f"""
I have OCR-extracted text from a document, but it's very unstructured and messy.
Please:
- Fix grammar and punctuation
- Clean headers/footers/line breaks
- Structure the paragraphs logically
- Maintain technical terms

\n{text}
"""
    response = llm_cleaner.invoke(prompt)
    return response.content

# ------------------------- #
# Main Processing Pipeline
# ------------------------- #

def process_document(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=5500, chunk_overlap=500)
    chunks = splitter.split_text(text)
    documents = [Document(page_content=chunk, metadata={"chunk_id": i}) for i, chunk in enumerate(chunks)]

    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vectorstore = FAISS.from_documents(documents, embedding_model)

    retriever = vectorstore.as_retriever()
    llm_qa = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm_qa,
        retriever=retriever,
        memory=memory
    )
    return qa_chain
