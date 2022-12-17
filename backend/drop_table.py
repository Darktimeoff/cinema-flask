

from app.config import config
from main import create_app, configure_app
import app.models

from app.setup.db import db

if __name__ == '__main__':
    app = create_app(config)
    api = configure_app(app)
    
    with app.app_context():
        db.drop_all()