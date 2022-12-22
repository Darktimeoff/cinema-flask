import pytest
from unittest.mock import Mock

@pytest.fixture()
def query_mock():
    class Query:
        offset = 0
        limit = 0
        data = []

        def __init__(self, data = []):
            self.data = data

        def count(self):
            return self
        def offset(self, value = 0):
            self.offset = value
            return self
        def limit(self, value = 0):
            self.limit = value
            return self.data[self.offset:self.offset + self.limit]
    
    query = Query()
    query.count = Mock()

    return query