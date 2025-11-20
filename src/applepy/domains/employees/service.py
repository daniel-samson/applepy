from sqlalchemy.orm import Session

from applepy.services.base import BaseService

from .models import Employee
from .repository import EmployeeRepository
from .schemas import EmployeeCreate, EmployeeRecord


class EmployeeService(BaseService[Employee, int, EmployeeCreate, EmployeeRecord]):
    """Business logic for employee operations.

    Inherits generic CRUD operations from BaseService, providing domain-specific
    method names for semantic clarity in the business logic layer.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Employee service.

        Args:
            session: SQLAlchemy session for database operations
        """
        repo = EmployeeRepository(session)
        super().__init__(repo, EmployeeRecord)

    def get_all_employees(self) -> list[EmployeeRecord]:
        """Get all employees.

        Returns:
            List of all employee records
        """
        return self.get_all()

    def get_employee_by_id(self, employee_number: int) -> EmployeeRecord:
        """Get an employee by number.

        Args:
            employee_number: The employee number

        Returns:
            The employee record

        Raises:
            NotFoundException: If employee not found
        """
        return self.get_by_id(employee_number)

    def create_employee(self, data: EmployeeCreate) -> EmployeeRecord:
        """Create a new employee.

        Args:
            data: Employee creation data

        Returns:
            The created employee record
        """
        return self.create(data)

    def update_employee(self, data: EmployeeRecord) -> EmployeeRecord:
        """Update an existing employee.

        Args:
            data: Employee record with updated data

        Returns:
            The updated employee record

        Raises:
            NotFoundException: If employee not found
        """
        return self.update(data)

    def delete_employee_by_id(self, employee_number: int) -> None:
        """Delete an employee by number.

        Args:
            employee_number: The employee number to delete

        Raises:
            NotFoundException: If employee not found
        """
        self.delete_by_id(employee_number)
