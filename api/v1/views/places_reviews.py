#!/usr/bin/python3
"""Review API"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Get method for reviews of a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review)
    place_review = []
    for review in reviews.values():
        if review.place_id == place_id:
            place_review.append(review.to_dict())
    return jsonify(place_review)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Get a review by its id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create  Reviews """
    if (storage.get(Place, place_id)) is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, 'Not a JSON')
    if "text" not in req.get:
        abort(400, 'Missing text')
    if "user_id" not in req.get:
        abort(400, 'Missing user_id')
    user_id = req.get('user_id')
    if (storage.get(User, user_id) is None):
        abort(404)

    req['place_id'] = place_id
    new_review = Review(**req)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review"""
    review = storage.get(Review, review_id)
    req = request.get_json()

    if review is None:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')

    exept = ['created_at', 'updated_at', 'id', 'user_id', 'place_id']
    for key, value in req.items():
        if key not in exept:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
