from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.String()
    code = fields.String()
    name = fields.String()
    price = fields.Float()
    description = fields.String()
    weight = fields.String()
    establishmentID = fields.String()
    establishmentName = fields.String()
    establishmentDistance = fields.String()
    photo = fields.String()