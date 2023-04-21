#i set the secret key as an environmental variable and pulled it from the os package
#i had to install python dotenv to perform this
import os 

#this is define to show where the database lives
basedir = os.path.abspath(os.path.dirname(__file__))
#i set up a configuration class to send the secret key to the initalization module
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-string'
    #i use this to set up the sql lite database for a flask sql alchemy configuration
    #i join the base direction with the apps database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #this turns off a tool i dont need which send a signal to the app everytime a change is about to be made
    SQLALCHEMY_TRACK_MODIFICATIONS = False