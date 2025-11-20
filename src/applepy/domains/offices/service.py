from sqlalchemy.orm import Session

from applepy.services.base import BaseService

from .models import Office
from .repository import OfficeRepository
from .schemas import OfficeCreate, OfficeRecord


class OfficeService(BaseService[Office, str, OfficeCreate, OfficeRecord]):
    """Business logic for office operations.

    Inherits generic CRUD operations from BaseService, providing domain-specific
    method names and additional convenience methods for office management.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Office service.

        Args:
            session: SQLAlchemy session for database operations
        """
        repo = OfficeRepository(session)
        super().__init__(repo, OfficeRecord)

    def get_all_offices(self) -> list[OfficeRecord]:
        """Get all offices.

        Returns:
            List of all office records
        """
        return self.get_all()

    def get_office_by_id(self, office_code: str) -> OfficeRecord:
        """Get an office by its code.

        Args:
            office_code: The office code

        Returns:
            The office record

        Raises:
            NotFoundException: If office not found
        """
        return self.get_by_id(office_code)

    def create_office(self, data: OfficeCreate) -> OfficeRecord:
        """Create a new office.

        Args:
            data: Office creation data

        Returns:
            The created office record
        """
        return self.create(data)

    def update_office(self, data: OfficeRecord) -> OfficeRecord:
        """Update an existing office.

        Args:
            data: Office record with updated data

        Returns:
            The updated office record

        Raises:
            NotFoundException: If office not found
        """
        return self.update(data)

    def delete_office(self, data: OfficeRecord) -> None:
        """Delete an office by record.

        Args:
            data: Office record to delete

        Raises:
            NotFoundException: If office not found
        """
        self.delete_office_by_id(data.office_code)

    def delete_office_by_id(self, office_code: str) -> None:
        """Delete an office by its code.

        Args:
            office_code: The office code to delete

        Raises:
            NotFoundException: If office not found
        """
        self.delete_by_id(office_code)
