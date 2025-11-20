from sqlalchemy.orm import Session

from .repository import EmployeeRepository
from .schemas import EmployeeCreate, EmployeeRecord


class EmployeeService:
    """Business logic and validation for employee operations."""

    def __init__(self, session: Session):
        self.repo = EmployeeRepository(session)

    def get_all_employees(self) -> list[EmployeeRecord]:
        employees = self.repo.get_all_employees()
        return [EmployeeRecord.model_validate(employee) for employee in employees]

    def get_employee_by_id(self, employee_number: int) -> EmployeeRecord:
        employee = self.repo.get_employee_by_id(employee_number)
        return EmployeeRecord.model_validate(employee)

    def create_employee(self, data: EmployeeCreate) -> EmployeeRecord:
        employee = self.repo.create_employee(data)
        return EmployeeRecord.model_validate(employee)

    def update_employee(self, data: EmployeeRecord) -> EmployeeRecord:
        employee = self.repo.update_employee(data)
        return EmployeeRecord.model_validate(employee)

    def delete_employee(self, employee_number: int) -> None:
        self.repo.delete_employee_by_id(employee_number)
