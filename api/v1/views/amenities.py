#!/usr/bin/python3
""" Amenities """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    all = []
    for am in storage.all(Amenity).values():
        all.append(am.to_dict())
    return jsonify(all)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id=None):
    """Retrieves a State object"""
    if not amenity_id:
        return (self.get_amenities())
    else:
        am = storage.get(Amenity, amenity_id)
        if am is None:
            abort(404)
        return jsonify(am.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """Deletes a Amenity object"""
    am = storage.get(Amenity, amenity_id)
    if am is None:
        abort(404)
    else:
        storage.delete(am)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a amenity """
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    elif "name" not in req:
        abort(400, "Missing name")
    new = Amenity(name=req['name'])
    storage.new(new)
    storage.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenitie(amenity_id=None):
    """ update amenity """
    am = storage.get(Amenity, amenity_id)
    attr = ['id', 'created_at', 'updated_at']
    if am is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in attr:
            setattr(am, key, value)
    am.save()
    return (jsonify(am.to_dict()), 200)
