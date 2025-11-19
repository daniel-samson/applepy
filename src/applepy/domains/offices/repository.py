from typing import List

from sqlalchemy.orm import Session

from applepy.exceptions import NotFoundException

from .models import Office
from .schemas import OfficeCreate, OfficeRecord


class OfficeRepository:
    """Office repository. Takes pydantic models and returns SQLAlchemy db models"""

    def __init__(self, session: Session):
        self.session = session

    def all(self) -> List[Office]:
        return self.session.query(Office).all()

    def get(self, office_code: str) -> Office:
        office = (
            self.session.query(Office).filter(Office.office_code == office_code).first()
        )
        if not office:
            raise NotFoundException("Office not found")
        return office

    def create(self, data: OfficeCreate) -> Office:
        office = Office(
            office_code=data.office_code,
            city=data.city,
            state=data.state,
            country=data.country,
            phone=data.phone,
            address_line_1=data.address_line_1,
            address_line_2=data.address_line_2,
            postal_code=data.postal_code,
            territory=data.territory,
        )
        self.session.add(office)
        return office

    def update(self, data: OfficeRecord) -> Office:
        office = (
            self.session.query(Office)
            .filter(Office.office_code == data.office_code)
            .first()
        )
        if office is None:
            raise NotFoundException("Office not found")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(office, key, value)
        return office

    def delete(self, office_code: str) -> None:
        office = (
            self.session.query(Office).filter(Office.office_code == office_code).first()
        )
        if not office:
            raise NotFoundException("Office not found")
        self.session.delete(office)
