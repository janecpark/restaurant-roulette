from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
  

    def __repr__(self):
        return f'<User #{self.id}: {self.username}, {self.email}>'

    @classmethod
    def signup(cls, username, password, email):
        """Sign up user"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username = username,
            password = hashed_pwd,
            email = email,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with username and password
        Check username and password and authenticate
        """
        
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Restaurant(db.Model):
    """Restaurant information"""

    __tablename__= ('restaurants')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    price_range = db.Column(db.String, nullable=True, default= 'N/A')
    url = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    yelp_id = db.Column(db.String, nullable=False)
    rev_num = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String, nullable=True, default='N/A')

    user = db.relationship('User', secondary= 'favorites', backref='restaurants')
    

class Favorite(db.Model):
    """Favorites table"""

    __tablename__=('favorites')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rest_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    rest_name = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', backref="favorites")
    restaurant = db.relationship('Restaurant', backref="favorites")


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)
