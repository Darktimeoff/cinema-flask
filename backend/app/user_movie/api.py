from flask_restx import Resource, Namespace
from flask import request
from app.decorators.api import serialized, auth_required
from app.container import user_schema
from .container import user_movie_service

user_movie_ns = Namespace('favourites/movies')

@user_movie_ns.route('/<int:movie_id>/')
class Favourite(Resource):
    @auth_required
    @serialized(user_schema)
    def post(self, user, movie_id):
        user = user_movie_service.add_to_favourite(user.id, movie_id)

        return user

    @auth_required
    @serialized(user_schema)
    def delete(self, user, movie_id):
        user = user_movie_service.delete_from_favourite(user.id, movie_id)

        return user
        