from sqlalchemy.orm import Session

from applepy.services.base import BaseService

from .models import Office
from .repository import OfficeRepository
from .schemas import OfficeCreate, OfficeRecord


class OfficeService(BaseService[Office, str, OfficeCreate, OfficeRecord]):
    """Office service for CRUD operations on Office entities.

    Inherits all business logic from BaseService.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Office service.

        Args:
            session: SQLAlchemy session for database operations
        """
        repo = OfficeRepository(session)
        super().__init__(repo, OfficeRecord)
