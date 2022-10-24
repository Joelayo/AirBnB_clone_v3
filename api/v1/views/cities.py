#!/usr/bin/python3
"""This module implements a view for city objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
import models


@app_views.route('/cities', strict_slashes=False, methods=['GET'])
def retrieve_city_objs():
    """ Shows all city objects """
    myList = []
    for value in models.storage.all("City").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def show_city(city_id):
    """ Retrieves a city object, raise a 404 error if not linked """
    state = models.storage.get("City", city_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes a city object in db storage """
    state = models.storage.get("City", city_id)
    if state is None:
        abort(404)
    state.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/cities/', strict_slashes=False, methods=['POST'])
def create_city():
    ''' Creates a new city object '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    state = City(**content)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    ''' Upddate the city object with the given state_id '''
    state = models.storage.get("City", city_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
