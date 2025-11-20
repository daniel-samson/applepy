"""Tests for office domain routes."""

import uuid

from werkzeug.test import Client


def test_get_offices(client: Client) -> None:
    """Test listing all offices."""
    response = client.get("/offices")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert "items" in response.json["data"]  # type: ignore[index, operator]
    assert "count" in response.json["data"]  # type: ignore[index, operator]


def test_create_office(client: Client) -> None:
    """Test creating a new office."""
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
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert response.json["data"]["city"] == office_data["city"]  # type: ignore[index]


def test_get_office_by_id(client: Client) -> None:
    """Test getting a single office by ID."""
    # First create an office
    unique_id = str(uuid.uuid4())[:5]
    office_data = {
        "office_code": f"GET{unique_id}",
        "city": f"TestCity{unique_id}",
        "state": "MA",
        "country": "USA",
        "phone": "(617) 555-0100",
        "address_line_1": "100 Hanover Street",
        "address_line_2": "Suite 200",
        "postal_code": "02108",
        "territory": "1",
    }
    create_response = client.post(
        "/offices", json=office_data, content_type="application/json"
    )
    assert create_response.status_code == 201
    office_code = office_data["office_code"]

    # Now fetch that office
    response = client.get(f"/offices/{office_code}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert response.json["data"]["office_code"] == office_code  # type: ignore[index]


def test_update_office_success(client: Client) -> None:
    """Test successfully updating an office."""
    unique_id = str(uuid.uuid4())[:5]
    office_data = {
        "office_code": f"UPD{unique_id}",
        "city": f"TestCity{unique_id}",
        "state": "MA",
        "country": "USA",
        "phone": "(617) 555-0100",
        "address_line_1": "100 Hanover Street",
        "address_line_2": "Suite 200",
        "postal_code": "02108",
        "territory": "1",
    }
    # First create an office
    create_response = client.post(
        "/offices", json=office_data, content_type="application/json"
    )
    assert create_response.status_code == 201

    # Now update it
    updated_data = {**office_data, "city": "UpdatedCity"}
    update_response = client.put(
        f"/offices/{office_data['office_code']}",
        json=updated_data,
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert update_response.headers["Content-Type"] == "application/json"
    assert "data" in update_response.json  # type: ignore[operator]
    assert update_response.json["data"]["city"] == "UpdatedCity"  # type: ignore[index]


def test_update_office_code_mismatch(client: Client) -> None:
    """Test that update fails when URL office_code doesn't match body office_code."""
    office_data = {
        "office_code": "NYC",
        "city": "New York",
        "state": "NY",
        "country": "USA",
        "phone": "(212) 555-0100",
        "address_line_1": "Broadway",
        "address_line_2": None,
        "postal_code": "10001",
        "territory": "1",
    }
    response = client.put(
        "/offices/LA",  # URL says LA
        json=office_data,  # But body says NYC
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]
    assert "must match" in response.json["error"]  # type: ignore[index, operator]


def test_delete_office_success(client: Client) -> None:
    """Test successfully deleting an office."""
    unique_id = str(uuid.uuid4())[:5]
    office_data = {
        "office_code": f"DEL{unique_id}",
        "city": f"TestCity{unique_id}",
        "state": "MA",
        "country": "USA",
        "phone": "(617) 555-0100",
        "address_line_1": "100 Hanover Street",
        "address_line_2": "Suite 200",
        "postal_code": "02108",
        "territory": "1",
    }
    # First create an office
    create_response = client.post(
        "/offices", json=office_data, content_type="application/json"
    )
    assert create_response.status_code == 201
    office_code = office_data["office_code"]

    # Delete the office
    delete_response = client.delete(f"/offices/{office_code}")
    assert delete_response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/offices/{office_code}")
    assert get_response.status_code == 404


def test_get_office_not_found(client: Client) -> None:
    """Test that getting a non-existent office returns 404."""
    response = client.get("/offices/NONEXISTENT")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_update_office_not_found(client: Client) -> None:
    """Test that updating a non-existent office returns 404."""
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
    """Test that deleting a non-existent office returns 404."""
    response = client.delete("/offices/NONEXISTENT")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_office_no_json(client: Client) -> None:
    """Test that creating an office with no JSON returns error."""
    response = client.post("/offices", json=None, content_type="application/json")
    # When json=None is passed, the body is "null" which parses as None
    # This should trigger the "No JSON data provided" check
    assert response.status_code in (400, 500)
    assert "error" in response.json  # type: ignore[operator]


def test_create_office_invalid_json(client: Client) -> None:
    """Test that creating an office with invalid JSON returns error."""
    response = client.post(
        "/offices",
        data="invalid json",
        content_type="application/json",
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_office_missing_required_fields(client: Client) -> None:
    """Test that creating an office with missing fields returns error."""
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
    """Test that updating an office with no JSON returns error."""
    response = client.put(
        "/offices/TEST001", json=None, content_type="application/json"
    )
    assert response.status_code in (400, 500)
    assert "error" in response.json  # type: ignore[operator]


def test_update_office_invalid_json(client: Client) -> None:
    """Test that updating an office with invalid JSON returns error."""
    response = client.put(
        "/offices/TEST001",
        data="invalid json",
        content_type="application/json",
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]
