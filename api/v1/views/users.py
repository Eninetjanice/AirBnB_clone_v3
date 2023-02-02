#!/usr/bin/python3
"""User API view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_request, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def list_users():
    """ Retrieves all users """
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """ Get a user by it's id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Delete a user by ID and return empty JSON in its place """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a new User """
    get_json = request.get_json()
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)

    new_user = User(**get_json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Update User by <state_id> """
    user_update = storage.get(User, user_id)
    req = request.get_json()

    if user_update is None:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')

    exx = ['id', 'created_at', 'updated_at', 'email']
    for key, value in req.items():
        if key not in exx:
            setattr(user_update, key, value)
    storage.save()
    return jsonify(user_update.to_dict()), 200
