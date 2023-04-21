#we will ahve to import the databse from the app
#import login for the user loader
from app import db, login
#this allows to set up an exact time the post was created
from datetime import datetime
#this allows me to set up password security in the app
from werkzeug.security import generate_password_hash, check_password_hash
#i import the user mixin to inherent a user 
from flask_login import UserMixin

#i create a class user to create a database
#i add user mixin to show the user is coming from the database
class User(db.Model, UserMixin):
    #i set up my columns in the data giving each column a set of circumstances
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    trainer_code = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #i create a relationship before the user and the post database, calling the user the author
    posts = db.relationship('Post', backref='author')

    #i set up an initialization to pass the key word arguments into self,, self bneing instance of user
    def __init__(self, **kwargs):
        #i want to make sure this continues to take in key word arguments
        super().__init__(**kwargs)
        #generate password uses sha256 to create a hidden password
        self.password = generate_password_hash(kwargs.get('password'))
        #then i add the info to self and commit to database, self being instance of user
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"
    
    #this will check the password to see if the user uses the correct password
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

# i use the user loader to get the current user from the user db
@login.user_loader
def get_a_user_by_id(user_id):
    return db.session.get(User, user_id)

#i create a class post to set up a pokemon post database
class Post(db.Model):
    #i define my columns with each having their own circumstances
    id = db.Column(db.Integer, primary_key=True)
    pokemon = db.Column(db.String(25), nullable=False)
    evolutions = db.Column(db.String(50), nullable=False)
    strengths = db.Column(db.String(25), nullable=False)
    weaknesses = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #i set up a foreign key so that my users are connected to their posts
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #i set up an initialization to pass the key word arguments into self
    def __init__(self, **kwargs):
        #i want to make sure this continues to take in key word arguments
        super().__init__(**kwargs)
        #i add the info to self and commit to database
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Post {self.id}|{self.pokemon}>"