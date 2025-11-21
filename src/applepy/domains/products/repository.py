from sqlalchemy.orm import Session

from applepy.repositories.base import BaseRepository

from .models import Product
from .schemas import ProductCreate, ProductRecord


class ProductRepository(BaseRepository[Product, str, ProductCreate, ProductRecord]):
    """Product repository for CRUD operations on Product entities.

    Inherits all CRUD operations from BaseRepository.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Product repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        super().__init__(session, Product, "product_code")
