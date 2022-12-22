from flask_restx import Resource, Namespace
from flask import request
from app.decorators.api import serialized, auth_required
from .container import user_movie_service
from app.movies.container import movie_schemas

user_movie_ns = Namespace('favourites/movies')

@user_movie_ns.route('/')
class Favourites(Resource):
    @serialized(movie_schemas)
    @auth_required
    def get(self, user):
        movies = user_movie_service.get_all(user.id)

        return movies
@user_movie_ns.route('/<int:movie_id>/')
class Favourite(Resource):
    @auth_required
    @serialized(movie_schemas)
    def post(self, user, movie_id):
        user = user_movie_service.add_to_favourite(user.id, movie_id)

        return user

    @auth_required
    @serialized(movie_schemas)
    def delete(self, user, movie_id):
        user = user_movie_service.delete_from_favourite(user.id, movie_id)

        return user
        