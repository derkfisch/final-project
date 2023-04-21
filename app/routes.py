#from app i import the app and the database so i can provide routes
from app import app, db
#these are the imported tools i need to navigate through the app
from flask import render_template, redirect, url_for, flash
#import all of the forms from the form file so the user can enter/search information
from app.forms import SignUpForm, LoginForm, PostForm, SearchForm
#import all of the models so the user can add to the database
from app.models import User, Post
#import the login tools so the user is limited in what they can do if/if not signed in
from flask_login import login_user, logout_user, login_required, current_user

#the base route has a get and post method which allow for the route to receive 
@app.route('/', methods=["GET", "POST"])
def index():
    #I gather the info from the pokemon in the post db by defining posts 
    posts = Post.query.all()
    #i define form as an instance of search form
    form = SearchForm()
    #when the user submits the form
    if form.validate_on_submit():
        #i define the search term as the input in the form
        search_term = form.search_term.data
        #this is the line that allows me to search for pokemon strengths/evolutions/weaknesses/names
        posts = db.session.execute(db.select(Post).where((Post.pokemon.ilike(f"%{search_term}%")) | (Post.evolutions.ilike(f"%{search_term}%")) | (Post.strengths.ilike(f"%{search_term}%")) | (Post.weaknesses.ilike(f"%{search_term}%")))).scalars().all()
    #render template loads the html that is called
    #i also pass an instance of posts into the posts in the index page
    #i pass the instance of form from the user into the search form
    return render_template('index.html', posts=posts, form=form)

#i create a signup route for users to sign up
#post method allows users to send the filled out form to the route(inherently the signup form)
@app.route('/signup', methods=["GET", "POST"])
def signup():
    #i define form as an instance of the sign up form info
    form = SignUpForm()
    #when the user submits the form of the given info and it is valid
    if form.validate_on_submit():
        #i get the data from the users input in the form fields
        username = form.username.data
        trainer_code = form.trainer_code.data
        email = form.email.data
        password = form.password.data
        #we must check our database to see if that user already exists using db
        check_user = db.session.execute(db.select(User).filter((User.username == username)| (User.email == email))).scalars().all()
        #if the user already in the database, we let the user know they must try something else
        if check_user:
            flash("Username/Email already exists", "warning")
            #i then redirect the user back to the beginning of the signup page
            return redirect(url_for('signup'))
        #if the user is unique, we pass this user input into the User database with the given information
        new_user = User(username=username, trainer_code=trainer_code, email=email, password=password)
        #i send the user a message to let them know everythings goood then send them to the login page to put in their new account info
        flash(f"{new_user.username}, let's catch 'em all!", "success")
        return redirect(url_for('login'))
    #i load the signup page and pass in an instance of the user form into the sign up form
    return render_template('signup.html', form=form)


#i create a login route for the user to login
#post method allows the user to send the login info to the route(inherently the loginform)
@app.route('/login', methods=["GET", "POST"])
def login():
    #i define form as an instance of the login form
    form = LoginForm()
    #when the user submits log in info and it is valid
    if form.validate_on_submit():
        #i get the data from the users input in the form fields
        username = form.username.data
        password = form.password.data
        #this route checks the User data base for the username
        user = User.query.filter_by(username=username).first()
        #if username exists and password matches, i log in the user and flash a message to tell them that
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{username}, you are logged in buddy!", "success")
            #i then redirect the logged in user home
            return redirect(url_for('index'))
        #if the user didnt type in correct info i tell them then redirect to the login
        else:
            flash('Something went wrong...', 'danger')
            return redirect(url_for('login'))
    #i render the login page and pass in an isntance of the user form into the login form
    return render_template('login.html', form=form)

#i create a logout route for the user to log out
@app.route('/logout')
#to use log out route, you must be logged in
#i do this using login required from flask login package
@login_required
def logout():
    #i use the tools from the flask login package to logout the user, tell them, then redirect them back to the home page
    logout_user()
    flash("Come back soon!", "success")
    return redirect(url_for('index'))

