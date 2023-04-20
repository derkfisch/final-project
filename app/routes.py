from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, LoginForm, PostForm, SearchForm
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/', methods=["GET", "POST"])
def index():
    posts = Post.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.search_term.data
        posts = db.session.execute(db.select(Post).where((Post.pokemon.ilike(f"%{search_term}%")) | (Post.evolutions.ilike(f"%{search_term}%")) | (Post.strengths.ilike(f"%{search_term}%")) | (Post.weaknesses.ilike(f"%{search_term}%")))).scalars().all()
    return render_template('index.html', posts=posts, form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Validated')
        username = form.username.data
        trainer_code = form.trainer_code.data
        email = form.email.data
        password = form.password.data
        print(username, trainer_code, email, password)
        check_user = db.session.execute(db.select(User).filter((User.username == username)| (User.email == email))).scalars().all()
        if check_user:
            flash("Username/Email already exists", "warning")
            return redirect(url_for('signup'))
        new_user = User(username=username, trainer_code=trainer_code, email=email, password=password)
        flash(f"{new_user.username}, let's catch 'em all!", "success")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated')
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{username}, you are logged in buddy!", "success")
            return redirect(url_for('index'))
        else:
            flash('Something went wrong...', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Come back soon!", "success")
    return redirect(url_for('index'))

@app.route('/create', methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        print('Form Validated')
        pokemon = form.pokemon.data
        evolutions = form.evolutions.data
        strengths = form.strengths.data
        weaknesses = form.weaknesses.data
        image_url = form.image_url.data
        new_post = Post(pokemon=pokemon, evolutions=evolutions, strengths=strengths, weaknesses=weaknesses, image_url=image_url, user_id=current_user.id)
        flash(f"{new_post.pokemon} was added", "success")
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/edit/<post_id>', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    form = PostForm()
    post_to_edit = Post.query.get_or_404(post_id)
    if post_to_edit.author != current_user:
        flash(f'Log in to edit {post_to_edit.pokemon}', 'warning')
        return(redirect(url_for('index')))
    
    if form.validate_on_submit():
        post_to_edit.pokemon = form.pokemon.data
        post_to_edit.evolutions = form.evolutions.data
        post_to_edit.strengths = form.strengths.data
        post_to_edit.weaknesses = form.weaknesses.data
        post_to_edit.image_url = form.image_url.data
        db.session.commit()
        flash(f"{post_to_edit.pokemon}'s Updated!", "success")
        return redirect(url_for('index'))

    form.pokemon.data = post_to_edit.pokemon
    form.evolutions.data = post_to_edit.evolutions
    form.strengths.data = post_to_edit.strengths
    form.weaknesses.data = post_to_edit.weaknesses
    form.image_url.data = post_to_edit.image_url
    return render_template('edit.html', form=form, post=post_to_edit)

@app.route('/delete/<post_id>')
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if post_to_delete.author != current_user:
        flash(f"Log in to delete {post_to_delete.pokemon}", "warning")
        return redirect(url_for('index'))
    
    db.session.delete(post_to_delete)
    db.session.commit()
    flash(f"{post_to_delete.pokemon} is gone!", "warning")
    return redirect(url_for('index'))


#@app.route('/<int:id>')
#def pokemon_detail(id):
#   return render_template(
#       'pokemon_detail.html',
#       pokemon=pokemon,
#       form=form,
#   )