#!/usr/bin/python3
"""This module implements a view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
import models


@app_views.route(
    '/places/<place_id>/review',
    strict_slashes=False,
    methods=['GET'])
def retrieve_review_objs(place_id):
    """ Shows all review objects """
    place = models.storage.get("Place", place_id)
    if place:
        reviewsList = []
        for value in models.storage.all("Review").values():
            if value.place_id == place_id:
                reviewsList.append(value.to_dict())
        return jsonify(reviewsList)
    abort(404)


@app_views.route(
    '/reviews/review_id>',
    strict_slashes=False,
    methods=['GET'])
def show_review(review_id):
    """ Retrieves a review object, raise a 404 error if not linked """
    review = models.storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_place(review_id):
    """ Deletes a review object in db storage """
    review = models.storage.get("Review", review_id)
    if review:
        review.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False,
    methods=['POST'])
def create_review(place_id):
    ''' Creates a new review object '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in request.json:
        return jsonify({"error": "Missing text"}), 400
    if models.storage.get("Place", place_id) is None:
        abort(404)

    data = request.get_json()
    if models.storage.get("User", data["user_id"]) is None:
        abort(404)
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    ''' Update the review object with the given review_id '''
    review = models.storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key not in [
            'id',
            'created_at',
            'updated_at',
            'user_id',
                'place_id']:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
