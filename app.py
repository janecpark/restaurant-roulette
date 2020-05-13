import os
from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify
from models import db, connect_db, User, Restaurant, Favorite
from form import UserForm, LoginForm
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import requests
import json
import random


CURR_USER_KEY = 'curr_user'

app = Flask(__name__)
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

BASE_URL ='https://api.yelp.com/v3/businesses/search'
LOCATION_URL = "http://www.mapquestapi.com/geocoding/v1/address"


def get_result(num):
    """Get API result"""
    if 'name' in session:
        pop_session()

    HEADERS = {'Authorization': f'bearer {API_KEY}'}
    payload = {}

    PARAMS = {'term': 'restaurant',
              'limit': num,
              'latitude': session['latitude'],
              'longitude': session['longitude'],
              'open_now': True,
              'offset': num}

    resp = requests.request("GET", BASE_URL, params=PARAMS, headers = HEADERS, data = payload)
        
    if resp is None:
        return jsonify({'error': 'Invalid response'}),422

    data = resp.json()
    restaurants = data['businesses']
    return restaurants


def get_result_pref(cuisine,price,distance):
    """Get API results with preferences"""
    if 'name' in session:
        pop_session()
      
    HEADERS = {'Authorization': f'bearer {API_KEY}'}
    payload = {}

    PARAMS = {'term': 'restaurant',
              'limit': 1,
              'latitude': session['latitude'],
              'longitude': session['longitude'],
              'open_now': True,
              'offset': 2,
              'distance': distance,
              'categories': cuisine,
              'price': price }

    resp = requests.request("GET", BASE_URL, params=PARAMS, headers = HEADERS, data = payload)
        
    if resp is None:
        return jsonify({'error': 'Invalid response'}),422

    data = resp.json()
    restaurants = data['businesses']    
    return restaurants

def add_to_session(response):
    session['id'] = response[0]['id']
    session['name'] = response[0]['name']
    session['rating'] = response[0]['rating']
    session['price_range'] = 'N/A' or response[0]['price'] 
    session['image_url'] = response[0]['image_url'] 
    session['url'] = response[0]['url']
    session['phone'] = response[0]['phone']
    session['rev_num'] = response[0]['review_count']
 
    
def pop_session():
    session.pop('name')
    session.pop('id')
    session.pop('rating')
    session.pop('price_range')
    session.pop('image_url')
    session.pop('url')
    session.pop('phone')
    session.pop('rev_num')

@app.route('/spin', methods=['GET', 'POST'])
def lucky_spin():
    """Post and render response"""

    response = get_result(1)
    add_to_session(response)
    return jsonify(response)

@app.route('/nearbyRes', methods=["GET", "POST"])
def nearby():
    """Render response for nearby restaurants"""
    response = get_result(12)
    return jsonify(response)
    
@app.route('/handleRes', methods=['POST'])        
def handle_result():
    """Route to handle result and add to session"""
    data = request.get_json()
    obj = json.loads(data)

    res_id = obj['id']
    name = obj['name']
    image_url = obj['image_url']
    rating = obj['rating']
    phone = obj['phone']
    review_count = obj['review_count']
    price = obj['price']
    url = obj['url']

    if 'name' in session:
        pop_session()

    session['id'] = res_id
    session['name'] = name
    session['rating'] = rating
    session['price_range'] = price
    session['image_url'] = image_url
    session['url'] = url
    session['phone'] = phone
    session['rev_num'] = review_count

    return jsonify({'result': 'success'})
   
 
@app.route('/user/pref', methods=["GET", "POST"])
def set_pref():
    """Set preferences for the user"""
  
    cuisine = request.form.get('cuisine') 
    price = request.form.get('price') 
    distance = request.form.get('distance')

    if not price:
        price = random.randint(1,4)
    if not distance:
        distance = random.randint(482, 32100)
    print(cuisine,price,distance)
    
    if cuisine:
        response = get_result_pref(cuisine,price,distance)
        if response and g.user:
            add_to_session(response)
            name = response[0]['name']
            user = User.query.get_or_404(g.user.id)
         
            favres = Favorite.query.filter(Favorite.rest_name == name).filter(Favorite.user_id == user.id).first()
        else:
            favres = None
    
        return render_template('/users/userresult.html', response=response, favres=favres)
    else:
        return render_template('/users/preferences.html')


