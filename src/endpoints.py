from flask import Blueprint
from flask_restful import Api
from src.resources.user import User
from src.resources.login import Login
from src.resources.establishment import Establishment
from src.resources.product import Product
from src.resources.product_establishment import ProductEstablishment
from src.resources.product_unique import ProductUnique


api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

api.add_resource(User, '/user')
api.add_resource(Login, '/login')
api.add_resource(Establishment, '/establishment')
api.add_resource(Product, '/product')
api.add_resource(ProductEstablishment, '/product_establishment')
api.add_resource(ProductUnique, '/product_unique')