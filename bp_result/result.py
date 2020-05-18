from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify, Blueprint, make_response
from models import db, connect_db, User, Restaurant, Favorite
from api.api_req import get_result, get_result_pref
from flask_login import login_required, login_user, current_user, logout_user
import requests
import random
import json

result = Blueprint('result', __name__, template_folder='templates')


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

@result.route('/spin', methods=['GET', 'POST'])
def lucky_spin():
    """Post and render response"""
    if 'name' in session:
        pop_session()
    response = get_result(1)
    add_to_session(response)
    return jsonify(response)

@result.route('/cuisine/<string:cuisine>', methods=["GET"])
def get_cuisine(cuisine):
    if 'name' in session:
        pop_session()

    data = get_result_pref(cuisine, 1, 3000)
    response = data['businesses']

    if response and current_user.is_authenticated:
        add_to_session(response)
    return jsonify(response)
    

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
    
        return render_template('/result/userresult.html', response=response, favres=favres)

    return render_template('/result/preferences.html')

    

@result.route('/handleRes', methods=['POST'])        
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