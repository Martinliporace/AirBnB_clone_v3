#!/usr/bin/python3
""" states """

from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=['GET'])
def get_states():
    """Retrieves the list of all State objects"""
    all = []
    for st in storage.all(State).values():
        all.append(st.to_dict())
    return jsonify(all)


@app_views.route("/states/<state_id>", methods=['GET'])
def get_state(state_id=None):
    """Retrieves a State object"""
    if not state_id:
        return (self.get_states())
    else:
        st = storage.get(State, state_id)
        if st is None:
            abort(404)
        return jsonify(st.to_dict())
