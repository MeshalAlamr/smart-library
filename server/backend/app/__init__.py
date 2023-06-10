from flask import Flask
import sys
import os
from flask_pymongo import PyMongo

app = Flask(__name__, static_folder='../../frontend/static',
            template_folder='../../frontend/templates')

app.config['MONGO_URI'] = 'mongodb://mongodb:27017/mltask'

mongo = PyMongo(app)

from backend.app import routes