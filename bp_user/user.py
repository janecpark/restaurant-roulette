from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify, Blueprint
from models import db, connect_db, User, Restaurant, Favorite
from form import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, login_user, current_user, logout_user
import requests


user = Blueprint('user', __name__, template_folder='templates')

    
@user.route('/', methods=["GET", 'POST'])
def home_page():
    """Show homepage"""
    session.permanent = True
    return render_template('/user/homepage.html')
   

@user.route('/login', methods=["GET", "POST"])
def login():
    """Log in user"""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        login_user(user, remember=True)
        if user is False:
            flash('Invalid username/password', 'danger')
            return redirect('/user/login.html')
        else:
            flash(f"Welcome, {user.username}!", 'success')
            return redirect('/')
            
    return render_template('user/login.html', form=form)

@user.route('/logout')
def logout():
    """Log out user"""

    logout_user()

    flash("Log Out Successful", 'success')
    return render_template('user/logout.html')

@user.route('/signup', methods=['GET', 'POST'])
def user_signup():
    """Create new user and add to database"""
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username is already taken", 'danger')
            return render_template('/user/signup.html', form=form)
        login_user(user, remember=True)
        return redirect('/')
    
    else:
        return render_template('/user/signup.html', form=form)

@user.route('/checkuser', methods=['GET'])
def send_user():
    """Send user information to client"""
    if current_user.is_authenticated:
        user = User.query.get_or_404(current_user.id)
        ser = serialize(user)
        return jsonify(ser)
    else:
        return jsonify({'Error': 'User unavailable'})

def serialize(self):
    return{
            "username": self.username,
        }   