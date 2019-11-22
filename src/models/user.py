from marshmallow import Schema, fields
from passlib.hash import pbkdf2_sha256 as sha256


class UserSchema(Schema):
    USER_ID = fields.String()
    USER_EMAIL = fields.String()
    USER_NAME = fields.String()
    USER_LAST_NAME = fields.String()
    USER_PASSWORD = fields.String()
    USER_PHONE = fields.String()


class RespostaSchema(Schema):
    statusCode = fields.String()
    registrosInseridos = fields.String()
    dataPost = fields.String()


class UserEnt:
    def __init__(self, user_id=None, user_email=None, user_name=None, user_last_name=None, user_password=None, user_phone=None):
        self.user_id = user_id,
        self.user_email = user_email,
        self.user_name = user_name,
        self.user_last_name = user_last_name,
        self.user_password = user_password,
        self.user_phone = user_phone

class UserModel():
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)