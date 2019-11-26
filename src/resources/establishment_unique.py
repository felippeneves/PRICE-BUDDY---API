from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort
from src.controllers.establishment_unique import EstablishmentUniqueController
from flask import request


class EstablishmentUnique(Resource):
    @jwt_required
    def get(self):
        establishment_unique = EstablishmentUniqueController()

        try:
            result = establishment_unique.listar(request.args.get('establishmentID'))


            if not result:
                abort(404, message="Nenhum registro encontrado na base de dados")

            return result
        except:
            abort(404, message="Falha na chamada da API")









