from marshmallow import Schema, fields

class BaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class DirectorSchema(BaseSchema):
    name = fields.String(required=True)

class GenreSchema(BaseSchema):
    name = fields.String(required=True)

class MovieSchema(BaseSchema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    trailer = fields.Url(required=True)
    year = fields.Integer(required=True)
    rating = fields.Integer(required=True)

    genre = fields.Nested(GenreSchema, dump_only=True)
    director = fields.Nested(DirectorSchema, dump_only=True)
