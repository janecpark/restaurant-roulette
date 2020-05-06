import os
from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify
from models import db, connect_db, User, Restaurant, Favorite
from form import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError
from yelpAPI import get_my_key
import requests
import json


CURR_USER_KEY = 'curr_user'


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///restaurant'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)
db.create_all()

BASE_URL ='https://api.yelp.com/v3/businesses/search'



def get_result():
    HEADERS = {'Authorization': f'bearer {get_my_key}'}
    payload = {}

    PARAMS = {'term': 'restaurant',
              'limit': 1,
              'location': 'Las Vegas',
               'open_now': True,
               'offset': 5}

    resp = requests.request("GET", BASE_URL, params=PARAMS, headers = HEADERS, data = payload)
        
    if resp is None:
        return jsonify({'error': 'Invalid response'}),422

    data = resp.json()
    restaurants = data['businesses']
    
    return restaurants

def get_result_pref(cuisine,price,distance):
    if 'id' in session:
        session.pop('id')
        session.pop('name')
        session.pop('rating')
        session.pop('price_range')
        session.pop('cuisine')
        session.pop('image_url')
        session.pop('url')
      

    HEADERS = {'Authorization': f'bearer {get_my_key}'}
    payload = {}

    PARAMS = {'term': 'restaurant',
              'limit': 1,
              'location': 'Las Vegas',
              'open_now': True,
              'offset': 5,
              'distance': distance,
              'categories': cuisine,
              'price': price }

    resp = requests.request("GET", BASE_URL, params=PARAMS, headers = HEADERS, data = payload)
        
    if resp is None:
        return jsonify({'error': 'Invalid response'}),422

    data = resp.json()
    restaurants = data['businesses']    
    return restaurants

@app.route('/spin', methods=['GET', 'POST'])
def lucky_spin():

    response = get_result()

    return render_template('results.html', response=response)

 
@app.route('/user/pref', methods=["GET", "POST"])
def set_pref():
    """Set preferences for the user"""
  
    cuisine = request.form.get('cuisine') 
    price = request.form.get('price') 
    distance = request.form.get('distance') 
   

    if cuisine:
        response = get_result_pref(cuisine,price,distance)
        if response:        
            session['id'] = response[0]['id']
            session['name'] = response[0]['name']
            session['rating'] = response[0]['rating']
            session['price_range'] = response[0]['price']
            session['cuisine'] = cuisine
            session['image_url'] = response[0]['image_url']
            session['url'] = response[0]['url']
        
    
        return render_template('/users/userresult.html', response=response)
    else:

        return render_template('/users/preferences.html')

#######User favorites###########
@app.route('/user/add_fav', methods=["GET", "POST"])
def add_user_fav():
    """Show user's list of favorite restaurants"""
    if not g.user:
        flash('Please log in/ sign up to save results', 'danger')
        return redirect('/users/login')
    
    rest_id= session['id']
    liked_res = Favorite.query.get_or_404(rest_id)

    if liked_res in g.user.favorites:
        flash('Already in favorites', 'danger')
        return redirect('/')
    else:
        # rest_id = session['id']      
        name = session['name']
        rating = session['rating']
        price_range = session['price_range'] 
        cuisine_id = session['cuisine']
        url = session['url'] 
        image_url = session['image_url']

        res = Restaurant(
            id=rest_id, 
            name=name, 
            rating=rating,
            price_range=price_range, 
            cuisine_id=cuisine_id,
            url = url,
            image_url = image_url
        )


        db.session.add(res)
        db.session.commit()

        fav = Favorite(
            user_id = g.user.id,
            restaurant_id = rest_id
        )

        db.session.add(fav)
        db.session.commit()

        flash('Added to Favorites!', 'success')        
        return redirect('/')
    


@app.route('/users/favorites/<int:user_id>')
def show_fav(user_id):
    """Show list of favorite restaurants"""
    user = User.query.get_or_404(user_id)


    return render_template('/users/favorites.html', user=user, favs=user.favorites)

@app.route('/fav/delete/<int:fav_id>')
def delete_fav(fav_id):
    """Remove favorites """
    fav = Favorite.query.get_or_404(fav_id)
    db.session.delete(fav)
    db.session.commit()
    return redirect(f'/users/favorites/{g.user.id}')

########################### User Login ############################

@app.route('/users/signup', methods=['GET', 'POST'])
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
            return render_template('/users/signup.html', form=form)
    
        do_login(user)

        return redirect('/')
    
    else:
        return render_template('/users/signup.html', form=form)

@app.route('/users/login', methods=["GET", "POST"])
def login():
    """Log in user"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcom, {user.username}!", 'success')
            return redirect('/')
        
        flash('Invalid username/password', 'danger')

    return render_template('users/login.html', form=form)

@app.route('/users/logout')
def logout():
    """Log out user"""

    do_logout()

    flash("You have logged out", 'success')
    return redirect('/')


######Log in and homepage########

@app.before_request
def add_user_to_g():
    """If user is logged in, add user to flask global""" 

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    
    else:
        g.user = None

def do_login(user):
    """Log in user"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def home_page():
    """Show homepage"""

    # if g.user:
    #     user=g.user
    return render_template('homepage.html')
    # else:
    #     return render_template('homeanon.html')


# @app.after_request
# def add_header(req):
#     """Add non-caching headers on every request."""

#     req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     req.headers["Pragma"] = "no-cache"
#     req.headers["Expires"] = "0"
#     req.headers['Cache-Control'] = 'public, max-age=0'
#     return req
