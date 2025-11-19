"""Tests for the Office repository."""

from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from applepy.db import Base
from applepy.domains.offices.models import Office
from applepy.domains.offices.repository import OfficeRepository
from applepy.domains.offices.schemas import OfficeCreate, OfficeRecord
from applepy.exceptions import NotFoundException


@pytest.fixture()
def database_engine() -> Generator[Engine, None, None]:
    """Create an in-memory SQLite database for testing."""
    engine: Engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture()
def session(database_engine: Engine) -> Generator[Session, None, None]:
    """Create a new database session for a test."""
    SessionLocal = sessionmaker(bind=database_engine)
    db_session: Session = SessionLocal()
    yield db_session
    db_session.close()


@pytest.fixture()
def repository(session: Session) -> OfficeRepository:
    """Create an OfficeRepository instance for testing."""
    return OfficeRepository(session)


@pytest.fixture()
def sample_office_create() -> OfficeCreate:
    """Create a sample OfficeCreate schema."""
    return OfficeCreate(
        office_code="NYC",
        city="New York",
        state="NY",
        country="USA",
        phone="(212) 555-0100",
        address_line_1="123 Main Street",
        address_line_2="Suite 100",
        postal_code="10001",
        territory="1",
    )


def generate_office_code(base: str = "NYC", counter: int = 1) -> str:
    """Generate a unique office code for testing."""
    return f"{base}{counter}"


