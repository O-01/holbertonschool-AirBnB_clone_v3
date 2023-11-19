#!/usr/bin/python3
"""API users view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route(
    '/users/<user_id>',
    methods=['GET'],
    strict_slashes=False
)
def users_get(user_id=None):
    """
    Retrieves list of all user objects upon GET request
    OR
    Retrieves specific user object upon GET request
    """
    if user_id is not None:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        else:
            return jsonify(user.to_dict())
    else:
        return jsonify(
            [user.to_dict() for user in storage.all(User).values()]
        )


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def users_delete(user_id):
    """Deletes specified user object if found upon DELETE request"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_post():
    """Creates user object upon POST request"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    elif 'email' not in request.get_json():
        abort(400, 'Missing email')
    elif 'password' not in request.get_json():
        abort(400, 'Missing password')
    else:
        new_user = User(**request.get_json())
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False
)
def users_put(user_id):
    """Updates specified user object if found upon PUT request"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    elif not request.get_json():
        abort(400, description='Not a JSON')
    else:
        [
            setattr(user, key, value)
            for key, value in request.get_json().items()
            if key not in ['id', 'email', 'created_at', 'updated_at']
        ]
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
