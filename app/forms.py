#Flask form allows us a structure(stringfield,passwordfield,etc) to create other forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, EqualTo

#this form allows a user to sign up
class SignUpForm(FlaskForm):
    #allow the user to create a username -- required
    username = StringField('What is Your PokemonGO Username?', validators=[InputRequired()])
    #allow the user to create a trainer_code -- required
    trainer_code = StringField('What is Your Trainer Code?', validators=[InputRequired()])
    #allow the user to create an email -- required
    email = EmailField('Enter an Email', validators=[InputRequired()])
    #user is required to create password and confirm it
    password = PasswordField('Create Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    #allow user to submit new account info
    submit = SubmitField('Get Signed Up')

#this form allows users to login after they have created an account
class LoginForm(FlaskForm):
    #login user by giving them a form to fill out their username and password -- info required
    username = StringField('What is Your PokemonGO Username?', validators=[InputRequired()])
    password = PasswordField('Enter Your Password', validators=[InputRequired()])
    #allow user to submit information to log in
    submit = SubmitField('Get Logged In')

#this form allows the user to post a new pokemon
class PostForm(FlaskForm):
    #allow user to create pokemon name --required
    pokemon = StringField('What Pokemon would you like to add?', validators=[InputRequired()])
    #allow user to add any evolutions --requuired
    evolutions = StringField('What evolution(s) is/are this Pokemon tied to?', validators=[InputRequired()])
    #allow user to add any strengths or weaknesses --required
    strengths = StringField('What type is this Pokemon strong against?', validators=[InputRequired()])
    weaknesses = StringField('What type is this Pokemon weak against?', validators=[InputRequired()])
    #allow user to add an image of the pokemon --required
    image_url = StringField('Image URL')
    #allow user to submit pokemon post
    submit = SubmitField('Post Pokemon')

#this form allows the user to search for a pokemon
class SearchForm(FlaskForm):
    #allow the user to input what they are searching for in the pokemon post
    search_term = StringField('ex. Pikachu', validators=[InputRequired()])
    #allow user to submit pokemon search
    submit = SubmitField('Search')