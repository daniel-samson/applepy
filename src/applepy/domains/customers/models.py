from typing import Optional

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from applepy.db import Base


class Customer(Base):
    """Database model for customer data"""

    __tablename__ = "customers"

    customer_number: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    address_line_1: Mapped[str] = mapped_column(String(50), nullable=False)
    address_line_2: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=None
    )
    postal_code: Mapped[Optional[str]] = mapped_column(
        String(15), nullable=True, default=None
    )
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    sales_rep_employee_number: Mapped[Optional[int]] = mapped_column(
        nullable=True, default=None
    )
    credit_limit: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2), nullable=True, default=None
    )
