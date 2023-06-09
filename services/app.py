import io
import pytesseract
from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import base64
import torch
from transformers import pipeline
from flask_pymongo import PyMongo

hf_name = "pszemraj/led-base-book-summary"

summarizer = pipeline(
    "summarization",
    hf_name,
    device=0 if torch.cuda.is_available() else -1,
    # device = -1,
)

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Meshal\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mltask'

mongo = PyMongo(app)


def extract_text_from_pdf(pdf):
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
    pages = convert_from_bytes(pdf)
    text_data = ""
    for page in pages:
        text = pytesseract.image_to_string(page)
        text_data += text + "\n"
    return text_data




@app.route("/status", methods=["GET"])
def status():
    """
    A function to check the status of the server.
    """
    return jsonify({"Status": "OK!"})


@app.route("/extract", methods=["POST"])
def extract():
    """
    A function that extracts text from PDF documents.
    """
    data = request.get_json()
    file_encoded = data["file"]
    file_content = base64.b64decode(file_encoded)
    print("extracting text from pdf...")
    pdf_text = extract_text_from_pdf(file_content)
    return jsonify({"data": pdf_text})


@app.route("/summarize", methods=["POST"])
def summarize():
    """
    A function that summarizes text.
    """
    data = request.get_json()
    text = data["text"]
    print("summarizing text...")
    summary = summarizer(
        text,
        min_length=8,
        max_length=1000,
        no_repeat_ngram_size=3,
        encoder_no_repeat_ngram_size=3,
        repetition_penalty=3.5,
        num_beams=4,
        do_sample=False,
        early_stopping=True,
    )[0]["summary_text"]
    return jsonify({"data": summary})

@app.route("/insert", methods=["POST"])
def insert_documents():
    resources = mongo.db.resources
    if request.method == 'POST':
        data = request.get_json()
        document = data['document']
        result = resources.insert_one(document)  
        print("Inserted document ID: ,", result.inserted_id)
        return jsonify({"data": "Document inserted successfully!"})

if __name__ == "__main__":
    app.run(debug=True, port="8000")
