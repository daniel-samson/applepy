from collections.abc import Generator

import pytest
from flask import Flask
from werkzeug.test import Client

from applepy.flask import create_app


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    app = create_app()
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
