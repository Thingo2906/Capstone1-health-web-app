"""Seed file to make sample data for users db. We will
execute this seed.py before we run app.py"""

from models import User, db, Post
from app import app

# Create all tables


# If table isn't empty, empty it
User.query.delete()

# Add users
with app.app_context():
    db.drop_all()
    db.create_all()
    user1 = User.signup(
    username="lili111",
    password="lili111",
    email="lili111@gmail.com",
    first_name ="Lili",
    last_name ="Cooper",
    image_url = "/static/images/default-pic.png"
    )

    user2 = User.signup(
    username="John333",
    password="john333",
    email="john333@gmail.com",
    first_name ="John",
    last_name="Smith",
    image_url = "/static/images/default-pic.png"

    )
     
    user3 = User.signup(
    username="Henry444",
    password="henry444",
    email="henry444@gmail.com",
    first_name="Henry",
    last_name = "Lee",
    image_url= "/static/images/default-pic.png"
    )
    


# Add posts
    post1 = Post(user_id=user1.id, title="The Best Vegetables to Eat When You're Trying to Lose Weight",
           content = "Here are seven vegetables that are particularly helpful for weight loss: Spinach, Broccoli, Spaghetti squash, Brussels sprouts, Green peas, Cauliflower, Sweet potato.",
            image_url = "https://www.deaconess.com/getattachment/91644d96-0005-4a94-88e2-b312efc1fe7f/Eat-Your-Veggies!")
    post2 = Post(user_id=user2.id, title='How does fat leave your body?', content = "The triglycerides release fat as carbon dioxide and water atoms during fat metabolism or oxidation. In other words, fat leaves the body as carbon dioxide when you exhale. The fat which becomes water mixes into your circulation until it's lost as urine, tears, sweat and other bodily fluids.")
    post3 = Post(user_id=user3.id, title='Food is my life', content = "I Love to cook everyday")

# Add new objects to session, so they'll persist
    db.session.add_all([user1, user2, user3])
    db.session.add_all([post1, post2, post3])

# Commit--otherwise, this never gets saved!
    db.session.commit()

