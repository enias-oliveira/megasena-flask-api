from datetime import timedelta
from flask import Blueprint, request, current_app
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
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

    from src.serializers.log_user_schema import log_user_schema

    request_errors = log_user_schema.validate(body)

    if request_errors:
        return {
            "msg": "Invalid or missing User request fields."
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    logged_user: UserModel = UserModel.query.filter_by(email=email).first()

    if not logged_user or not logged_user.validate_password(password):
        return {
            "error": "Invalid user credentials or user not found."
        }, HTTPStatus.FORBIDDEN

    access_token = create_access_token(
        identity=logged_user.id, expires_delta=timedelta(days=7)
    )

    return {
        "user_id": logged_user.id,
        "access_token": access_token,
    }, HTTPStatus.CREATED


@users_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_user(id):
    if get_jwt_identity() != id:
        return {"msg": "Invalid token."}, HTTPStatus.UNAUTHORIZED

    body = request.get_json()

    from src.serializers.update_user_schema import update_user_schema

    request_errors = update_user_schema.validate(body)

    if request_errors:
        return {
            "msg": "Invalid or missing User request fields."
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    session = current_app.db.session
    new_password = body.pop("password", "")

    user: UserModel = UserModel.query.get(id)

    if new_password:
        user.password = new_password
        session.add(user)

    if body:
        UserModel.query.filter_by(id=id).update(body)

    session.commit()

    return {}, HTTPStatus.NO_CONTENT


@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    if get_jwt_identity() != id:
        return {"msg": "Invalid token."}, HTTPStatus.UNAUTHORIZED

    session = current_app.db.session

    user: UserModel = UserModel.query.get(id)

    session.delete(user)
    session.commit()

    return {}, HTTPStatus.NO_CONTENT
