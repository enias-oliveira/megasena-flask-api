from marshmallow import Schema, fields


class LogUserSchema(Schema):
    """
    POST: /api/users/login
    {
    email (str),
    password (str)
    }
    """

    email = fields.Str(required=True)
    password = fields.Str(required=True)


log_user_schema = LogUserSchema()
