#!/usr/bin/python3
""" Place API view """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """ Get method for places in a  city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    city_place = []
    for place in places.values():
        if place.city_id == city_id:
            city_place.append(place.to_dict())
    return jsonify(city_place)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """ Retrieves a place by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a place by ID and return empty JSON in its place """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create a new Place """
    if storage.get(City, city_id) is None:
        abort(404)
    get_json = request.get_json()
    if not get_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in get_json.get:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if get_json.get('user_id') is None:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_id = get_json.get('user_id')
    if (storage.get(User, user_id) is None):
        abort(404)

    get_json['city_id'] = city_id
    new_place = Place(**get_json)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update place by its id """
    place_update = storage.get(Place, place_id)
    req = request.get_json()

    if place_update is None:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')

    exept = ['created_at', 'updated_at', 'id', 'user_id', 'city_id']
    for key, value in req.items():
        if key not in exept:
            setattr(place_update, key, value)
    place_update.save()
    return jsonify(place_update.to_dict()), 200
