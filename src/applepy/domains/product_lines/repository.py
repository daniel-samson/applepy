from sqlalchemy.orm import Session

from applepy.repositories.base import BaseRepository

from .models import ProductLine
from .schemas import ProductLineCreate, ProductLineRecord


class ProductLineRepository(
    BaseRepository[ProductLine, str, ProductLineCreate, ProductLineRecord]
):
    """Product line repository for CRUD operations on ProductLine entities.

    Inherits all CRUD operations from BaseRepository.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the ProductLine repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        super().__init__(session, ProductLine, "product_line")
