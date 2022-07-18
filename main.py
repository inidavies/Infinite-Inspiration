from flask import Flask, render_template, url_for, flash, redirect
import requests
from random import randint
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

  
@app.route("/board", methods=['GET', 'POST'])
def board():
    return render_template('board.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")