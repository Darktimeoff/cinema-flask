from flask_restx import Resource, Namespace
from flask import request
from app.decorators.api import auth_required, serialized
from .container import user_service
from app.container import user_schema

user_ns = Namespace("user", description="user related operations")

@user_ns.route("/")
class User(Resource):
    @auth_required
    @serialized(user_schema)
    def get(self, user):
        return user

    @auth_required
    @serialized(user_schema)
    def patch(self, user):
        data = request.get_json()

        updated_user = user_service.update(user.id, data)

        return updated_user

    
@user_ns.route("/password/")
class UserPassword(Resource):
    @auth_required
    def post(self, user):
        data = request.get_json()

        user = user_service.change_password(user.id, data)

        return {"message": "success", "status": 0}, 200