from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from applepy.db import Base


class ProductLine(Base):
    """Database model for product line data."""

    __tablename__ = "product_lines"

    product_line: Mapped[str] = mapped_column(String(50), primary_key=True)
    text_description: Mapped[Optional[str]] = mapped_column(
        String(4000), nullable=True, default=None
    )
    html_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image: Mapped[Optional[bytes]] = mapped_column(nullable=True)
