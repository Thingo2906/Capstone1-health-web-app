# run these tests like:
#
#    python -m unittest test_user_model.py
# Or Press Ctrl+Shift+P
import os
from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from models import db, User 

os.environ['DATABASE_URL'] = "postgresql:///healthy-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test USER model."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("username1", "password", "email1@email.com", "first_name", "last_name", None)
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("username2", "password", "email2@email.com", "first_name", "last_name", None)
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            password="HASHED_PASSWORD",
            email="test@test.com",
            first_name ="first_name",
            last_name = "last_name",
        )

        db.session.add(u)
        db.session.commit()

        # User should have no posts & no BMI results
        self.assertEqual(len(u.posts), 0)
        self.assertEqual(len(u.user_bmi), 0)

     # Signup Tests
    #
    ####
    def test_valid_signup(self):
        u_test = User.signup("testtesttest", "password", "testtest@test.com", "first_name", "last_name", None)
        uid = 5555
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertNotEqual(u_test.password, "password")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertEqual(u_test.first_name, "first_name")
        self.assertEqual(u_test.last_name, "last_name")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "password","test@test.com", "first_name", "last_name", None)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", "password", None, "first_name", "last_name", None)
        uid = 123789
        invalid.id = uid
        with self.assertRaises(IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "", "email@email.com", "first_name", "last_name", None)
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", None, "email@email.com", "first_name", "last_name", None)
    


