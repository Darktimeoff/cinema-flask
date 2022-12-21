import pytest
from app.movies.service import MovieService
from app.movies.dao import MovieDao
from app.exceptions.http import BadRequestError, NotFoundError
from app.movies.const import MOVIE_NOT_FOUND, UNCORECT_ID_TYPE

class TestMovieService:
    movie_service: MovieService

    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao: MovieDao):
        self.movie_service = MovieService(dao=movie_dao)


    def test_get_all_return_value(self, movie_list):
        self.movie_service.dao.get_query.return_value = movie_list
        result = self.movie_service.get_all()

        assert type(result) is list, 'expected list returned type'
        assert result == movie_list, 'expected same list'

    def test_get_all_ordered(self, sorted_by_year):
        self.movie_service.dao.order_by_year.return_value = sorted_by_year

        result = self.movie_service.get_all('new')

        assert type(result) is list, 'expected list returned type'
        assert result == sorted_by_year, 'expected same list'

    def test_get_all_first_uncorrect_args(self, movie_list):
        self.movie_service.dao.get_query.return_value = movie_list

        result = self.movie_service.get_all(123)

        assert type(result) is list, 'expected list returned type'
        assert result == movie_list, 'expected same list'

    def test_get_by_id_return_value(self, movie_list):
        movie = movie_list[0]
        self.movie_service.dao.get_by_id.return_value = movie

        result = self.movie_service.get_by_id(1)

        assert type(result) is dict, 'expected dict returned type'
        assert result == movie, 'expected same value'

    def test_get_id_uncorrect_type(self):
        with pytest.raises(BadRequestError) as e:
            self.movie_service.get_by_id('123')

        assert e.value.status_code == 1, 'expected status code 1'
        assert str(e.value) == UNCORECT_ID_TYPE, 'expected same string'

    def test_get_by_id_not_found(self):
        self.movie_service.dao.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError) as e:
            self.movie_service.get_by_id(10)

        assert e.value.status_code == 2, 'expected status code 2'
        assert str(e.value) == MOVIE_NOT_FOUND, 'expected same string'

    def test_get_id_without_args(self):
        with pytest.raises(TypeError):
            self.movie_service.get_by_id()