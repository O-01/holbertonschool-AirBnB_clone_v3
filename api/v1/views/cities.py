#!/usr/bin/python3
""" """
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
def cities_from_state_get(state_id=None):
    """
    Retrieves list of all State objects upon GET request
    OR
    Retrieves specific State object upon GET request
    """
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            return jsonify(state.to_dict())
    else:
        return jsonify(
            [state.to_dict() for state in storage.all(State).values()]
        )

@app_views.route(
    '/cities/<city_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_city_by_id(city_id=None):
    """
    Retrieves list of all City objects upon GET request
    OR
    Retrieves specific City object upon GET request
    """
    if city_id is not None:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            return jsonify(city.to_dict())
    else:
        return jsonify(
            [city.to_dict() for city in storage.all(City).values()]
        )

@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def cities_delete(city_id):
    """Deletes specified city object if found upon DELETE request"""
    city = storage.get(city, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def cities_post(state_id=None):
    """Creates city object upon POST request"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    json_data = request.get_json()

    if "name" not in json_data:
        return jsonify({"error": "Missing name"}), 400

    new_city = City(**json_data)
    new_city.state_id = state_id.id
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201

@app_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False
)
def citys_put(city_id=None):
    """Updates specified city object if found upon PUT request"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    json_data = request.get_json()

    for key, value in json_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()

    return jsonify(city.to_dict()), 200


