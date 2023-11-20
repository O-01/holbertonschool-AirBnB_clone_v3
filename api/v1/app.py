#!/usr/bin/python3
"""json api"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import environ

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def remover(exception):
    """remove current session"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    return make_response(jsonify(error="Not found"), 404)


if __name__ == "__main__":
    app.run(
        host=environ.get('HBNB_API_HOST', '0.0.0.0'),
        port=environ.get('HBNB_API_PORT', '5000'),
        threaded=True
    )
