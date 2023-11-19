#!/usr/bin/python3
"""API cities view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False
)
def cities_from_state_get(state_id):
    """Retrieves list of all City objects of a given State upon GET request"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(
        [
            city.to_dict()
            for city in state.cities
        ]
    )


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_get(city_id):
    """Retrieves specific City object upon GET request"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_delete(city_id):
    """Deletes specified City object if found upon DELETE request"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
)
def cities_post(state_id):
    """Creates City object upon POST request"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    elif not request.get_json():
        abort(400, description='Not a JSON')
    elif 'name' not in request.get_json():
        abort(400, 'Missing name')
    else:
        new_city = City(**request.get_json())
        new_city.state_id = state_id
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def cities_put(city_id):
    """Updates specified State object if found upon PUT request"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    elif not request.get_json():
        abort(400, description='Not a JSON')
    else:
        [
            setattr(city, key, value)
            for key, value in request.get_json().items()
            if key not in ['id', 'state_id' 'created_at', 'updated_at']
        ]
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
