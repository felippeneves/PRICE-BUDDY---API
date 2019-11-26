from marshmallow import Schema, fields

class EstablishmentUniqueSchema(Schema):
    id = fields.String()
    name = fields.String()
    description = fields.String()
    phone = fields.String()
    operatingHours = fields.String()
    address = fields.String()
    number = fields.String()
    complement = fields.String()
    neighborhood = fields.String()
    city = fields.String()
    state = fields.String()
    country = fields.String()
    photo = fields.String()