from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    """Validation for order data."""

    model_config = ConfigDict(from_attributes=True)

    order_date: date
    required_date: date
    shipped_date: Optional[date] = None
    status: str
    comments: Optional[str] = None
    customer_number: int


class OrderCreate(OrderBase):
    """Validation for new order on creation."""

    pass


class OrderRecord(OrderBase):
    """Validation for existing order on read."""

    order_number: int
