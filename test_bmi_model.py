import os
from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from models import db, User, UserBMI

os.environ['DATABASE_URL'] = "postgresql:///healthy-test"

from app import app

db.create_all()

class BMIModelTestCase(TestCase):
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

    def test_bmi_model(self):
        """Does basic model work?"""
        p = UserBMI(user_id=self.uid, age=30, weight=60, height=170, bmi= 22.4, health_condition="health_condition")
        db.session.add(p)
        db.session.commit()

        self.assertEqual(len(self.u.user_bmi), 1)
        self.assertEqual(self.u.user_bmi[0].age, 30)
        self.assertEqual(self.u.user_bmi[0].weight, 60)
        self.assertEqual(self.u.user_bmi[0].height, 170)
        self.assertEqual(self.u.user_bmi[0].bmi, 22.4)
        self.assertEqual(self.u.user_bmi[0].health_condition, "health_condition")


       
      

