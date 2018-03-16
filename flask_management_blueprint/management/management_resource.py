"""Resource to manage api settings"""
from flask import jsonify
from flask import Blueprint, render_template, abort
from .app_info import AppInfo
from .health_check import HealthCheck


def setup_blueprint():
    """Creates a blueprint and register its routes"""
    blueprint = Blueprint('Management', __name__)
    blueprint.route('/management/app-info', methods=['GET'])(app_info)
    blueprint.route('/management/health-check', methods=['GET'])(health_check)
    return blueprint


def app_info():
    """Returns general informations about the application"""
    return jsonify(AppInfo.app_info())


def health_check():
    """Returns general informations about the health of the application"""
    info = AppInfo.app_info()
    info['Components'] = HealthCheck.check_resources_health()
    return jsonify(info)
