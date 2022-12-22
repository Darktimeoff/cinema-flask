import pytest
from app.user.service import UserService
from app.models import User
from app.exceptions.service import ValidationError
from app.exceptions.http import NotFoundError

from app.user.const import INVALID_ID_TYPE, PASSWORD_DOESNOT_MATCH, USER_NOT_FOUND, INVALID_BODY,INVALIDA_DATA_FOR_CHANGE_PASSWORD, INVALID_KEYS_FOR_UPDATE

class TestUserService:
    user_service: UserService

    @pytest.fixture(autouse=True)
    def user_service(self, user_dao):
        self.user_service = UserService(user_dao)

    def test_get_user_by_email(self):
        user = self.user_service.get_by_email("test@test.com")

        assert type(user) is User, 'incorrect type returned'
    
    def test_get_user_by_email_not_found(self):
        user = self.user_service.dao.get_by_email.return_value = None
        
        assert user is None, 'incorrect type returned'
    
    def test_get_user_by_email_not_pass_args(self):
        with pytest.raises(TypeError):
            self.user_service.get_by_email()

    def test_get_user_by_email_uncorrect_args(self):
        self.user_service.dao.get_by_email.return_value = None

        user = self.user_service.get_by_email(123)

        assert user is None, 'incorrect type returned'

    def test_get_by_id(self):
        user = self.user_service.get_by_id(1)

        assert type(user) is User, 'incorrect type returned'

    def test_get_by_id_not_pass_args(self):
        with pytest.raises(TypeError):
            self.user_service.get_by_id()
    
    def test_get_by_id_uncorrect_type_id(self):
        with pytest.raises(ValidationError) as e:
            self.user_service.get_by_id('123123')
        
        assert str(e.value) == INVALID_ID_TYPE
        assert e.value.status_code == 1

    def test_get_by_id_not_found(self):
        self.user_service.dao.get_by_id.return_value = None
        
        with pytest.raises(NotFoundError) as e:
            self.user_service.get_by_id(1)

        assert str(e.value) == USER_NOT_FOUND
        assert e.value.status_code == 2

    def test_create(self):
        data = {
            "email": "test@test.com",
            "password": "test"
        }

        orig = data.copy()

        user = self.user_service.create(data)

        assert type(user) is User, 'incorrect type returned'
        assert user.email == orig['email'], 'incorrect email returned'
        assert user.password != orig['password'], 'return orig password, must be hash function'

    def test_create_data_type_error(self):
        with pytest.raises(ValidationError) as e:
            self.user_service.create(123)
        
        assert str(e.value) == INVALID_BODY
        assert e.value.status_code == 1

    def test_create_data_invalid(self):
        data = {
            "email": "testtest.com",
            "password": "test"
        }

        with pytest.raises(ValidationError) as e:
            self.user_service.create(data)
        
        assert e.value.status_code == 2
    
    def test_create_data_not_all_required_pass(self):
        data = {
            "email": "test@test.com",
        }

        with pytest.raises(ValidationError) as e:
            self.user_service.create(data)
        
        assert e.value.status_code == 2

    def test_update(self):
        data = {
            "name": "test",
            "password": "test"
        }

        orig = data.copy()

        user = self.user_service.update(1, data)

        assert type(user) is User, 'incorrect type returned'
        assert user.name == orig['name'], 'incorrect name returned'
        assert user.password != orig['password'], 'return orig password, must be hash function'

    def test_update_not_pass_passwords(self):
        data = {
            "name": "test",
        }


        user = self.user_service.update(1, data)

        assert 'password' not in data, 'doesn`t contain password'
    
    def test_update_id_type_error(self):
        with pytest.raises(ValidationError) as e:
            self.user_service.update('12', {})

        assert str(e.value) == INVALID_ID_TYPE
        assert e.value.status_code == 1

    def test_update_data_type_error(self):
        with pytest.raises(ValidationError) as e:
            self.user_service.update(1, '123')

        assert str(e.value) == INVALID_BODY
        assert e.value.status_code == 2
    
    def test_update_invalid_keys(self):
        data = {
            "email": "test@test.com",
            "test": "test"
        }

        with pytest.raises(ValidationError) as e:
            self.user_service.update(1, data)
        
        assert str(e.value) == INVALID_KEYS_FOR_UPDATE
        assert e.value.status_code == 3

    def test_update_not_found(self):
        data = {
            "name": "test",
            "password": "test"
        }

        self.user_service.dao.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as e:
            self.user_service.update(1, data)

        assert str(e.value) == USER_NOT_FOUND
        assert e.value.status_code == 4

    def test_delete(self):
        result = self.user_service.delete(1)

        assert result is True, 'incorrect type returned'

    def test_delete_id_type_uncorrect(self):
        with pytest.raises(ValidationError) as e:
            self.user_service.delete('12')

        assert str(e.value) == INVALID_ID_TYPE
        assert e.value.status_code == 1 

    def test_delete_not_found(self):
        self.user_service.dao.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as e:
            self.user_service.delete(1)

        assert str(e.value) == USER_NOT_FOUND
        assert e.value.status_code == 2

    def test_generate_password(self):
        value = self.user_service.generate_password('test')

        assert type(value) is str, 'expected str value'
        assert len(value) > 20, 'expected more than 20 symbols' 

    def test_compare_password(self):
        password = self.user_service.generate_password('test')
        result = self.user_service.compare_password(password, 'test')

        assert result is True, 'must be same'

    def test_compare_password_diff(self):
        password = self.user_service.generate_password('test1')
        result = self.user_service.compare_password(password, 'test')

        assert result is False, 'must be diff'

    def test_change_password(self):
        old_password = 'test'
        new_password = 'test1'

        result = self.user_service.change_password(1, {
            'old_password': old_password,
            'new_password': new_password
        })

        check_new_password = self.user_service.compare_password(result.password, new_password)
        
        assert check_new_password is True
        assert type(result) is User, 'result must be User'

    def test_change_password_id_typeerror(self):
        with pytest.raises(ValidationError) as e:
            self.user_service.change_password('1', {})
        assert str(e.value) == INVALID_ID_TYPE
        assert e.value.status_code == 1
    
    def test_change_password_body_typeerror(self):
        with pytest.raises(ValidationError) as e:
            self.user_service.change_password(1, '1')
        assert str(e.value) == INVALID_BODY
        assert e.value.status_code == 2

    def test_change_password_payload_invalid(self):
        with pytest.raises(ValidationError) as e:
            self.user_service.change_password(1, {'password_old': 123, 'password_new': 123})
        assert str(e.value) == INVALIDA_DATA_FOR_CHANGE_PASSWORD
        assert e.value.status_code == 3

    def test_change_password_payload_invalid(self):

        self.user_service.dao.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as e:
            self.user_service.change_password(1, {'old_password': 123, 'new_password': 123})
        assert str(e.value) == USER_NOT_FOUND
        assert e.value.status_code == 4

    def test_change_password_not_compare(self):
        old_password = 'test1'
        new_password = 'test2'
        
        with pytest.raises(ValidationError) as e:
            self.user_service.change_password(1, {
                'old_password': old_password,
                'new_password': new_password
            })
        assert str(e.value) == PASSWORD_DOESNOT_MATCH
        assert e.value.status_code == 5