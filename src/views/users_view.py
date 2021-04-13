from flask import Blueprint, request


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["POST"])
def create_user():
    body = request.get_json()

    return body, 200
