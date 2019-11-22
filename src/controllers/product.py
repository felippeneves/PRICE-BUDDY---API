from src.models.product import ProductSchema
from src.config import config_connection
import os
import base64
import pyodbc
from flask import abort

class ProductController:

    def listar(self, productInfo, establishmentID, latitude, longitude):
        statusCode = 200
        connection = config_connection()
        result = None

        try:
            cursor = connection.cursor()

            if establishmentID:

                rows = cursor.execute(

                    "	select p.PRODUCT_ID id,																				                 	" +
                    "		p.PRODUCT_CODE code,                                                                                                " +
                    "		p.PRODUCT_NAME name,                                                                                                " +
                    "		round(pe.PRODUCT_PRICE, 2) price,                                                                                   " +
                    "		p.PRODUCT_DESCRIPTION description,                                                                                  " +
                    "		p.PRODUCT_WEIGHT weight,                                                                                            " +
                    "		e.ESTABLISHMENT_ID establishmentID,                                                                                 " +
                    "		e.ESTABLISHMENT_NAME establishmentName,                                                                             " +
                    "		round(geography::Point(?, ?, 4326)                                                    					            " +
                    "		.STDistance(geography::Point(a.ADDRESS_LATITUDE, a.ADDRESS_LONGITUDE, 4326)), 0) as establishmentDistance           " +
                    "	from TB_PRODUCT  p                                                                                                      " +
                    "	join TB_PRODUCT_ESTABLISHMENT pe                                                                                        " +
                    "	on pe.PRODUCT_ID = p.PRODUCT_ID                                                                                         " +
                    "	and pe.ESTABLISHMENT_ID = ?	                                                                                            " +
                    "	join TB_ESTABLISHMENT e                                                                                                 " +
                    "	on e.ESTABLISHMENT_ID = pe.ESTABLISHMENT_ID                                                                             " +
                    "	join TB_ADDRESS a                                                                                                       " +
                    "	on a.ADDRESS_ID = e.ADDRESS_ID                                                                                          " +
                    "	order by establishmentDistance																							"
                    , latitude, longitude, establishmentID).fetchall()
            else:
                productInfoLike = '%' + productInfo + '%'


                rows = cursor.execute(
                    "	select p.PRODUCT_ID id,																				                    " +
                    "		p.PRODUCT_CODE code,                                                                                                " +
                    "		p.PRODUCT_NAME name,                                                                                                " +
                    "		round(pe.PRODUCT_PRICE, 2) price,                                                                                   " +
                    "		p.PRODUCT_DESCRIPTION description,                                                                                  " +
                    "		p.PRODUCT_WEIGHT weight,                                                                                            " +
                    "		e.ESTABLISHMENT_ID establishmentID,                                                                                 " +
                    "		e.ESTABLISHMENT_NAME establishmentName,                                                                             " +
                    "		round(geography::Point(?, ?, 4326)                                                    					            " +
                    "		.STDistance(geography::Point(a.ADDRESS_LATITUDE, a.ADDRESS_LONGITUDE, 4326)), 0) as establishmentDistance           " +
                    "	from TB_PRODUCT  p                                                                                                      " +
                    "	join TB_PRODUCT_ESTABLISHMENT pe                                                                                        " +
                    "	on pe.PRODUCT_ID = p.PRODUCT_ID                                                                                         " +
                    "	join TB_ESTABLISHMENT e                                                                                                 " +
                    "	on e.ESTABLISHMENT_ID = pe.ESTABLISHMENT_ID                                                                             " +
                    "	join TB_ADDRESS a                                                                                                       " +
                    "	on a.ADDRESS_ID = e.ADDRESS_ID                                                                                          " +
                    "	where upper(p.PRODUCT_NAME) like upper(?)                                                                               " +
                    "	order by establishmentDistance																							"
                    , latitude, longitude, productInfoLike).fetchall()

                if (rows is None) or (rows and len(rows) == 0):
                    rows = cursor.execute(
                        "	select p.PRODUCT_ID id,																				                    " +
                        "		p.PRODUCT_CODE code,                                                                                                " +
                        "		p.PRODUCT_NAME name,                                                                                                " +
                        "		round(pe.PRODUCT_PRICE, 2) price,                                                                                   " +
                        "		p.PRODUCT_DESCRIPTION description,                                                                                  " +
                        "		p.PRODUCT_WEIGHT weight,                                                                                            " +
                        "		e.ESTABLISHMENT_ID establishmentID,                                                                                 " +
                        "		e.ESTABLISHMENT_NAME establishmentName,                                                                             " +
                        "		round(geography::Point(?, ?, 4326)                                                    					            " +
                        "		.STDistance(geography::Point(a.ADDRESS_LATITUDE, a.ADDRESS_LONGITUDE, 4326)), 0) as establishmentDistance           " +
                        "	from TB_PRODUCT  p                                                                                                      " +
                        "	join TB_PRODUCT_ESTABLISHMENT pe                                                                                        " +
                        "	on pe.PRODUCT_ID = p.PRODUCT_ID                                                                                         " +
                        "	join TB_ESTABLISHMENT e                                                                                                 " +
                        "	on e.ESTABLISHMENT_ID = pe.ESTABLISHMENT_ID                                                                             " +
                        "	join TB_ADDRESS a                                                                                                       " +
                        "	on a.ADDRESS_ID = e.ADDRESS_ID                                                                                          " +
                        "	where p.PRODUCT_CODE = ?                                                                                                " +
                        "	order by establishmentDistance																				            "
                        , latitude, longitude, productInfo).fetchall()



            if rows and len(rows) > 0:

                pathPhotos = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'photos', 'products', 'small'))
                listProducts = list()

                for row in rows:
                    image = os.path.join(pathPhotos, row.id + '.png')
                    try:
                        with open(image, "rb") as imageFile:
                            imgStr = base64.b64encode(imageFile.read())
                    except:
                        imgStr = None

                    listProducts.append(dict(
                        id=row.id,
                        code=row.code,
                        name=row.name,
                        price=row.price,
                        description=row.description,
                        weight=row.weight,
                        establishmentID=row.establishmentID,
                        establishmentName=row.establishmentName,
                        establishmentDistance=row.establishmentDistance,
                        photo=imgStr
                    ))

                    schema = ProductSchema(many=True)
                    result = schema.dump(listProducts)
            else:
                statusCode = 404
        except pyodbc.DatabaseError as err:
            print(err)
            statusCode = 400
        finally:
            connection.close()

        if statusCode != 200:
            if statusCode == 404:
                abort(404, 'Nenhum produto encontrado')
            else:
                abort(400, 'Falha ao buscar os Produtos')
        else:
            return result