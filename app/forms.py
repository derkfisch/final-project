from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, EqualTo


class SignUpForm(FlaskForm):
    username = StringField('What is Your PokemonGO Username?', validators=[InputRequired()])
    trainer_code = StringField('What is Your Trainer Code?', validators=[InputRequired()])
    email = EmailField('Enter an Email', validators=[InputRequired()])
    password = PasswordField('Create Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Get Signed Up')

class LoginForm(FlaskForm):
    username = StringField('What is Your PokemonGO Username?', validators=[InputRequired()])
    password = PasswordField('Enter Your Password', validators=[InputRequired()])
    submit = SubmitField('Get Logged In')

class PostForm(FlaskForm):
    pokemon = StringField('What Pokemon would you like to add?', validators=[InputRequired()])
    evolutions = StringField('What evolution(s) is/are this Pokemon tied to?', validators=[InputRequired()])
    strengths = StringField('What type is this Pokemon strong against?', validators=[InputRequired()])
    weaknesses = StringField('What type is this Pokemon weak against?', validators=[InputRequired()])
    image_url = StringField('Image URL')
    submit = SubmitField('Post Pokemon')

class SearchForm(FlaskForm):
    search_term = StringField('ex. Pikachu', validators=[InputRequired()])
    submit = SubmitField('Search')