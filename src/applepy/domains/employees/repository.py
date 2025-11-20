from sqlalchemy.orm import Session

from applepy.repositories.base import BaseRepository

from .models import Employee
from .schemas import EmployeeCreate, EmployeeRecord


class EmployeeRepository(BaseRepository[Employee, int, EmployeeCreate, EmployeeRecord]):
    """Employee repository for CRUD operations on Employee entities.

    Inherits all CRUD operations from BaseRepository.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Employee repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        super().__init__(session, Employee, "employee_number")
