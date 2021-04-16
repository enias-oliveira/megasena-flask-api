import pytest
from flask_testing import TestCase

from src.models.user_model import UserModel
from src.app import create_app
from src.configurations.database import db


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

    expected_response = {"id": 1, "name": "ioasys", "email": "ioasys@mail.com"}
    expected_user_name = "ioasys"

    actual_response = test_client.post("/api/users/signup", json=given).get_json()
    actual_user_name = UserModel.query.get(1).name

    assert actual_response == expected_response
    assert actual_user_name == expected_user_name
