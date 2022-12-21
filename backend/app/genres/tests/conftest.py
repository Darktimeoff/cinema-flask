import pytest
from unittest.mock import Mock
from app.genres.dao import GenreDAO

@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None, None)

    genre_dao.get_query = Mock()
    genre_dao.get_all = Mock()
    genre_dao.get_by_id = Mock()


    return genre_dao

@pytest.fixture()
def genre_list():
    return [
        {"id": 1, "name": 'Test'}, {"id": 2, "name": 'Test2'},
    ]