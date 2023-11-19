#!/usr/bin/python3
"""API amenities view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False
)
def amenities_get(amenity_id=None):
    """
    Retrieves list of all Amenity objects upon GET request
    OR
    Retrieves specific Amenity object upon GET request
    """
    if amenity_id is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        else:
            return jsonify(amenity.to_dict())
    else:
        return jsonify(
            [amenity.to_dict() for amenity in storage.all(Amenity).values()]
        )


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def amenitys_delete(amenity_id):
    """Deletes specified Amenity object if found upon DELETE request"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenitys_post():
    """Creates Amenity object upon POST request"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    elif 'name' not in request.get_json():
        abort(400, 'Missing name')
    else:
        new_amenity = Amenity(**request.get_json())
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False
)
def amenities_put(amenity_id):
    """Updates specified Amenity object if found upon PUT request"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif not request.get_json():
        abort(400, description='Not a JSON')
    else:
        [
            setattr(amenity, key, value)
            for key, value in request.get_json().items()
            if key not in ['id', 'created_at', 'updated_at']
        ]
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
