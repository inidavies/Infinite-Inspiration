from flask import Flask, render_template, url_for, flash, redirect, session
import requests
from random import randint
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
from forms import Search_Form
import os

def request_images(theme):
    # Import the hidden client id and secret from os
    CLIENT_ID = os.environ.get('UNSPLASH_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('UNSPLASH_CLIENT_SECRET')

    # Make request to unsplash api for a list of 9 images
    headers = {'Authorization': 'Client-ID {token}'.format(token=CLIENT_ID), 'Accept-Version': 'v1'}
    BASE_URL = 'https://api.unsplash.com/'
    PARAMS = {'query': theme, 'orientation': 'landscape', 'count': 9}
    r = requests.get(BASE_URL + '/photos/random', params = PARAMS, headers=headers)
    data = r.json()
    return data


def display_images(images):
    image_urls =[]
    for image in images:
        image_urls.append(image['urls']['regular'])
        print(image['urls']['regular'])
    return image_urls


#Create a flask app for the website
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

# Assign the flask app an secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)


# Home webpage function
@app.route("/", methods=['GET', 'POST'])
def home():
    search_form = Search_Form() #Flask Form object
    if search_form.validate_on_submit(): # checks if search entry is valid
        session['search_term'] = search_form.search.data 
        return redirect(url_for('board')) # if so - send to board page
    return render_template('home.html', form=search_form)


# Inspiration board webpage function
@app.route("/board", methods=['GET'])
def board():
    image_data = request_images(session.get("search_term")) #makes request to the API based on the user's inputed search
    image_urls = display_images(image_data)
    return render_template('board.html', images=image_urls)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")