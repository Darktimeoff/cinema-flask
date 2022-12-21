from app.models import Genre
from app.schemas import GenreSchema
from app.setup.db import db

from .dao import GenreDAO
from .service import GenreService

genre_schema = GenreSchema()
genre_schemas = GenreSchema(many=True)

genre_dao = GenreDAO(Genre, db)
genre_service = GenreService(genre_dao)
