"""Employee CRUD routes."""

from applepy.routes.base import CrudRoutes

from .schemas import EmployeeCreate, EmployeeRecord
from .service import EmployeeService


class EmployeeRoutes(CrudRoutes[EmployeeCreate, EmployeeRecord, int]):
    """CRUD routes for employees.

    Automatically generates:
    - GET /employees - List all employees
    - GET /employees/<employee_number> - Get employee by number
    - POST /employees - Create new employee
    - PUT /employees/<employee_number> - Update employee
    - DELETE /employees/<employee_number> - Delete employee
    """

    path = "/employees"
    service_class = EmployeeService
    create_schema = EmployeeCreate
    record_schema = EmployeeRecord
    id_param_name = "employee_number"
