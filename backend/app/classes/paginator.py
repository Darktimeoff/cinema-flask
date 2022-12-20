from math import ceil

class Paginator:
    __query = None
    __by_page = None

    def __init__(self, query, by_page=None):
        self.__by_page = by_page
        self.__query = query

    @property
    def count(self):
        return self.__query.count()

    @property
    def num_pages(self):
        return ceil(self.count / self.__by_page) if self.count else 0

    @property
    def num_items(self):
        return self.count
    
    def page(self,page: int):
        offset = (page - 1) * self.__by_page

        return self.__query.offset(offset).limit(self.__by_page)