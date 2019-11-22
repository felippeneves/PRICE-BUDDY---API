from flask import Blueprint
from flask_restful import Api
from resources.phone import Phone
from resources.user import User


admin = Blueprint('api', __name__)

api = Api(admin)
api.add_resource(Phone, '/phone')
api.add_resource(User, '/user')


# @admin.route("/admin")
# def index():
#     return "Essa e a pagina de admin"
#
@admin.route("/api/user")
def phones():
    return api.resources(User)
#
# @admin.route("/admin/user")
# def users():
#     return "teste2"
