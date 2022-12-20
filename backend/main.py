from logging import basicConfig

from app.config import config
from app.exceptions.http import BasicHTTPError
from app.setup.api import api
from app.setup.db import db
from app.urls import register_urls
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

load_dotenv(override=True)
basicConfig(filename='basic.log')


def base_service_error_handler(exception: BasicHTTPError):
    return jsonify({'message': str(exception), "status": exception.status_code}), exception.code


def create_app(config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)
    app.app_context().push()

    return app


def configure_app(app: Flask):
    db.init_app(app)
    api.init_app(app)
    CORS(app)
    Migrate(app, db, render_as_batch=True)

    app.register_error_handler(BasicHTTPError, base_service_error_handler)

    return api


app = create_app(config)
api = configure_app(app)
register_urls(api)

if __name__ == '__main__':
    app.run()
