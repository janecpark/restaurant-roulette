import os
from unittest import TestCase

from models import db, connect_db, User, Favorite, Restaurant

os.environ['DATABASE_URL'] = "postgresql:///restaurant-test"

from app import app, CURR_USER_KEY

db.create_all()

class FavViewTestCase(TestCase):
    """Test view for user"""
    
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    )
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("abc", "password", "test1@test.com")
        self.u1_id = 778
        self.u1.id = self.u1_id
        self.u2 = User.signup("efg", "password", "test2@test.com")
        self.u2_id = 884
        self.u2.id = self.u2_id

        db.session.commit()

        self.testrest = Restaurant(name="Yummy", rating="4", price_range=None, url="www.yummy.com", image_url="www.image.com", yelp_id="1234", rev_num=None, phone=None)
        self.testrest_id = 1234
        self.testrest.id = self.testrest_id

        self.r1 = Restaurant(name="Sushi", rating="3", price_range=None, url="www.yummy2.com", image_url="www.image2.com", yelp_id="2345", rev_num=None, phone=None)
        self.r1_id = 2345
        self.r1.id = self.r1_id

        db.session.add_all([self.testrest, self.r1])
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def setup_fav(self):
        f1 = Favorite(rest_id=self.testrest.id, rest_name='Yummy', user_id=8989)
        f2 = Favorite(rest_id=self.r1_id, rest_name="Sushi", user_id=8989)
        db.session.add_all([f1,f2])
        db.session.commit()
    
    def test_user_fav(self):
        self.setup_fav()

        with self.client as c:
            resp = c.get(f"/users/favorites/{self.testuser.id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Yummy', str(resp.data))

    def test_remove_fav(self):
        self.setup_fav()
        f = Favorite.query.filter(Favorite.rest_id ==self.testrest.id).one()
        self.assertIsNotNone(f)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post(f'/fav/delete/{self.testrest.id}', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            f = Favorite.query.all()
            self.assertEqual(len(f), 0)
    
    def test_get_all_fav(self):
        self.setup_fav()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get('/getfav')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Yummy', str(resp.data))
            self.assertIn('Sushi', str(resp.data))
    