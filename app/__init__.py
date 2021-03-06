from flask import Flask
from config import Config, basedir
from google.cloud import firestore
from google.cloud import storage


app = Flask(__name__)
app.config.from_object(Config)
firedb = firestore.Client()
db = storage.Client()

from app import routes, models

from data.comparison_data import a_l_c_comp, s_l_c_comp, a_l_p_comp, s_l_p_comp
from functions_and_classes.display_only_ops import article_comps as ac
