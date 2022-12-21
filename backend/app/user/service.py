from app.exceptions.http import NotFoundError
from app.exceptions.service import ValidationError
from app.utils.security import compare_hashfunc, str_to_hashfunc

from .const import (INVALID_BODY, INVALID_ID_TYPE, INVALID_KEYS_FOR_UPDATE,
                    USER_NOT_FOUND)
from .container import user_schema
from .dao import UserDAO


class UserService:
    dao: UserDAO

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_by_id(self, id: int):
        if type(id) is not int:
            raise ValidationError(message=INVALID_ID_TYPE, status_code=1)

        user = self.dao.get_by_id(id)

        if not user:
            raise NotFoundError(message=USER_NOT_FOUND, status_code=2)

        return user

    def create(self, data: dict):
        if type(data) is not dict:
            raise ValidationError(message=INVALID_BODY, status_code=1)

        errors = user_schema.validate(data)

        if errors:
            raise ValidationError(errors[0], status_code=2)

        data['password'] = self.generate_password(data['password'])

        return self.dao.create(data)

    def update(self, id: int, data: dict):
        if type(id) is not int:
            raise ValidationError(message=INVALID_ID_TYPE, status_code=1)

        if type(data) is not dict:
            raise ValidationError(message=INVALID_BODY, status_code=2)

        keys = set(user_schema.fields.keys())
        data_keys = set(data.keys())

        if not data_keys.issubset(keys):
            raise ValidationError(
                message=INVALID_KEYS_FOR_UPDATE, status_code=3)

        user = self.dao.get_by_id(id)

        if not user:
            raise NotFoundError(message=USER_NOT_FOUND, status_code=4)

        if 'password' in data:
            data['password'] = self.generate_password(data['password'])

        user = self.dao.update(id, data)

        return user

    def delete(self, id: int):
        if type(id) is not int:
            raise ValidationError(message=INVALID_ID_TYPE, status_code=1)

        user = self.dao.get_by_id(id)

        if not user:
            raise NotFoundError(message=USER_NOT_FOUND, status_code=4)

        self.dao.delete(id)

        return True

    def generate_password(self, password: str) -> str:
        return str_to_hashfunc(password)

    def compare_password(self, password_user: str, password: str) -> bool:
        return compare_hashfunc(password_user, password_user)
