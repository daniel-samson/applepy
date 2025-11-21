from sqlalchemy.orm import Session

from applepy.services.base import BaseService

from .models import Product
from .repository import ProductRepository
from .schemas import ProductCreate, ProductRecord


class ProductService(BaseService[Product, str, ProductCreate, ProductRecord]):
    """Product service for CRUD operations on Product entities.

    Inherits all business logic from BaseService.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Product service.

        Args:
            session: SQLAlchemy session for database operations
        """
        repo = ProductRepository(session)
        super().__init__(repo, ProductRecord)
