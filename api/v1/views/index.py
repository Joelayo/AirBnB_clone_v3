#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


hbnbText = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnbStatus"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnbStats():
    """hbnbStats"""
    return_dict = {}
    for key, value in hbnbText.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)


@app_views.route('/api/v1/stats', strict_slashes=False)
def obj_counts():
    """return number of objects by type"""
    obj_dict = {}
    for i in hbnbText:
        obj_dict[i] = storage.count(hbnbText[i])
    return jsonify(obj_dict)


if __name__ == "__main__":
    pass
