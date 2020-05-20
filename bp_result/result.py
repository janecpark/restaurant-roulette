from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify, Blueprint, make_response, abort
from models import db, connect_db, User, Restaurant, Favorite
from api.api_req import get_result, get_result_pref
from bp_error.error_handlers import handle400
from flask_login import login_required, login_user, current_user, logout_user

import requests
import random
import json

result = Blueprint('result', __name__, template_folder='templates')


def add_to_session(response):
    session['id'] = response[0]['id']
    session['name'] = response[0]['name']
    session['rating'] = response[0]['rating']
    session['price_range'] = response[0]['price'] or 'n/a'
    session['image_url'] = response[0]['image_url'] 
    session['url'] = response[0]['url']
    session['phone'] = response[0]['phone']
    session['rev_num'] = response[0]['review_count']
    session['address'] = response[0]['location']['address1']
    session['city'] = response[0]['location']['city']
    session['state'] = response[0]['location']['state']
    session['zipcode'] = response[0]['location']['zip_code']
    
def pop_session():
    session.pop('name')
    session.pop('id')
    session.pop('rating')
    session.pop('price_range')
    session.pop('image_url')
    session.pop('url')
    session.pop('phone')
    session.pop('address')
    session.pop('city')
    session.pop('state')
    session.pop('zipcode')


@result.route('/cuisine', methods=["GET", "POST"])
def get_cuisine():
    try:
        if 'name' in session:
            pop_session()
        data = request.get_json()
        resp = get_result_pref(data, 5, 4000)
        response = resp['businesses']

        if response:
            add_to_session(response)
            return jsonify(response)

    except:
        return jsonify("Error:", "No Response")
            

@result.route('/result')
def session_result():
    if 'name' in session:
        name = session['name']
        if current_user.is_authenticated:
            user = User.query.get_or_404(current_user.id)
            favres = Favorite.query.filter(Favorite.rest_name == name).filter(Favorite.user_id == user.id).first()
        else:
            favres = None
    else:
        favres = None
    
    return render_template('/result/session-result.html', favres=favres)    

@result.route('/nearbyRes', methods=["GET", "POST"])
def nearby():
    """Render response for nearby restaurants"""
    if 'name' in session:
        pop_session()
    response = get_result(12)
    return jsonify(response)

@result.route('/set-options', methods=["GET", 'POST'])
def set_pref():
    """Set preferences for the user"""
    
    if request.method == 'POST':
        cuisine = request.form.get('cuisine') 
        price = request.form.get('price') 
        distance = request.form.get('distance')
        data = get_result_pref(cuisine, price, distance)
        response = data['businesses']

        if response and current_user.is_authenticated:
            add_to_session(response)
            name = response[0]['name']
            user = User.query.get_or_404(current_user.id)
            favres = Favorite.query.filter(Favorite.rest_name == name).filter(Favorite.user_id == user.id).first()
        else:
            favres = None
    
        return render_template('/result/session-result.html', favres=favres)

    return render_template('/result/preferences.html')

@result.route('/handleRes', methods=["GET", 'POST'])        
def handle_result():
    """Route to handle result and add to session"""
    obj = request.get_json()

    if 'name' in session:
        pop_session()

    session['id'] = obj['id']
    session['name'] = obj['name']
    session['image_url'] = obj['image_url']
    session['rating'] = obj['rating']
    session['phone'] = obj['phone']
    session['rev_num'] = obj['review_count']
    session['price_range'] = obj['price']
    session['url'] = obj['url']
    session['address'] = obj['address']
    session['city'] = obj['city']
    session['state'] = obj['state']
    session['zipcode'] = obj['zip_code']

    return jsonify({'result': 'success'})

@result.route('/error')
def render_error():
    return render_template('result/error.html')