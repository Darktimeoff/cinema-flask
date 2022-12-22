import pytest
from app.user.service import UserService
from app.auth.service import AuthService
from app.exceptions.http import NotFoundError, BadRequestError
from app.exceptions.service import ValidationError, UniqueError
from app.auth.const import UNCORECT_TYPE_EMAIL_PASSWORD, USER_PASSWORD_WRONG, USER_EXISTS, USER_WRONG_REFRESH_TOKEN, INVALID_TOKEN_TYPE, UNCORECT_TYPE_REFRESH_TOKEN
from unittest.mock import Mock
from app.utils.security import get_refresh_token, get_access_token

class TestAuthService:
    auth_service: AuthService

    @pytest.fixture(autouse=True)
    def auth_service(self, user_service):
        self.auth_service = AuthService(user_service)

    def test_login(self, user):
        self.auth_service.user_service.get_by_email.return_value = user
        self.auth_service.user_service.compare_password.return_value = True

        data = self.auth_service.login('test@gmail.com', 'test')
        access_token = data['access_token']
        refresh_token = data['refresh_token']

        assert type(access_token) is str, 'must be string'
        assert type(refresh_token) is str,'must be string'
        assert access_token.count('.') == 2,'token must be have header, payload, signature'
        assert refresh_token.count('.') == 2,'token must be have header, payload, signature'

    def test_login_email_invalid_type(self):
        with pytest.raises(ValidationError) as e:
            self.auth_service.login(1, 'asd')
        
        assert str(e.value) == UNCORECT_TYPE_EMAIL_PASSWORD
        assert e.value.status_code == 1
    
    def test_login_not_found(self):
        self.auth_service.user_service.get_by_email.return_value = None

        with pytest.raises(NotFoundError) as e:
            self.auth_service.login('test@gmail.com', 'test')
        
        assert str(e.value) == UNCORECT_TYPE_EMAIL_PASSWORD
        assert e.value.status_code == 2

    def test_login_password_invalid_type(self, user):
        self.auth_service.user_service.get_by_email.return_value = user

        with pytest.raises(ValidationError) as e:
            self.auth_service.login('test@gmail.com', 123)
        
        assert str(e.value) == UNCORECT_TYPE_EMAIL_PASSWORD
        assert e.value.status_code == 3

    def test_login_password_not_compare(self, user):
        self.auth_service.user_service.get_by_email.return_value = user
        self.auth_service.user_service.compare_password.return_value = False

        with pytest.raises(BadRequestError) as e:
            self.auth_service.login('test@gmail.com', '123')
        
        assert str(e.value) == USER_PASSWORD_WRONG
        assert e.value.status_code == 4
        
    def test_register(self, user):
        self.auth_service.user_service.get_by_email.return_value = None
        self.auth_service.user_service.create.return_value = user
        self.auth_service.user_service.compare_password.return_value = True
        self.auth_service.login = Mock(return_value={
            "access_token": 'asd.asdsa.asd',
            "refresh_token": 'asd.asdsa.asd'
        })

        data = self.auth_service.register('test@gmail.com', 'test')

        access_token = data['access_token']
        refresh_token = data['refresh_token']

        assert type(access_token) is str, 'must be string'
        assert type(refresh_token) is str,'must be string'
        assert access_token.count('.') == 2,'token must be have header, payload, signature'
        assert refresh_token.count('.') == 2,'token must be have header, payload, signature'

    def test_register_email_invalid_type(self):
        with pytest.raises(ValidationError) as e:
            self.auth_service.register(1, 'asd')

        assert str(e.value) == UNCORECT_TYPE_EMAIL_PASSWORD
        assert e.value.status_code == 1

    def test_register_password_invalid_type(self):
        with pytest.raises(ValidationError) as e:
            self.auth_service.register(1, 'asd')

        assert str(e.value) == UNCORECT_TYPE_EMAIL_PASSWORD
        assert e.value.status_code == 1

    def test_register_unique(self, user):
        self.auth_service.user_service.get_by_email.return_value = user
        
        with pytest.raises(UniqueError) as e:
            self.auth_service.register('test@gmail.com', 'test')
        
        assert str(e.value) == USER_EXISTS
        assert e.value.status_code == 2

    def test_approve_refresh_token(self, user):
        self.auth_service.user_service.get_by_email.return_value = user
        data = self.auth_service.approve_refresh_token(user.refresh_token)

        access_token = data['access_token']
        refresh_token = data['refresh_token']

        assert type(access_token) is str, 'must be string'
        assert type(refresh_token) is str,'must be string'
        assert access_token.count('.') == 2,'token must be have header, payload, signature'
        assert refresh_token.count('.') == 2,'token must be have header, payload, signature'

    def test_approve_refresh_token_invalid_type(self):
        with pytest.raises(ValidationError) as e:
            self.auth_service.approve_refresh_token(123)

        assert str(e.value) == UNCORECT_TYPE_REFRESH_TOKEN
        assert e.value.status_code == 1
    
    def test_approve_refresh_token_uncorrect(self):
        with pytest.raises(BadRequestError) as e:
            self.auth_service.approve_refresh_token('assadsad')

        assert str(e.value) == INVALID_TOKEN_TYPE
        assert e.value.status_code == 2

    def test_approve_refresh_diff_user_refresh_token(self, user):
        self.auth_service.user_service.get_by_email.return_value = user
        
        with pytest.raises(BadRequestError) as e:
            self.auth_service.approve_refresh_token(get_refresh_token({"email": "123213"}))

        assert str(e.value) == USER_WRONG_REFRESH_TOKEN
        assert e.value.status_code == 5

    def test_user_refresh_token(self, user):
        def update(id, data):
            for k, v in data.items():
                setattr(user, k, v)

            return user

        self.auth_service.user_service.update = update

        tokens = {
            "refresh_token": get_refresh_token({"email": user.email}),
            "access_token": get_access_token({"email": user.email})
        }

        prev_refresh = user.refresh_token

        new_user = self.auth_service.update_user_refresh_token(user, tokens)

        assert new_user.refresh_token != prev_refresh, 'users update refersh token'
        assert new_user.refresh_token == tokens['refresh_token'], 'user must have new token'

    def test_generate_tokens(self, user):
        self.auth_service.user_service.get_by_email.return_value = user
        self.auth_service.user_service.compare_password.return_value = True

        data = self.auth_service.generate_tokens('test@gmail.com', 'test', None)
        access_token = data['access_token']
        refresh_token = data['refresh_token']

        assert type(access_token) is str, 'must be string'
        assert type(refresh_token) is str,'must be string'
        assert access_token.count('.') == 2,'token must be have header, payload, signature'
        assert refresh_token.count('.') == 2,'token must be have header, payload, signature'
        

