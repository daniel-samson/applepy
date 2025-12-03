"""Tests for customer domain routes."""

import uuid

from werkzeug.test import Client


def test_get_customers(client: Client) -> None:
    """Test listing all customers."""
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert "items" in response.json["data"]  # type: ignore[index, operator]
    assert "count" in response.json["data"]  # type: ignore[index, operator]


def test_create_customer(client: Client) -> None:
    """Test creating a new customer."""
    customer_data = {
        "customer_name": "Test Company",
        "contact_last_name": "Doe",
        "contact_first_name": "John",
        "phone": "+1-555-0100",
        "address_line_1": "123 Main St",
        "address_line_2": None,
        "city": "Boston",
        "state": "MA",
        "postal_code": "02108",
        "country": "USA",
        "sales_rep_employee_number": None,
        "credit_limit": 50000.00,
    }
    response = client.post(
        "/customers", json=customer_data, content_type="application/json"
    )
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert response.json["data"]["customer_name"] == "Test Company"  # type: ignore[index]
    assert response.json["data"]["contact_last_name"] == "Doe"  # type: ignore[index]
    assert response.json["data"]["contact_first_name"] == "John"  # type: ignore[index]
    assert "customer_number" in response.json["data"]  # type: ignore[index, operator]


def test_get_customer_by_id(client: Client) -> None:
    """Test getting a single customer by ID."""
    # First create a customer
    customer_data = {
        "customer_name": "Another Company",
        "contact_last_name": "Smith",
        "contact_first_name": "Jane",
        "phone": "+1-555-0101",
        "address_line_1": "456 Oak Ave",
        "address_line_2": None,
        "city": "Cambridge",
        "state": "MA",
        "postal_code": "02139",
        "country": "USA",
        "sales_rep_employee_number": None,
        "credit_limit": 75000.00,
    }
    create_response = client.post(
        "/customers", json=customer_data, content_type="application/json"
    )
    assert create_response.status_code == 201
    customer_id = create_response.json["data"]["customer_number"]  # type: ignore[index]

    # Now fetch that customer
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert response.json["data"]["customer_number"] == customer_id  # type: ignore[index]
    assert response.json["data"]["customer_name"] == "Another Company"  # type: ignore[index]


