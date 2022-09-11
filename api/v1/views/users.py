
#!/usr/bin/python3
""" Amenities """

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects """
    all = []
    for us in storage.all(User).values():
        all.append(us.to_dict())
    return (jsonify(all), 200)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id=None):
    """Retrieves a User object"""
    if not user_id:
        return (self.get_users())
    else:
        us = storage.get(User, user_id)
        if us is None:
            abort(404)
        return (jsonify(us.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id=None):
    """Deletes a User object"""
    us = storage.get(User, user_id)
    if us is None:
        abort(404)
    else:
        storage.delete(us)
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a user """
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    elif "email" not in req:
        abort(400, "Missing email")
    elif "password" not in req:
        abort(400, "Missing password")
    new = User(email=req['email'], password=req['password'])
    storage.new(new)
    storage.save()
    return (jsonify(new.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id=None):
    """ update user """
    us = storage.get(User, user_id)
    attr = ['id', 'email', 'created_at', 'updated_at']
    if us is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in attr:
            setattr(us, key, value)
    us.save()
    return (jsonify(us.to_dict()), 200)
