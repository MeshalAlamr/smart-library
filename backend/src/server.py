import io
import pytesseract
from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import base64

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Meshal\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

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

@app.route('/status', methods=['GET'])
def status():
    """
    A function to check the status of the server.
    """
    return jsonify({'Status': 'OK!'})

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
