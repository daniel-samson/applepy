from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    """Validation for employee data."""

    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    email: str
    job_title: str
    extension: Optional[str] = None
    office_code: Optional[str] = None
    reports_to: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    """Validation for new employees on creation."""

    pass


class EmployeeRecord(EmployeeBase):
    """Validation for existing employees on update."""

    employee_number: int
