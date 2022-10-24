#!/usr/bin/python3
"""This module implements a view for city objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
import models


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False,
    methods=['GET'])
def retrieve_city_objs(state_id):
    """ Shows all city objects """
    state = models.storage.get("State", state_id)
    if state:
        myList = []
        for value in models.storage.all("City").values():
            if value.state_id == state_id:
                myList.append(value.to_dict())
        return jsonify(myList)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def show_city(city_id):
    """ Retrieves a city object, raise a 404 error if not linked """
    city = models.storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes a city object in db storage """
    city = models.storage.get("City", city_id)
    if city:
        city.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id):
    ''' Creates a new city object '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    if models.storage.get("State", state_id) is None:
        abort(404)
    data = request.get_json()
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    ''' Upddate the city object with the given state_id '''
    city = models.storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
