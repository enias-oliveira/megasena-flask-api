from flask import Blueprint, request, current_app
from http import HTTPStatus

import sqlalchemy

from src.models.user_model import UserModel
from src.serializers.user_model_schema import user_model_schema


users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/signup", methods=["POST"])
def create_user():
    session = current_app.db.session
    body = request.get_json()

    from src.serializers.create_user_schema import create_user_schema

    request_errors = create_user_schema.validate(body)

    if request_errors:
        return {
            "msg": "Invalid or missing User request fields."
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    user_name = body["name"]
    email = body["email"]
    password = body["password"]

    try:
        new_user = UserModel(name=user_name, email=email)
        new_user.password = password

        session.add(new_user)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        return {
            "msg": "Name or email is already taken."
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    serialized_user = user_model_schema.dump(new_user)
    return serialized_user, HTTPStatus.CREATED
