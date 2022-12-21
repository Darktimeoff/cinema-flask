import pytest
from unittest.mock import Mock
from app.directors.dao import DirectorDao

@pytest.fixture()
def director_dao():
    director_dao = DirectorDao(None, None)

    director_dao.get_query = Mock()
    director_dao.get_all = Mock()
    director_dao.get_by_id = Mock()


    return director_dao

@pytest.fixture()
def director_list():
    return [
        {"id": 1, "name": 'Test'}, {"id": 2, "name": 'Test2'},
    ]