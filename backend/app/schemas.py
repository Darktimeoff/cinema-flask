from marshmallow import Schema, fields

class MovieSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    trailer = fields.Url(required=True)
    year = fields.Integer(required=True)
    rating = fields.Integer(required=True)
    