#######User favorites###########
@app.route('/user/add_fav/', methods=["GET", "POST"])
def add_user_fav():
    """Show user's list of favorite restaurants"""
    if not g.user:
        flash('Please log in/ sign up to save results', 'danger')
        return redirect('/users/login')

    yelp_id = session['id']      
    name = session['name']
    rating = session['rating']
    price_range = session['price_range'] 
    url = session['url'] 
    image_url = session['image_url'] 
    phone = session['phone']
    rev_num = session['rev_num']
    user = g.user

    result = {"name": name, 
              "rating": rating, 
              "price_range": price_range,
              "url": url,
              "image_url": image_url,
              "user": user}

    res_data = Restaurant.query.filter(Restaurant.yelp_id==yelp_id).first()
    all_res = Restaurant.query.all()
        
    if res_data in all_res:
        fav = Favorite(rest_id=res_data.id, user_id=g.user.id, rest_name=res_data.name)
        db.session.add(fav)
        db.session.commit()
        return redirect('/')

    else:
        res = Restaurant(
            yelp_id=yelp_id, 
            name=name, 
            rating=rating,
            price_range=price_range, 
            url = url,
            image_url = image_url,
            rev_num = rev_num,
            phone = phone
        )

        db.session.add(res)
        db.session.commit()

        rest = Restaurant.query.filter_by(name=name).one()
        
        fav = Favorite(
            user_id = g.user.id,
            rest_id = rest.id,
            rest_name = name
        )
      
        db.session.add(fav)
        db.session.commit()   
        return jsonify(result)

@app.route('/users/favorites/<int:user_id>')
def show_fav(user_id):
    """Show list of favorite restaurants"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/favorites.html', user=user, favs=user.favorites)

@app.route('/fav/delete/<int:res_id>', methods=["POST"])
def delete_fav(res_id):
    """Remove favorites """
    fav = Favorite.query.filter(Favorite.rest_id==res_id).filter(Favorite.user_id == g.user.id).one()
    db.session.delete(fav)
    db.session.commit()
    return redirect(f'/users/favorites/{g.user.id}')

@app.route('/getfav', methods=['GET', 'POST'])
def get_fav():
    """Get a list of user's favorites"""
    favres = db.session.query(Restaurant).join(Favorite, Favorite.rest_id == Restaurant.id).filter(Favorite.user_id == g.user.id).all()
    serialized = [serialize_fav(f) for f in favres]

    return jsonify(serialized)

def serialize_fav(item):
    return{
            "name": item.name
        }

@app.route('/findID', methods=['GET', "POST"])
def find_and_delete():
    """Find restaurant using name and remove from favorites"""
    data = request.get_json()
    toDelete = Restaurant.query.filter(Restaurant.name == data).one()
    delete = delete_fav(toDelete.id)
    return jsonify(delete)

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

@app.route('/checkuser', methods=['GET'])
def send_user():
    """Send user information to client"""
    if g.user:
        user = User.query.get_or_404(g.user.id)
        ser = serialize(user)
        return jsonify(ser)
    else:
        return jsonify({'Error': 'User unavailable'})

def serialize(self):
    return{
            "username": self.username,
        }


@app.route('/users/login', methods=["GET", "POST"])
def login():
    """Log in user"""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        if user:
            do_login(user)
            flash(f"Welcome, {user.username}!", 'success')
            return redirect('/')
        flash('Invalid username/password', 'danger')
    return render_template('users/login.html', form=form)

@app.route('/users/logout')
def logout():
    """Log out user"""

    do_logout()

    flash("Log Out Successful", 'success')
    return redirect('/')

############User location #############

@app.route('/location', methods=["GET", "POST"])
def get_user_location():
    """Get user's location and save to session"""
    data = request.get_json()
    if 'latitude' in session:
        session.pop('latitude')
        session.pop('longitude')
    session['latitude'] = data['lat']
    session['longitude'] = data['lon']
    return jsonify(data)

@app.route('/getloc/<string:address>', methods=["GET", "POST"])
def get_location(address):
    """Look up user's address input"""
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={MAP_KEY}&location={address}"

    payload = {}

    response = requests.request("GET", url, data = payload)
    data = response.json()
    lat = data['results'][0]['locations'][0]['latLng']['lat']
    lon = data['results'][0]['locations'][0]['latLng']['lng']
    result = {
        'lat': lat,
        'lon': lon
    }
    return jsonify(result)

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



@app.route('/', methods=["GET", 'POST'])
def home_page():
    """Show homepage"""
    return render_template('homepage.html')
   
@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
