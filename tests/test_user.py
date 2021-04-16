from pytest import fixture

from flask_jwt_extended import decode_token

from src.models.user_model import UserModel
from src.app import create_app


@fixture(scope="module")
def test_app():
    app = create_app()
    app.app_context().push()
    app.db.create_all()

    yield app

    app.db.session.remove()
    app.db.drop_all()


@fixture(scope="module")
def test_client(test_app):
    return test_app.test_client()


@fixture
def user_body():
    return {
        "name": "ioasys",
        "email": "ioasys@mail.com",
        "password": "b4ckEnd",
    }


def test_standard_user_creation(test_client, user_body):
    expected_response = {
        "id": 1,
        "name": "ioasys",
        "email": "ioasys@mail.com",
    }
    expected_user_name = user_body["name"]
    expected_user_email = user_body["email"]

    actual_response = test_client.post(
        "/api/users/signup",
        json=user_body,
    ).get_json()

    actual_user = UserModel.query.get(1)
    actual_user_name = actual_user.name
    actual_user_email = actual_user.email

    assert actual_response == expected_response
    assert actual_user_name == expected_user_name
    assert actual_user_email == expected_user_email


def test_user_login(test_client, user_body):
    user_body.pop("name")

    expected_jwt_id = 1
    expected_response_status = 201

    actual_response = test_client.post("/api/users/login", json=user_body)
    actual_status = actual_response.status_code
    actual_response_token = actual_response.get_json().get("access_token")
    actual_jwt_id = decode_token(actual_response_token).get("sub")

    assert expected_response_status == actual_status
    assert expected_jwt_id == actual_jwt_id
