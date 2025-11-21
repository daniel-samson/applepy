from sqlalchemy.orm import Session

from applepy.repositories.base import BaseRepository

from .models import Order
from .schemas import OrderCreate, OrderRecord


class OrderRepository(BaseRepository[Order, int, OrderCreate, OrderRecord]):
    """Order repository for CRUD operations on Order entities.

    Inherits all CRUD operations from BaseRepository.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Order repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        super().__init__(session, Order, "order_number")
