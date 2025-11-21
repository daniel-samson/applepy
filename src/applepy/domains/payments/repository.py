from sqlalchemy.orm import Session

from applepy.exceptions import NotFoundException

from .models import Payment
from .schemas import PaymentCreate, PaymentRecord


class PaymentRepository:
    """Payment repository for CRUD operations on Payment entities.

    Uses composite primary key (customer_number, check_number).
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Payment repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        self.session = session

    def all(self) -> list[Payment]:
        """Retrieve all payments.

        Returns:
            List of all Payment instances from the database
        """
        return self.session.query(Payment).all()

    def get(self, customer_number: int, check_number: str) -> Payment:
        """Retrieve a payment by its composite key.

        Args:
            customer_number: The customer number
            check_number: The check number

        Returns:
            The Payment instance if found

        Raises:
            NotFoundException: If no record with the given keys exists
        """
        entity = (
            self.session.query(Payment)
            .filter(
                Payment.customer_number == customer_number,
                Payment.check_number == check_number,
            )
            .first()
        )

        if not entity:
            raise NotFoundException("Payment not found")

        return entity

    def get_by_customer(self, customer_number: int) -> list[Payment]:
        """Retrieve all payments for a customer.

        Args:
            customer_number: The customer number

        Returns:
            List of Payment instances for the customer
        """
        return (
            self.session.query(Payment)
            .filter(Payment.customer_number == customer_number)
            .all()
        )

    def create(self, data: PaymentCreate) -> Payment:
        """Create a new payment.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The newly created Payment instance
        """
        entity = Payment(**data.model_dump())
        self.session.add(entity)
        self.session.flush()
        return entity

    def update(self, data: PaymentRecord) -> Payment:
        """Update an existing payment.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The updated Payment instance

        Raises:
            NotFoundException: If no record with the given keys exists
        """
        entity = (
            self.session.query(Payment)
            .filter(
                Payment.customer_number == data.customer_number,
                Payment.check_number == data.check_number,
            )
            .first()
        )

        if not entity:
            raise NotFoundException("Payment not found")

        update_data = data.model_dump(exclude_unset=True)
        update_data.pop("customer_number", None)
        update_data.pop("check_number", None)

        for key, value in update_data.items():
            setattr(entity, key, value)

        return entity

    def delete(self, customer_number: int, check_number: str) -> None:
        """Delete a payment by its composite key.

        Args:
            customer_number: The customer number
            check_number: The check number

        Raises:
            NotFoundException: If no record with the given keys exists
        """
        entity = (
            self.session.query(Payment)
            .filter(
                Payment.customer_number == customer_number,
                Payment.check_number == check_number,
            )
            .first()
        )

        if not entity:
            raise NotFoundException("Payment not found")

        self.session.delete(entity)
