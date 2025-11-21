from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from applepy.db import Base

if TYPE_CHECKING:
    from applepy.domains.customers.models import Customer


class Payment(Base):
    """Database model for payment data."""

    __tablename__ = "payments"

    customer_number: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_number"), primary_key=True
    )
    check_number: Mapped[str] = mapped_column(String(50), primary_key=True)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    customer: Mapped[Optional["Customer"]] = relationship("Customer")
