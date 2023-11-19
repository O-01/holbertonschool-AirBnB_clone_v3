#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import abort, jsonify, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route(
    '/states/<state_id>',
    methods=['GET'],
    strict_slashes=False
)
def states_get(state_id=None):
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
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def states_delete(state_id):
    """Deletes specified State object if found upon DELETE request"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """Creates State object upon POST request"""
    pass


@app_views.route(
    '/states/<state_id>',
    methods=['PUT'],
    strict_slashes=False
)
def states_put(state_id):
    """Updates specified State object if found upon PUT request"""
    pass
