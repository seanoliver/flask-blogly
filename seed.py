"""Seed file to make sample data for users db."""

from models import User, db, connect_db, Post
from app import app
from sqlalchemy.sql.functions import now


# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# An alternative if you don't want to drop
# and recreate your tables:
# User.query.delete()

# Add Users
matt = User(first_name='Matt', last_name='Gregerson')
sean = User(first_name='Sean', last_name='Oliver')
theRock = User(first_name='The', last_name='Rock', image_url='https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dXNlciUyMHByb2ZpbGV8ZW58MHx8MHx8&w=1000&q=80')

# Add new objects to session, so they'll persist
db.session.add(matt)
db.session.add(sean)
db.session.add(theRock)


# Add Posts
example_title = "Exploring the World of Virtual Reality"
example_content = """\
Virtual reality (VR) has been a buzzword in the technology industry for the past decade. This immersive technology has revolutionized the way we interact with digital environments and opened up new possibilities for gaming, education, and training.

One of the most significant breakthroughs in VR has been the development of more affordable and accessible headsets. In the early days, VR headsets were bulky, expensive, and required high-end computers to operate. However, recent advances in technology have led to more compact and affordable devices, making VR accessible to a broader audience.

Virtual reality offers unparalleled gaming experiences, allowing players to step into the shoes of their favorite characters and explore lifelike environments. From action-packed shooters to heart-pounding horror games, VR provides a new level of immersion that traditional gaming simply cannot match.

But the potential of VR extends beyond gaming. In the field of education, VR has become an invaluable tool for creating interactive and engaging learning experiences. Students can take virtual field trips, explore historical sites, and even perform complex surgeries, all from the safety of their classroom.

Moreover, VR has also proven to be highly effective in training professionals across various industries. For example, pilots can practice their skills in realistic flight simulators, while firefighters can learn to tackle blazes in a controlled virtual environment. This hands-on approach to training not only saves time and resources but also reduces the risk of accidents and injuries.

Despite the many benefits of virtual reality, there are still challenges to overcome. Motion sickness and discomfort can deter users from fully embracing the technology. Additionally, developers must continue to create compelling content that entices users to invest in VR systems.

In conclusion, virtual reality is an exciting technology that has the potential to transform the way we interact with digital worlds. As VR becomes more accessible and affordable, we can expect to see even more innovative applications across various industries. The future is bright for virtual reality, and we are only just beginning to scratch the surface of its capabilities."""

new_post = Post(title=example_title, content=example_content, created_at=now(), user_id=1)

db.session.add(new_post)

# Commit--otherwise, this never gets saved!
db.session.commit()