#!/usr/bin/python3
""" cities """

from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id=None):
    """Retrieves the list of all State objects"""
    all = []
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    for ci in states.cities:
        all.append(ci.to_dict())
    return jsonify(all)


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id=None):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id=None):
    """Deletes a City object"""
    ci = storage.get(City, city_id)
    if ci is None:
        abort(404)
    else:
        storage.delete(ci)
        storage.save()
        return (jsonify({}), 200)


@app_views.route("states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id=None):
    """ Creates a citie """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    elif "name" not in req:
        abort(400, "Missing name")
    new = City(name=req['name'], state_id=states.id)
    storage.new(new)
    storage.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id=None):
    """ update city """
    ci = storage.get(City, city_id)
    attr = ['id', 'created_at', 'updated_at']
    if ci is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in attr:
            setattr(ci, key, value)
    ci.save()
    return (jsonify(ci.to_dict()), 200)
