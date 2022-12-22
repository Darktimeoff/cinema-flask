from .service import UserMovieService
from app.classes.dao import Dao
from app.setup.db import db
from app.movies.container import movie_service
from app.user.container import user_service

dao = Dao(db)
user_movie_service = UserMovieService(user_service, movie_service, dao)