"""Order CRUD routes."""

from applepy.routes.base import CrudRoutes

from .schemas import OrderCreate, OrderRecord
from .service import OrderService


class OrderRoutes(CrudRoutes[OrderCreate, OrderRecord, int]):
    """CRUD routes for orders.

    Automatically generates:
    - GET /orders - List all orders
    - GET /orders/<order_number> - Get order by number
    - POST /orders - Create new order
    - PUT /orders/<order_number> - Update order
    - DELETE /orders/<order_number> - Delete order
    """

    path = "/orders"
    service_class = OrderService
    create_schema = OrderCreate
    record_schema = OrderRecord
    id_param_name = "order_number"
