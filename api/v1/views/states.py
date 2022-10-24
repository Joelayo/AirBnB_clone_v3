#!/usr/bin/python3
"""This module implements a view for state objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
import models


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def retrieve_state_objs():
    """ Shows all states objects """
    myList = []
    for value in models.storage.all("State").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def show_state(state_id):
    """ Retrieves a state object, raise a 404 error if not linked """
    state = models.storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a state object in db storage """
    state = models.storage.get("State", state_id)
    if state:
        state.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def create_state():
    ''' Creates a new state object '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    state = State(**content)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    ''' Upddate the state object with the given state_id '''
    state = models.storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
