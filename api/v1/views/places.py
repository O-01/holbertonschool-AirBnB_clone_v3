#!/usr/bin/python3
"""API places view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False
)
def places_from_city_get(city_id):
    """
    Retrieves list of all Place objects of a given City upon GET request
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(
        [
            place.to_dict()
            for place in city.places
        ]
    )


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_get(place_id):
    """Retrieves specific Place object upon GET request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def places_delete(place_id):
    """Deletes specified Place object if found upon DELETE request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route(
    '/cities/<city_id>/places',
    methods=['POST'],
    strict_slashes=False
)
def places_post(city_id):
    """Creates State object upon POST request"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    elif not request.get_json():
        abort(400, description='Not a JSON')
    elif 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    elif storage.get(User, request.get_json()['user_id']) is None:
        abort(404)
    elif 'name' not in request.get_json():
        abort(400, 'Missing name')
    else:
        new_place = Place(**request.get_json())
        new_place.city_id = city_id
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def places_put(place_id):
    """Updates specified State object if found upon PUT request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif not request.get_json():
        abort(400, description='Not a JSON')
    else:
        [
            setattr(place, key, value)
            for key, value in request.get_json().items()
            if key not in [
                'id', 'user_id', 'city_id' 'created_at', 'updated_at'
            ]
        ]
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
