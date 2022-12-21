from app.decorators.api import pagination, serialized
from flask_restx import Namespace, Resource

from .container import genre_schema, genre_schemas, genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class Genres(Resource):
    @serialized(genre_schemas)
    @pagination(12)
    def get(self):
        return genre_service.get_all()


@genre_ns.route('/<int:genre_id>/')
class Genre(Resource):
    @serialized(genre_schema)
    def get(self, genre_id: int):
        movie = genre_service.get_by_id(genre_id)

        return movie
