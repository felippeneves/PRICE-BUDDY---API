from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort
from src.controllers.product_unique import ProductUniqueController
from flask import request


class ProductUnique(Resource):
    @jwt_required
    def get(self):
        product_unique = ProductUniqueController()

        try:
            result = product_unique.listar(request.args.get('productID'), request.args.get('establishmentID'))


            if not result:
                abort(404, message="Nenhum registro encontrado na base de dados")

            return result
        except:
            abort(404, message="Falha na chamada da API")









