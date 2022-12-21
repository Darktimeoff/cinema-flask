import pytest
from unittest.mock import Mock
from app.movies.dao import MovieDao
from app.models import Movie

@pytest.fixture()
def movie_dao():
    movie_dao = MovieDao(None, None)

    movie_dao.order_by_year = Mock()
    movie_dao.get_query = Mock()
    movie_dao.get_all = Mock()
    movie_dao.get_by_id = Mock()


    return movie_dao

@pytest.fixture()
def movie_list():
    return [
        {"id": 1, "year": 10}, {"id": 2, "year": 11},
    ]

@pytest.fixture()
def sorted_by_year():
    return [
        {"id": 2, "year": 11},{"id": 1, "year": 10}
    ]