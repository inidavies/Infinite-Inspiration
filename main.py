from flask import Flask, render_template, url_for, flash, redirect
import requests
from random import randint
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy
from forms import Search_Form

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/", methods=['GET', 'POST'])
def home():
    search_form = Search_Form() #Flask Form object
    if search_form.validate_on_submit(): # checks if entries are valid
        return redirect(url_for('board')) # if so - send to board page
    return render_template('home.html', form=search_form)

  
@app.route("/board", methods=['GET', 'POST'])
def board():
    return render_template('board.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")