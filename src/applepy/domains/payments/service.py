from sqlalchemy.orm import Session

from .repository import PaymentRepository
from .schemas import PaymentCreate, PaymentRecord


class PaymentService:
    """Payment service for CRUD operations on Payment entities.

    Uses composite primary key (customer_number, check_number).
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Payment service.

        Args:
            session: SQLAlchemy session for database operations
        """
        self.repo = PaymentRepository(session)

    def all(self) -> list[PaymentRecord]:
        """Retrieve all payments.

        Returns:
            List of all PaymentRecord instances
        """
        entities = self.repo.all()
        return [PaymentRecord.model_validate(e) for e in entities]

    def get(self, customer_number: int, check_number: str) -> PaymentRecord:
        """Retrieve a payment by its composite key.

        Args:
            customer_number: The customer number
            check_number: The check number

        Returns:
            The PaymentRecord instance
        """
        entity = self.repo.get(customer_number, check_number)
        return PaymentRecord.model_validate(entity)

    def get_by_customer(self, customer_number: int) -> list[PaymentRecord]:
        """Retrieve all payments for a customer.

        Args:
            customer_number: The customer number

        Returns:
            List of PaymentRecord instances for the customer
        """
        entities = self.repo.get_by_customer(customer_number)
        return [PaymentRecord.model_validate(e) for e in entities]

    def create(self, data: PaymentCreate) -> PaymentRecord:
        """Create a new payment.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The newly created PaymentRecord instance
        """
        entity = self.repo.create(data)
        return PaymentRecord.model_validate(entity)

    def update(self, data: PaymentRecord) -> PaymentRecord:
        """Update an existing payment.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The updated PaymentRecord instance
        """
        entity = self.repo.update(data)
        return PaymentRecord.model_validate(entity)

    def delete(self, customer_number: int, check_number: str) -> None:
        """Delete a payment by its composite key.

        Args:
            customer_number: The customer number
            check_number: The check number
        """
        self.repo.delete(customer_number, check_number)
