from flask import Flask, render_template, url_for, flash, redirect, session, request
import requests
from random import randint
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
from forms import Search_Form, Image_Click
import os
from color import background_color
from images import get_images


def get_urls(images):
    image_urls =[]
    for image in images:
        image_urls.append(image['regular_url'])
    return image_urls

def get_credit(images, spotlight):
    image_author = []
    for image in images:
        if spotlight == image['regular_url']:
            image_urls.append([image['photographer'], image['photographer_profile']])
            break
    return image_author

def search_image(form):
    # Gets the search term from the form
    if form.validate_on_submit(): # checks if search entry is valid
        # Makes request to the API based on the user's inputed search; better implementation with a database, move to home page
        image_data = get_images(form.search.data)
        session['search_results'] = image_data
        return True

#Create a flask app for the website
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

# Assign the flask app an secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)


# Home webpage function
@app.route("/", methods=['GET', 'POST'])
def home():
    search_form = Search_Form() #Flask Form object
    if search_image(search_form) == True:
        return redirect(url_for('board')) # if so - send to board page
    
    return render_template('home.html', form=search_form)


# Inspiration board webpage function
@app.route("/board", methods=['GET', 'POST'])
def board():
    search_form = Search_Form() #Flask Form object
    if search_image(search_form) == True:
        return redirect(url_for('board')) # if so - send to board page

    # Makes request to the API based on the user's inputed search; better implementation with a database  
    image_data = session['search_results']
    
    # Gets a list of the requested images (url)
    image_urls = get_urls(image_data)

    # Handles requests with varying list sizes
    if len(image_urls) < 6:
        image_urls = -1
    elif 4 >= len(image_urls) and  len(image_urls) < 9:
        main_img = len(image_urls)-1
    else:
        main_img = 4
    
    page_colors = background_color(image_urls[main_img])
    bgcolor = page_colors['light']
    navcolor = page_colors['dark']
    
    # When image is clicked, redirect to webpage displaying credits to the author
    if request.method == 'POST':
        #image_click_event = Image_Click() #image click form
        session['image_click_url'] = request.form.get('submit')
        return redirect(url_for("credit")) # Go to the credit page

    return render_template('board.html', form=search_form, images=image_urls, bgcolor = bgcolor, navcolor=navcolor, home=url_for("home"))

# Author credit webpage function
@app.route("/credit", methods=['GET', 'POST'])
def credit():
    search_form = Search_Form() #Flask Form object
    if search_image(search_form) == True:
        return redirect(url_for('board')) # if so - send to board page

    # Returns author information; better implementation with a database
    # author_data = get_credit(session['image_click_url'])
    
    image_url = session['image_click_url']
    # Changes the page color scheme based on the main image color
    page_colors = background_color(image_url)
    bgcolor = page_colors['light']
    navcolor = page_colors['dark']

    return render_template('credit.html',form=search_form, image=image_url, bgcolor = bgcolor, navcolor=navcolor)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")