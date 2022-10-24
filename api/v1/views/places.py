#!/usr/bin/python3
"""This module implements a view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
import models


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['GET'])
def retrieve_place_objs(city_id):
    """ Shows all place objects """
    city = models.storage.get("City", city_id)
    if city:
        placesList = []
        eachPlace = models.storage.all("Place")
        for value in eachPlace.values():
            if value.city_id == city_id:
                placesList.append(value.to_dict())
        return jsonify(placesList)
    abort(404)


@app_views.route('/places/place_id>', strict_slashes=False, methods=['GET'])
def show_place(place_id):
    """ Retrieves a place object, raise a 404 error if not linked """
    place = models.storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a place object in db storage """
    place = models.storage.get("Place", place_id)
    if place:
        place.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['POST'])
def create_place(city_id):
    ''' Creates a new place object '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    if models.storage.get("City", city_id) is None:
        abort(404)

    data = request.get_json()
    if models.storage.get("User", data["user_id"]) is None:
        abort(404)
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_user(place_id):
    ''' Update the place object with the given place_id '''
    place = models.storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200
