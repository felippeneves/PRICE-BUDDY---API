from src.models.establishment import EstablishmentSchema
from src.config import config_connection
import os
import base64

class EstablishmentController:

    def listar(self, latitude, longitude):
        connection = config_connection()
        cursor = connection.cursor()
        rows = cursor.execute(
            "	select TB_ESTABLISHMENT.ESTABLISHMENT_ID as id,				   																					" +
            "		   TB_ESTABLISHMENT.ESTABLISHMENT_CNPJ as cnpj,                                                                                             " +
            "		   TB_ESTABLISHMENT.ESTABLISHMENT_NAME as name,                                                                                             " +
            "		   TB_ESTABLISHMENT.ESTABLISHMENT_DESCRIPTION as description,                                                                               " +
            "		   TB_ESTABLISHMENT.ESTABLISHMENT_PHONE as phone,                                                                                           " +
            "		   TB_ADDRESS.ADDRESS_ADDRESS_NAME as addres,                                                                                               " +
            "		   TB_ADDRESS.ADDRESS_NUMBER as number,                                                                                                     " +
            "		   TB_ADDRESS.ADDRESS_COMPLEMENT complement,                                                                                                " +
            "		   TB_ADDRESS.ADDRESS_NEIGHBORHOOD as neighborhood,                                                                                         " +
            "		   TB_ADDRESS.ADDRESS_CITY as city,                                                                                                         " +
            "		   TB_ADDRESS.ADDRESS_STATE as state,                                                                                                       " +
            "		   TB_ADDRESS.ADDRESS_COUNTRY as country,                                                                                                   " +
            "		   TB_ADDRESS.ADDRESS_LATITUDE as latitude,                                                                                                 " +
            "		   TB_ADDRESS.ADDRESS_LONGITUDE as longitude,                                                                                               " +
            "		   round(geography::Point(?, ?, 4326).STDistance(geography::Point(TB_ADDRESS.ADDRESS_LATITUDE, TB_ADDRESS.ADDRESS_LONGITUDE, 4326)),        " +
            "		   0)                                                                                                                                       " +
            "	       as distance                                                                                                                              " +
            "	from TB_ESTABLISHMENT                                                                                                                           " +
            "	join TB_ADDRESS                                                                                                                                 " +
            "	on TB_ADDRESS.ADDRESS_ID = TB_ESTABLISHMENT.ADDRESS_ID                                                                                          " +
            "	order by distance                                                                                                                               "
        , latitude, longitude).fetchall()
        pathPhotos = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'photos', 'establishments', 'small'))

        listEstablishments = list()

        for row in rows:
            image = os.path.join(pathPhotos, row.id + '.png')
            try:
                with open(image, "rb") as imageFile:
                    imgStr = base64.b64encode(imageFile.read())
            except:
                imgStr = None
            listEstablishments.append(dict(
                                id = row.id,
                                cnpj = row.cnpj,
                                name = row.name,
                                description = row.description,
                                phone = row.phone,
                                addres = row.addres,
                                number = row.number,
                                complement = row.complement,
                                neighborhood = row.neighborhood,
                                city = row.city,
                                state = row.state,
                                country = row.country,
                                latitude = row.latitude,
                                longitude = row.longitude,
                                distance = row.distance,
                                photo = imgStr
                            ))

        schema = EstablishmentSchema(many=True)
        result = schema.dump(listEstablishments)
        connection.close()

        return result


    def getOperatingHours(self):
        s = 'teste'

    # Se precisar testar
    # pathPhotos = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'photos', 'establishments'))
    #
    # image = os.path.join(pathPhotos, 'c23f337a-4b7c-450c-9dc8-23af1ec70f0b.png')
    #
    # img = Image.open(image)
    # if img.verify():
    #     img = img.rotate(180)
    #     img.save(image)
    # img = Image.open(image)
    # byteImage = img.tobytes(encoder_name='raw')

    # imgString = str(byteImage, 'utf-8')