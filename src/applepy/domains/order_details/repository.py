from sqlalchemy.orm import Session

from applepy.exceptions import NotFoundException

from .models import OrderDetail
from .schemas import OrderDetailCreate, OrderDetailRecord


class OrderDetailRepository:
    """Order detail repository for CRUD operations on OrderDetail entities.

    Uses composite primary key (order_number, product_code).
    """

    def __init__(self, session: Session) -> None:
        """Initialize the OrderDetail repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        self.session = session

    def all(self) -> list[OrderDetail]:
        """Retrieve all order details.

        Returns:
            List of all OrderDetail instances from the database
        """
        return self.session.query(OrderDetail).all()

    def get(self, order_number: int, product_code: str) -> OrderDetail:
        """Retrieve an order detail by its composite key.

        Args:
            order_number: The order number
            product_code: The product code

        Returns:
            The OrderDetail instance if found

        Raises:
            NotFoundException: If no record with the given keys exists
        """
        entity = (
            self.session.query(OrderDetail)
            .filter(
                OrderDetail.order_number == order_number,
                OrderDetail.product_code == product_code,
            )
            .first()
        )

        if not entity:
            raise NotFoundException("OrderDetail not found")

        return entity

    def get_by_order(self, order_number: int) -> list[OrderDetail]:
        """Retrieve all order details for an order.

        Args:
            order_number: The order number

        Returns:
            List of OrderDetail instances for the order
        """
        return (
            self.session.query(OrderDetail)
            .filter(OrderDetail.order_number == order_number)
            .all()
        )

    def create(self, data: OrderDetailCreate) -> OrderDetail:
        """Create a new order detail.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The newly created OrderDetail instance
        """
        entity = OrderDetail(**data.model_dump())
        self.session.add(entity)
        self.session.flush()
        return entity

    def update(self, data: OrderDetailRecord) -> OrderDetail:
        """Update an existing order detail.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The updated OrderDetail instance

        Raises:
            NotFoundException: If no record with the given keys exists
        """
        entity = (
            self.session.query(OrderDetail)
            .filter(
                OrderDetail.order_number == data.order_number,
                OrderDetail.product_code == data.product_code,
            )
            .first()
        )

        if not entity:
            raise NotFoundException("OrderDetail not found")

        update_data = data.model_dump(exclude_unset=True)
        update_data.pop("order_number", None)
        update_data.pop("product_code", None)

        for key, value in update_data.items():
            setattr(entity, key, value)

        return entity

    def delete(self, order_number: int, product_code: str) -> None:
        """Delete an order detail by its composite key.

        Args:
            order_number: The order number
            product_code: The product code

        Raises:
            NotFoundException: If no record with the given keys exists
        """
        entity = (
            self.session.query(OrderDetail)
            .filter(
                OrderDetail.order_number == order_number,
                OrderDetail.product_code == product_code,
            )
            .first()
        )

        if not entity:
            raise NotFoundException("OrderDetail not found")

        self.session.delete(entity)
