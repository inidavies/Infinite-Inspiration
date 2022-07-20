from flask import Flask, render_template, url_for, flash, redirect, session, request
import requests
from random import randint
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
from forms import Search_Form, Image_Click
import os
from color import background_color
#from images import unsplash.py

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
@app.route("/board", methods=['GET', 'POST'])
def board():
    image_data = request_images(session.get("search_term")) # makes request to the API based on the user's inputed search
    image_urls = display_images(image_data) # get a list of the requested images (url)
    bgcolor = "#C9BBCF"

    # Handles requests with varying list sizes
    if len(image_urls) < 6:
        image_urls = -1
    elif 4 >= len(image_urls) and  len(image_urls) < 9:
        bgcolor = background_color(len(image_urls)-1)
    else:
        bgcolor = background_color(image_urls[4])
    
    # When image is clicked, redirect to webpage displaying credits to the author
    if request.method == 'POST':
        #image_click_event = Image_Click() #image click form
        session['image_click_url'] = request.form.get('submit')
        return redirect(url_for("credit")) # Go to the credit page

    return render_template('board.html', images=image_urls, bgcolor = bgcolor, home=url_for("home"))

# Author credit webpage function
@app.route("/credit", methods=['GET', 'POST'])
def credit():
    image_url = session['image_click_url']
    bgcolor = background_color(image_url) # changes the page color scheme based on the main image color

    return render_template('credit.html', image=image_url, bgcolor = bgcolor)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")