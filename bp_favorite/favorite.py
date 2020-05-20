from flask import Flask, render_template, request, flash, redirect, session, url_for, g, jsonify, Blueprint
from models import db, connect_db, User, Restaurant, Favorite
from flask_login import login_required, login_user, current_user, logout_user
import requests
import json

fav = Blueprint('fav', __name__, template_folder='templates')

@fav.route('/add_fav/', methods=["GET", "POST"])
def add_user_fav():
    """Add user's favorite to database"""

    yelp_id = session['id']      
    name = session['name']
    rating = session['rating']
    price_range = session['price_range'] 
    url = session['url'] 
    image_url = session['image_url'] 
    phone = session['phone']
    rev_num = session['rev_num']
  
    res_data = Restaurant.query.filter(Restaurant.yelp_id==yelp_id).first()
    all_res = Restaurant.query.all()
        
    if res_data in all_res:
        # if the restaurant is already in db, add rest to fav list
        fav = Favorite(rest_id=res_data.id, user_id=current_user.id, rest_name=res_data.name)
        db.session.add(fav)
        db.session.commit()
        return redirect('/')

    else:
        res = Restaurant(yelp_id=yelp_id, name=name, rating=rating, price_range=price_range, url = url, image_url = image_url, rev_num = rev_num, phone = phone)

        db.session.add(res)
        db.session.commit()

        rest = Restaurant.query.filter_by(name=name).one()
        
        fav = Favorite(user_id = current_user.id, rest_id = rest.id, rest_name = name)
      
        db.session.add(fav)
        db.session.commit()
      
        return res

@fav.route('/favorites/<int:user_id>')
def show_fav(user_id):
    """Show list of favorite restaurants"""
    user = User.query.get_or_404(user_id)
    return render_template('/favorite/favorites.html', user=user, favs=user.favorites)

@fav.route('/fav/delete/<int:res_id>', methods=["POST"])
def delete_fav(res_id):
    """Remove favorites """
    fav = Favorite.query.filter(Favorite.rest_id==res_id).filter(Favorite.user_id == current_user.id).one()
    db.session.delete(fav)
    db.session.commit()
    return redirect(f'/favorite/favorites/{current_user.id}')

@fav.route('/getfav', methods=['GET', 'POST'])
def get_fav():
    """Get a list of user's favorites"""
    favres = db.session.query(Restaurant).join(Favorite, Favorite.rest_id == Restaurant.id).filter(Favorite.user_id == current_user.id).all()
    serialized = [serialize_fav(f) for f in favres]
    return jsonify(serialized)

def serialize_fav(item):
    return{
            "name": item.name
        }

@fav.route('/findID', methods=['GET', "POST"])
def find_and_delete():
    """Find restaurant using name and remove from favorites"""
    data = request.get_json()
    toDelete = Restaurant.query.filter(Restaurant.name == data).one()
    delete = delete_fav(toDelete.id)
    return jsonify(delete)

