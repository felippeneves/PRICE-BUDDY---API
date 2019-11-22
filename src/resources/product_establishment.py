from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort
from src.controllers.product_establishment import ProductEstablishmentController
from flask import request




class ProductEstablishment(Resource):
    @jwt_required
    def get(self):
        productEstablishment = ProductEstablishmentController()

        try:
            result = productEstablishment.listar(request.args.get('establishmentID'), request.args.get('productCode'), request.args.get('latitude'), request.args.get('longitude'))

            if not result:
                abort(404, message="Nenhum registro encontrado na base de dados")

            return result
        except:
            abort(404, message="Falha na chamada da API")









