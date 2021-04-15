from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from http import HTTPStatus

from src.models.ticket_model import TicketModel
from src.services.ticket_numbers import (
    ticket_numbers_creator,
    ticket_numbers_list_to_string,
)


megasenas_bp = Blueprint("megasenas", __name__, url_prefix="/api/megasenas")


@megasenas_bp.route("")
def hello_megasena():
    return {"msg": "Hello Megasena"}, HTTPStatus.OK


@megasenas_bp.route("", methods=["POST"])
@jwt_required()
def create_ticket():
    body = request.get_json()

    from src.serializers.create_ticket_schema import create_ticket_schema

    request_errors = create_ticket_schema.validate(body)

    if request_errors:
        return {
            "msg": "Invalid or missing Megasena request fields."
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    request_numbers = body.get("numbers")
    ticket_numbers = ticket_numbers_creator(request_numbers)
    ticket_numbers_serialized = ticket_numbers_list_to_string(ticket_numbers)

    user_id = get_jwt_identity()
    ticket: TicketModel = TicketModel(
        ticket_numbers=ticket_numbers_serialized, user_id=user_id
    )

    session = current_app.db.session
    session.add(ticket)
    session.commit()

    return {"user_id": user_id, "data": ticket_numbers}, HTTPStatus.OK
