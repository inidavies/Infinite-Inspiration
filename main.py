from flask import Flask, render_template
from flask import url_for, flash, redirect
from flask import session, request
import requests
from random import randint
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
from forms import Search_Form
import os
from color import background_color
from images import get_images
from dbtable import previous_boards
from dbtable import create_database, create_table

# Variables to be used globally
Search_term = ""
Search_results = {}
Image_click_url = ""
Bgdark = ""
Bglight = ""
History = []

# Just in case server goes down while someone is using our website
if os.path.exists('boards.db'):
    os.remove('boards.db')

# Create the database to store search history
engine = create_database()


def get_urls(images):
    ''' Gets the url variables for each element in
    the list of images '''

    image_urls = []
    if type(images) is list:
        for image in images:
            image_urls.append(image['regular_url'])
        return image_urls
    else:
        return -1


def get_theme(images):
    ''' Gets the theme variables for each element in
    the list of images '''

    image_themes = []
    for theme in images:
        image_themes.append(theme[5]['theme'])
    return image_themes
    board_urls = []


def get_credit(images, spotlight):
    ''' Gets the photographer name and profile link variables
    from each element in the list of images '''

    image_author = []
    for image in images:
        if spotlight == image['regular_url']:
            image_author.append(image['photographer'])
            image_author.append(image['photographer_profile'])
            break
    return image_author


def search_image(form):
    ''' Uses the search form data to make the api request
    and returns a dictionary of the search results '''

    global Search_term
    global Search_results

    # Gets the search term from the form
    if form.validate_on_submit():
        # Makes request to the API based on the user's inputed search
        image_data = create_table(engine, form.search.data)
        Search_term = form.search.data
        Search_results = image_data
        return True


def get_main(image_urls):
    ''' Handles API requests with varying
    search result dictionary sizes '''

    if len(image_urls) < 6:
        main_img = -1
    elif 4 >= len(image_urls) and len(image_urls) < 9:
        main_img = len(image_urls) - 1
    else:
        main_img = 4
    return main_img


# Create a flask app for the website
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

# Assign the flask app an secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)


# Home webpage function
@app.route("/", methods=['GET', 'POST'])
def home():
    ''' This function renders the home page template
    and it's functionality'''

    # Search bar functionality
    search_form = Search_Form()  # Flask Form object
    valid_search = search_image(search_form)
    if valid_search is True:
        # if so - send to board page
        return redirect(url_for('board', search_term=search_form.search.data))

    ''' If the user has not made previous searches
    during the current session the link to the faves page
    will not be visible '''
    display = "block"
    if History == []:
        display = "none"

    return render_template('home.html', form=search_form,
                           display=display, faves=url_for("faves"))


# Inspiration board webpage function
@app.route("/board/<search_term>", methods=['GET', 'POST'])
def board(search_term):
    ''' This function renders the board page template
    and it's functionality'''

    global Search_term
    global Search_results
    global Image_click_url
    global Bgdark
    global Bglight
    global History

    # Search bar functionality
    search_form = Search_Form()  # Flask Form object
    valid_search = search_image(search_form)
    if valid_search is True:
        # if so - send to board page
        return redirect(url_for('board', search_term=search_form.search.data))

    # Makes request to the API based on the user's inputed search
    image_data = Search_results

    # Gets a list of the requested images (url)
    image_urls = get_urls(image_data)
    # In case there is a timeout with the color picker API
    if type(image_urls) is list:
        # Changes the page color scheme based on the main image color
        main_index = get_main(image_urls)
        page_colors = background_color(image_urls[main_index])
        if type(page_colors) is dict:
            bgcolor = page_colors['light']
            navcolor = page_colors['dark']
        else:
            bgcolor = "#C9BBCF"
            navcolor = "#898AA6"
    else:
        bgcolor = "#C9BBCF"
        navcolor = "#898AA6"

    if request.method == 'POST':
        # The click event is either refresh or a clicked image
        click_event = request.form.get('submit')
        if click_event == "refresh":
            # Refreshes the webpage with the current search
            image_data = create_table(engine, search_term)
            Search_results = image_data
            image_urls = get_urls(image_data)
            if type(image_urls) is list:
                # Changes the page color scheme based on the main image color
                main_index = get_main(image_urls)
                page_colors = background_color(image_urls[main_index])
                if type(page_colors) is dict:
                    bgcolor = page_colors['light']
                    navcolor = page_colors['dark']
                else:
                    bgcolor = "#C9BBCF"
                    navcolor = "#898AA6"
            else:
                bgcolor = "#C9BBCF"
                navcolor = "#898AA6"
        else:
            ''' When image is clicked, redirect to webpage
                displaying credits to the author '''

            Image_click_url = click_event
            # Changes the page color scheme based on the main image color
            page_colors = background_color(click_event)
            if type(page_colors) is dict:
                Bglight = page_colors["light"]
                Bgdark = page_colors["dark"]
            else:
                Bglight = "#C9BBCF"
                Bgdark = "#898AA6"
            return redirect(url_for("credit"))  # Go to the credit page

    return render_template('board.html', form=search_form, images=image_urls,
                           bgcolor=bgcolor, navcolor=navcolor,
                           home=url_for("home"), faves=url_for("faves"))


