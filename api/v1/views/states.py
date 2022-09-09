#!/usr/bin/python3
""" states """

from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all = []
    for st in storage.all(State).values():
        all.append(st.to_dict())
    return jsonify(all)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Retrieves a State object"""
    if not state_id:
        return (self.get_states())
    else:
        st = storage.get(State, state_id)
        if st is None:
            abort(404)
        return jsonify(st.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id=None):
    """Deletes a State object"""
    st = storage.get(State, state_id)
    if st is None:
        abort(404)
    else:
        storage.delete(st)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """ Creates a state """
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    elif "name" not in req:
        abort(400, "Missing name")
    new = State(name=req['name'])
    storage.new(new)
    storage.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update(state_id=None):
    """ update state """
    st = storage.get(State, state_id)
    attr = ['id', 'created_at', 'updated_at']
    if st is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for key, value in st.items():
        if key not in attr:
            setattr(st, key, value)
    st.save()
    return (jsonify(st.to_dict()), 201)
