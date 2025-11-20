"""Tests for employee domain routes."""

import uuid

from werkzeug.test import Client


def test_get_employees(client: Client) -> None:
    """Test listing all employees."""
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert "items" in response.json["data"]  # type: ignore[index, operator]
    assert "count" in response.json["data"]  # type: ignore[index, operator]


def test_create_employee(client: Client, test_office: dict) -> None:  # type: ignore[name-defined]
    """Test creating a new employee."""
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": f"john.doe.{uuid.uuid4()}@example.com",
        "job_title": "Sales Engineer",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    response = client.post(
        "/employees", json=employee_data, content_type="application/json"
    )
    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert response.json["data"]["first_name"] == "John"  # type: ignore[index]
    assert response.json["data"]["last_name"] == "Doe"  # type: ignore[index]
    assert response.json["data"]["email"] == employee_data["email"]  # type: ignore[index]
    assert "employee_number" in response.json["data"]  # type: ignore[index, operator]


def test_get_employee_by_id(client: Client, test_office: dict) -> None:  # type: ignore[name-defined]
    """Test getting a single employee by ID."""
    # First create an employee
    employee_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": f"jane.smith.{uuid.uuid4()}@example.com",
        "job_title": "Sales Manager",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    create_response = client.post(
        "/employees", json=employee_data, content_type="application/json"
    )
    assert create_response.status_code == 201
    employee_id = create_response.json["data"]["employee_number"]  # type: ignore[index]

    # Now fetch that employee
    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json  # type: ignore[operator]
    assert response.json["data"]["employee_number"] == employee_id  # type: ignore[index]
    assert response.json["data"]["first_name"] == "Jane"  # type: ignore[index]


