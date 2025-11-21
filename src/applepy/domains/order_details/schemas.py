from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderDetailBase(BaseModel):
    """Validation for order detail data."""

    model_config = ConfigDict(from_attributes=True)

    order_number: int
    product_code: str
    quantity_ordered: int
    price_each: Decimal
    order_line_number: int


class OrderDetailCreate(OrderDetailBase):
    """Validation for new order detail on creation."""

    pass


class OrderDetailRecord(OrderDetailBase):
    """Validation for existing order detail on read."""

    pass
