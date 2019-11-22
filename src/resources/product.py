from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort
from src.controllers.product import ProductController
from flask import request




class Product(Resource):
    @jwt_required
    def get(self):
        product = ProductController()

        try:
            result = product.listar(request.args.get('productInfo'), request.args.get('establishmentID'), request.args.get('latitude'), request.args.get('longitude'))

            if not result:
                abort(404, message="Nenhum registro encontrado na base de dados")

            return result
        except NameError:
            abort(404, message="Falha na chamada da API")









