from marshmallow import Schema, fields


class ProductEstablishmentSchema(Schema):
    productID = fields.String()
    productCode = fields.String()
    productName = fields.String()
    productPrice = fields.Float()
    productDescription = fields.String()
    productWeight = fields.String()
    establishmentID = fields.String()
    establishmentName = fields.String()
    establishmentPhone = fields.String()
    addressID = fields.String()
    addressName = fields.String()
    addressNumber = fields.String()
    addressComplement = fields.String()
    addressNeighborhood = fields.String()
    addressCity = fields.String()
    addressState = fields.String()
    addressCountry = fields.String()
    distance = fields.String()
