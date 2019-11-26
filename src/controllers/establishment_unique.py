from src.models.establishment_unique import EstablishmentUniqueSchema
from src.config import config_connection
import os
import base64
import pyodbc
from flask import abort


class EstablishmentUniqueController:

    def listar(self, establishmentID):
        statusCode = 200
        connection = config_connection()
        result = None

        try:
            cursor = connection.cursor()

            row = cursor.execute(
            "	select  e.ESTABLISHMENT_ID id,								 " +
            "			e.ESTABLISHMENT_NAME name,                           " +
            "			e.ESTABLISHMENT_DESCRIPTION description,             " +
            "			e.ESTABLISHMENT_PHONE phone,                         " +
            "			e.ESTABLISHMENT_OPERATING_HOURS operatingHours,      " +
            "			a.ADDRESS_ADDRESS_NAME address,                      " +
            "			a.ADDRESS_NUMBER number,                             " +
            "			a.ADDRESS_COMPLEMENT complement,                     " +
            "			a.ADDRESS_NEIGHBORHOOD neighborhood,                 " +
            "			a.ADDRESS_CITY city,                                 " +
            "			a.ADDRESS_STATE state,                               " +
            "			a.ADDRESS_COUNTRY country                            " +
            "	from TB_ESTABLISHMENT e                                      " +
            "	join TB_ADDRESS a                                            " +
            "	on a.ADDRESS_ID = e.ADDRESS_ID                               " +
            "	where e.ESTABLISHMENT_ID = ?                                 ",
            establishmentID).fetchone()

            pathPhotos = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'photos', 'establishments', 'big'))

            if row and len(row) > 0:
                schema = EstablishmentUniqueSchema()

                image = os.path.join(pathPhotos, row.id + '.png')
                try:
                    with open(image, "rb") as imageFile:
                        imgStr = base64.b64encode(imageFile.read())
                except:
                    imgStr = None

                result = schema.dump(
                    dict(
                        id=row.id,
                        name=row.name,
                        description=row.description,
                        phone=row.phone,
                        operatingHours=row.operatingHours,
                        address=row.address,
                        number=row.number,
                        complement=row.complement,
                        neighborhood=row.neighborhood,
                        city=row.city,
                        state=row.state,
                        country = row.country,
                        photo=imgStr
                    )
                )
            else:
                statusCode = 404

        except pyodbc.DatabaseError as err:
            print(err)
            statusCode = 400
        finally:
            connection.close()


        if statusCode != 200:
            if statusCode == 404:
                abort(404, 'Estabelecimento Não encontrado')
            else:
                abort(400, 'Falha ao buscar o Estabelecimento')
        else:
            return result