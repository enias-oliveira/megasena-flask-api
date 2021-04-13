from flask import Blueprint, request
from http import HTTPStatus

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/", methods=["POST"])
def create_user():
    body = request.get_json()

    from src.serializers.create_user_request_schema import CreateUserRequestSchema

    request_schema = CreateUserRequestSchema()
    errors = request_schema.validate(body)

    if errors:
        return {
            "msg": "Invalid or missing User request fields."
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    return body, HTTPStatus.OK
