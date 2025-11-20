from typing import Optional

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    """Validation for employee data."""

    first_name: str
    last_name: str
    email: str
    job_title: str
    office_code: Optional[str]
    reports_to: Optional[int]


class EmployeeCreate(EmployeeBase):
    """Validation for new employees on creation."""

    pass


class EmployeeRecord(EmployeeBase):
    """Validation for existing employees on update."""

    employee_number: int
