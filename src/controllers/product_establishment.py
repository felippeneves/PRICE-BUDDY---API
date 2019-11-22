from src.models.product_establishment import ProductEstablishmentSchema
from src.config import config_connection
from flask import abort


class ProductEstablishmentController:

    def listar(self, establishmentID, productCode, latitude, longitude):
        connection = config_connection()
        cursor = connection.cursor()

        query = "	select p.PRODUCT_ID productID,																										   " \
        "		   p.PRODUCT_CODE productCode,                                                                                                             " \
        "		   p.PRODUCT_NAME productName,                                                                                                             " \
        "		   round(p.PRODUCT_PRICE, 2) productPrice,                                                                                                 " \
        "		   p.PRODUCT_DESCRIPTION productDescription,                                                                                               " \
        "		   p.PRODUCT_WEIGHT productWeight,                                                                                                         " \
        "		   e.ESTABLISHMENT_ID establishmentID,                                                                                                     " \
        "		   e.ESTABLISHMENT_NAME establishmentName,                                                                                                 " \
        "		   e.ESTABLISHMENT_PHONE establishmentPhone,                                                                                               " \
        "		   a.ADDRESS_ID addressID,                                                                                                                 " \
        "		   a.ADDRESS_ADDRESS_NAME addressName,                                                                                                     " \
        "		   a.ADDRESS_NUMBER addressNumber,                                                                                                         " \
        "		   a.ADDRESS_COMPLEMENT addressComplement,                                                                                                 " \
        "		   a.ADDRESS_NEIGHBORHOOD addressNeighborhood,                                                                                             " \
        "		   a.ADDRESS_CITY addressCity,                                                                                                             " \
        "		   a.ADDRESS_STATE addressState,                                                                                                           " \
        "		   a.ADDRESS_COUNTRY addressCountry,                                                                                                       " \
        "		    round(geography::Point(?, ?, 4326).STDistance(geography::Point(a.ADDRESS_LATITUDE, a.ADDRESS_LONGITUDE, 4326)),   					   " \
        "		   0)                                                                                                                                      " \
        "	       as distance                                                                                                                             " \
        "	from TB_PRODUCT_ESTABLISHMENT pe                                                                                                               " \
        "	join TB_ESTABLISHMENT e                                                                                                                        " \
        "	on e.ESTABLISHMENT_ID = pe.ESTABLISHMENT_ID                                                                                                    " \
        "	join TB_ADDRESS a                                                                                                                              " \
        "	on a.ADDRESS_ID = e.ADDRESS_ID                                                                                                                 " \
        "	join TB_PRODUCT p                                                                                                                              " \
        "	on p.PRODUCT_ID = pe.PRODUCT_ID                                                                                                                "

        if establishmentID:
            query += "	where pe.ESTABLISHMENT_ID = ?                                                                            									   "
        elif productCode:
            query += "	and p.PRODUCT_CODE = ?                                                                            									           "
        else:
            abort(400, 'Falha na chamada da API')

        query += " order by productName         "

        rows = cursor.execute(query, latitude, longitude, establishmentID if establishmentID else productCode).fetchall()
        schema = ProductEstablishmentSchema(many=True)
        result = schema.dump(rows)
        connection.close()

        return result