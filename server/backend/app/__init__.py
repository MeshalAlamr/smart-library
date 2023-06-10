import os
import sys

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(
    __name__,
    static_folder="../../frontend/static",
    template_folder="../../frontend/templates",
)

mongo_url = os.getenv("MONGO_ADDRESS", "localhost")
mongo_url = f"mongodb://{mongo_url}:27017/mltask"
app.config["MONGO_URI"] = mongo_url

mongo = PyMongo(app)

from backend.app import routes
