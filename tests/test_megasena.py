from pytest import fixture

from src.models.ticket_model import TicketModel
from src.app import create_app


@fixture()
def test_app():
    app = create_app()
    app.app_context().push()
    app.db.create_all()

    yield app

    app.db.session.remove()
    app.db.drop_all()


@fixture()
def test_client(test_app):
    return test_app.test_client()


@fixture()
def access_token(test_client):
    user_body = {"name": "megasena", "email": "megasena@mail.com", "password": "Mega"}

    login_body = {"email": "megasena@mail.com", "password": "Mega"}

    test_client.post(
        "/api/users/signup",
        json=user_body,
    ).get_json()

    login_response = test_client.post("/api/users/login", json=login_body)

    return login_response.get_json().get("access_token")


def test_create_ticket(test_client, access_token):
    body = {"numbers": 8}

    expected_status_code = 200
    expected_ticket_id = 1
    expected_numbers_length = 8

    actual_response = test_client.post(
        "/api/megasenas",
        headers={"Authorization": f"Bearer {access_token}"},
        json=body,
    )
    actual_response_json = actual_response.get_json()

    actual_status_code = actual_response.status_code
    actual_ticket_id = actual_response_json.get("megasena_ticket_id")
    actual_numbers_length = len(actual_response_json.get("ticket_numbers"))

    assert actual_status_code == expected_status_code
    assert actual_ticket_id == expected_ticket_id
    assert actual_numbers_length == expected_numbers_length


def test_last_megasena_draw(test_client, access_token):
    expected_status_code = 200
    expected_draw_numbers = [3, 20, 22, 32, 35, 50]

    actual_response = test_client.get(
        "/api/megasenas/draws",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    actual_status_code = actual_response.status_code
    actual_numbers = actual_response.get_json().get("latest_draw")

    assert actual_status_code == expected_status_code
    assert actual_numbers == expected_draw_numbers


def test_list_tickets(test_client, access_token):
    body = {"numbers": 8}

    first_ticket = (
        test_client.post(
            "/api/megasenas",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
        )
        .get_json()
        .get("ticket_numbers")
    )

    second_ticket = (
        test_client.post(
            "/api/megasenas",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
        )
        .get_json()
        .get("ticket_numbers")
    )

    megasenas_response = (
        test_client.get(
            "/api/megasenas",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        .get_json()
        .get("megasena_tickets")
    )

    assert megasenas_response[1]["ticket_numbers"] == first_ticket
    assert megasenas_response[0]["ticket_numbers"] == second_ticket
