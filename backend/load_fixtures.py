from app.setup.db import db
from contextlib import suppress
from app.setup.db.models import Base
from typing import Type
from main import create_app, configure_app
from app.config import config
from app.models import Genre, Director, Movie
from sqlalchemy.exc import IntegrityError
from app.utils.main import read_json

def load_data(data, model: Type[Base]) -> None:
    for item in data:
        item['id'] = item.pop('pk')
        db.session.add(model(**item))

if __name__ == '__main__':
    fixtures = read_json("fixtures.json")
    app = create_app(config)
    api = configure_app(app)

    with app.app_context():
        load_data(fixtures['genres'], Genre)
        load_data(fixtures['directors'], Director)
        load_data(fixtures['movies'], Movie)

        with suppress(IntegrityError):
            db.session.commit()