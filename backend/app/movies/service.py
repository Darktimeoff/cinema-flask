from .dao import MovieDao
from app.models import Movie
from app.exceptions.http import BadRequestError, NotFoundError
from .const import UNCORECT_ID_TYPE, MOVIE_NOT_FOUND
from sqlalchemy import desc

class MovieService:
    dao: MovieDao

    def __init__(self, dao: MovieDao):
        self.dao = dao

    def get_all(self, status=None):
        query = self.dao.query
        if status == 'new':
            query = query.order_by(desc(Movie.year))
        return query
    
    def get_by_id(self, id: int) -> Movie:
        if type(id) is not int:
            raise BadRequestError(message=UNCORECT_ID_TYPE, status_code=1)
        
        movie = self.dao.get_by_id(id)

        if not movie:
            raise NotFoundError(message=MOVIE_NOT_FOUND, status_code=2)

        return movie
