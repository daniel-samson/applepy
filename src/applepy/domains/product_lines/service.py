from sqlalchemy.orm import Session

from applepy.services.base import BaseService

from .models import ProductLine
from .repository import ProductLineRepository
from .schemas import ProductLineCreate, ProductLineRecord


class ProductLineService(
    BaseService[ProductLine, str, ProductLineCreate, ProductLineRecord]
):
    """Product line service for CRUD operations on ProductLine entities.

    Inherits all business logic from BaseService.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the ProductLine service.

        Args:
            session: SQLAlchemy session for database operations
        """
        repo = ProductLineRepository(session)
        super().__init__(repo, ProductLineRecord)
