from app.exceptions.http import NotFoundError
from app.exceptions.service import ValidationError
from app.utils.security import compare_hashfunc, str_to_hashfunc

from .const import (INVALID_BODY, INVALID_ID_TYPE, INVALID_KEYS_FOR_UPDATE,
                    USER_NOT_FOUND, INVALIDA_DATA_FOR_CHANGE_PASSWORD, PASSWORD_DOESNOT_MATCH)
from app.container import user_schema
from .dao import UserDAO


class UserService:
    dao: UserDAO

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_by_email(self, email: str):
        return self.dao.get_by_email(email)

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
            raise ValidationError(list(errors.items())[0][1][0], status_code=2)

        data['password'] = self.generate_password(data['password'])
    
        return self.dao.create(data)

    def update(self, id: int, data: dict):
        if type(id) is not int:
            raise ValidationError(message=INVALID_ID_TYPE, status_code=1)

        if type(data) is not dict:
            raise ValidationError(message=INVALID_BODY, status_code=2)
        
        if 'favourite_genre' in data:
            data['favorite_genre_id'] = data['favourite_genre']
            del data['favourite_genre']

        keys = set(user_schema.declared_fields.keys())
        data_keys = set(data.keys())

        if not data_keys.issubset(keys):
            raise ValidationError(
                message=INVALID_KEYS_FOR_UPDATE, status_code=3)

        user = self.dao.get_by_id(id)

        if not user:
            raise NotFoundError(message=USER_NOT_FOUND, status_code=4)

        if 'password' in data:
            data['password'] = self.generate_password(data['password'])
        print('___update___',data)
        user = self.dao.update(id, data)

        return user

    def delete(self, id: int):
        if type(id) is not int:
            raise ValidationError(message=INVALID_ID_TYPE, status_code=1)

        user = self.dao.get_by_id(id)

        if not user:
            raise NotFoundError(message=USER_NOT_FOUND, status_code=2)

        self.dao.delete(id)

        return True

    def change_password(self, id: int, data: dict):
        if type(id) is not int:
            raise ValidationError(message=INVALID_ID_TYPE, status_code=1)
        
        if type(data) is not dict:
            raise ValidationError(message=INVALID_BODY, status_code=2)

        if set(data.keys()) != {'old_password', 'new_password'}:
            raise ValidationError(
                message=INVALIDA_DATA_FOR_CHANGE_PASSWORD, status_code=3)

        user = self.dao.get_by_id(id)

        if not user:
            raise NotFoundError(message=USER_NOT_FOUND, status_code=4)

        if not self.compare_password(user.password, data['old_password']):
            raise ValidationError(message=PASSWORD_DOESNOT_MATCH, status_code=5)

        new_password = {
            "password": self.generate_password(data['new_password'])
        }

        user = self.dao.update(id, new_password)

        return user
        


    def generate_password(self, password: str) -> str:
        return str_to_hashfunc(password)

    def compare_password(self, password_user: str, password: str) -> bool:
        return compare_hashfunc(password_user, password)
