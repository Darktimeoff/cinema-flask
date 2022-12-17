from pathlib import Path
from typing import Type

from .utils.main import get_env

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    JSON_AS_ASCII = False

    ITEMS_PER_PAGE = 12

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRE_MINUTES = int(get_env('TOKEN_EXPIRE_MINUTES'))
    TOKEN_EXPIRE_DAYS = int(get_env('TOKEN_EXPIRE_DAYS'))

    PWD_HASH_SALT = get_env('SALT')
    PWD_HASH_ITERATIONS = 100_000
    PWD_SECRET = get_env('JWT_SECRET')
    PWD_ALG = get_env('JWT_ALG')

    RESTX_JSON = {
        'ensure_ascii': False,
    }


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        BASE_DIR.joinpath('cinema.db').as_posix()


class ProductionConfig(BaseConfig):
    DEBUG = False


class ConfigFactory:
    flask_env = get_env('ENV')

    @classmethod
    def get_config(cls) -> Type[BaseConfig]:
        if cls.flask_env == 'development':
            return DevelopmentConfig
        elif cls.flask_env == 'production':
            return ProductionConfig
        elif cls.flask_env == 'testing':
            return TestingConfig
        raise NotImplementedError


config = ConfigFactory.get_config()
