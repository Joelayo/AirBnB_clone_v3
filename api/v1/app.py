#!/usr/bin/python3
"""app.py to connect to API"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ Return JSON instead of HTML """
    data = {"error": "Not found"}
    return (jsonify(data), 404)


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST"), port=os.getenv("HBNB_API_PORT"),
            threaded=True)
