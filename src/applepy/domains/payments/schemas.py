from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    """Validation for payment data."""

    model_config = ConfigDict(from_attributes=True)

    customer_number: int
    check_number: str
    payment_date: date
    amount: Decimal


class PaymentCreate(PaymentBase):
    """Validation for new payment on creation."""

    pass


class PaymentRecord(PaymentBase):
    """Validation for existing payment on read."""

    pass
