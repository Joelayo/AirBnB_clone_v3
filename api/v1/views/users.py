#!/usr/bin/python3
"""This module implements a view for amenities objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import user
from models.user import User
import models


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def retrieve_user_objs():
    """ Shows all user objects """
    myList = []
    for value in models.storage.all("User").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def show_user(user_id):
    """ Retrieves a user object, raise a 404 error if not linked """
    user = models.storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a user object in db storage """
    user = models.storage.get("User", user_id)
    if user:
        user.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users/', strict_slashes=False, methods=['POST'])
def create_user():
    ''' Creates a new user object '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    content = request.get_json()
    user = User(**content)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    ''' Upddate the user object with the given amenity_id '''
    user = models.storage.get("User", amenity_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
