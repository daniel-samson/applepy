from collections.abc import Generator

import pytest
from flask import Flask
from werkzeug.test import Client

from applepy.flask import app as applepyflask


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    app = applepyflask
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask) -> Client:
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> object:
    return app.test_cli_runner()


def test_request_root(client: Client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json == {"message": "Hello, World!"}


def test_get_offices(client: Client) -> None:
    response = client.get("/offices")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "offices" in response.json  # type: ignore[operator]


def test_create_office(client: Client) -> None:
    import uuid

    unique_id = str(uuid.uuid4())[:5]
    office_data = {
        "office_code": f"TST{unique_id}",
        "city": f"TestCity{unique_id}",
        "state": "MA",
        "country": "USA",
        "phone": "(617) 555-0100",
        "address_line_1": "100 Hanover Street",
        "address_line_2": "Suite 200",
        "postal_code": "02108",
        "territory": "1",
    }
    response = client.post(
        "/offices", json=office_data, content_type="application/json"
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "office" in response.json  # type: ignore[operator]
    assert response.json["office"]["city"] == office_data["city"]  # type: ignore[index]


def test_create_office_no_json(client: Client) -> None:
    response = client.post("/offices", json=None, content_type="application/json")
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")
    # When json=None is passed, the body is "null" which parses as None
    # This should trigger the "No JSON data provided" check
    assert response.status_code in (400, 500)
    assert "error" in response.json  # type: ignore[operator]


def test_get_office_not_found(client: Client) -> None:
    response = client.get("/offices/NONEXISTENT")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_update_office_not_found(client: Client) -> None:
    office_data = {
        "office_code": "NONEXISTENT",
        "city": "TestCity",
        "state": "MA",
        "country": "USA",
        "phone": "(617) 555-0100",
        "address_line_1": "100 Hanover Street",
        "address_line_2": "Suite 200",
        "postal_code": "02108",
        "territory": "1",
    }
    response = client.put(
        "/offices/NONEXISTENT",
        json=office_data,
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_delete_office_not_found(client: Client) -> None:
    response = client.delete("/offices/NONEXISTENT")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_office_invalid_json(client: Client) -> None:
    response = client.post(
        "/offices",
        data="invalid json",
        content_type="application/json",
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_office_missing_required_fields(client: Client) -> None:
    office_data = {
        "city": "TestCity",
        # Missing required fields like office_code, state, etc.
    }
    response = client.post(
        "/offices", json=office_data, content_type="application/json"
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_update_office_no_json(client: Client) -> None:
    response = client.put(
        "/offices/TEST001", json=None, content_type="application/json"
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_update_office_invalid_json(client: Client) -> None:
    response = client.put(
        "/offices/TEST001",
        data="invalid json",
        content_type="application/json",
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]
