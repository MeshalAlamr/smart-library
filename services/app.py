import os
import pytesseract
from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import base64
import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from flask_pymongo import PyMongo
from scipy.special import expit
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# summarizer_hf = "pszemraj/led-base-book-summary"
summarizer_hf = "models/summarizer"

summarizer_pipeline = pipeline(
    "summarization",
    summarizer_hf,
    device=0 if torch.cuda.is_available() else -1,
)

# topic_hf = "cardiffnlp/tweet-topic-21-multi"
topic_hf = "models/topic_model"
topic_tokenizer = AutoTokenizer.from_pretrained(topic_hf)
topic_model = AutoModelForSequenceClassification.from_pretrained(topic_hf)
topic_class_mapping = topic_model.config.id2label


# sentiment_hf = "cardiffnlp/twitter-roberta-base-sentiment"
sentiment_hf = "models/sentiment_pipeline"

sentiment_labels = {
    "LABEL_0": 'negative',
    "LABEL_1": 'neutral',
    "LABEL_2": 'positive'
}

sentiment_pipeline = pipeline(
    task='sentiment-analysis',
    model=sentiment_hf,
    device=0 if torch.cuda.is_available() else -1
    )

similarity_hf = "sentence-transformers/all-MiniLM-L6-v2"
similarity_model = SentenceTransformer(similarity_hf)

app = Flask(__name__)

if not os.getenv("CONTAINERIZED", False):
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Users\Meshal\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    )

mongo_url = os.getenv("MONGO_ADDRESS", "localhost")
mongo_url = f"mongodb://{mongo_url}:27017/mltask"
app.config['MONGO_URI'] = mongo_url

mongo = PyMongo(app)
resources = mongo.db.resources
queries = mongo.db.queries


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
    summary = summarizer_pipeline(
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
    """
    A function that inserts documents into the database.
    """
    try:
        mongo.db.list_collection_names()
    except:
        return jsonify({"data": "An error occurred while connecting to the database. Please try again later."})
    if request.method == 'POST':
        data = request.get_json()
        document = data['document']
        result = resources.insert_one(document)  
        print("Inserted document ID: ,", result.inserted_id)
        return jsonify({"data": "Document inserted successfully!"})

@app.route("/topic", methods=["POST"])
def topic():
    """
    A function that predicts topics of a text.
    """
    data = request.get_json()
    text = data["text"]
    print("predicting topics...")
    tokens = topic_tokenizer(text, return_tensors='pt')
    output = topic_model(**tokens)
    scores = expit(output[0][0].detach().numpy())
    predictions = (scores >= 0.4) * 1

    topics = []
    # Map to classes
    for i in range(len(predictions)):
        if predictions[i]:
            pred = topic_class_mapping[i].replace('_', ' ').title()
            topics.append(pred)
    
    # join topics with comma
    topics = ", ".join(topics)

    return jsonify({"data": topics})

@app.route("/sentiment", methods=["POST"])
def sentiment():
    """
    A function that predicts the sentiment of a text.
    """
    data = request.get_json()
    text = data["text"]

    print("predicting sentiment...")
    predicted_sentiment = sentiment_pipeline(text)[0]['label']
    predicted_sentiment = sentiment_labels[predicted_sentiment].title()

    return jsonify({"data": predicted_sentiment})

@app.route("/search", methods=["POST"])
def search():
    """
    A function that searches for documents in the database.
    """
    data = request.get_json()
    query = data["query"]
    print("searching for documents...")
    query_vector = similarity_model.encode([query])
    documents = resources.find()
    results = []
    for document in documents:
        if 'summary' not in document:
            continue
        document_vector = similarity_model.encode([document['summary']])
        similarity_score = cosine_similarity(query_vector, document_vector)[0][0]
        results.append((document, similarity_score))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    results = [result[0] for result in results]

    if len(results) == 0:
        print("No results found.")

    document = {
        'type': document['type'] if document['type'] else 'None',
        'name': document['name'] if document['name'] else 'None',
        'author': document['author'] if document['author'] else 'None',
        'year': document['year'] if document['year'] else 'None',
        'publisher': document['publisher'] if document['publisher'] else 'None',
        'summary': document['summary'] if document['summary'] else 'None',
        'topics': document['topics'] if document['topics'] else 'None',
        'sentiment': document['sentiment'] if document['sentiment'] else 'None',
    }
    print(results)
    return jsonify({"data": document})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)