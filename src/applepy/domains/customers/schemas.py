"""Customer schemas for validation."""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    """Base schema for customer data validation."""

    model_config = ConfigDict(from_attributes=True)

    customer_name: str
    contact_last_name: str
    contact_first_name: str
    phone: str
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str
    sales_rep_employee_number: Optional[int] = None
    credit_limit: Optional[Decimal] = None


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer."""

    pass


class CustomerRecord(CustomerBase):
    """Schema for an existing customer record."""

    customer_number: int
