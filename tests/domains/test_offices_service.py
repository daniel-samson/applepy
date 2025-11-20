"""Tests for the Office service with mocked repository."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from applepy.domains.offices.models import Office
from applepy.domains.offices.schemas import OfficeCreate, OfficeRecord
from applepy.domains.offices.service import OfficeService
from applepy.exceptions import NotFoundException


@pytest.fixture()
def mock_session() -> Mock:
    """Create a mock database session."""
    return MagicMock()


@pytest.fixture()
def office_service(mock_session: Mock) -> OfficeService:
    """Create an OfficeService with a mocked session."""
    return OfficeService(mock_session)


@pytest.fixture()
def sample_office_model() -> Office:
    """Create a sample Office model instance."""
    return Office(
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


@pytest.fixture()
def sample_office_record() -> OfficeRecord:
    """Create a sample OfficeRecord schema."""
    return OfficeRecord(
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


class TestOfficeServiceGetAllOffices:
    """Tests for the get_all_offices() method."""

    def test_get_all_offices_returns_empty_list(
        self, office_service: OfficeService
    ) -> None:
        """Test get_all_offices returns empty list when no offices exist."""
        with patch.object(office_service.repo, "all", return_value=[]) as mock_all:
            result = office_service.get_all_offices()

            assert result == []
            mock_all.assert_called_once()

    def test_get_all_offices_returns_all_offices(
        self,
        office_service: OfficeService,
        sample_office_model: Office,
    ) -> None:
        """Test get_all_offices returns all offices from repository."""
        offices = [sample_office_model]

        with patch.object(office_service.repo, "all", return_value=offices) as mock_all:
            result = office_service.get_all_offices()

            assert len(result) == 1
            assert isinstance(result[0], OfficeRecord)
            assert result[0].office_code == "NYC"
            assert result[0].city == "New York"
            mock_all.assert_called_once()

    def test_get_all_offices_returns_multiple_offices(
        self, office_service: OfficeService
    ) -> None:
        """Test get_all_offices with multiple offices."""
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
        offices = [office1, office2]

        with patch.object(office_service.repo, "all", return_value=offices) as mock_all:
            result = office_service.get_all_offices()

            assert len(result) == 2
            assert result[0].office_code == "NYC"
            assert result[1].office_code == "LAX"
            mock_all.assert_called_once()

    def test_get_all_offices_converts_to_office_record(
        self, office_service: OfficeService, sample_office_model: Office
    ) -> None:
        """Test that get_all_offices converts models to OfficeRecord."""
        with patch.object(
            office_service.repo, "all", return_value=[sample_office_model]
        ):
            result = office_service.get_all_offices()

            assert isinstance(result[0], OfficeRecord)
            assert result[0].phone == "(212) 555-0100"
            assert result[0].address_line_1 == "123 Main Street"


class TestOfficeServiceGetOfficeById:
    """Tests for the get_office_by_id() method."""

    def test_get_office_by_id_returns_office(
        self,
        office_service: OfficeService,
        sample_office_model: Office,
    ) -> None:
        """Test get_office_by_id returns the correct office."""
        with patch.object(
            office_service.repo, "get", return_value=sample_office_model
        ) as mock_get:
            result = office_service.get_office_by_id("NYC")

            assert isinstance(result, OfficeRecord)
            assert result.office_code == "NYC"
            assert result.city == "New York"
            mock_get.assert_called_once_with("NYC")

    def test_get_office_by_id_raises_not_found_exception(
        self, office_service: OfficeService
    ) -> None:
        """Test get_office_by_id raises NotFoundException."""
        with patch.object(
            office_service.repo,
            "get",
            side_effect=NotFoundException("Office not found"),
        ):
            with pytest.raises(NotFoundException, match="Office not found"):
                office_service.get_office_by_id("NONEXISTENT")

    def test_get_office_by_id_converts_to_office_record(
        self,
        office_service: OfficeService,
        sample_office_model: Office,
    ) -> None:
        """Test that get_office_by_id converts model to OfficeRecord."""
        with patch.object(office_service.repo, "get", return_value=sample_office_model):
            result = office_service.get_office_by_id("NYC")

            assert isinstance(result, OfficeRecord)
            assert hasattr(result, "office_code")
            assert hasattr(result, "city")
            assert hasattr(result, "state")

    def test_get_office_by_id_with_all_fields(
        self,
        office_service: OfficeService,
        sample_office_model: Office,
    ) -> None:
        """Test get_office_by_id with all fields populated."""
        with patch.object(office_service.repo, "get", return_value=sample_office_model):
            result = office_service.get_office_by_id("NYC")

            assert result.office_code == "NYC"
            assert result.city == "New York"
            assert result.state == "NY"
            assert result.country == "USA"
            assert result.phone == "(212) 555-0100"
            assert result.address_line_1 == "123 Main Street"
            assert result.address_line_2 == "Suite 100"
            assert result.postal_code == "10001"
            assert result.territory == "1"


class TestOfficeServiceCreateOffice:
    """Tests for the create_office() method."""

    def test_create_office_calls_repository(
        self,
        office_service: OfficeService,
        sample_office_create: OfficeCreate,
        sample_office_model: Office,
    ) -> None:
        """Test create_office calls repository create method."""
        with patch.object(
            office_service.repo, "create", return_value=sample_office_model
        ) as mock_create:
            result = office_service.create_office(sample_office_create)

            mock_create.assert_called_once_with(sample_office_create)
            assert isinstance(result, OfficeRecord)

    def test_create_office_returns_office_record(
        self,
        office_service: OfficeService,
        sample_office_create: OfficeCreate,
        sample_office_model: Office,
    ) -> None:
        """Test create_office returns OfficeRecord."""
        with patch.object(
            office_service.repo, "create", return_value=sample_office_model
        ):
            result = office_service.create_office(sample_office_create)

            assert isinstance(result, OfficeRecord)
            assert result.city == "New York"

    def test_create_office_with_minimal_data(
        self, office_service: OfficeService
    ) -> None:
        """Test create_office with minimal data."""
        office_data = OfficeCreate(
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
        office_model = Office(
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

        with patch.object(
            office_service.repo, "create", return_value=office_model
        ) as mock_create:
            result = office_service.create_office(office_data)

            assert result.city == "Boston"
            mock_create.assert_called_once_with(office_data)

    def test_create_office_preserves_all_fields(
        self,
        office_service: OfficeService,
        sample_office_create: OfficeCreate,
        sample_office_model: Office,
    ) -> None:
        """Test create_office preserves all fields."""
        with patch.object(
            office_service.repo, "create", return_value=sample_office_model
        ):
            result = office_service.create_office(sample_office_create)

            assert result.city == sample_office_create.city
            assert result.state == sample_office_create.state
            assert result.country == sample_office_create.country
            assert result.phone == sample_office_create.phone
            assert result.address_line_1 == sample_office_create.address_line_1


class TestOfficeServiceUpdateOffice:
    """Tests for the update_office() method."""

    def test_update_office_calls_repository(
        self,
        office_service: OfficeService,
        sample_office_record: OfficeRecord,
        sample_office_model: Office,
    ) -> None:
        """Test update_office calls repository update method."""
        with patch.object(
            office_service.repo, "update", return_value=sample_office_model
        ) as mock_update:
            result = office_service.update_office(sample_office_record)

            mock_update.assert_called_once_with(sample_office_record)
            assert isinstance(result, OfficeRecord)

    def test_update_office_returns_office_record(
        self,
        office_service: OfficeService,
        sample_office_record: OfficeRecord,
        sample_office_model: Office,
    ) -> None:
        """Test update_office returns OfficeRecord."""
        with patch.object(
            office_service.repo, "update", return_value=sample_office_model
        ):
            result = office_service.update_office(sample_office_record)

            assert isinstance(result, OfficeRecord)

    def test_update_office_with_modified_fields(
        self, office_service: OfficeService
    ) -> None:
        """Test update_office with modified fields."""
        updated_office = OfficeRecord(
            office_code="NYC",
            city="New York City",
            state="NY",
            country="USA",
            phone="(212) 555-0200",
            address_line_1="456 Park Avenue",
            address_line_2="Floor 20",
            postal_code="10022",
            territory="2",
        )
        office_model = Office(
            office_code="NYC",
            city="New York City",
            state="NY",
            country="USA",
            phone="(212) 555-0200",
            address_line_1="456 Park Avenue",
            address_line_2="Floor 20",
            postal_code="10022",
            territory="2",
        )

        with patch.object(
            office_service.repo, "update", return_value=office_model
        ) as mock_update:
            result = office_service.update_office(updated_office)

            assert result.city == "New York City"
            assert result.phone == "(212) 555-0200"
            mock_update.assert_called_once_with(updated_office)

    def test_update_office_raises_not_found_exception(
        self,
        office_service: OfficeService,
        sample_office_record: OfficeRecord,
    ) -> None:
        """Test update_office raises NotFoundException."""
        with patch.object(
            office_service.repo,
            "update",
            side_effect=NotFoundException("Office not found"),
        ):
            with pytest.raises(NotFoundException, match="Office not found"):
                office_service.update_office(sample_office_record)


class TestOfficeServiceDeleteOffice:
    """Tests for the delete_office_by_id() method."""

    def test_delete_office_by_id_calls_repository(
        self, office_service: OfficeService
    ) -> None:
        """Test delete_office_by_id calls repository delete method."""
        with patch.object(office_service.repo, "delete") as mock_delete:
            office_service.delete_office_by_id("NYC")

            mock_delete.assert_called_once_with("NYC")

    def test_delete_office_by_id_raises_not_found_exception(
        self, office_service: OfficeService
    ) -> None:
        """Test delete_office_by_id raises NotFoundException."""
        with patch.object(
            office_service.repo,
            "delete",
            side_effect=NotFoundException("Office not found"),
        ):
            with pytest.raises(NotFoundException, match="Office not found"):
                office_service.delete_office_by_id("NONEXISTENT")

    def test_delete_office_with_multiple_calls(
        self, office_service: OfficeService
    ) -> None:
        """Test deleting multiple offices sequentially."""
        with patch.object(office_service.repo, "delete") as mock_delete:
            office_service.delete_office_by_id("NYC")
            office_service.delete_office_by_id("LAX")
            office_service.delete_office_by_id("CHI")

            assert mock_delete.call_count == 3
            mock_delete.assert_any_call("NYC")
            mock_delete.assert_any_call("LAX")
            mock_delete.assert_any_call("CHI")


class TestOfficeServiceRepositoryInteraction:
    """Tests for service interaction with repository."""

    def test_service_creates_repository_with_session(self, mock_session: Mock) -> None:
        """Test service creates repository with provided session."""
        service = OfficeService(mock_session)

        assert service.repo is not None
        assert service.repo.session == mock_session

    def test_service_uses_same_repository_instance(self, mock_session: Mock) -> None:
        """Test service reuses the same repository instance."""
        service = OfficeService(mock_session)
        repo1 = service.repo
        repo2 = service.repo

        assert repo1 is repo2

    def test_service_delegates_to_repository(
        self, office_service: OfficeService, sample_office_model: Office
    ) -> None:
        """Test that service delegates operations to repository."""
        with (
            patch.object(
                office_service.repo, "all", return_value=[sample_office_model]
            ) as mock_all,
            patch.object(
                office_service.repo, "get", return_value=sample_office_model
            ) as mock_get,
        ):
            office_service.get_all_offices()
            office_service.get_office_by_id("NYC")

            mock_all.assert_called_once()
            mock_get.assert_called_once_with("NYC")


class TestOfficeServiceErrorHandling:
    """Tests for error handling in service."""

    def test_service_propagates_not_found_exception_from_get(
        self, office_service: OfficeService
    ) -> None:
        """Test service propagates NotFoundException from get."""
        with patch.object(
            office_service.repo,
            "get",
            side_effect=NotFoundException("Office not found"),
        ):
            with pytest.raises(NotFoundException):
                office_service.get_office_by_id("NONEXISTENT")

    def test_service_propagates_not_found_exception_from_update(
        self,
        office_service: OfficeService,
        sample_office_record: OfficeRecord,
    ) -> None:
        """Test service propagates NotFoundException from update."""
        with patch.object(
            office_service.repo,
            "update",
            side_effect=NotFoundException("Office not found"),
        ):
            with pytest.raises(NotFoundException):
                office_service.update_office(sample_office_record)

    def test_service_propagates_not_found_exception_from_delete(
        self, office_service: OfficeService
    ) -> None:
        """Test service propagates NotFoundException from delete."""
        with patch.object(
            office_service.repo,
            "delete",
            side_effect=NotFoundException("Office not found"),
        ):
            with pytest.raises(NotFoundException):
                office_service.delete_office_by_id("NONEXISTENT")
