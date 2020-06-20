from flask import Flask
from config import config
from google.cloud import firestore
from google.cloud import storage
from functions_and_


app = Flask(__name__)
app.config.from_object(config
db = firestore.Client()

from app import routes, models
