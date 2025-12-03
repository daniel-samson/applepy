"""Customer CRUD routes."""

from applepy.routes.base import CrudRoutes

from .schemas import CustomerCreate, CustomerRecord
from .service import CustomerService


class CustomerRoutes(CrudRoutes[CustomerCreate, CustomerRecord, int]):
    """CRUD routes for customers.

    Automatically generates REST API endpoints:
    - GET /customers - List all customers
    - GET /customers/<customer_number> - Get customer by number
    - POST /customers - Create new customer
    - PUT /customers/<customer_number> - Update customer
    - DELETE /customers/<customer_number> - Delete customer
    """

    path = "/customers"
    service_class = CustomerService
    create_schema = CustomerCreate
    record_schema = CustomerRecord
    id_param_name = "customer_number"
