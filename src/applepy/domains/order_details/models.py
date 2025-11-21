from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, Numeric, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from applepy.db import Base

if TYPE_CHECKING:
    from applepy.domains.orders.models import Order
    from applepy.domains.products.models import Product


class OrderDetail(Base):
    """Database model for order detail data."""

    __tablename__ = "order_details"

    order_number: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.order_number"), primary_key=True
    )
    product_code: Mapped[str] = mapped_column(
        String(15), ForeignKey("products.product_code"), primary_key=True
    )
    quantity_ordered: Mapped[int] = mapped_column(Integer, nullable=False)
    price_each: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    order_line_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    order: Mapped[Optional["Order"]] = relationship("Order")
    product: Mapped[Optional["Product"]] = relationship("Product")
