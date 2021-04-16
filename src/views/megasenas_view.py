from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from http import HTTPStatus

from src.models.ticket_model import TicketModel
from src.models.user_model import UserModel
from src.services.ticket_numbers import ticket_numbers_creator


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

    user_id = get_jwt_identity()
    ticket: TicketModel = TicketModel(user_id=user_id)

    request_numbers = body.get("numbers")
    numbers = ticket_numbers_creator(request_numbers)

    ticket.ticket_numbers = numbers

    session = current_app.db.session
    session.add(ticket)
    session.commit()

    from src.serializers.ticket_model_serializer import TicketSerializer

    serialized_ticket = TicketSerializer(ticket)

    return serialized_ticket, HTTPStatus.OK


@megasenas_bp.route("/draws", methods=["GET"])
@jwt_required()
def read_draw():

    from src.services.megasena_draw import draw_numbers_supplier

    draw_numbers = draw_numbers_supplier()

    return {"latest_draw": draw_numbers}, HTTPStatus.OK


@megasenas_bp.route("/results", methods=["GET"])
@jwt_required()
def read_results():
    user_id = get_jwt_identity()
    user: UserModel = UserModel.query.get(user_id)
    last_ticket: TicketModel = user.ticket_list[-1]

    from src.services.megasena_draw import get_correct_ticket_numbers

    correct_ticket_numbers = get_correct_ticket_numbers(last_ticket.ticket_numbers)

    from src.services.megasena_draw import draw_numbers_supplier

    last_draw = draw_numbers_supplier()

    return {
        "user_id": user_id,
        "last_ticket": {
            "ticket_id": last_ticket.id,
            "ticket_numbers": last_ticket.ticket_numbers,
        },
        "last_megasena_draw": last_draw,
        "correct_count": len(correct_ticket_numbers),
        "correct_numbers": correct_ticket_numbers,
    }, HTTPStatus.OK
