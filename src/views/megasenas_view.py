from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from http import HTTPStatus

from src.services.ticket_numbers import ticket_numbers_creator


megasenas_bp = Blueprint("megasenas", __name__, url_prefix="/api/megasenas")


@megasenas_bp.route("")
def hello_megasena():
    return {"msg": "Hello Megasena"}, HTTPStatus.OK


@megasenas_bp.route("", methods=["POST"])
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

    return {"data": ticket_numbers}, HTTPStatus.OK
