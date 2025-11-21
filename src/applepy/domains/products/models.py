from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Numeric, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from applepy.db import Base

if TYPE_CHECKING:
    from applepy.domains.product_lines.models import ProductLine


class Product(Base):
    """Database model for product data."""

    __tablename__ = "products"

    product_code: Mapped[str] = mapped_column(String(15), primary_key=True)
    product_name: Mapped[str] = mapped_column(String(70), nullable=False)
    product_line: Mapped[str] = mapped_column(
        String(50), ForeignKey("product_lines.product_line"), nullable=False
    )
    product_line_ref: Mapped[Optional["ProductLine"]] = relationship("ProductLine")
    product_scale: Mapped[str] = mapped_column(String(10), nullable=False)
    product_vendor: Mapped[str] = mapped_column(String(50), nullable=False)
    product_description: Mapped[str] = mapped_column(Text, nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    buy_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    msrp: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
