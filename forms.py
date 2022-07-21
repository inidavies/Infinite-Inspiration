from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Search_Form(FlaskForm):
    search = StringField('Search a theme')

class Refresh_Form(FlaskForm):
    ref_btn = SubmitField("refresh")