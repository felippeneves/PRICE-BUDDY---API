from marshmallow import Schema, fields


class EstablishmentSchema(Schema):
    id = fields.String()
    cnpj = fields.String()
    name = fields.String()
    price = fields.Float()
    description = fields.String()
    phone = fields.String()
    addres = fields.String()
    number = fields.String()
    complement = fields.String()
    neighborhood = fields.String()
    city = fields.String()
    state = fields.String()
    country = fields.String()
    latitude = fields.String()
    longitude = fields.String()
    distance = fields.String()
    photo = fields.String()