"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request, flash
from models import connect_db, db, User, DEFAULT_IMG, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.get('/')
def show_homepage():
    """Shows the 5 most recent posts on the website."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('homepage.html', posts = posts)

@app.get('/users')
def show_users():
    """Show list of all current users"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.get('/users/new')
def display_add_user_form():
    """Displays the form to add a new user"""

    return render_template('new_user_form.html')


@app.post('/users/new')
def add_new_user():
    """Adds new user to the database. (Add requirements) and redirects to the users page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url', DEFAULT_IMG)

    new_user = User(
        first_name = first_name,
        last_name = last_name,
        image_url = image_url
    )

    db.session.add(new_user)
    db.session.commit()

    flash(f"New user, {first_name} {last_name}, has been created!")

    return redirect('/users')


@app.get('/users/<int:user_id>')
def user_info_page(user_id):
    """Shows information about the given user."""

    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template(
        "user_profile.html",
        user=user, posts=posts
    )

@app.get('/users/<int:user_id>/edit')
def edit_user_info(user_id):
    """Shows the edit user form for a user."""
    user = User.query.get_or_404(user_id)

    return render_template("edit_user.html", user=user)


@app.post('/users/<user_id>/edit')
def process_edit_form(user_id):
    """Processes users edits and returns user to users page"""

    user = User.query.get(int(user_id))
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url', 'https://picsum.photos/100')

    db.session.commit()

    flash(f"Updated user profile!")

    return redirect(f"/users/{ user.id }")

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes a user from our list of users then redirects user to homepage."""

    # FIXME: First, confirm the user actually exists (get_or_404)

    Post.query.filter(Post.user_id == user_id).delete()
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    flash(f"User has been deleted!")
    return redirect('/') # FIXME: redirect directly to /users (need to change tests too)

# ============================================================================ #
# Post Routes                                                                  #
# ============================================================================ #

@app.get('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)

    return render_template("new_post_form.html", user=user)

@app.post('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    title = request.form.get('title')
    content = request.form.get('content')

    new_post = Post(
        title = title,
        content = content,
        user_id = user_id
    )

    db.session.add(new_post)
    db.session.commit()

    flash(f'Created New Post: {title}')

    return redirect(f"/users/{user_id}")


@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template("post.html", post=post, user=user) # FIXME: Can use 'post.user' instead

@app.get('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template('edit_post.html', post=post, user=user) # FIXME: Same as above


@app.post('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')

    db.session.commit()

    flash(f'Edited Post: {post.title}!')

    return redirect(f'/posts/{post.id}')


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete the post."""
    # FIXME: First confirm the post exists and then delete
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()

    flash(f"Your post has been deleted!")
    return redirect('/') # FIXME: redirect to /users/user_id instead