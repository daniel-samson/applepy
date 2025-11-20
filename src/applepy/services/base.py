"""Generic base service for business logic operations."""

from typing import Generic, Type, TypeVar

from pydantic import BaseModel

from applepy.repositories.base import BaseRepository

# Type variables (must match BaseRepository)
T = TypeVar("T")  # Model class
K = TypeVar("K")  # ID type
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)  # Create schema
RecordSchemaT = TypeVar("RecordSchemaT", bound=BaseModel)  # Record/response schema


class BaseService(Generic[T, K, CreateSchemaT, RecordSchemaT]):
    """Generic service base class providing business logic for CRUD operations.

    This base class eliminates code duplication across domain services by providing
    generic implementations of common business operations. It handles transformation
    between database models and Pydantic schemas, delegating actual database
    operations to the repository layer.

    Type parameters:
        T: The SQLAlchemy model class (e.g., Office, Employee)
        K: The ID field type (e.g., str for office_code, int for employee_number)
        CreateSchemaT: Pydantic schema for creation (e.g., OfficeCreate)
        RecordSchemaT: Pydantic schema for responses (e.g., OfficeRecord)
    """

    def __init__(
        self,
        repo: BaseRepository[T, K, CreateSchemaT, RecordSchemaT],
        schema_class: Type[RecordSchemaT],
    ) -> None:
        """Initialize the service with a repository and schema class.

        Args:
            repo: Repository instance for database operations
            schema_class: Pydantic schema class for response transformation
        """
        self.repo = repo
        self.schema_class = schema_class

    def get_all(self) -> list[RecordSchemaT]:
        """Retrieve all records and transform to response schema.

        Returns:
            List of records transformed to Pydantic schema instances
        """
        entities = self.repo.all()
        return [self.schema_class.model_validate(entity) for entity in entities]

    def get_by_id(self, id_value: K) -> RecordSchemaT:
        """Retrieve a single record by ID and transform to response schema.

        Args:
            id_value: The value of the primary key field

        Returns:
            Record transformed to Pydantic schema instance

        Raises:
            NotFoundException: If no record with the given ID exists
        """
        entity = self.repo.get(id_value)
        return self.schema_class.model_validate(entity)

    def create(self, data: CreateSchemaT) -> RecordSchemaT:
        """Create a new record from validated schema and transform response.

        Args:
            data: Pydantic create schema with field values

        Returns:
            Created record transformed to Pydantic response schema

        Raises:
            ValidationError: If schema validation fails (from caller)
            DatabaseError: If database operation fails
        """
        entity = self.repo.create(data)
        return self.schema_class.model_validate(entity)

    def update(self, data: RecordSchemaT) -> RecordSchemaT:
        """Update an existing record from validated schema and transform response.

        Args:
            data: Pydantic record schema with updated field values

        Returns:
            Updated record transformed to Pydantic response schema

        Raises:
            NotFoundException: If no record with the given ID exists
            ValidationError: If schema validation fails (from caller)
        """
        entity = self.repo.update(data)
        return self.schema_class.model_validate(entity)

    def delete_by_id(self, id_value: K) -> None:
        """Delete a record by its primary key.

        Args:
            id_value: The value of the primary key field

        Raises:
            NotFoundException: If no record with the given ID exists
        """
        self.repo.delete(id_value)
