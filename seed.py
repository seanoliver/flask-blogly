"""Seed file to make sample data for users db."""

from models import User, db, connect_db
from app import app

# Create all tables
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