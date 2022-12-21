from flask import request
from flask_restx import Resource, Namespace
from app.decorators.api import pagination, serialized
from .container import movie_schemas, movie_service, movie_schema

movie_ns = Namespace('movies')

@movie_ns.route('/')
class Movies(Resource):
    @serialized(movie_schemas)
    @pagination(12)
    def get(self):
        status = request.args.get('status', None)

        return movie_service.get_all(status)

@movie_ns.route('/<int:movie_id>/')
class Movie(Resource):
    @serialized(movie_schema)
    def get(self, movie_id: int):
        movie = movie_service.get_by_id(movie_id)
    
        return movie 
