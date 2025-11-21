from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    """Validation for product data."""

    model_config = ConfigDict(from_attributes=True)

    product_name: str
    product_line: str
    product_scale: str
    product_vendor: str
    product_description: str
    quantity_in_stock: int
    buy_price: Decimal
    msrp: Decimal


class ProductCreate(ProductBase):
    """Validation for new product on creation."""

    product_code: str


class ProductRecord(ProductBase):
    """Validation for existing product on read."""

    product_code: str
