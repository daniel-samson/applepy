from sqlalchemy.orm import Session

from .repository import OrderDetailRepository
from .schemas import OrderDetailCreate, OrderDetailRecord


class OrderDetailService:
    """Order detail service for CRUD operations on OrderDetail entities.

    Uses composite primary key (order_number, product_code).
    """

    def __init__(self, session: Session) -> None:
        """Initialize the OrderDetail service.

        Args:
            session: SQLAlchemy session for database operations
        """
        self.repo = OrderDetailRepository(session)

    def all(self) -> list[OrderDetailRecord]:
        """Retrieve all order details.

        Returns:
            List of all OrderDetailRecord instances
        """
        entities = self.repo.all()
        return [OrderDetailRecord.model_validate(e) for e in entities]

    def get(self, order_number: int, product_code: str) -> OrderDetailRecord:
        """Retrieve an order detail by its composite key.

        Args:
            order_number: The order number
            product_code: The product code

        Returns:
            The OrderDetailRecord instance
        """
        entity = self.repo.get(order_number, product_code)
        return OrderDetailRecord.model_validate(entity)

    def get_by_order(self, order_number: int) -> list[OrderDetailRecord]:
        """Retrieve all order details for an order.

        Args:
            order_number: The order number

        Returns:
            List of OrderDetailRecord instances for the order
        """
        entities = self.repo.get_by_order(order_number)
        return [OrderDetailRecord.model_validate(e) for e in entities]

    def create(self, data: OrderDetailCreate) -> OrderDetailRecord:
        """Create a new order detail.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The newly created OrderDetailRecord instance
        """
        entity = self.repo.create(data)
        return OrderDetailRecord.model_validate(entity)

    def update(self, data: OrderDetailRecord) -> OrderDetailRecord:
        """Update an existing order detail.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The updated OrderDetailRecord instance
        """
        entity = self.repo.update(data)
        return OrderDetailRecord.model_validate(entity)

    def delete(self, order_number: int, product_code: str) -> None:
        """Delete an order detail by its composite key.

        Args:
            order_number: The order number
            product_code: The product code
        """
        self.repo.delete(order_number, product_code)
