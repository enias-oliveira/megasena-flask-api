from datetime import timedelta
from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token
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


@users_bp.route("/login", methods=["POST"])
def log_user():
    body = request.get_json()
    email = body["email"]
    password = body["password"]

    logged_user: UserModel = UserModel.query.filter_by(email=email).first()

    if not logged_user or not logged_user.validate_password(password):
        return {
            "error": "Invalid user credentials or user not found."
        }, HTTPStatus.FORBIDDEN

    access_token = create_access_token(
        identity=logged_user.id, expires_delta=timedelta(days=7)
    )

    return {"access_token": access_token}, HTTPStatus.CREATED
