import io 
import pytesseract
import uvicorn

from fastapi import FastAPI, Form, UploadFile, File
from pdf2image import convert_from_bytes
from typing import Dict, Optional, List, Annotated

app = FastAPI()

def extract_text_from_pdf(pdf: bytes) -> str:
    """
    A function to convert multi-page pdf to images
    @misc{PythonTe58:online,
    author = {},
    title = {Python Tesseract PDF & OCR Example - Data Analytics},
    howpublished = {url{https://vitalflux.com/python-tesseract-pdf-ocr-example/}},
    month = {},
    year = {},
    note = {(Accessed on 06/01/2023)}
    }
    """
    # Changed from path to bytes and pass pdf as byte data
    pages = convert_from_bytes(pdf)
     
    # Extract text from each page using Tesseract OCR
    text_data = ''
    for page in pages:
        text = pytesseract.image_to_string(page)
        text_data += text + '\n'
     
    # Return the text data
    return text_data

@app.get('/status', status_code=200)
async def status() -> Dict:
    """
    A function to check the status of the server.
    """
    return {'Status': 'OK!'}

@app.post('/extract', status_code=200)
async def extract(file: Annotated[bytes, File()]) -> Dict: 
    """
    A function that extracts text from PDF documents.
    """
    
    pdf_text = extract_text_from_pdf(file)
    return {'data': pdf_text}

    
if __name__ == "__main__":
    uvicorn.run('server:app', reload=True)