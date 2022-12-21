from app.exceptions.http import BadRequestError, NotFoundError
from app.exceptions.service import UniqueError, ValidationError
from app.models import User
from app.user.container import user_schema
from app.user.service import UserService
from app.utils.security import decode_jwt, get_access_token, get_refresh_token

from .const import (UNCORECT_TYPE_EMAIL_PASSWORD, UNCORECT_TYPE_REFRESH_TOKEN,
                    USER_EXISTS, USER_NOT_FOUND, USER_PASSWORD_WRONG,
                    USER_WRONG_REFRESH_TOKEN)


class AuthService:
    user_service: UserService

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email: str, password: str, refresh_token: str) -> dict:
        if type(email) is not str or type(password) is not str:
            raise ValidationError(
                message=UNCORECT_TYPE_EMAIL_PASSWORD, status_code=1)

        user = self.user_service.get_by_email(email)

        if not user:
            raise NotFoundError(message=USER_NOT_FOUND, status_code=2)

        if not self.user_service.compare_password(user.password, password):
            raise BadRequestError(
                message=USER_PASSWORD_WRONG, status_code=3)

        if refresh_token and not (user.refresh_token != refresh_token):
            raise BadRequestError(
                message=USER_WRONG_REFRESH_TOKEN, status_code=4)

        data = user_schema.dump(user)

        access_token = get_access_token(data)
        refresh_token = get_refresh_token(data)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def update_user_refresh_token(self, user, tokens) -> User:
        data = {
            'refresh_token': tokens['refresh_token']
        }

        user = self.user_service.update(user.id, data)

        return user

    def register(self, email: str, password: str) -> dict:
        user = self.user_service.get_by_email(email)

        if user:
            raise UniqueError(message=USER_EXISTS, status_code=1)

        data = {
            'email': email,
            'password': password,
        }

        user = self.user_service.create(data)

        tokens = self.login(email, password)

        return tokens

    def login(self, email: str, password: str, refresh_token: str = None) -> dict:
        tokens = self.generate_tokens(email, password)

        user = self.update_user_refresh_token(user, tokens, refresh_token)

        return tokens

    def approve_refresh_token(self, refresh_token: str):
        if type(refresh_token) is not str:
            raise ValidationError(
                message=UNCORECT_TYPE_REFRESH_TOKEN, status_code=1)

        data = decode_jwt(refresh_token)

        user = self.user_service.get_by_email(data['email'])

        if not user:
            raise NotFoundError(message=USER_NOT_FOUND, status_code=2)

        tokens = self.login(user.email, user.password, user.refresh_token)

        return tokens
