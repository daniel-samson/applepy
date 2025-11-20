from typing import Optional

from pydantic import BaseModel, ConfigDict


class OfficeBase(BaseModel):
    """Validates office data"""

    model_config = ConfigDict(from_attributes=True)

    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: str
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    territory: Optional[str]
    phone: Optional[str]


class OfficeCreate(OfficeBase):
    """Validates new office data on creation"""

    office_code: str


class OfficeRecord(OfficeBase):
    """Validates existing office data on read"""

    office_code: str
