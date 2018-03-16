"""A module that creates a Flask App and registers its blueprints."""
import sys
import os

LIB_PATH = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, LIB_PATH)

from flask import Flask
from flask_management_blueprint.management import setup_blueprint, AppInfo, HealthCheck

def sample_check_resource():
    return True
    
def create_api(name):
    """Function that returns a Flask API with its blueprints registered."""
    api = Flask(name)
    api.register_blueprint(setup_blueprint())
    AppInfo.register_resource(sample_check_resource)
    HealthCheck.register_resource('httpbin', 'https://httpbin.org/get')

    return api
