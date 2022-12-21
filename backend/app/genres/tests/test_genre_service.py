import pytest
from app.genres.dao import GenreDAO
from app.genres.service import GenreService
from app.genres.const import (UNCORECT_ID_TYPE, GENRE_NOT_FOUND)
from app.exceptions.http import BadRequestError, NotFoundError

class TestGenreService:
    genre_service: GenreService
    
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao: GenreDAO):
        self.genre_service = GenreService(genre_dao)

    parametres_return_value = (
        ([{"id": 1, "username": 'john'}]),
        (None),
        ([])
    )
    @pytest.mark.parametrize("genres", parametres_return_value)
    def test_get_all_return_value(self, genres):
        self.genre_service.dao.get_query.return_value = genres
        result = self.genre_service.get_all()

        assert result == genres, 'expected same data'

    def test_get_by_id_return_value(self, genre_list):
        genre = genre_list[0]
        self.genre_service.dao.get_by_id.return_value = genre

        result = self.genre_service.get_by_id(1)

        assert type(result) is dict, 'expected dict returned type'
        assert result == genre, 'expected same value'

    def test_get_id_uncorrect_type(self):
        with pytest.raises(BadRequestError) as e:
            self.genre_service.get_by_id('123')

        assert e.value.status_code == 1, 'expected status code 1'
        assert str(e.value) == UNCORECT_ID_TYPE, 'expected same string'

    def test_get_by_id_not_found(self):
        self.genre_service.dao.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError) as e:
            self.genre_service.get_by_id(10)

        assert e.value.status_code == 2, 'expected status code 2'
        assert str(e.value) == GENRE_NOT_FOUND, 'expected same string'

    def test_get_id_without_args(self):
        with pytest.raises(TypeError):
            self.genre_service.get_by_id()