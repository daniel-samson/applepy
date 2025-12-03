"""Customer service for business logic."""

from sqlalchemy.orm import Session

from applepy.services.base import BaseService

from .models import Customer
from .repository import CustomerRepository
from .schemas import CustomerCreate, CustomerRecord


class CustomerService(BaseService[Customer, int, CustomerCreate, CustomerRecord]):
    """Customer service for CRUD operations on Customer entities.

    Inherits all business logic from BaseService including:
    - create: Create a new customer with validation
    - get: Get a customer by customer_number
    - get_all: Get all customers
    - update: Update an existing customer with validation
    - delete: Delete a customer
    """

    def __init__(self, session: Session) -> None:
        """Initialize the Customer service.

        Args:
            session: SQLAlchemy session for database operations
        """
        repo = CustomerRepository(session)
        super().__init__(repo, CustomerRecord)
