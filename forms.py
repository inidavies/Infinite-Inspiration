from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Search_Form(FlaskForm):
    search = StringField('Search a theme',
                           validators=[DataRequired(), Length(min=2, max=20)])

class Image_Click(FlaskForm):
    img_btn = SubmitField()