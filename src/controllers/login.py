import uuid
from src.models.login import AnswerSchema, LoginModel
from src.config import config_connection
import pyodbc
from flask import abort
from flask_jwt_extended import (
    create_access_token,
)
from datetime import datetime, timedelta

class LoginController:

    def login(self, data):

        statusCode = 200
        connection = config_connection()
        userExists = False
        result = None

        try:
            connection.autocommit = False
            cursor = connection.cursor()

            dataLogin = data[0]

            row = cursor.execute("select * from TB_USER where USER_EMAIL = ?",str(dataLogin.get("USER_EMAIL"))).fetchone()
            if row and len(row) > 0:
                userExists = True


            if userExists:
                if LoginModel.verify_hash(str(dataLogin.get("USER_PASSWORD")), row.USER_PASSWORD):
                    expires = timedelta(days=120)
                    schema = AnswerSchema()
                    object = schema.dump(
                        dict(
                            id = row.USER_ID,
                            email = row.USER_EMAIL,
                            name = row.USER_NAME,
                            lastName = row.USER_LAST_NAME,
                            phone = row.USER_PHONE
                        )
                    )
                    access_token = create_access_token(identity = object, expires_delta=expires)
                    result = schema.dump(
                        dict(
                            id = row.USER_ID,
                            email = row.USER_EMAIL,
                            name = row.USER_NAME,
                            lastName = row.USER_LAST_NAME,
                            phone = row.USER_PHONE,
                            accessToken = access_token
                        )
                    )
                else:
                    statusCode = 404
            else:
                statusCode = 404
        except pyodbc.DatabaseError as err:
            print(err)
            connection.rollback()
            statusCode = 400
        else:
            connection.commit()
        finally:
            connection.autocommit = True
            connection.close()


        if statusCode != 200:
            if statusCode == 404:
                if userExists:
                    abort(404, 'Senha inválida')
                else:
                    abort(404, 'Usuário não encontrado')
            else:
                abort(400, 'Falha ao realizar o login')
        else:
            return result

