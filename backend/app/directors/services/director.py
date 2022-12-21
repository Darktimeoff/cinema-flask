from app.directors.const.service import DIRECTOR_NOT_FOUND, UNCORECT_ID_TYPE
from app.directors.dao.director import DirectorDao
from app.exceptions.http import BadRequestError, NotFoundError
from app.models import Director


class DirectorService:
    dao: DirectorDao

    def __init__(self, dao: DirectorDao):
        self.dao = dao

    def get_all(self):
        return self.dao.query

    def get_by_id(self, id: int) -> Director:
        if type(id) is not int:
            raise BadRequestError(message=UNCORECT_ID_TYPE, status_code=1)

        director = self.dao.get_by_id(id)

        if not director:
            raise NotFoundError(message=DIRECTOR_NOT_FOUND, status_code=2)

        return director
