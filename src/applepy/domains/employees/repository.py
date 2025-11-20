from sqlalchemy.orm import Session

from applepy.exceptions import NotFoundException

from .models import Employee
from .schemas import EmployeeCreate, EmployeeRecord


class EmployeeRepository:
    """Employee repository. Takes pydantic models and returns SQLAlchemy db models"""

    def __init__(self, db_session: Session):
        self.session = db_session

    def get_all_employees(self) -> list[Employee]:
        return self.session.query(Employee).all()

    def create_employee(self, data: EmployeeCreate) -> Employee:
        employee = Employee(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            job_title=data.job_title,
            office_code=data.office_code,
            reports_to=data.reports_to,
        )
        self.session.add(employee)
        return employee

    def get_employee_by_id(self, employee_number: int) -> Employee:
        employee = (
            self.session.query(Employee)
            .filter(Employee.employee_number == employee_number)
            .first()
        )
        if not employee:
            raise NotFoundException(f"Employee with number {employee_number} not found")

        return employee

    def update_employee(self, data: EmployeeRecord) -> Employee:
        employee = (
            self.session.query(Employee)
            .filter(Employee.employee_number == data.employee_number)
            .first()
        )
        if not employee:
            raise NotFoundException(
                f"Employee with number {data.employee_number} not found"
            )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(employee, key, value)

        return employee

    def delete_employee(self, employee: EmployeeRecord) -> None:
        self.delete_employee_by_id(employee.employee_number)

    def delete_employee_by_id(self, employee_number: int) -> None:
        employee = (
            self.session.query(Employee)
            .filter(Employee.employee_number == employee_number)
            .first()
        )
        if not employee:
            raise NotFoundException(f"Employee with number {employee_number} not found")

        self.session.delete(employee)
