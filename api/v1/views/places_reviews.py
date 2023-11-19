#!/usr/bin/python3
"""Reviews API view"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False
)
def reviews_of_place_get(place_id):
    """Gets a list of all Review objects of a given Place upon GET request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(
        [
            review.to_dict()
            for review in place.reviews
        ]
    )


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviews_get(review_id):
    """Retrieves specific Review object upon GET request"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def reviews_delete(review_id):
    """Deletes specified Review object if found upon DELETE request"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False
)
def reviews_post(place_id):
    """Creates Review object upon POST request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif not request.get_json():
        abort(400, description='Not a JSON')
    elif 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    elif storage.get(User, request.get_json()['user_id']) is None:
        abort(404)
    elif 'text' not in request.get_json():
        abort(400, 'Missing text')
    else:
        new_review = Review(**request.get_json())
        new_review.place_id = place_id
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def reviews_put(review_id):
    """Updates specified Review object if found upon PUT request"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    elif not request.get_json():
        abort(400, description='Not a JSON')
    else:
        [
            setattr(review, key, value)
            for key, value in request.get_json().items()
            if key not in [
                'id',
                'user_id',
                'place_id',
                'created_at',
                'updated_at'
            ]
        ]
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
