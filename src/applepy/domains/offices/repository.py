from sqlalchemy.orm import Session

from applepy.repositories.base import BaseRepository

from .models import Office
from .schemas import OfficeCreate, OfficeRecord


class OfficeRepository(BaseRepository[Office, str, OfficeCreate, OfficeRecord]):
    """Office repository for CRUD operations on Office entities.

    Inherits all CRUD operations from BaseRepository.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Office repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        super().__init__(session, Office, "office_code")
