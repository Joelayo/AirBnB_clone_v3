#!/usr/bin/python3
"""This module implements a view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
import models


@app_views.route('/places/<place_id>/review', strict_slashes=False, methods=['GET'])
def retrieve_review_objs(place_id):
    """ Shows all review objects """
    place = models.storage.get("Place", place_id)
    if place is None:
        abort(404)
    myList = []
    for value in models.storage.all("Review").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/reviews/review_id>', strict_slashes=False, methods=['GET'])
def show_review(review_id):
    """ Retrieves a review object, raise a 404 error if not linked """
    state = models.storage.get("Review", review_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_place(review_id):
    """ Deletes a review object in db storage """
    state = models.storage.get("Review", review_id)
    if state is None:
        abort(404)
    state.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def create_review(place_id):
    ''' Creates a new review object '''
    place = models.storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    user_id = models.storage.get("User", user_id)
    if user_id is None:
        abort(404)
    if 'text' not in request.json:
        return jsonify({"error": "Missing text"}), 400
    content = request.get_json()
    state = Review(**content)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    ''' Update the review object with the given review_id '''
    state = models.storage.get("Review", review_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
