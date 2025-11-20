from sqlalchemy.orm import Session

from applepy.repositories.base import BaseRepository

from .models import Employee
from .schemas import EmployeeCreate, EmployeeRecord


class EmployeeRepository(BaseRepository[Employee, int, EmployeeCreate, EmployeeRecord]):
    """Employee repository for CRUD operations on Employee entities.

    Inherits generic CRUD operations from BaseRepository, providing specialized
    implementations only where needed for Employee-specific behavior.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Employee repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        super().__init__(session, Employee, "employee_number")

    def get_all_employees(self) -> list[Employee]:
        """Get all employees.

        Returns:
            List of all employee records
        """
        return self.all()

    def get_employee_by_id(self, employee_number: int) -> Employee:
        """Get an employee by ID.

        Args:
            employee_number: The employee number

        Returns:
            The employee record

        Raises:
            NotFoundException: If employee not found
        """
        return self.get(employee_number)

    def create_employee(self, data: EmployeeCreate) -> Employee:
        """Create a new employee.

        Args:
            data: Employee creation data

        Returns:
            The created employee record
        """
        return self.create(data)

    def update_employee(self, data: EmployeeRecord) -> Employee:
        """Update an existing employee.

        Args:
            data: Employee record with updated data

        Returns:
            The updated employee record

        Raises:
            NotFoundException: If employee not found
        """
        return self.update(data)

    def delete_employee(self, employee: EmployeeRecord) -> None:
        """Delete an employee by record.

        Args:
            employee: Employee record to delete

        Raises:
            NotFoundException: If employee not found
        """
        self.delete_employee_by_id(employee.employee_number)

    def delete_employee_by_id(self, employee_number: int) -> None:
        """Delete an employee by ID.

        Args:
            employee_number: The employee number to delete

        Raises:
            NotFoundException: If employee not found
        """
        self.delete(employee_number)
