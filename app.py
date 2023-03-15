"""Blogly application."""

import os

from flask import Flask, redirect, render_template
from models import connect_db, db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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

    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    # An alternative if you don't want to drop
    # and recreate your tables:
    # Pet.query.delete()

    # Add pets
    matt = User(first_name='Matt', last_name='Gregerson')
    sean = User(first_name='Sean', last_name='Oliver')
    theRock = User(first_name='The', last_name='Rock', image_url='https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dXNlciUyMHByb2ZpbGV8ZW58MHx8MHx8&w=1000&q=80')

    # Add new objects to session, so they'll persist
    db.session.add(matt)
    db.session.add(sean)
    db.session.add(theRock)

# Commit--otherwise, this never gets saved!
    db.session.commit()

    users = User.query.all()
    return render_template('users.html', users=users)

@app.get('/users/new')
def display_add_user_form():
    """Displays the form to add a new user"""

    return render_template('new_user_form.html')


@app.post('/users/new')
def add_new_user():

    pass

    # return redirect('/users')


@app.get('/users/<user_id>')
def user_info_page(user_id):
    """Shows information about the given user."""

    pass

@app.get('/users/<user_id>/edit')
def edit_user_info(user_id):
    """Shows the edit user form for a user."""

# GET /users/[user-id]/edit
# Show the edit page for a user.

# Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
    pass


@app.post('/users/<user_id>/edit')
def process_edit_form(user_id):
    """Processes users edits and returns user to users page"""


# Process the edit form, returning the user to the /users page.
    pass

    redirect('/users')

@app.post('/users/<user_id>/delete')
def delete_user(user_id):
    """Deletes a user from our list of users"""

    pass

    redirect('/')


# POST /users/[user-id]/delete
# Delete the user.