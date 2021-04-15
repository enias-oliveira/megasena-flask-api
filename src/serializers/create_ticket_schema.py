from marshmallow import Schema, fields, validate


class CreateTicketSchema(Schema):
    """
    POST: /api/megasenas
    {
    numbers (int)
    }
    """

    numbers = fields.Integer(
        validate=validate.Range(min=6, max=10),
        required=True,
    )


create_ticket_schema = CreateTicketSchema()
