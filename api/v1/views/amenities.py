#!/usr/bin/python3
"""This module implements a view for amenities objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
import models


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def retrieve_amenity_objs():
    """ Shows all amenities objects """
    myList = []
    for value in models.storage.all("Amenity").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['GET'])
def show_amenity(amenity_id):
    """ Retrieves an amenity object, raise a 404 error if not linked """
    amenity = models.storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes an amenity object in db storage """
    amenity = models.storage.get("Amenity", amenity_id)
    if amenity:
        amenity.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities/', strict_slashes=False, methods=['POST'])
def create_amenity():
    ''' Creates a new amenity object '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    amenity = Amenity(**content)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['PUT'])
def update_amenity(amenity_id):
    ''' Upddate the amenity object with the given amenity_id '''
    amenity = models.storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
