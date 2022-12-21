from flask import jsonify, request
from flask_restx import Namespace, Resource

from .container import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/login/')
class Login(Resource):
    def post(self):
        body = request.get_json()

        response = auth_service.login(
            body.get('email', None), body.get('password', None))

        return jsonify(response)

    def put(self):
        body = request.get_json()

        response = auth_service.approve_refresh_token(
            body.get('refresh_token', None))

        return jsonify(response)


@auth_ns.route('/register/')
class Register(Resource):
    def post(self):
        body = request.get_json()

        response = auth_service.register(
            body.get('email', None), body.get('password', None))

        return response
