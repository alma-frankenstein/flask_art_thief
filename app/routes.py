from surprise_me import get_random_picture
from app import app
from flask import render_template

@app.route('/')
@app.route('/surprises')
def surprises():
    # return("pretend it's a picture")
    # return get_random_picture
    return render_template('index.html')