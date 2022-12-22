from flask_restx import Api

from .auth.api import auth_ns
from .directors.api import director_ns
from .genres.api import genre_ns
from .movies.api import movie_ns
from .user.api import user_ns
from .user_movie.api import user_movie_ns


def register_urls(api: Api):
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(user_movie_ns)
    api.add_namespace(auth_ns)
