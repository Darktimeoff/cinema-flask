from app.classes.dao import Dao
from app.models import Movie
from sqlalchemy import desc

class MovieDao(Dao):
    __model: Movie
    def __init__(self, model: Movie, db):
        super().__init__(db)
        self.__model = model

    def set_query(self):
        self.__query = self.__model.query
        return self.__query

    def get_query(self):
        return self.query

    def order_by_year(self):
        return self.query.order_by(desc(Movie.year))

    def get_all(self):
        return self.query.all() #type: ignore

    def get_by_id(self, id: int):
        return self.query.get(id)

