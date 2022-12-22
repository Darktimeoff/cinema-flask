from app.user.service import UserService
from app.movies.service import MovieService
from app.exceptions.service import ValidationError
from app.classes.dao import Dao
from .const import INVALID_ID_TYPE

class UserMovieService:
    user_service: UserService
    movie_service: MovieService
    dao: Dao

    def __init__(self, user_service: UserService, movie_service: MovieService, dao: Dao):
        self.user_service = user_service
        self.movie_service = movie_service
        self.dao = dao

    def add_to_favourite(self, uid: int, mid: int):
        if type(uid) is not int or type(mid) is not int:
            raise ValidationError(message=INVALID_ID_TYPE, status_code=1)

        user = self.user_service.get_by_id(uid)
        movie = self.movie_service.get_by_id(mid)

        user.favourite_movies.append(movie)
        self.dao.update_data_in_db(user)

        return user

    def delete_from_favourite(self, uid: int, mid: int):
        if type(uid) is not int or type(mid) is not int:
            raise ValidationError(message=INVALID_ID_TYPE, status_code=1)

        user = self.user_service.get_by_id(uid)
        movie = self.movie_service.get_by_id(mid)

        user.favourite_movies.remove(movie)
        self.dao.update_data_in_db(user)

        return user

