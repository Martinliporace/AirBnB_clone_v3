#!/usr/bin/python3
""" Places """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_places_reviews(place_id=None):
    """ Retrieves the list of all Reviews objects """
    all = []
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    for re in places.reviews:
        all.append(re.to_dict())
    return jsonify(all)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id=None):
    """Retrieves a Review object"""
    re = storage.get(Review, review_id)
    if re is None:
        abort(404)
    return jsonify(re.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id=None):
    """Deletes a Review object"""
    re = storage.get(Review, review_id)
    if re is None:
        abort(404)
    else:
        storage.delete(re)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id=None):
    """ Creates a review """
    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    elif "user_id" not in req:
        abort(400, "Missing user_id")
    elif "text" not in req:
        abort(400, "Missing text")
    us = storage.get(User, req['user_id'])
    if not us:
        abort(404)
    new = Review(text=req['text'], place_id=place_id, user_id=req[us.id])
    storage.new(new)
    storage.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id=None):
    """ update review """
    re = storage.get(Review, review_id)
    attr = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if re is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in attr:
            setattr(re, key, value)
    re.save()
    return (jsonify(pl.to_dict()), 200)
