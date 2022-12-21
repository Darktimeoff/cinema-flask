from app.exceptions.http import BadRequestError, NotFoundError
from .const import GENRE_NOT_FOUND, UNCORECT_ID_TYPE
from .dao import GenreDAO
from app.models import Genre


class GenreService:
    dao: GenreDAO

    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_query()

    def get_by_id(self, id: int) -> Genre:
        if type(id) is not int:
            raise BadRequestError(message=UNCORECT_ID_TYPE, status_code=1)

        genre = self.dao.get_by_id(id)

        if not genre:
            raise NotFoundError(message=GENRE_NOT_FOUND, status_code=2)

        return genre
