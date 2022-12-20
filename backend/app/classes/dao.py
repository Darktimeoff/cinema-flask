from typing import TypeVar, Generic
import logging

T = TypeVar('T')

class Dao(Generic[T]):
    __query: T | None = None
    __db = None

    def __init__(self, db):
        self.__db = db

    @property
    def db(self):
        return self.__db
    
    @property
    def db_session(self):
        return self.db.session

    @property
    def query(self):
        return self.set_query()

    def start_session(self):
        self.db_session.close()
        self.db_session.begin()

    def add_to_db(self, data):
        self.start_session()

        try:
            self.db_session.add(data)
        except Exception as e:
            self.db_session.rollback()
            logging.exception(f'Rollback add data transaction {data}')
            raise
        else:
            self.db_session.commit()
    
    def delete_from_db(self, data):
        self.start_session()

        try:
            self.db_session.delete(data)
        except Exception as e:
            self.db_session.rollback()
            logging.exception(f'Rollback delete transaction {data}')
            raise
        else:
            self.db_session.commit()
    
    def update_data_in_db(self, data):
        self.start_session()

        try:
            self.db_session.add(data)
        except Exception as e:
            self.db_session.rollback()
            logging.exception(f'Rollback update_data_in_db transaction')
            raise
        else:
            self.db_session.commit()
    
    def clear_query(self):
        self.__query = None