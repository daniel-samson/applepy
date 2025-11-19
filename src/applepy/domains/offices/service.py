from typing import Sequence

from sqlalchemy.orm import Session

from .repository import OfficeRepository
from .schemas import OfficeCreate, OfficeRecord


class OfficeService:
    """Business logic for office operations"""

    def __init__(self, session: Session):
        self.repo = OfficeRepository(session)

    def get_all_offices(self) -> Sequence[OfficeRecord]:
        offices = self.repo.all()
        return [OfficeRecord.model_validate(office) for office in offices]

    def get_office_by_id(self, office_code: str) -> OfficeRecord:
        office = self.repo.get(office_code)
        return OfficeRecord.model_validate(office)

    def create_office(self, data: OfficeCreate) -> OfficeRecord:
        office = self.repo.create(data)
        return OfficeRecord.model_validate(office)

    def update_office(self, data: OfficeRecord) -> OfficeRecord:
        office = self.repo.update(data)
        return OfficeRecord.model_validate(office)

    def delete_office(self, data: OfficeRecord) -> None:
        self.delete_office_by_id(data.office_code)

    def delete_office_by_id(self, office_code: str) -> None:
        self.repo.delete(office_code)
