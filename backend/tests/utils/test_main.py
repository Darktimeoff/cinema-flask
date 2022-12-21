import pytest
from app.utils.main import get_env

class TestGetEnv:
    def test_get_env(self):
        value =  get_env("ENV")
        assert value == 'development', 'value should be development'

    def test_get_env_exception(self):
        with pytest.raises(KeyError):
            get_env('ENV1')
