from marshmallow import Schema, fields

class BaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class DirectorSchema(BaseSchema):
    name = fields.String(required=True)
    movies = fields.List(fields.Nested(lambda: MovieSchema(exclude=('genre', 'director',))), dump_only=True)

class GenreSchema(BaseSchema):
    name = fields.String(required=True)
    movies = fields.List(fields.Nested(lambda: MovieSchema(exclude=('genre', 'director',))), dump_only=True)

class MovieSchema(BaseSchema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    trailer = fields.Url(required=True)
    year = fields.Integer(required=True)
    rating = fields.Integer(required=True)

    genre = fields.Nested(lambda: GenreSchema(exclude=('movies', )), dump_only=True)
    director = fields.Nested(lambda: DirectorSchema(exclude=('movies', )), dump_only=True)

class UserSchema(BaseSchema):
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True)
    name = fields.String()
    surname = fields.String()
    refresh_token = fields.String(load_only=True)
    favorite_genre_id = fields.Integer(load_only=True)
    favorite_genre = fields.Nested(GenreSchema, dump_only=True)
    favourite_movies = fields.List(fields.Nested(MovieSchema), dump_only=True)