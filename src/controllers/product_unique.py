from src.models.product_unique import ProductUniqueSchema
from src.config import config_connection
import os
import base64
import pyodbc
from flask import abort


class ProductUniqueController:

    def listar(self, productID, establishmentID):
        statusCode = 200
        connection = config_connection()
        result = None

        try:
            cursor = connection.cursor()

            row = cursor.execute(
            # "	select  p.PRODUCT_ID id,											" +
            # "			p.PRODUCT_CODE code,                                        " +
            # "			p.PRODUCT_NAME name,                                        " +
            # "			p.PRODUCT_DESCRIPTION description,                          " +
            # "			p.PRODUCT_WEIGHT weight,                                    " +
            # "			e.ESTABLISHMENT_ID establishmentID,                         " +
            # "			e.ESTABLISHMENT_NAME establishmentName,                     " +
            # "			e.ESTABLISHMENT_PHONE establishmentPhone,                   " +
            # "			a.ADDRESS_ADDRESS_NAME establishmentAddress,                " +
            # "			a.ADDRESS_NUMBER establishmentNumber,                       " +
            # "			a.ADDRESS_COMPLEMENT establishmentComplement,               " +
            # "			a.ADDRESS_NEIGHBORHOOD establishmentNeighborhood,           " +
            # "			a.ADDRESS_CITY establishmentCity,                           " +
            # "			a.ADDRESS_STATE establishmentState,                         " +
            # "			a.ADDRESS_COUNTRY establishmentCountry,                     " +
            # "			a.ADDRESS_LATITUDE establishmentLatitude,                   " +
            # "			a.ADDRESS_LONGITUDE establishmentLongitude                  " +
            # "	from TB_PRODUCT p, TB_ESTABLISHMENT e                               " +
            # "	join TB_ADDRESS a                                                   " +
            # "	on a.ADDRESS_ID = e.ADDRESS_ID                                      " +
            # "	where p.PRODUCT_ID = ?                                              " +
            # "	and e.ESTABLISHMENT_ID = ?                                          ",
            "	select  p.PRODUCT_ID id,											" +
            "			p.PRODUCT_CODE code,                                        " +
            "			p.PRODUCT_NAME name,                                        " +
            "		    round(pe.PRODUCT_PRICE, 2) price,                           " +
            "			p.PRODUCT_DESCRIPTION description,                          " +
            "			p.PRODUCT_WEIGHT weight,                                    " +
            "			e.ESTABLISHMENT_ID establishmentID,                         " +
            "			e.ESTABLISHMENT_NAME establishmentName,                     " +
            "			e.ESTABLISHMENT_PHONE establishmentPhone,                   " +
            "			a.ADDRESS_ADDRESS_NAME establishmentAddress,                " +
            "			a.ADDRESS_NUMBER establishmentNumber,                       " +
            "			a.ADDRESS_COMPLEMENT establishmentComplement,               " +
            "			a.ADDRESS_NEIGHBORHOOD establishmentNeighborhood,           " +
            "			a.ADDRESS_CITY establishmentCity,                           " +
            "			a.ADDRESS_STATE establishmentState,                         " +
            "			a.ADDRESS_COUNTRY establishmentCountry,                     " +
            "			a.ADDRESS_LATITUDE establishmentLatitude,                   " +
            "			a.ADDRESS_LONGITUDE establishmentLongitude                  " +
            "	from TB_PRODUCT_ESTABLISHMENT pe                                    " +
            "	join TB_PRODUCT p                                                   " +
            "	on p.PRODUCT_ID = pe.PRODUCT_ID                                     " +
            "	join TB_ESTABLISHMENT e                                             " +
            "	on e.ESTABLISHMENT_ID = pe.ESTABLISHMENT_ID                         " +
            "	join TB_ADDRESS a                                                   " +
            "	on a.ADDRESS_ID = e.ADDRESS_ID                                      " +
            "	where pe.PRODUCT_ID = ?                                             " +
            "	and pe.ESTABLISHMENT_ID = ?                                         ",
            productID, establishmentID).fetchone()

            pathPhotos = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'photos', 'products', 'big'))

            if row and len(row) > 0:
                schema = ProductUniqueSchema()

                # rows = cursor.execute(
                #     "	select  d.DAYWEEK_NAME,					" +
                #     "			d.DAYWEEK_SHORT_NAME,           " +
                #     "			o.OPERATION_START_DATE,         " +
                #     "			o.OPERATION_FINAL_DATE          " +
                #     "	from TB_OPERATION o                     " +
                #     "	join TB_DAY_WEEK d                      " +
                #     "	on d.DAYWEEK_ID = o.DAYWEEK_ID          " +
                #     "	where o.ESTABLISHMENT_ID = ?            ",
                #     establishmentID).fetchall()
                #
                # days = ''
                # establishmentFlgOpen = ''
                #
                # for row in rows:
                #

                image = os.path.join(pathPhotos, row.id + '.png')
                try:
                    with open(image, "rb") as imageFile:
                        imgStr = base64.b64encode(imageFile.read())
                except:
                    imgStr = None

                result = schema.dump(
                    dict(
                        id = row.id,
                        code = row.code,
                        name = row.name,
                        price = row.price,
                        description = row.description,
                        weight = row.weight,
                        establishmentID = row.establishmentID,
                        establishmentName = row.establishmentName,
                        establishmentPhone = row.establishmentPhone,
                        establishmentAddress = row.establishmentAddress,
                        establishmentNumber = row.establishmentNumber,
                        establishmentComplement = row.establishmentComplement,
                        establishmentNeighborhood = row.establishmentNeighborhood,
                        establishmentCity = row.establishmentCity,
                        establishmentState = row.establishmentState,
                        establishmentCountry = row.establishmentCountry,
                        establishmentLatitude = row.establishmentLatitude,
                        establishmentLongitude = row.establishmentLongitude,
                        # establishmentOperatingHours = fields.String(),
                        # establishmentFlgOpen = fields.String(),
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
                abort(404, 'Produto Não encontrado')
            else:
                abort(400, 'Falha ao buscar o Produto')
        else:
            return result