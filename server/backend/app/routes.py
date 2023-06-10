from flask import app, jsonify, render_template, request, redirect, url_for, flash
import requests
from backend.app import app
from tempfile import NamedTemporaryFile
import os
import base64
from io import BytesIO
import time

# time.sleep(10)
backend_url = os.getenv("BACKEND_API_ADDRESS", "localhost")
backend_url = f"http://{backend_url}:8000"

try:
    requests.get(f'{backend_url}/status')
except requests.exceptions.ConnectionError or ConnectionRefusedError:
    assert False, "Backend server is not running."
# response = requests.get(f'{backend_url}/status')
# if response.status_code != 200 or response.json()['Status'] != 'OK!':
#     assert False, "Backend server is not running."

from backend.app import mongo

# print("Waiting for MongoDB to start...")
# while True:
#     try:
#         mongo.db.list_collection_names()
#         break
#     except:
#         time.sleep(1)
# print("MongoDB started.")

# print("Waiting for backend server to start...")
# while True:
#     try:
#         response = requests.get(f'{backend_url}/status')
#         if response.status_code == 200 and response.json()['Status'] == 'OK!':
#             break
#     except:
#         time.sleep(1)
# print("Backend server started.")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'input-form' in request.form:
            print("Processing document...")
            file = request.files['pdf']
            if not file:
                return render_template("index.html")
            
            # Encode the file content as base64
            file_content = file.read()
            file_encoded = base64.b64encode(file_content).decode('utf-8')

            # Send the file to the backend server
            print("Extracting text from PDF...")
            response = requests.post(f'{backend_url}/extract', json={'file': file_encoded})
            if response.status_code == 200:
                extracted_text = response.json()['data']
            else:
                return render_template("index.html", msg="Error: Could not extract text from PDF.")

            print("Summarizing text...")
            response = requests.post(f'{backend_url}/summarize', json={'text': extracted_text})
            if response.status_code == 200:
                summary = response.json()['data']
            
            print("Predicting topics...")
            response = requests.post(f'{backend_url}/topic', json={'text': summary})
            if response.status_code == 200:
                topics = response.json()['data']

            print("Predicting sentiment...")
            response = requests.post(f'{backend_url}/sentiment', json={'text': summary})
            if response.status_code == 200:
                sentiment = response.json()['data']
            
            print("Formatting data...")
            document = {
                'type': request.form['type'].title(),
                'name': request.form['name'],
                'author': request.form['author'],
                'year': request.form['year'],
                'publisher': request.form['publisher'],
                'summary': summary,
                'topics': topics,
                'sentiment': sentiment
            }
            return render_template("index.html", document=document)
        
        elif 'preview-form' in request.form:
            if "cancel-button" in request.form:
                return render_template("index.html", msg="Document not inserted. Operation cancelled.")
            else:
                document = {
                    'type': request.form['type'],
                    'name': request.form['name'],
                    'author': request.form['author'],
                    'year': request.form['year'],
                    'publisher': request.form['publisher'],
                    'summary': request.form['summary'],
                    'topics': request.form['topics'],
                    'sentiment': request.form['sentiment']
                }
                response = requests.post(f'{backend_url}/insert', json={'document': document})
                if response.status_code == 200:
                    print("Document inserted successfully!")
                return render_template("index.html", msg="Document inserted successfully!")
        else:
            return render_template("index.html")
    return render_template("index.html", document="ay")

if __name__ == "__main__":
    app.run(debug=True)

