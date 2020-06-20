from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, NewGreenCoffee, NewRoastSession, NewRoastedCoffee, NewTastingSession
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, GreenCoffee, RoastSession, RoastedCoffee, TastingSession
from google.cloud import firestore


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Personal Identity in Hume's Treatise")

@app.route('/publications')
def publications():
    return render_template('publications.html', title="List of Publications Processed")

@app.route('/publication/<identifier>')
def publication(identifier):
    
    return render_template('publication.html', title=pub.title)


@app.route('/literature')
def literature():
    return render_template('literature.html', title="Overview of the Personal Identity Literature")

@app.route('/project')
def project():
    return render_template('project.html', title="Overview of the Project")
