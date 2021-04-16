import pytest

from src.models.user_model import UserModel
from src.app import create_app


@pytest.fixture
def test_app():
    app = create_app()
    app.app_context().push()
    app.db.create_all()

    yield app

    app.db.session.remove()
    app.db.drop_all()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


def test_standard_user_creation(test_client):
    given = {
        "name": "ioasys",
        "email": "ioasys@mail.com",
        "password": "b4ckEnd",
    }

    expected_response = {
        "id": 1,
        "name": "ioasys",
        "email": "ioasys@mail.com",
    }
    expected_user_name = given["name"]
    expected_user_email = given["email"]

    actual_response = test_client.post(
        "/api/users/signup",
        json=given,
    ).get_json()

    actual_user = UserModel.query.get(1)
    actual_user_name = actual_user.name
    actual_user_email = actual_user.email

    assert actual_response == expected_response
    assert actual_user_name == expected_user_name
    assert actual_user_email == expected_user_email
