from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from http import HTTPStatus

from src.models.ticket_model import TicketModel
from src.models.user_model import UserModel
from src.services.ticket_numbers import (
    ticket_numbers_creator,
    ticket_numbers_list_to_string,
)


megasenas_bp = Blueprint("megasenas", __name__, url_prefix="/api/megasenas")


@megasenas_bp.route("", methods=["GET"])
@jwt_required()
def list_tickets():
    user_id = get_jwt_identity()

    user: UserModel = UserModel.query.get(user_id)
    user_tickets = user.ticket_list

    from src.serializers.ticket_model_serializer import TicketsSerializer

    serialized_tickets = TicketsSerializer(user_tickets)

    return serialized_tickets, HTTPStatus.OK


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

    from src.serializers.ticket_model_serializer import TicketSerializer

    serialized_ticket = TicketSerializer(ticket)

    return serialized_ticket, HTTPStatus.OK


@megasenas_bp.route("/draw", methods=["GET"])
@jwt_required()
def read_draw():

    from src.services.megasena_draw import draw_numbers_supplier

    draw_numbers = draw_numbers_supplier()

    return {"latest_draw": draw_numbers}, HTTPStatus.OK
