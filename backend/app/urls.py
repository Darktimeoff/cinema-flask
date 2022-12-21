from flask_restx import Api
from .movies.api import movie_ns
from .directors.api import director_ns

def register_urls(api: Api):
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
