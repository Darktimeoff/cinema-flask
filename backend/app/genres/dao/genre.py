from app.classes.dao import Dao
from app.models import Genre


class GenreDAO(Dao):
    __model: Genre

    def __init__(self, model: Genre, db):
        super().__init__(db)
        self.__model = model

    def set_query(self):
        self.__query = self.__model.query
        return self.__query

    def get_all(self):
        return self.query.all()  # type: ignore

    def get_by_id(self, id: int):
        return self.query.get(id)
