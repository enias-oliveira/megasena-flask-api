from pytest import fixture

from flask_jwt_extended import decode_token

from werkzeug.security import check_password_hash

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


def test_standard_user_creation(test_client):
    user_body = {
        "name": "ioasys",
        "email": "ioasys@mail.com",
        "password": "b4ckEnd",
    }

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


def test_user_login(test_client):
    login_body = {
        "email": "ioasys@mail.com",
        "password": "b4ckEnd",
    }

    expected_jwt_id = 1
    expected_response_status = 201

    actual_response = test_client.post("/api/users/login", json=login_body)
    actual_status = actual_response.status_code
    actual_response_token = actual_response.get_json().get("access_token")
    actual_jwt_id = decode_token(actual_response_token).get("sub")

    assert expected_response_status == actual_status
    assert expected_jwt_id == actual_jwt_id


def test_user_edit_name(test_client):
    login_body = {
        "email": "ioasys@mail.com",
        "password": "b4ckEnd",
    }

    body = {"name": "Python"}

    login_response = test_client.post("/api/users/login", json=login_body)
    access_token = login_response.get_json().get("access_token")

    expected_status = 204

    actual_response = test_client.patch(
        "/api/users/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=body,
    )

    acutal_status = actual_response.status_code

    assert acutal_status == expected_status

    expected_user_name_in_db = "Python"

    actual_user_name_in_db = UserModel.query.get(1).name

    assert actual_user_name_in_db == expected_user_name_in_db


def test_user_edit_email(test_client):
    login_body = {
        "email": "ioasys@mail.com",
        "password": "b4ckEnd",
    }

    body = {"email": "python@mail.com"}

    login_response = test_client.post("/api/users/login", json=login_body)
    access_token = login_response.get_json().get("access_token")

    expected_status = 204

    actual_response = test_client.patch(
        "/api/users/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=body,
    )

    acutal_status = actual_response.status_code

    assert acutal_status == expected_status

    expected_user_email_in_db = "python@mail.com"

    actual_user_email_in_db = UserModel.query.get(1).email

    assert actual_user_email_in_db == expected_user_email_in_db


def test_user_edit_password(test_client):
    login_body = {
        "email": "python@mail.com",
        "password": "b4ckEnd",
    }

    body = {"password": "PythonNoobMaster"}

    login_response = test_client.post("/api/users/login", json=login_body)
    access_token = login_response.get_json().get("access_token")

    expected_status = 204

    actual_response = test_client.patch(
        "/api/users/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=body,
    )

    acutal_status = actual_response.status_code

    assert acutal_status == expected_status

    expected_user_password_in_db = "PythonNoobMaster"

    actual_user_password_hash_in_db = UserModel.query.get(1).password_hash

    assert check_password_hash(
        actual_user_password_hash_in_db, expected_user_password_in_db
    )


def test_user_edit_all(test_client):
    login_body = {
        "email": "python@mail.com",
        "password": "PythonNoobMaster",
    }

    body = {"name": "Potato", "password": "BigPotato", "email": "potato@mail.com"}

    login_response = test_client.post("/api/users/login", json=login_body)
    access_token = login_response.get_json().get("access_token")

    expected_status = 204

    actual_response = test_client.put(
        "/api/users/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=body,
    )

    acutal_status = actual_response.status_code

    assert acutal_status == expected_status

    user_in_db: UserModel = UserModel.query.get(1)

    expected_user_name_in_db = "Potato"
    expected_user_email_in_db = "potato@mail.com"
    expected_user_password_in_db = "BigPotato"

    actual_user_name_in_db = user_in_db.name
    actual_user_email_in_db = user_in_db.email
    actual_user_password_hash_in_db = user_in_db.password_hash

    assert actual_user_name_in_db == expected_user_name_in_db
    assert actual_user_email_in_db == expected_user_email_in_db
    assert check_password_hash(
        actual_user_password_hash_in_db, expected_user_password_in_db
    )


def test_user_delete(test_client):
    login_body = {"password": "BigPotato", "email": "potato@mail.com"}

    login_response = test_client.post("/api/users/login", json=login_body)
    access_token = login_response.get_json().get("access_token")

    expected_status = 204

    actual_response = test_client.delete(
        "/api/users/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    acutal_status = actual_response.status_code

    assert acutal_status == expected_status

    assert UserModel.query.get(1) == None
