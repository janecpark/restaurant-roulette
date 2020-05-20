import os
from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify, Blueprint
from models import db, connect_db, User, Restaurant, Favorite
from flask_login import LoginManager, current_user
from dotenv import load_dotenv


#BLUEPRINTS
from bp_user.user import user
from bp_favorite.favorite import fav
from bp_location.location import location
from bp_result.result import result
from bp_error.error_handlers import error 


app = Flask(__name__)


app.register_blueprint(user)
app.register_blueprint(fav)
app.register_blueprint(location)
app.register_blueprint(result)
app.register_blueprint(error)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///restaurant'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret1")
app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['token'] = os.environ.get('token')
API_KEY = os.getenv('API_KEY')
token = os.getenv('token')
MAP_KEY = os.getenv('MAP_KEY')

connect_db(app)
db.create_all()
load_dotenv()
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



