import os
from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from models import db, Post, User

os.environ['DATABASE_URL'] = "postgresql:///healthy-test"

from app import app

db.create_all()

class PostModelTestCase(TestCase):
    """Test Post Model ."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "password", "testing@test.com", "first_name", "last_name", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_post_model(self):
        """Does basic model work?"""
        p = Post(title="title", content="content", user_id=self.uid)
        db.session.add(p)
        db.session.commit()

        self.assertEqual(len(self.u.posts), 1)
        self.assertEqual(self.u.posts[0].title, "title")
        self.assertEqual(self.u.posts[0].content, "content")
       
      



