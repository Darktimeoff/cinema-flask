import pytest 
from app.classes.paginator import Paginator

data = [1,2,3,4,5,6,7,8,9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
by_page = 2

class TestPaginator:
    paginator: Paginator

    @pytest.fixture(autouse=True)
    def paginator(self, query_mock):
        query_mock.data = data

        self.paginator = Paginator(query_mock, by_page)

    parameters_count = (
        (6),
        (5),
        (1),
        (0)
    )
    @pytest.mark.parametrize("count",parameters_count)
    def test_count(self, count):
        self.paginator.query.count.return_value = count

        assert self.paginator.count == count, "count mismatch"

    parameters = (
        (6, 3),
        (5, 3),

        (1, 1),
        (0, 0)
    )
    @pytest.mark.parametrize("count, pages",parameters)
    def test_num_pages(self, count, pages):
        self.paginator.query.count.return_value = count

        assert self.paginator.num_pages == pages, f'expected num_pages to be {pages}'

    parameters_list = (
        (1, data[0:by_page]),
        (2, data[by_page:2*by_page]),
        (10, data[len(data) - by_page:]),
    )

    @pytest.mark.parametrize("page, pagination_list",parameters_list)
    def test_num_pages(self, page, pagination_list):
        assert self.paginator.page(page) == pagination_list, f'expected same list'

    def test_num_pages_args_error(self):
        with pytest.raises(TypeError):
            self.paginator.page()
    
    def test_num_pages_args_failed_type(self):
        with pytest.raises(TypeError):
            self.paginator.page('a')
    