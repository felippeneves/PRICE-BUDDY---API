from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort
from src.controllers.establishment import EstablishmentController
from flask import request




class Establishment(Resource):
    @jwt_required
    def get(self):
        establishments = EstablishmentController()

        try:
            result = establishments.listar(request.args.get('latitude'), request.args.get('longitude'))

            if not result:
                abort(404, message="Nenhum registro encontrado na base de dados")

            return result
        except:
            abort(404, message="Falha na chamada da API")









