from flask import Flask, render_template, url_for, flash, redirect, session, request
import requests
from random import randint
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
from forms import Search_Form
import os
from color import background_color
from images import get_images
from dbtable import previous_boards, create_database, create_table

#Variables


#just in case server goes down while someone is using our website
if os.path.exists('boards.db'):
    os.remove('boards.db')

# Create the database to store search history
engine = create_database()

def get_urls(images):
    image_urls =[]
    for image in images:
        image_urls.append(image['regular_url'])
    return image_urls

def get_theme(images):
    image_themes =[]
    for theme in images:
        image_themes.append(theme[5]['theme'])
    return image_themes
    board_urls =[]

def get_credit(images, spotlight):
    image_author = []
    for image in images:
        if spotlight == image['regular_url']:
            image_author.append(image['photographer'])
            image_author.append(image['photographer_profile'])
            break
    return image_author

def search_image(form):
    # Gets the search term from the form
    if form.validate_on_submit(): # checks if search entry is valid
        # Makes request to the API based on the user's inputed search; better implementation with a database, move to home page
        image_data = create_table(engine, form.search.data)
        session["search_term"] = form.search.data
        session['search_results'] = image_data
        return True

def get_main(image_urls):
    # Handles requests with varying list sizes
    if len(image_urls) < 6:
        main_img = -1
    elif 4 >= len(image_urls) and  len(image_urls) < 9:
        main_img = len(image_urls)-1
    else:
        main_img = 4
    return main_img


#Create a flask app for the website
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

# Assign the flask app an secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)


# Home webpage function
@app.route("/", methods=['GET', 'POST'])
def home():
    #Flask Form object
    search_form = Search_Form()
    if search_image(search_form) == True:
        return redirect(url_for('board', search_term=search_form.search.data)) # if so - send to board page
    
    return render_template('home.html', form=search_form)


# Inspiration board webpage function
@app.route("/board/<search_term>", methods=['GET', 'POST'])
def board(search_term):
    #Search bar
    #Flask Form object
    search_form = Search_Form()
    if search_image(search_form) == True:
        return redirect(url_for('board', search_term=search_form.search.data)) # if so - send to board page

    # Makes request to the API based on the user's inputed search
    image_data = session['search_results']
    # Gets a list of the requested images (url)
    image_urls = get_urls(image_data)

    # Changes the page color scheme based on the main image color
    main_index = get_main(image_urls)
    page_colors = background_color(image_urls[main_index])
    bgcolor = page_colors['light']
    navcolor = page_colors['dark']
    
    if request.method == 'POST':
        image_click_url = request.form.get('submit')
        if image_click_url == "refresh":
            # Refreshes the webpage with the current search
            image_data = create_table(engine, search_term)
            session['search_results'] = image_data
            image_urls = get_urls(image_data)
            main_index = get_main(image_urls)
            page_colors = background_color(image_urls[main_index])
            bgcolor = page_colors['light']
            navcolor = page_colors['dark']
        else:
            # When image is clicked, redirect to webpage displaying credits to the author
            session['image_click_url'] = image_click_url 
            # Changes the page color scheme based on the main image color
            page_colors = background_color(image_click_url)
            session['bglight'] = page_colors["light"]
            session['bgdark'] = page_colors["dark"]
            return redirect(url_for("credit")) # Go to the credit page

    return render_template('board.html', form=search_form, images=image_urls, bgcolor = bgcolor, navcolor=navcolor, home=url_for("home"), faves=url_for("faves"))


# Author credit webpage function
@app.route("/credit", methods=['GET', 'POST'])
def credit():
    #Flask Form object
    search_form = Search_Form()
    if search_image(search_form) == True:
        return redirect(url_for('board', search_term=search_form.search.data)) # if so - send to board page
    
    image_url = session['image_click_url']

    # Returns author information
    image_data = session['search_results']
    author_data = get_credit(image_data, image_url)
    author_name = author_data[0]
    author_profile = author_data[1]

    bgcolor = session['bglight']
    navcolor = session['bgdark']

    return render_template('credit.html',form=search_form, image=image_url, bgcolor = bgcolor, navcolor=navcolor, a_profile=author_profile, a_name=author_name,  faves=url_for("faves"))

@app.route("/favs", methods=['GET', 'POST'])
def faves():
    #Flask Form object
    search_form = Search_Form()
    if search_image(search_form) == True:
        return redirect(url_for('board', search_term=search_form.search.data)) # if so - send to board page
    
    history = previous_boards()

    # Get main display image, store boards in a session variable
    board_urls =[]
    session["history"] = []
    for board in history:
        board_urls.append(board[4]['thumb_url'])
        session["history"].append(board)
    image_themes = get_theme(history)

    # Get board images
    image_urls =[]
    for board in history:
        image_urls.append(board)
    
    image_themes = get_theme(history)


    if request.method == 'POST':
        # Sets session search results to the chosen previous search results
        board_key = int(request.form.get('submit'))
        session['search_results'] = session["history"][board_key]
        # Redirects to a page displaying that board
        return redirect(url_for("board", search_term="past_board"))

    return render_template('faves.html', form=search_form, board=board_urls, themes=image_themes)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")