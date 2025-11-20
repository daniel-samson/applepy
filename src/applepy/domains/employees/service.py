from sqlalchemy.orm import Session

from applepy.services.base import BaseService

from .models import Employee
from .repository import EmployeeRepository
from .schemas import EmployeeCreate, EmployeeRecord


class EmployeeService(BaseService[Employee, int, EmployeeCreate, EmployeeRecord]):
    """Employee service for CRUD operations on Employee entities.

    Inherits all business logic from BaseService.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Employee service.

        Args:
            session: SQLAlchemy session for database operations
        """
        repo = EmployeeRepository(session)
        super().__init__(repo, EmployeeRecord)
