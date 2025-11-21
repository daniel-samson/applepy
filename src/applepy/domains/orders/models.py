from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from applepy.db import Base

if TYPE_CHECKING:
    from applepy.domains.customers.models import Customer


class Order(Base):
    """Database model for order data."""

    __tablename__ = "orders"

    order_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    required_date: Mapped[date] = mapped_column(Date, nullable=False)
    shipped_date: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True, default=None
    )
    status: Mapped[str] = mapped_column(String(15), nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    customer_number: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_number"), nullable=False
    )
    customer: Mapped[Optional["Customer"]] = relationship("Customer")
