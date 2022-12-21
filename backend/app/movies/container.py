from .service import MovieService
from .dao import MovieDao
from app.models import Movie
from app.setup.db import db
from app.schemas import MovieSchema

movie_schema = MovieSchema()
movie_schemas = MovieSchema(many=True)

movie_dao = MovieDao(Movie, db)
movie_service = MovieService(movie_dao)