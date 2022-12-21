from app.decorators.api import pagination, serialized
from flask import request
from flask_restx import Namespace, Resource

from .container import director_schema, director_schemas, director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class Directors(Resource):
    @serialized(director_schemas)
    @pagination(12)
    def get(self):
        return director_service.get_all()


@director_ns.route('/<int:director_id>/')
class Director(Resource):
    @serialized(director_schema)
    def get(self, director_id: int):
        director = director_service.get_by_id(director_id)

        return director
