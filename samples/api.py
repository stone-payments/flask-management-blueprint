"""A module that creates a Flask App and registers its blueprints."""
import sys
import os

LIB_PATH = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, LIB_PATH)

from flask import Flask
from flask_management_blueprint import setup_blueprint


def create_api(name):
    """Function that returns a Flask API with its blueprints registered."""
    api = Flask(name)
    api.register_blueprint(setup_blueprint())
    return api
