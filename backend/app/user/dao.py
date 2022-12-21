from app.classes.dao import Dao
from app.models import User


class UserDAO(Dao):
    __model: User

    def __init__(self, model: User, db):
        super().__init__(db)
        self.__model = model

    def set_query(self):
        self.__query = self.__model.query

        return self.__query

    def get_by_id(self, id: int) -> User | None:
        return self.query.get(id)

    def get_by_email(self, email: str) -> User | None:
        return self.query.filter(User.email == email).first()

    def create(self, data: dict) -> User:
        user = User(**data)

        self.add_to_db(user)

        return user

    def delete(self, id: int) -> User | None:
        user = self.get_by_id(id)

        if user is None:
            return None

        self.delete_from_db(user)

        return user

    def update(self, id: int, data: dict) -> User | None:
        user = self.get_by_id(id)

        if user is None:
            return None

        for key, value in data.items():
            setattr(user, key, value)

        self.update_data_in_db(user)

        return user
