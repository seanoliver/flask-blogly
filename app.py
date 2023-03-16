"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request, flash
from models import connect_db, db, User
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
def list_users():
    """Redirect to list of users"""

    return redirect('/users')

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
    """Adds new user to the database and redirects to the users page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url', '')

    new_user = User(
        first_name = first_name,
        last_name = last_name,
        image_url = image_url
    )

    db.session.add(new_user)
    db.session.commit()

    flash(f"New user, {first_name} {last_name}, has been created!")

    return redirect('/users')


@app.get('/users/<user_id>')
def user_info_page(user_id):
    """Shows information about the given user."""

    user = User.query.get(int(user_id))
    image_url = user.image_url or 'https://picsum.photos/100'

    return render_template(
        "user_profile.html",
        user=user,
        image_url=image_url
    )

@app.get('/users/<user_id>/edit')
def edit_user_info(user_id):
    """Shows the edit user form for a user."""
    user = User.query.get(int(user_id))
    image_url = user.image_url or ''


    return render_template("edit_user.html", user=user, image_url=image_url)


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

@app.post('/users/<user_id>/delete')
def delete_user(user_id):
    """Deletes a user from our list of users"""

    User.query.filter(User.id == int(user_id)).delete()
    db.session.commit()

    flash(f"User has been deleted!")
    return redirect('/')