def test_update_customer_success(client: Client) -> None:
    """Test successfully updating a customer."""
    # Create a customer
    customer_data = {
        "customer_name": "Original Name",
        "contact_last_name": "Johnson",
        "contact_first_name": "Bob",
        "phone": "+1-555-0102",
        "address_line_1": "789 Elm St",
        "address_line_2": None,
        "city": "Somerville",
        "state": "MA",
        "postal_code": "02143",
        "country": "USA",
        "sales_rep_employee_number": None,
        "credit_limit": 25000.00,
    }
    create_response = client.post(
        "/customers", json=customer_data, content_type="application/json"
    )
    assert create_response.status_code == 201
    customer_id = create_response.json["data"]["customer_number"]  # type: ignore[index]

    # Update the customer
    updated_data = {
        "customer_name": "Updated Name",
        "contact_last_name": "Johnson",
        "contact_first_name": "Bob",
        "phone": "+1-555-0102",
        "address_line_1": "789 Elm St",
        "address_line_2": None,
        "city": "Somerville",
        "state": "MA",
        "postal_code": "02143",
        "country": "USA",
        "sales_rep_employee_number": None,
        "credit_limit": 30000.00,
        "customer_number": customer_id,
    }
    update_response = client.put(
        f"/customers/{customer_id}",
        json=updated_data,
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert update_response.headers["Content-Type"] == "application/json"
    assert "data" in update_response.json  # type: ignore[operator]
    assert update_response.json["data"]["customer_name"] == "Updated Name"  # type: ignore[index]
    assert (
        float(update_response.json["data"]["credit_limit"]) == 30000.00  # type: ignore[index, arg-type]
    )


def test_update_customer_number_mismatch(client: Client) -> None:
    """Test that update fails when URL customer_number doesn't match body."""
    customer_data = {
        "customer_name": "Mismatch Test",
        "contact_last_name": "Williams",
        "contact_first_name": "Alice",
        "phone": "+1-555-0103",
        "address_line_1": "321 Pine St",
        "address_line_2": None,
        "city": "Boston",
        "state": "MA",
        "postal_code": "02110",
        "country": "USA",
        "sales_rep_employee_number": None,
        "credit_limit": 10000.00,
        "customer_number": 999999,
    }
    response = client.put(
        "/customers/1",  # URL says 1
        json=customer_data,  # But body says 999999
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]
    assert "must match" in response.json["error"]  # type: ignore[index, operator]


def test_delete_customer_success(client: Client) -> None:
    """Test successfully deleting a customer."""
    # Create a customer
    customer_data = {
        "customer_name": "Delete Me Inc",
        "contact_last_name": "Brown",
        "contact_first_name": "Charlie",
        "phone": "+1-555-0104",
        "address_line_1": "999 Delete St",
        "address_line_2": None,
        "city": "Boston",
        "state": "MA",
        "postal_code": "02115",
        "country": "USA",
        "sales_rep_employee_number": None,
        "credit_limit": 5000.00,
    }
    create_response = client.post(
        "/customers", json=customer_data, content_type="application/json"
    )
    assert create_response.status_code == 201
    customer_id = create_response.json["data"]["customer_number"]  # type: ignore[index]

    # Delete the customer
    delete_response = client.delete(f"/customers/{customer_id}")
    assert delete_response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == 404


def test_get_customer_not_found(client: Client) -> None:
    """Test that getting a non-existent customer returns 404."""
    response = client.get("/customers/999999")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_update_customer_not_found(client: Client) -> None:
    """Test that updating a non-existent customer returns 404."""
    customer_data = {
        "customer_name": "Non-existent",
        "contact_last_name": "Lee",
        "contact_first_name": "David",
        "phone": "+1-555-0105",
        "address_line_1": "404 Not Found St",
        "address_line_2": None,
        "city": "Boston",
        "state": "MA",
        "postal_code": "02116",
        "country": "USA",
        "sales_rep_employee_number": None,
        "credit_limit": 0.00,
        "customer_number": 999999,
    }
    response = client.put(
        "/customers/999999",
        json=customer_data,
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_delete_customer_not_found(client: Client) -> None:
    """Test that deleting a non-existent customer returns 404."""
    response = client.delete("/customers/999999")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_customer_no_json(client: Client) -> None:
    """Test that creating a customer with no JSON returns error."""
    response = client.post("/customers", json=None, content_type="application/json")
    assert response.status_code in (400, 500)
    assert "error" in response.json  # type: ignore[operator]


def test_create_customer_invalid_json(client: Client) -> None:
    """Test that creating a customer with invalid JSON returns error."""
    response = client.post(
        "/customers",
        data="invalid json",
        content_type="application/json",
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_customer_missing_required_fields(client: Client) -> None:
    """Test that creating a customer with missing fields returns error."""
    customer_data = {
        "customer_name": "Incomplete Inc",
        # Missing required fields like contact_last_name, contact_first_name, etc.
    }
    response = client.post(
        "/customers", json=customer_data, content_type="application/json"
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_update_customer_no_json(client: Client) -> None:
    """Test that updating a customer with no JSON returns error."""
    response = client.put("/customers/1", json=None, content_type="application/json")
    assert response.status_code in (400, 500)
    assert "error" in response.json  # type: ignore[operator]


def test_create_customer_with_sales_rep(
    client: Client,
    test_office: dict,  # type: ignore[name-defined]
) -> None:
    """Test creating a customer with a sales rep relationship."""
    # First create a sales rep employee
    sales_rep_data = {
        "first_name": "Sales",
        "last_name": "Representative",
        "email": f"sales.rep.{uuid.uuid4()}@example.com",
        "job_title": "Sales Rep",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    sales_rep_response = client.post(
        "/employees", json=sales_rep_data, content_type="application/json"
    )
    assert sales_rep_response.status_code == 201
    sales_rep_id = sales_rep_response.json["data"]["employee_number"]  # type: ignore[index]

    # Now create a customer with this sales rep
    customer_data = {
        "customer_name": "Big Client Corp",
        "contact_last_name": "Martinez",
        "contact_first_name": "Grace",
        "phone": "+1-555-0106",
        "address_line_1": "555 Business Blvd",
        "address_line_2": "Suite 200",
        "city": "Boston",
        "state": "MA",
        "postal_code": "02118",
        "country": "USA",
        "sales_rep_employee_number": sales_rep_id,
        "credit_limit": 100000.00,
    }
    response = client.post(
        "/customers", json=customer_data, content_type="application/json"
    )
    assert response.status_code == 201
    assert (
        response.json["data"]["sales_rep_employee_number"] == sales_rep_id  # type: ignore[index]
    )


def test_create_customer_with_optional_fields(client: Client) -> None:
    """Test creating a customer with optional fields set to None."""
    customer_data = {
        "customer_name": "Minimal Data Inc",
        "contact_last_name": "Miller",
        "contact_first_name": "Henry",
        "phone": "+1-555-0107",
        "address_line_1": "777 Minimal St",
        "address_line_2": None,
        "city": "Boston",
        "state": None,
        "postal_code": None,
        "country": "USA",
        "sales_rep_employee_number": None,
        "credit_limit": None,
    }
    response = client.post(
        "/customers", json=customer_data, content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json["data"]["address_line_2"] is None  # type: ignore[index]
    assert response.json["data"]["state"] is None  # type: ignore[index]
    assert response.json["data"]["postal_code"] is None  # type: ignore[index]
    assert response.json["data"]["sales_rep_employee_number"] is None  # type: ignore[index]
    assert response.json["data"]["credit_limit"] is None  # type: ignore[index]


def test_create_multiple_customers(client: Client) -> None:
    """Test creating multiple customers."""
    customers = []
    for i in range(3):
        customer_data = {
            "customer_name": f"Company {i}",
            "contact_last_name": f"Last{i}",
            "contact_first_name": f"First{i}",
            "phone": f"+1-555-010{i}",
            "address_line_1": f"{i} Street",
            "address_line_2": None,
            "city": "Boston",
            "state": "MA",
            "postal_code": f"0210{i}",
            "country": "USA",
            "sales_rep_employee_number": None,
            "credit_limit": 10000.00 * (i + 1),
        }
        response = client.post(
            "/customers", json=customer_data, content_type="application/json"
        )
        assert response.status_code == 201
        customers.append(response.json["data"])  # type: ignore[index]

    # Verify we can list them
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json["data"]["count"] >= 3  # type: ignore[index]


def test_update_customer_with_new_sales_rep(
    client: Client,
    test_office: dict,  # type: ignore[name-defined]
) -> None:
    """Test updating a customer to assign a different sales rep."""
    # Create sales rep 1
    sales_rep1_data = {
        "first_name": "SalesRep1",
        "last_name": "One",
        "email": f"salesrep1.{uuid.uuid4()}@example.com",
        "job_title": "Sales Rep",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    sales_rep1_response = client.post(
        "/employees", json=sales_rep1_data, content_type="application/json"
    )
    sales_rep1_id = sales_rep1_response.json["data"]["employee_number"]  # type: ignore[index]

    # Create sales rep 2
    sales_rep2_data = {
        "first_name": "SalesRep2",
        "last_name": "Two",
        "email": f"salesrep2.{uuid.uuid4()}@example.com",
        "job_title": "Sales Rep",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    sales_rep2_response = client.post(
        "/employees", json=sales_rep2_data, content_type="application/json"
    )
    sales_rep2_id = sales_rep2_response.json["data"]["employee_number"]  # type: ignore[index]

    # Create customer with sales rep 1
    customer_data = {
        "customer_name": "Transfer Corp",
        "contact_last_name": "Taylor",
        "contact_first_name": "Ivy",
        "phone": "+1-555-0108",
        "address_line_1": "888 Transfer Ave",
        "address_line_2": None,
        "city": "Boston",
        "state": "MA",
        "postal_code": "02119",
        "country": "USA",
        "sales_rep_employee_number": sales_rep1_id,
        "credit_limit": 60000.00,
    }
    customer_response = client.post(
        "/customers", json=customer_data, content_type="application/json"
    )
    customer_id = customer_response.json["data"]["customer_number"]  # type: ignore[index]

    # Update customer to use sales rep 2
    updated_data = {
        "customer_name": "Transfer Corp",
        "contact_last_name": "Taylor",
        "contact_first_name": "Ivy",
        "phone": "+1-555-0108",
        "address_line_1": "888 Transfer Ave",
        "address_line_2": None,
        "city": "Boston",
        "state": "MA",
        "postal_code": "02119",
        "country": "USA",
        "sales_rep_employee_number": sales_rep2_id,
        "credit_limit": 60000.00,
        "customer_number": customer_id,
    }
    update_response = client.put(
        f"/customers/{customer_id}",
        json=updated_data,
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert (
        update_response.json["data"]["sales_rep_employee_number"]  # type: ignore[index]
        == sales_rep2_id
    )
