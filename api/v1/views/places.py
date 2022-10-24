#!/usr/bin/python3
"""This module implements a view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
import models


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def retrieve_place_objs(city_id):
    """ Shows all place objects """
    place = models.storage.get("City", city_id)
    if place is None:
        abort(404)
    myList = []
    for value in models.storage.all("Place").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/places/place_id>', strict_slashes=False, methods=['GET'])
def show_place(place_id):
    """ Retrieves a place object, raise a 404 error if not linked """
    state = models.storage.get("Place", place_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a place object in db storage """
    state = models.storage.get("Place", place_id)
    if state is None:
        abort(404)
    state.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def create_place(city_id):
    ''' Creates a new place object '''
    place = models.storage.get("City", city_id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    user_id = models.storage.get("User", user_id)
    if user_id is None:
        abort(404)
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    state = Place(**content)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_user(place_id):
    ''' Update the place object with the given place_id '''
    state = models.storage.get("Place", place_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
