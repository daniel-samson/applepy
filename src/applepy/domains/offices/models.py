from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from applepy.db import Base


class Office(Base):
    """Database model for office data"""

    __tablename__ = "offices"

    office_code: Mapped[str] = mapped_column(String(10), primary_key=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    address_line_1: Mapped[str] = mapped_column(String(255), nullable=True)
    address_line_2: Mapped[str] = mapped_column(String(255), nullable=True)
    state: Mapped[str] = mapped_column(String(50), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(10), nullable=True)
    territory: Mapped[str] = mapped_column(String(10), nullable=True)
