#!/usr/bin/python3
""" cities """

from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.cities import City


@app_views.route("/cities", methods=['GET'], strict_slashes=False)
def get_cities():
    """Retrieves the list of all State objects"""
    all = []
    for ci in storage.all(City).values():
        all.append(ci.to_dict())
    return jsonify(all)


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id=None):
    """Retrieves a City object"""
    if not city_id:
        return (self.get_cities())
    else:
        ci = storage.get(City, city_id)
        if ci is None:
            abort(404)
        return jsonify(ci.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete(city_id=None):
    """Deletes a City object"""
    ci = storage.get(City, city_id)
    if ci is None:
        abort(404)
    else:
        storage.delete(ci)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create():
    """ Creates a citie """
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    elif "name" not in req:
        abort(400, "Missing name")
    new = City(name=req['name'])
    storage.new(new)
    storage.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update(city_id=None):
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
