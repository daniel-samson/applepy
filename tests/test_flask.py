"""Tests for Flask application."""

from werkzeug.test import Client


def test_request_root(client: Client) -> None:
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json["message"] == "Hello, World!"  # type: ignore[index]
    assert response.json["error"] is None  # type: ignore[index]
