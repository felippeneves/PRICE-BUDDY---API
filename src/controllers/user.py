import uuid
# from models.user import UserSchema, RespostaSchema, UserEnt
from src.models.user import UserSchema, RespostaSchema, UserModel

# from config import config_connection
from src.config import config_connection

import pyodbc
from datetime import datetime
from flask import abort


class UserController:

    # def listar(self):
    #     connection = config_connection()
    #     cursor = connection.cursor()
    #     rows = cursor.execute("select * from TB_USER").fetchall()
    #     schema = UserSchema(many=True)
    #     result = schema.dump(rows)
    #     connection.close()
    #
    #     return result

    def inserir(self, data):

        count = 0
        statusCode = 200
        connection = config_connection()

        try:
            connection.autocommit = False
            cursor = connection.cursor()
            countRegister = 0

            for dado in data:
                row = cursor.execute("select count(1) as user_count from TB_USER where USER_EMAIL = ?", str(dado.get("USER_EMAIL"))).fetchone()
                countRegister += row.user_count

            if countRegister > 0:
                statusCode = 409
            else:
                for dado in data:
                    password = UserModel.generate_hash(str(dado.get("USER_PASSWORD")))
                    count += cursor.execute(
                        'insert into TB_USER(USER_ID, USER_EMAIL, USER_NAME, USER_LAST_NAME, USER_PASSWORD, USER_PHONE) values(?, ?, ?, ?, ?, ?);',
                        (str(uuid.uuid4()).upper(), str(dado.get("USER_EMAIL")), str(dado.get("USER_NAME")),
                         str(dado.get("USER_LAST_NAME")), password, str(dado.get("USER_PHONE")))
                    ).rowcount
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
            if statusCode == 409:
                abort(409, 'Usuário já cadastrado')
            else:
                abort(400, 'Não foi possível adicionar o usuário')
        else:
            schema = RespostaSchema()
            result = schema.dump(
                dict
                    (
                    statusCode=statusCode,
                    registrosInseridos=count,
                    dataPost=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                )
            )

            return result