def test_update_employee_success(client: Client, test_office: dict) -> None:  # type: ignore[name-defined]
    """Test successfully updating an employee."""
    # Create an employee
    employee_email = f"bob.johnson.{uuid.uuid4()}@example.com"
    employee_data = {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": employee_email,
        "job_title": "Sales Rep",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    create_response = client.post(
        "/employees", json=employee_data, content_type="application/json"
    )
    assert create_response.status_code == 201
    employee_id = create_response.json["data"]["employee_number"]  # type: ignore[index]

    # Update the employee (need to keep same email for unique constraint)
    updated_data = {
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": employee_email,
        "job_title": "Senior Sales Rep",
        "office_code": test_office["office_code"],
        "reports_to": None,
        "employee_number": employee_id,
    }
    update_response = client.put(
        f"/employees/{employee_id}",
        json=updated_data,
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert update_response.headers["Content-Type"] == "application/json"
    assert "data" in update_response.json  # type: ignore[operator]
    assert update_response.json["data"]["job_title"] == "Senior Sales Rep"  # type: ignore[index]


def test_update_employee_code_mismatch(client: Client) -> None:
    """Test that update fails when URL employee_number doesn't match body."""
    employee_data = {
        "first_name": "Alice",
        "last_name": "Williams",
        "email": f"alice.williams.{uuid.uuid4()}@example.com",
        "job_title": "Account Manager",
        "office_code": None,
        "reports_to": None,
        "employee_number": 999,
    }
    response = client.put(
        "/employees/1",  # URL says 1
        json=employee_data,  # But body says 999
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]
    assert "must match" in response.json["error"]  # type: ignore[index, operator]


def test_delete_employee_success(client: Client, test_office: dict) -> None:  # type: ignore[name-defined]
    """Test successfully deleting an employee."""
    # Create an employee
    employee_data = {
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": f"charlie.brown.{uuid.uuid4()}@example.com",
        "job_title": "Sales Director",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    create_response = client.post(
        "/employees", json=employee_data, content_type="application/json"
    )
    assert create_response.status_code == 201
    employee_id = create_response.json["data"]["employee_number"]  # type: ignore[index]

    # Delete the employee
    delete_response = client.delete(f"/employees/{employee_id}")
    assert delete_response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/employees/{employee_id}")
    assert get_response.status_code == 404


def test_get_employee_not_found(client: Client) -> None:
    """Test that getting a non-existent employee returns 404."""
    response = client.get("/employees/999999")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_update_employee_not_found(client: Client) -> None:
    """Test that updating a non-existent employee returns 404."""
    employee_data = {
        "first_name": "David",
        "last_name": "Lee",
        "email": f"david.lee.{uuid.uuid4()}@example.com",
        "job_title": "Consultant",
        "office_code": None,
        "reports_to": None,
        "employee_number": 999999,
    }
    response = client.put(
        "/employees/999999",
        json=employee_data,
        content_type="application/json",
    )
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_delete_employee_not_found(client: Client) -> None:
    """Test that deleting a non-existent employee returns 404."""
    response = client.delete("/employees/999999")
    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_employee_no_json(client: Client) -> None:
    """Test that creating an employee with no JSON returns error."""
    response = client.post("/employees", json=None, content_type="application/json")
    assert response.status_code in (400, 500)
    assert "error" in response.json  # type: ignore[operator]


def test_create_employee_invalid_json(client: Client) -> None:
    """Test that creating an employee with invalid JSON returns error."""
    response = client.post(
        "/employees",
        data="invalid json",
        content_type="application/json",
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_employee_missing_required_fields(client: Client) -> None:
    """Test that creating an employee with missing fields returns error."""
    employee_data = {
        "first_name": "Eve",
        # Missing required fields like last_name, email, job_title
    }
    response = client.post(
        "/employees", json=employee_data, content_type="application/json"
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_update_employee_no_json(client: Client) -> None:
    """Test that updating an employee with no JSON returns error."""
    response = client.put("/employees/1", json=None, content_type="application/json")
    assert response.status_code in (400, 500)
    assert "error" in response.json  # type: ignore[operator]


def test_update_employee_invalid_json(client: Client) -> None:
    """Test that updating an employee with invalid JSON returns error."""
    response = client.put(
        "/employees/1",
        data="invalid json",
        content_type="application/json",
    )
    assert response.status_code == 500
    assert response.headers["Content-Type"] == "application/json"
    assert "error" in response.json  # type: ignore[operator]


def test_create_employee_with_manager(client: Client, test_office: dict) -> None:  # type: ignore[name-defined]
    """Test creating an employee with a manager relationship."""
    # First create a manager
    manager_data = {
        "first_name": "Frank",
        "last_name": "Wilson",
        "email": f"frank.wilson.{uuid.uuid4()}@example.com",
        "job_title": "Manager",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    manager_response = client.post(
        "/employees", json=manager_data, content_type="application/json"
    )
    assert manager_response.status_code == 201
    manager_id = manager_response.json["data"]["employee_number"]  # type: ignore[index]

    # Now create an employee reporting to that manager
    employee_data = {
        "first_name": "Grace",
        "last_name": "Taylor",
        "email": f"grace.taylor.{uuid.uuid4()}@example.com",
        "job_title": "Sales Rep",
        "office_code": test_office["office_code"],
        "reports_to": manager_id,
    }
    response = client.post(
        "/employees", json=employee_data, content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json["data"]["reports_to"] == manager_id  # type: ignore[index]


def test_create_multiple_employees(client: Client, test_office: dict) -> None:  # type: ignore[name-defined]
    """Test creating multiple employees."""
    employees = []
    for i in range(3):
        employee_data = {
            "first_name": f"Employee{i}",
            "last_name": f"Last{i}",
            "email": f"employee{i}.{uuid.uuid4()}@example.com",
            "job_title": f"Title{i}",
            "office_code": test_office["office_code"],
            "reports_to": None,
        }
        response = client.post(
            "/employees", json=employee_data, content_type="application/json"
        )
        assert response.status_code == 201
        employees.append(response.json["data"])  # type: ignore[index]

    # Verify we can list them
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json["data"]["count"] >= 3  # type: ignore[index]


def test_create_employee_with_optional_fields(client: Client) -> None:
    """Test creating an employee with optional fields set to None."""
    employee_data = {
        "first_name": "Henry",
        "last_name": "Miller",
        "email": f"henry.miller.{uuid.uuid4()}@example.com",
        "job_title": "Analyst",
        "office_code": None,
        "reports_to": None,
    }
    response = client.post(
        "/employees", json=employee_data, content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json["data"]["office_code"] is None  # type: ignore[index]
    assert response.json["data"]["reports_to"] is None  # type: ignore[index]


def test_update_employee_with_new_manager(client: Client, test_office: dict) -> None:  # type: ignore[name-defined]
    """Test updating an employee to report to a different manager."""
    # Create manager 1
    manager1_data = {
        "first_name": "Manager1",
        "last_name": "One",
        "email": f"manager1.{uuid.uuid4()}@example.com",
        "job_title": "Manager",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    manager1_response = client.post(
        "/employees", json=manager1_data, content_type="application/json"
    )
    manager1_id = manager1_response.json["data"]["employee_number"]  # type: ignore[index]

    # Create manager 2
    manager2_data = {
        "first_name": "Manager2",
        "last_name": "Two",
        "email": f"manager2.{uuid.uuid4()}@example.com",
        "job_title": "Manager",
        "office_code": test_office["office_code"],
        "reports_to": None,
    }
    manager2_response = client.post(
        "/employees", json=manager2_data, content_type="application/json"
    )
    manager2_id = manager2_response.json["data"]["employee_number"]  # type: ignore[index]

    # Create employee reporting to manager1
    employee_email = f"ivy.martinez.{uuid.uuid4()}@example.com"
    employee_data = {
        "first_name": "Ivy",
        "last_name": "Martinez",
        "email": employee_email,
        "job_title": "Sales Rep",
        "office_code": test_office["office_code"],
        "reports_to": manager1_id,
    }
    employee_response = client.post(
        "/employees", json=employee_data, content_type="application/json"
    )
    employee_id = employee_response.json["data"]["employee_number"]  # type: ignore[index]

    # Update employee to report to manager2 (keep same email)
    updated_data = {
        "first_name": "Ivy",
        "last_name": "Martinez",
        "email": employee_email,
        "job_title": "Sales Rep",
        "office_code": test_office["office_code"],
        "reports_to": manager2_id,
        "employee_number": employee_id,
    }
    update_response = client.put(
        f"/employees/{employee_id}",
        json=updated_data,
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert update_response.json["data"]["reports_to"] == manager2_id  # type: ignore[index]
