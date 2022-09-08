#!/usr/bin/python3
""" index """

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status")
def status():
    """ Returns json message """
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """ Returns the number of each objects by type """
    dict = {"amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')}
    return jsonify(dict)
