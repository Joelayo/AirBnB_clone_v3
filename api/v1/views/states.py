#!/usr/bin/python3
"""This module implements a view for state objects"""
from api import app
from models.base_model import BaseModel

@app.route('/api/v1/states/', strict_slashes=False, methods=['GET'])
def retrieve_state_objs():

