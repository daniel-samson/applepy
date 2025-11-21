from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductLineBase(BaseModel):
    """Validation for product line data."""

    model_config = ConfigDict(from_attributes=True)

    text_description: Optional[str] = None
    html_description: Optional[str] = None


class ProductLineCreate(ProductLineBase):
    """Validation for new product line on creation."""

    product_line: str


class ProductLineRecord(ProductLineBase):
    """Validation for existing product line on read."""

    product_line: str
