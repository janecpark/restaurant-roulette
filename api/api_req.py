import os
from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify, Blueprint
from models import db, connect_db, User, Restaurant, Favorite
import requests
import random
import json


API_KEY = os.getenv('API_KEY')
token = os.getenv('token')
MAP_KEY = os.getenv('MAP_KEY')


BASE_URL ='https://api.yelp.com/v3/businesses/search'
LOCATION_URL = "http://www.mapquestapi.com/geocoding/v1/address"
REVERSE_URL = "http://www.mapquestapi.com/geocoding/v1/reverse"


def get_result(num):
    """Get API result"""
   
    HEADERS = {'Authorization': f'bearer {API_KEY}'}
    payload = {}
    PARAMS = {'term': 'restaurant',
            'limit': num,
            'latitude': session['latitude'],
            'longitude': session['longitude'],
            'offset': random.randint(0, 100)
            }

    resp = requests.request("GET", BASE_URL, params=PARAMS, headers = HEADERS, data = payload)
        
    if resp is None:
        return jsonify({'error': 'Invalid response'}),422

    data = resp.json()
    restaurants = data['businesses']
    return restaurants

def get_result_pref(cuisine,price,distance):
    """Get API results with preferences"""
      
    HEADERS = {'Authorization': f'bearer {API_KEY}'}
    payload = {}

    PARAMS = {'term': 'restaurant',
              'limit': 1,
              'latitude': session['latitude'],
              'longitude': session['longitude'],
              'offset': random.randint(0, 5),
              'distance': distance,
              'categories': cuisine,
              'price': price}

    resp = requests.request("GET", BASE_URL, params=PARAMS, headers = HEADERS, data = payload)
        
    if resp is None:
        return jsonify({'error': 'Invalid response'}),422

    data = resp.json()

    return data

def get_location(address):
    """Look up user's address input"""
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={MAP_KEY}&location={address}"

    payload = {}

    response = requests.request("GET", url, data = payload)
    data = response.json()
    return data

def get_city(lat,lng):
    """Reverse geolookup"""

    url = REVERSE_URL
    
    params={
        'lat': lat,
        'lng': lng,
        'key': {MAP_KEY}
    }
    
    resp = requests.get(url, params=params)
    location = resp.json()
    city = location['results'][0]['locations'][0]['adminArea5']
    session['city'] = city

    return city




