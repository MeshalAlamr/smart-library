from flask import Flask
import sys
import os

app = Flask(__name__, static_folder='../../frontend/static',
            template_folder='../../frontend/templates')


from backend.app import routes