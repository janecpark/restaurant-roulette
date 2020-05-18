import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = 'postgresql:///restaurant-test'

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for user"""

    def setUp(self):
        """"Create test cllient"""

        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "password", "email1@email.com")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "password", "email2@email.com")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)
        print(u1,u2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def teatDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        u = User(
            email = 'test@test.com',
            username = 'testuser',
            password = 'password123'
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.username, 'testuser')

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))


