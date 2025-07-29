from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil, os, uuid
from ocr_qa_utils import ocr_pdf, ocr_image_file, llm_ocr_text, process_document

app = FastAPI()
qa_chain = None

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global qa_chain
    ext = file.filename.split('.')[-1].lower()
    file_path = f"temp/{uuid.uuid4()}.{ext}"
    os.makedirs("temp", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if ext == "pdf":
        raw_text = ocr_pdf(file_path)
    elif ext in ["png", "jpg", "jpeg"]:
        raw_text = ocr_image_file(file_path)
    else:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

    cleaned_text = llm_ocr_text(raw_text)
    qa_chain = process_document(cleaned_text)
    
    return {"message": "File processed and QA system ready."}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    global qa_chain
    if qa_chain is None:
        return JSONResponse(status_code=400, content={"error": "Upload and process a file first."})
    
    response = qa_chain.invoke({"question": question})
    return {"answer": response["answer"]}
