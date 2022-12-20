from app.movies.dao.movie import MovieDao
from app.models import Movie
from app.exceptions.http import BadRequestError, NotFoundError
from app.movies.const.service import UNCORECT_ID_TYPE, MOVIE_NOT_FOUND

class MovieService:
    dao: MovieDao

    def __init__(self, dao: MovieDao):
        self.dao = dao

    def get_all(self):
        return self.dao.query
    
    def get_by_id(self, id: int) -> Movie:
        if type(id) is not int:
            raise BadRequestError(message=UNCORECT_ID_TYPE, status_code=1)
        
        movie = self.dao.get_by_id(id)

        if not movie:
            raise NotFoundError(message=MOVIE_NOT_FOUND, status_code=2)

        return movie
