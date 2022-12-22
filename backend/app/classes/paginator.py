from math import ceil

class Paginator:
    query = None
    by_page = None

    def __init__(self, query, by_page=None):
        self.by_page = by_page
        self.query = query

    @property
    def count(self):
        return self.query.count()

    @property
    def num_pages(self):
        return ceil(self.count / self.by_page) if self.count else 0
    
    def page(self,page: int):
        offset = (page - 1) * self.by_page

        return self.query.offset(offset).limit(self.by_page)