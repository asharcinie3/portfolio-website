# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect
from .utils.database.database  import database
from pprint import pprint
import json
import random
import functools

db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/illustrations')
def illustrations():
    return render_template('illustrations.html')

@app.errorhandler(404)
def page_not_found(error):
    return "Page not found", 404

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

@app.route('/projects')
def projects():
    try:
        return render_template('projects.html')
    except Exception as e:
        return str(e), 500
    
    
@app.route('/resume')
def resume():
    try:
        resume_data = db.getResumeData()
        return render_template('resume.html', resume_data=resume_data)
    except Exception as e:
        return str(e), 500

@app.route('/piano')
def piano():
    try:
        return render_template('piano.html')
    except Exception as e:
        return str(e), 500
    
