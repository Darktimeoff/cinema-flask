import pytest
from app.directors.dao import DirectorDao
from app.directors.service import DirectorService
from app.directors.const import (UNCORECT_ID_TYPE, DIRECTOR_NOT_FOUND)
from app.exceptions.http import BadRequestError, NotFoundError

class TestGenreService:
    director_service: DirectorService
    
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao: DirectorDao):
        self.director_service = DirectorService(director_dao)

    parametres_return_value = (
        ([{"id": 1, "name": 'Test'}]),
        (None),
        ([])
    )
    @pytest.mark.parametrize("directors", parametres_return_value)
    def test_get_all_return_value(self, directors):
        self.director_service.dao.get_query.return_value = directors
        result = self.director_service.get_all()

        assert result == directors, 'expected same data'

    def test_get_by_id_return_value(self, director_list):
        director = director_list[0]
        self.director_service.dao.get_by_id.return_value = director

        result = self.director_service.get_by_id(1)

        assert type(result) is dict, 'expected dict returned type'
        assert result == director, 'expected same value'

    def test_get_id_uncorrect_type(self):
        with pytest.raises(BadRequestError) as e:
            self.director_service.get_by_id('123')

        assert e.value.status_code == 1, 'expected status code 1'
        assert str(e.value) == UNCORECT_ID_TYPE, 'expected same string'

    def test_get_by_id_not_found(self):
        self.director_service.dao.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError) as e:
            self.director_service.get_by_id(10)

        assert e.value.status_code == 2, 'expected status code 2'
        assert str(e.value) == DIRECTOR_NOT_FOUND, 'expected same string'

    def test_get_id_without_args(self):
        with pytest.raises(TypeError):
            self.director_service.get_by_id()