# Author credit webpage function
@app.route("/credit", methods=['GET', 'POST'])
def credit():
    ''' This function renders the credit page template
    and it's functionality'''

    global Search_term
    global Search_results
    global Image_click_url
    global Bgdark
    global Bglight
    global History

    # Search functionality
    search_form = Search_Form()  # Flask Form object
    valid_search = search_image(search_form)
    if valid_search is True:
        # if so - send to board page
        return redirect(url_for('board', search_term=search_form.search.data))

    image_url = Image_click_url

    # Gets the author information
    image_data = Search_results
    author_data = get_credit(image_data, image_url)
    author_name = author_data[0]
    author_profile = author_data[1]

    ''' Gets the bg color for the author page;
    globally assgned in the board page'''
    bgcolor = Bglight
    navcolor = Bgdark

    return render_template('credit.html', form=search_form,
                           image=image_url, bgcolor=bgcolor,
                           navcolor=navcolor, a_profile=author_profile,
                           a_name=author_name,  faves=url_for("faves"))


@app.route("/favs", methods=['GET', 'POST'])
def faves():
    ''' This function renders the faves page template
    and it's functionality'''

    global Search_term
    global Search_results
    global Image_click_url
    global Bgdark
    global Bglight
    global History

    # Search functionality
    search_form = Search_Form()  # Flask Form object
    valid_search = search_image(search_form)
    if valid_search is True:
        # if so - send to board page
        return redirect(url_for('board', search_term=search_form.search.data))

    History = previous_boards()

    # Get main display image, store boards in a session/global variable
    board_urls = []
    bgcolors = []
    img_index = []
    index = 0
    for board in History:
        # Get the main image of each board from the list
        # Use the name image of the board as a thumbnail
        board_urls.append(board[4]['thumb_url'])

        # Get the bgcolors using the main image of the board
        # Store the colors in a list with corresponding indexes
        # to the board list
        page_colors = background_color(board[4]['thumb_url'])

        if type(page_colors) is int:
            bgcolor = "#C9BBCF"
            navcolor = "#898AA6"
            bgcolors.append([bgcolor, navcolor])
            img_index.append(index)
        else:
            bgcolors.append([page_colors['light'], page_colors['dark']])
            img_index.append(index)
        index += 1

        # Store the key/index for each image in a list for easy pairing
    image_themes = get_theme(History)

    # Get board images
    image_urls = []
    for board in History:
        image_urls.append(board)

    image_themes = get_theme(History)

    if request.method == 'POST':
        # Sets session search results to the chosen previous search results
        board_key = int(request.form.get('submit'))
        Search_results = History[board_key]
        # Redirects to a page displaying that board
        return redirect(url_for("board", search_term="past_board"))

    return render_template('faves.html', form=search_form,
                           board=board_urls, themes=image_themes,
                           bgcolors=bgcolors, img_index=img_index)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
