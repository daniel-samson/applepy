"""ProductLine CRUD routes."""

from applepy.routes.base import CrudRoutes

from .schemas import ProductLineCreate, ProductLineRecord
from .service import ProductLineService


class ProductLineRoutes(CrudRoutes[ProductLineCreate, ProductLineRecord, str]):
    """CRUD routes for product lines.

    Automatically generates:
    - GET /product-lines - List all product lines
    - GET /product-lines/<product_line> - Get product line by name
    - POST /product-lines - Create new product line
    - PUT /product-lines/<product_line> - Update product line
    - DELETE /product-lines/<product_line> - Delete product line
    """

    path = "/product-lines"
    service_class = ProductLineService
    create_schema = ProductLineCreate
    record_schema = ProductLineRecord
    id_param_name = "product_line"
