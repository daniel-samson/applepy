"""Generic base repository for CRUD operations."""

from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from applepy.exceptions import NotFoundException

# Type variables for generic CRUD operations
T = TypeVar("T")  # Model class
K = TypeVar("K")  # ID type (str, int, etc.)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)  # Create schema
RecordSchemaT = TypeVar("RecordSchemaT", bound=BaseModel)  # Record/response schema


class BaseRepository(Generic[T, K, CreateSchemaT, RecordSchemaT]):
    """Generic repository base class providing CRUD operations.

    This base class eliminates code duplication across domain repositories by
    providing generic implementations of common database operations (create, read,
    update, delete, list). Subclasses only need to specify the model class and
    configure field mappings.

    Type parameters:
        T: The SQLAlchemy model class (e.g., Office, Employee)
        K: The ID field type (e.g., str for office_code, int for employee_number)
        CreateSchemaT: Pydantic schema for creation (e.g., OfficeCreate)
        RecordSchemaT: Pydantic schema for responses (e.g., OfficeRecord)
    """

    def __init__(
        self,
        session: Session,
        model_class: Type[T],
        id_field_name: str,
    ) -> None:
        """Initialize the repository with session and model configuration.

        Args:
            session: SQLAlchemy session for database operations
            model_class: The SQLAlchemy model class for this repository
            id_field_name: Name of the primary key field (e.g., 'office_code')
        """
        self.session = session
        self.model_class = model_class
        self.id_field_name = id_field_name

    def all(self) -> list[T]:
        """Retrieve all records of this model type.

        Returns:
            List of all model instances from the database
        """
        return self.session.query(self.model_class).all()

    def get(self, id_value: K) -> T:
        """Retrieve a single record by its primary key.

        Args:
            id_value: The value of the primary key field

        Returns:
            The model instance if found

        Raises:
            NotFoundException: If no record with the given ID exists
        """
        id_field = getattr(self.model_class, self.id_field_name)
        entity = (
            self.session.query(self.model_class).filter(id_field == id_value).first()
        )

        if not entity:
            raise NotFoundException(f"{self.model_class.__name__} not found")

        return entity

    def create(self, data: CreateSchemaT) -> T:
        """Create a new record from validated schema data.

        Args:
            data: Pydantic schema instance with field values

        Returns:
            The newly created model instance with auto-generated fields populated
        """
        # Convert pydantic schema to dict and create model instance
        entity = self.model_class(**data.model_dump())
        self.session.add(entity)
        self.session.flush()  # Flush to populate auto-increment fields
        return entity

    def update(self, data: RecordSchemaT) -> T:
        """Update an existing record from validated schema data.

        Only fields that were explicitly set in the schema will be updated
        (using exclude_unset=True), allowing for partial updates.

        Args:
            data: Pydantic schema instance with field values including ID

        Returns:
            The updated model instance

        Raises:
            NotFoundException: If no record with the given ID exists
        """
        # Get ID value from schema
        id_value = getattr(data, self.id_field_name)

        # Query for existing entity
        id_field = getattr(self.model_class, self.id_field_name)
        entity = (
            self.session.query(self.model_class).filter(id_field == id_value).first()
        )

        if not entity:
            raise NotFoundException(f"{self.model_class.__name__} not found")

        # Get only the fields that were explicitly set
        update_data = data.model_dump(exclude_unset=True)

        # Don't update the primary key field
        update_data.pop(self.id_field_name, None)

        # Apply updates to model instance
        for key, value in update_data.items():
            setattr(entity, key, value)

        return entity

    def delete(self, id_value: K) -> None:
        """Delete a record by its primary key.

        Args:
            id_value: The value of the primary key field

        Raises:
            NotFoundException: If no record with the given ID exists
        """
        id_field = getattr(self.model_class, self.id_field_name)
        entity = (
            self.session.query(self.model_class).filter(id_field == id_value).first()
        )

        if not entity:
            raise NotFoundException(f"{self.model_class.__name__} not found")

        self.session.delete(entity)
