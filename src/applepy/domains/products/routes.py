"""Product CRUD routes."""

from applepy.routes.base import CrudRoutes

from .schemas import ProductCreate, ProductRecord
from .service import ProductService


class ProductRoutes(CrudRoutes[ProductCreate, ProductRecord, str]):
    """CRUD routes for products.

    Automatically generates:
    - GET /products - List all products
    - GET /products/<product_code> - Get product by code
    - POST /products - Create new product
    - PUT /products/<product_code> - Update product
    - DELETE /products/<product_code> - Delete product
    """

    path = "/products"
    service_class = ProductService
    create_schema = ProductCreate
    record_schema = ProductRecord
    id_param_name = "product_code"
