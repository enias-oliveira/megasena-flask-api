from marshmallow import Schema, fields


class UpdateUserSchema(Schema):
    """
    PATC or PUT: /api/users/{user_id}
    {
    name (str),
    email (str),
    password (str)
    }
    """

    name = fields.Str()
    email = fields.Str()
    password = fields.Str()


update_user_schema = UpdateUserSchema()
