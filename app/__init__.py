#after isntalling flask i had to import it use the tools to run the application
from flask import Flask
#i import the config class to get the SECRET KEY in my intialization
from config import Config
#after installing sqlalchemy, i imported it to create a sql lite database
from flask_sqlalchemy import SQLAlchemy
#i installed flask migrate to be able to migrate from the info from application to the database
from flask_migrate import Migrate
#installed/imported the flask login manager tools to keep logged out users from specific routes 
from flask_login import LoginManager

####i created an instance of the flask class to start
app = Flask(__name__)
###we need a secret key for the csrf token to work and cross-reference between inputted information in the app and the database
app.config.from_object(Config)
#i creat an instace of sqlalchemy to connect the app to database
db = SQLAlchemy(app)
#i create an instance of migrate to migrate information between the app and the database
migrate = Migrate(app, db)
#i set up an instance of loginmanager to use the login tools for the users
login = LoginManager(app)
#i tell the user where to redirect if a user is not logged in
login.login_view = 'login'
login.login_message = 'HEY PAL... you are gonna have to log in'
login.login_message_category = 'warning'

#imported all of the route from the routes file into the current package
#imported all of the models from the models file into the current package
#this is at the bottom to get around a circular imports error in flask
#reference first line in routes.py
from app import routes, models