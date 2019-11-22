from marshmallow import Schema, fields
from passlib.hash import pbkdf2_sha256 as sha256


class AnswerSchema(Schema):
    id = fields.String()
    email = fields.String()
    name = fields.String()
    lastName = fields.String()
    phone = fields.String()
    accessToken = fields.String()



class LoginEnt:
    def __init__(self, user_id=None, user_email=None, user_name=None, user_last_name=None, user_password=None, user_phone=None):
        self.user_id = user_id,
        self.user_email = user_email,
        self.user_name = user_name,
        self.user_last_name = user_last_name,
        self.user_password = user_password,
        self.user_phone = user_phone

class LoginModel():
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)