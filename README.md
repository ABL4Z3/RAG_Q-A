# OCR + LLM Question Answering System

This project is an OCR (Optical Character Recognition) and LLM (Large Language Model) based Question Answering system. It allows users to upload PDF or image documents, extracts text using OCR, processes the text with language models, and enables users to ask questions about the content of the uploaded documents.

## Features

- Upload PDF or image files (PNG, JPG, JPEG)
- Extract text from documents using OCR
- Process extracted text with language models for question answering
- Interactive web interface using Streamlit
- Backend API built with FastAPI

## Installation

1. Clone the repository and navigate to the project directory.

2. Create a Python virtual environment and activate it:

```bash
python -m venv myenv
# On Windows
myenv\Scripts\activate
# On macOS/Linux
source myenv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Backend

Start the FastAPI backend server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

The backend will be available at `http://localhost:8001`.

## Running the Frontend

Start the Streamlit frontend app:

```bash
streamlit run frontend/app.py
```

The frontend will open in your default web browser.

## Usage

1. Use the frontend interface to upload a PDF or image file.

2. The backend will process the file, extract text, and prepare the question answering system.

3. Enter your questions in the frontend input box and get answers based on the uploaded document.

## Project Structure

```
.
├── backend/
│   ├── main.py            # FastAPI backend application
│   ├── ocr_qa_utils.py    # OCR and QA utility functions for backend
├── frontend/
│   ├── app.py             # Streamlit frontend application
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation

```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
