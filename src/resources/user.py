from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort
# from controllers.user import UserController
from src.controllers.user import UserController



class User(Resource):
    @jwt_required
    def get(self):
        users = UserController()

        result = users.listar()

        if not result:
            abort(404, message="Nenhum registro encontrado na base de dados")

        return result

    def post(self):
        user = UserController()

        result = user.inserir(request.get_json(force=True))

        if not result:
            abort(400, 'Falha ao cadastrar usuário')

        return result







