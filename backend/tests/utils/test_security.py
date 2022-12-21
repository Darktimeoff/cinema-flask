import pytest
from app.utils.main import get_env
from app.utils.security import compare_hashfunc, str_to_hashfunc, get_access_token, decode_jwt, get_refresh_token, generate_jwt
import datetime
import calendar
import time
from jwt import ExpiredSignatureError, DecodeError

class TestStrToHashFunc:
    def test_str_to_hashfunc(self):
        value  = str_to_hashfunc('test')
        assert type(value) is str, 'expected str value'
        assert len(value) > 20, 'expected more than 20 symbols' 

    def test_str_to_hashfunc_empty(self):
        with pytest.raises(TypeError):
            str_to_hashfunc()

    def test_str_to_hashfunc_invalid(self):
        with pytest.raises(TypeError):
            str_to_hashfunc(123)
    
class TestCompareHashFunc:
    def test_correct_return_value(self):
        password = 'test'
        hash_func  = str_to_hashfunc(password)
        result  = compare_hashfunc(hash_func, password)

        assert result is True, 'expected True result'

    def test_with_not_equel_value(self):
        password = 'test'
        hash_func  = str_to_hashfunc(password)
        result = compare_hashfunc(hash_func, password + '1')
        assert result is False, 'expected False result'
    
    def test_empty(self):
        with pytest.raises(TypeError):
            compare_hashfunc()

    def test_not_correct_first_args(self):
        result = compare_hashfunc('test', 'test')
        assert result is False, 'expected False result, first must be hash function'
    
    def test_second_arg_must_be_string(self):
        with pytest.raises(TypeError):
            compare_hashfunc('123', 123)

    def test_first_arg_must_be_string(self):
        with pytest.raises(AttributeError):
            compare_hashfunc(12, '123')
        
@pytest.fixture()
def jwt_payload():
    return {
        "id": 1,
        "username": "test",
    }

class TestGenerateJwt:
    def test_correct_return_value(self, jwt_payload):
        delta = datetime.timedelta(seconds=1)
        result = generate_jwt(jwt_payload, delta)

        assert type(result) is str, 'result must be a string'
        assert len(result) > 20, 'result must not be empty'
        assert result.count('.') == 2, 'token must have 3 header, payload, and signature'
    
    def test_time_expiration(self, jwt_payload):
        seconds = 60
        delta = datetime.timedelta(seconds=seconds)

        result = generate_jwt(jwt_payload, delta)
        data = decode_jwt(result)

        timedelta = datetime.datetime.utcnow() + delta
        exp = calendar.timegm(timedelta.timetuple())

        assert 'exp' in data, 'token must have an expiration'
        assert data['exp'] == exp, f'expiration time must {seconds} seconds'
    
    def test_expiration(self, jwt_payload):
        mseconds = 100
        delta = datetime.timedelta(milliseconds=mseconds)

        result = generate_jwt(jwt_payload, delta)

        time.sleep(mseconds / 1000)

        with pytest.raises(ExpiredSignatureError):
            decode_jwt(result)

class TestGetAcessToken:
    def test_correct_return_value(self, jwt_payload):
        result = get_access_token(jwt_payload)

        assert type(result) is str, 'result must be a string'
        assert len(result) > 20, 'result must not be empty'
        assert result.count('.') == 2, 'token must have 3 header, payload, and signature'

    def test_time_expiration(self, jwt_payload):
        result = get_access_token(jwt_payload)
        data = decode_jwt(result)

        minutes = int(get_env('TOKEN_EXPIRE_MINUTES'))

        delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
        exp = calendar.timegm(delta.timetuple())

        assert 'exp' in data, 'token must have an expiration'
        assert data['exp'] == exp, f'expiration time must be less than {minutes} minutes'

    def test_with_uncorrect_payload(self):
        with pytest.raises(TypeError):
            get_access_token(123)
    
    def test_with_empty_first_arg(self):
        with pytest.raises(TypeError):
            get_access_token()

class TestGetRefreshToken:
    def test_correct_return_value(self, jwt_payload):
        result = get_refresh_token(jwt_payload)

        assert type(result) is str, 'result must be a string'
        assert len(result) > 20, 'result must not be empty'
        assert result.count('.') == 2, 'token must have 3 header, payload, and signature'

    def test_time_expiration(self, jwt_payload):
        result = get_refresh_token(jwt_payload)
        data = decode_jwt(result)

        days = int(get_env('TOKEN_EXPIRE_DAYS'))

        delta = datetime.datetime.utcnow() + datetime.timedelta(days=days)
        exp = calendar.timegm(delta.timetuple())


        assert 'exp' in data, 'token must have an expiration'
        assert data['exp'] == exp, f'expiration time must be {days} days'

    def test_with_uncorrect_payload(self):
        with pytest.raises(TypeError):
            get_refresh_token(123)
    
    def test_with_empty_first_arg(self):
        with pytest.raises(TypeError):
            get_refresh_token()

class TestDecodeJWT:
    def test_with_payload(self, jwt_payload):
        token = get_access_token(jwt_payload)
        data = decode_jwt(token)
        keys = set(data.keys())
        keys.add('exp')

        data_keys = set(data.keys())

        assert data_keys == keys, 'must have the same keys'
    
    def test_decode_error(self):
        with pytest.raises(DecodeError):
            decode_jwt('sadasd')

    def test_uncorrect_arg_type(self):
        with pytest.raises(DecodeError):
            decode_jwt(123)

    def test_with_empty_first_arg(self):
        with pytest.raises(TypeError):
            decode_jwt()

            