from sqlalchemy.orm import Session

from applepy.services.base import BaseService

from .models import Order
from .repository import OrderRepository
from .schemas import OrderCreate, OrderRecord


class OrderService(BaseService[Order, int, OrderCreate, OrderRecord]):
    """Order service for CRUD operations on Order entities.

    Inherits all business logic from BaseService.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Order service.

        Args:
            session: SQLAlchemy session for database operations
        """
        repo = OrderRepository(session)
        super().__init__(repo, OrderRecord)
