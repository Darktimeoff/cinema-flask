import app.models
from app.config import config
from app.setup.db import db
from main import configure_app, create_app

if __name__ == '__main__':
    app = create_app(config)
    api = configure_app(app)

    with app.app_context():
        db.create_all()
