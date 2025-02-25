#!/usr/bin/python3
""" Places """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id=None):
    """ Retrieves the list of all Place objects """
    all = []
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    for pl in cities.places:
        all.append(pl.to_dict())
    return jsonify(all)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id=None):
    """Retrieves a Place object"""
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    return jsonify(pl.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id=None):
    """Deletes a Place object"""
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    else:
        storage.delete(pl)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id=None):
    """ Creates a place """
    ci = storage.get(City, city_id)
    if ci is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    elif "name" not in req:
        abort(400, "Missing name")
    elif "user_id" not in req:
        abort(400, "Missing user_id")
    us = storage.get(User, req['user_id'])
    if not us:
        abort(404)
    new = Place(name=req['name'], city_id=ci.id, user_id=us.id)
    storage.new(new)
    storage.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id=None):
    """ update place """
    pl = storage.get(Place, place_id)
    attr = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    if pl is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in attr:
            setattr(pl, key, value)
    pl.save()
    return (jsonify(pl.to_dict()), 200)
