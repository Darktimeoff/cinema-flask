from app.directors.const.service import DIRECTOR_NOT_FOUND, UNCORECT_ID_TYPE
from app.directors.dao.director import DirectorDao
from app.exceptions.http import BadRequestError, NotFoundError
from app.models import Director
from sqlalchemy import desc


class DirectorService:
    dao: DirectorDao

    def __init__(self, dao: DirectorDao):
        self.dao = dao

    def get_all(self):
        return self.dao.query

    def get_by_id(self, id: int) -> Director:
        if type(id) is not int:
            raise BadRequestError(message=UNCORECT_ID_TYPE, status_code=1)

        movie = self.dao.get_by_id(id)

        if not movie:
            raise NotFoundError(message=DIRECTOR_NOT_FOUND, status_code=2)

        return movie
