from app.schemas import UserSchema
from .dao import UserDAO
from .service import UserService
from app.setup.db import db
from app.models import User

user_schema = UserSchema()
user_schemas = UserSchema(many=True)

user_dao = UserDAO(User, db)
user_service = UserService(user_dao)