from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from applepy.db import Base
from applepy.domains.offices.models import Office


class Employee(Base):
    __tablename__ = "employees"

    employee_number = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    job_title = Column(String(50), nullable=False)
    office_code: Mapped[str] = mapped_column(ForeignKey("offices.office_code"))
    office: Mapped["Office"] = relationship(Office)
    reports_to: Mapped[int] = mapped_column(ForeignKey("employees.employee_number"))
    manager: Mapped["Employee"] = relationship(
        "Employee", remote_side=[employee_number]
    )
    direct_reports: Mapped[list["Employee"]] = relationship(
        "Employee", back_populates="manager"
    )

    __table_args__ = (
        ForeignKeyConstraint(["reports_to"], ["employees.employee_number"]),
        ForeignKeyConstraint(["office_code"], ["offices.office_code"]),
        UniqueConstraint("email", name="unique_email"),
    )
