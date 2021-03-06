from marshmallow import Schema, fields


class CreateUserSchema(Schema):
    """
    POST: /api/users
    {
    name (str),
    email (str),
    password (str)
    }
    """

    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


create_user_schema = CreateUserSchema()