#i create a create route for the user to make a pokemon post
#the post method allows the user to send the pokemon post info to the route (inherently the postform)
@app.route('/create', methods=["GET", "POST"])
#a logged in user is required to use this route
@login_required
def create_post():
    #i define form as an instance of the post form
    form = PostForm()
    #if the user submits a valid form
    if form.validate_on_submit():
        #i get the data from the users input in the form fields
        pokemon = form.pokemon.data
        evolutions = form.evolutions.data
        strengths = form.strengths.data
        weaknesses = form.weaknesses.data
        image_url = form.image_url.data
        #i set this info to a new post and pass that info in the database
        new_post = Post(pokemon=pokemon, evolutions=evolutions, strengths=strengths, weaknesses=weaknesses, image_url=image_url, user_id=current_user.id)
        #i send the user back a message to let them know the pokemon was added
        flash(f"{new_post.pokemon} was added", "success")
        #i then redirect the user back to the home page
        return redirect(url_for('index'))
    #i render the create page and pass in an instanc of the user form into the post form
    return render_template('create.html', form=form)

#i create an edit route for the author of the pokemon post to edit their pokemon input
#the post method allows the user to send the pokemon information to the route
@app.route('/edit/<post_id>', methods=["GET", "POST"])
#to grab the post, the user must be logged in
@login_required
#i define the function edit post with the parameter of post id
def edit_post(post_id):
    #i define form as an instance of the post form
    form = PostForm()
    #i define the current post id in the post db as the post to edit
    post_to_edit = Post.query.get_or_404(post_id)
    #if the user isnt the author of the post i tell them to log in and redirect them to the home page
    if post_to_edit.author != current_user:
        flash(f'Log in to edit {post_to_edit.pokemon}', 'warning')
        return(redirect(url_for('index')))
    
    #if the author submits a valid form
    if form.validate_on_submit():
        #i get the data from the users input in the form fields
        post_to_edit.pokemon = form.pokemon.data
        post_to_edit.evolutions = form.evolutions.data
        post_to_edit.strengths = form.strengths.data
        post_to_edit.weaknesses = form.weaknesses.data
        post_to_edit.image_url = form.image_url.data
        # i connect this information back to the database and commit the new data
        db.session.commit()
        #i tell the user their update went through and redirect them home
        flash(f"{post_to_edit.pokemon}'s Updated!", "success")
        return redirect(url_for('index'))

    #i prepopulate the form for the user so they can edit what is already there
    form.pokemon.data = post_to_edit.pokemon
    form.evolutions.data = post_to_edit.evolutions
    form.strengths.data = post_to_edit.strengths
    form.weaknesses.data = post_to_edit.weaknesses
    form.image_url.data = post_to_edit.image_url
    #i render the edit template and send an instance of the user form to the post form 
    #and an instance of the edited post to the original post
    return render_template('edit.html', form=form, post=post_to_edit)

#i create a delete route to allow the user to delete their post
@app.route('/delete/<post_id>')
#this route requires the user to be logged in
@login_required
#i define the delete post function with the post id parameter
def delete_post(post_id):
    #i define the current post id in the post db as the post to delete
    post_to_delete = Post.query.get_or_404(post_id)
    #i check if the user is the author of the post before i allow them to delete
    if post_to_delete.author != current_user:
        #if theyre not the author, i tell them to log in and redirect them to the home page
        flash(f"Log in to delete {post_to_delete.pokemon}", "warning")
        return redirect(url_for('index'))
    
    #i connect this information back to the database and delete then commit it
    db.session.delete(post_to_delete)
    db.session.commit()
    #i send the user back a message to let them know and send them to home page
    flash(f"{post_to_delete.pokemon} is gone!", "warning")
    return redirect(url_for('index'))
