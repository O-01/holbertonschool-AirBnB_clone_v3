#!/usr/bin/python3
"""index module returns json status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status_index():
    """returns json status"""
    return jsonify(status="OK")
