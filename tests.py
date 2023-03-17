import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User, Post
from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase): # FIXME: Organize the post tests into their own class namespace
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()


        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        test_post = Post(
            title='test_title',
            content='test_content',
            user_id=test_user.id
        )

        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests whether our list of users is displayed correct at /users in our application"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("add_user", html)

    def test_user_profile(self):
        """Tests user profile page in our application."""
        with self.client as c:
            response = c.get(f'/users/{self.user_id}')
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
            self.assertIn('Edit', html)

    def test_edit_function(self):
        """Tests edit functionality on a profile in our application."""
        with self.client as c:
            user = User.query.one()
            response = c.post(f'/users/{user.id}/edit',
                              data={
                                'first_name': 'Bob',
                                'last_name': 'Bobenson',
                                'image_url': 'https://picsum.photos/200'
                              })
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(user.first_name, 'Bob')

            redirect_page = c.get(response.location)
            redirect_html = redirect_page.get_data(as_text=True)
            self.assertIn('Bob', redirect_html)


    def test_delete_function(self):
        """Tests delete functionality in our application"""
        with self.client as c:
            user = User.query.one()
            response = c.post(f'/users/{user.id}/delete')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(bool(User.query.all()), False)

            redirect_page = c.get(response.location)
            redirect_html = redirect_page.get_data(as_text=True)
            self.assertNotIn('test1_first', redirect_html)

    def test_edit_post(self):
        """Tests whether a user can edit a post in our application."""
        with self.client as c:

            post = Post.query.first() # FIXME: We already have self.post_id in class so we don't need this
            response = c.post(f'/posts/{post.id}/edit',
                              data={
                                'title': 'Here is a title',
                                'content': 'Have you ever been to the moon?'
                              }) # FIXME: follow_redirects = True and then we don't need the additional response.location lines below

            self.assertEqual(response.status_code, 302)
            self.assertEqual(post.title, 'Here is a title')

            redirect_page = c.get(response.location)
            print(response.location, 'Location of response')

            redirect_html = redirect_page.get_data(as_text=True)
            print(redirect_html, 'The redirected html!')
            self.assertIn('Have you ever been to the moon?', redirect_html)

    def test_add_new_post(self):
        """Test the post route for adding a new post"""

        with self.client as c:
            response = c.post(f'/users/{self.user_id}/posts/new',
                              data={
                                'title' : 'This is a new post!',
                                'content' : 'And it is so good to read a new post.',
                                'user_id' : self.user_id
                              }) # FIXME: Same comment re redirects

            self.assertEqual(response.status_code, 302)
            redirect_page = c.get(response.location)
            redirect_html = redirect_page.get_data(as_text=True)
            self.assertIn('This is a new post!', redirect_html)

    def test_delete_post(self):
        """Test deleting a post."""

        with self.client as c:
            response = c.post(f'/posts/{self.post_id}/delete') # FIXME: Same comment re: redirects

            self.assertEqual(response.status_code, 302)
            self.assertEqual(bool(Post.query.all()), False)


            # two redirects through / to /users
            redirect_page1 = c.get(response.location)
            redirect_page2 = c.get(redirect_page1.location)
            redirect_html = redirect_page2.get_data(as_text=True)
            self.assertIn('Your post has been deleted!', redirect_html) # FIXME: Add post title to flash message

    def test_show_post(self):
        """Test showing an individual post page."""

        with self.client as c:
            response = c.get(f'/posts/{self.post_id}')
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
            self.assertIn('test_title', html)