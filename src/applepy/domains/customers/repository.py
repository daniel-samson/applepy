"""Customer repository for database operations."""

from sqlalchemy.orm import Session

from applepy.repositories.base import BaseRepository

from .models import Customer
from .schemas import CustomerCreate, CustomerRecord


class CustomerRepository(BaseRepository[Customer, int, CustomerCreate, CustomerRecord]):
    """Customer repository for CRUD operations on Customer entities.

    Inherits all CRUD operations from BaseRepository including:
    - create: Create a new customer
    - get: Get a customer by customer_number
    - get_all: Get all customers
    - update: Update an existing customer
    - delete: Delete a customer
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Customer repository.

        Args:
            session: SQLAlchemy session for database operations
        """
        super().__init__(session, Customer, "customer_number")
