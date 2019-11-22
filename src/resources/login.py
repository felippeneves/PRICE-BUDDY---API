from flask import request
from flask_restful import Resource, abort
# from controllers.user import UserController
from src.controllers.login import LoginController


class Login(Resource):

    def post(self):
        login = LoginController()

        result = login.login(request.get_json(force=True))

        if not result:
            abort(400, 'Falha ao realizar o login')

        return result







