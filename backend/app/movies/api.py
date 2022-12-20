from flask_restx import Resource, Namespace
from app.decorators.pagination import pagination
from .container import movie_schemas, movie_service, movie_schema

movie_ns = Namespace('movies')

@movie_ns.route('/')
class Movies(Resource):
    @pagination(movie_schemas, 12)
    def get(self):
        return movie_service.get_all()

@movie_ns.route('/<int:movie_id>/')
class Movie(Resource):
    def get(self, movie_id: int):
        movie = movie_service.get_by_id(movie_id)
    
        return movie_schema.dump(movie) 
