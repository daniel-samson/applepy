from typing import Optional

from pydantic import BaseModel


class OfficeBase(BaseModel):
    """Validates office data"""

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

    pass


class OfficeRecord(OfficeBase):
    """Validates existing office data on read"""

    office_code: str

    model_config = {
        "from_attributes": True,
    }