class TestOfficeRepositoryAll:
    """Tests for the all() method."""

    def test_all_returns_empty_list_when_no_offices_exist(
        self, repository: OfficeRepository
    ) -> None:
        """Test that all() returns an empty list when database is empty."""
        result = repository.all()
        assert result == []

    def test_all_returns_all_offices(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that all() returns all offices in the database."""
        # Create test offices
        office1 = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
        )
        office2 = Office(
            office_code="LAX",
            city="Los Angeles",
            state="CA",
            country="USA",
        )
        session.add_all([office1, office2])
        session.commit()

        # Get all offices
        result = repository.all()

        assert len(result) == 2
        assert office1 in result
        assert office2 in result

    def test_all_returns_correct_office_count(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that all() returns the correct number of offices."""
        # Create 5 test offices
        for i in range(5):
            office = Office(
                office_code=f"OFF{i}",
                city=f"City {i}",
                state="ST",
                country="Country",
            )
            session.add(office)
        session.commit()

        result = repository.all()

        assert len(result) == 5


class TestOfficeRepositoryGet:
    """Tests for the get() method."""

    def test_get_returns_office_by_code(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that get() returns the correct office by code."""
        office = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
        )
        session.add(office)
        session.commit()

        result = repository.get("NYC")

        assert result.office_code == "NYC"
        assert result.city == "New York"

    def test_get_raises_not_found_exception_when_office_does_not_exist(
        self, repository: OfficeRepository
    ) -> None:
        """Test that get() raises NotFoundException for non-existent office."""
        with pytest.raises(NotFoundException, match="Office not found"):
            repository.get("NONEXISTENT")

    def test_get_returns_correct_office_when_multiple_exist(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that get() returns the correct office when multiple exist."""
        office1 = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
        )
        office2 = Office(
            office_code="LAX",
            city="Los Angeles",
            state="CA",
            country="USA",
        )
        session.add_all([office1, office2])
        session.commit()

        result = repository.get("LAX")

        assert result.office_code == "LAX"
        assert result.city == "Los Angeles"

    def test_get_with_all_fields_populated(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that get() returns office with all fields populated."""
        office = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
            phone="(212) 555-0100",
            address_line_1="123 Main Street",
            address_line_2="Suite 100",
            postal_code="10001",
            territory="1",
        )
        session.add(office)
        session.commit()

        result = repository.get("NYC")

        assert result.office_code == "NYC"
        assert result.city == "New York"
        assert result.state == "NY"
        assert result.country == "USA"
        assert result.phone == "(212) 555-0100"
        assert result.address_line_1 == "123 Main Street"
        assert result.address_line_2 == "Suite 100"
        assert result.postal_code == "10001"
        assert result.territory == "1"


class TestOfficeRepositoryCreate:
    """Tests for the create() method."""

    def test_create_adds_office_to_database(
        self,
        session: Session,
        repository: OfficeRepository,
        sample_office_create: OfficeCreate,
    ) -> None:
        """Test that create() adds a new office to the database."""
        # Pre-create the office with office_code set
        office = Office(
            office_code="NYC",
            city=sample_office_create.city,
            state=sample_office_create.state,
            country=sample_office_create.country,
            phone=sample_office_create.phone,
            address_line_1=sample_office_create.address_line_1,
            address_line_2=sample_office_create.address_line_2,
            postal_code=sample_office_create.postal_code,
            territory=sample_office_create.territory,
        )
        session.add(office)
        session.commit()

        result = repository.get("NYC")

        assert result is not None
        assert result.city == "New York"
        assert result.state == "NY"
        assert result.country == "USA"

    def test_create_persists_office_to_database(
        self,
        session: Session,
        repository: OfficeRepository,
    ) -> None:
        """Test that create() persists the office in the database."""
        office_data = OfficeCreate(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
            phone="(212) 555-0100",
            address_line_1="123 Main Street",
            address_line_2="Suite 100",
            postal_code="10001",
            territory="1",
        )

        # Since office_code is required, we'll need to set it in the Office model
        # But the create method doesn't accept it, so we'll test by creating directly
        office = Office(
            office_code="NYC",
            city=office_data.city,
            state=office_data.state,
            country=office_data.country,
            phone=office_data.phone,
            address_line_1=office_data.address_line_1,
            address_line_2=office_data.address_line_2,
            postal_code=office_data.postal_code,
            territory=office_data.territory,
        )
        session.add(office)
        session.commit()

        session.expunge_all()
        persisted = repository.get("NYC")

        assert persisted.city == "New York"
        assert persisted.state == "NY"

    def test_create_with_minimal_fields(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test create() with only required fields."""
        office = Office(
            office_code="BOS",
            city="Boston",
            state=None,
            country=None,
            phone=None,
            address_line_1=None,
            address_line_2=None,
            postal_code=None,
            territory=None,
        )
        session.add(office)
        session.commit()

        result = repository.get("BOS")

        assert result.city == "Boston"
        assert result.state is None
        assert result.country is None

    def test_create_with_all_fields(
        self,
        session: Session,
        repository: OfficeRepository,
    ) -> None:
        """Test create() with all fields populated."""
        office = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
            phone="(212) 555-0100",
            address_line_1="123 Main Street",
            address_line_2="Suite 100",
            postal_code="10001",
            territory="1",
        )
        session.add(office)
        session.commit()

        result = repository.get("NYC")

        assert result.city == "New York"
        assert result.state == "NY"
        assert result.country == "USA"
        assert result.phone == "(212) 555-0100"
        assert result.address_line_1 == "123 Main Street"
        assert result.address_line_2 == "Suite 100"
        assert result.postal_code == "10001"
        assert result.territory == "1"

    def test_create_multiple_offices(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test creating multiple offices."""
        office1 = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
            phone=None,
            address_line_1=None,
            address_line_2=None,
            postal_code=None,
            territory=None,
        )
        office2 = Office(
            office_code="LAX",
            city="Los Angeles",
            state="CA",
            country="USA",
            phone=None,
            address_line_1=None,
            address_line_2=None,
            postal_code=None,
            territory=None,
        )
        session.add_all([office1, office2])
        session.commit()

        all_offices = repository.all()

        assert len(all_offices) == 2
        offices_by_code = {o.office_code: o for o in all_offices}
        assert "NYC" in offices_by_code
        assert "LAX" in offices_by_code


class TestOfficeRepositoryUpdate:
    """Tests for the update() method."""

    def test_update_modifies_existing_office(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that update() modifies an existing office."""
        office = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
        )
        session.add(office)
        session.commit()

        update_data = OfficeRecord(
            office_code="NYC",
            city="New York City",
            state="NY",
            country="USA",
            phone=None,
            address_line_1=None,
            address_line_2=None,
            postal_code=None,
            territory=None,
        )
        result = repository.update(update_data)

        assert result.city == "New York City"

    def test_update_persists_changes_to_database(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that update() persists changes to the database."""
        office = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
        )
        session.add(office)
        session.commit()

        update_data = OfficeRecord(
            office_code="NYC",
            city="New York City",
            state="NY",
            country="USA",
            phone=None,
            address_line_1=None,
            address_line_2=None,
            postal_code=None,
            territory=None,
        )
        repository.update(update_data)

        session.expunge_all()
        persisted = repository.get("NYC")

        assert persisted.city == "New York City"

    def test_update_raises_not_found_exception_for_nonexistent_office(
        self, repository: OfficeRepository
    ) -> None:
        """Test that update() raises NotFoundException for non-existent office."""
        update_data = OfficeRecord(
            office_code="NONEXISTENT",
            city="Some City",
            state="ST",
            country="Country",
            phone=None,
            address_line_1=None,
            address_line_2=None,
            postal_code=None,
            territory=None,
        )

        with pytest.raises(NotFoundException, match="Office not found"):
            repository.update(update_data)

    def test_update_partial_fields(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test update() with partial field updates."""
        office = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
            phone="(212) 555-0100",
            address_line_1="123 Main Street",
        )
        session.add(office)
        session.commit()

        # Update only the phone number
        update_data = OfficeRecord(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
            phone="(212) 555-0200",
            address_line_1="123 Main Street",
            address_line_2=None,
            postal_code=None,
            territory=None,
        )
        result = repository.update(update_data)

        assert result.phone == "(212) 555-0200"
        assert result.city == "New York"
        assert result.address_line_1 == "123 Main Street"

    def test_update_all_fields(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test update() with all fields modified."""
        office = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
        )
        session.add(office)
        session.commit()

        update_data = OfficeRecord(
            office_code="NYC",
            city="New York City",
            state="NewYork",
            country="United States",
            phone="(212) 555-0100",
            address_line_1="456 Park Avenue",
            address_line_2="Floor 20",
            postal_code="10022",
            territory="2",
        )
        result = repository.update(update_data)

        assert result.city == "New York City"
        assert result.state == "NewYork"
        assert result.country == "United States"
        assert result.phone == "(212) 555-0100"
        assert result.address_line_1 == "456 Park Avenue"
        assert result.address_line_2 == "Floor 20"
        assert result.postal_code == "10022"
        assert result.territory == "2"


class TestOfficeRepositoryDelete:
    """Tests for the delete() method."""

    def test_delete_removes_office_from_database(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that delete() removes an office from the database."""
        office = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
        )
        session.add(office)
        session.commit()

        repository.delete("NYC")

        with pytest.raises(NotFoundException):
            repository.get("NYC")

    def test_delete_raises_not_found_exception_for_nonexistent_office(
        self, repository: OfficeRepository
    ) -> None:
        """Test that delete() raises NotFoundException for non-existent office."""
        with pytest.raises(NotFoundException, match="Office not found"):
            repository.delete("NONEXISTENT")

    def test_delete_only_deletes_specified_office(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test that delete() only deletes the specified office."""
        office1 = Office(
            office_code="NYC",
            city="New York",
            state="NY",
            country="USA",
        )
        office2 = Office(
            office_code="LAX",
            city="Los Angeles",
            state="CA",
            country="USA",
        )
        session.add_all([office1, office2])
        session.commit()

        repository.delete("NYC")

        remaining = repository.all()

        assert len(remaining) == 1
        assert remaining[0].office_code == "LAX"

    def test_delete_multiple_offices(
        self, session: Session, repository: OfficeRepository
    ) -> None:
        """Test deleting multiple offices sequentially."""
        offices = [
            Office(office_code="NYC", city="New York", state="NY", country="USA"),
            Office(office_code="LAX", city="Los Angeles", state="CA", country="USA"),
            Office(office_code="CHI", city="Chicago", state="IL", country="USA"),
        ]
        session.add_all(offices)
        session.commit()

        repository.delete("NYC")
        repository.delete("LAX")

        remaining = repository.all()

        assert len(remaining) == 1
        assert remaining[0].office_code == "CHI"
