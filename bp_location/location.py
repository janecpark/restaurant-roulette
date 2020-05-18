import os
from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify, Blueprint
from models import db, connect_db, User, Restaurant, Favorite
from api.api_req import get_city, get_location
import requests
import json

MAP_KEY = os.getenv('MAP_KEY')
location = Blueprint('location', __name__, template_folder='templates')

LOCATION_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MAP_URL = "https://open.mapquestapi.com/staticmap/v5/map"


@location.route('/location', methods=["GET", "POST"])
def get_user_location():
    """Get user's location and save to session"""
    data = request.get_json()
    session['latitude'] = data['lat']
    session['longitude'] = data['lon']
    city = get_city(session['latitude'], session['longitude'])

    return jsonify(city)


@location.route('/citysess', methods=['GET', "POST"])
def render_city():
    if 'city' in session:
        data = {'city': session['city']}
        return jsonify(data)
        
@location.route('/checksess', methods=['GET'])
def render_session():
    if 'latitude' in session:
        data = {'lat': session['latitude'], 'lon': session['longitude']}
    else:
        data = {'error': 'no session found'}
    return jsonify(data)


@location.route('/getloc/<string:address>', methods=["GET", "POST"])
def address_req(address):
    data = get_location(address)
    
    lat = data['results'][0]['locations'][0]['latLng']['lat']
    lon = data['results'][0]['locations'][0]['latLng']['lng']
    
    session['latitude'] = lat
    session['longitude'] = lon
    city = get_city(session['latitude'], session['longitude'])
    return jsonify(city)

