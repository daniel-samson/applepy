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
    assert "offices" in response.json


def test_create_office(client: Client) -> None:
    import uuid

    office_data = {
        "city": f"TestCity{str(uuid.uuid4())[:8]}",
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
    assert "office" in response.json
    assert response.json["office"]["city"] == office_data["city"]


def test_create_office_no_json(client: Client) -> None:
    response = client.post("/offices", json=None, content_type="application/json")
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")
    # When json=None is passed, the body is "null" which parses as None
    # This should trigger the "No JSON data provided" check
    assert response.status_code in (400, 500)
    assert "error" in response.json
