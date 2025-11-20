"""Base class for CRUD routes that automatically generates endpoints.

This module provides a generic CrudRoutes base class that generates standard
REST endpoints for any domain entity. Subclasses specify the service class,
schemas, and path, and all CRUD endpoints are created automatically.
"""

from typing import Any, Generic, Type, TypeVar

from flask import Blueprint, request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from applepy.exceptions import NotFoundException
from applepy.responses import ApiResponse, FlaskApiResponse, ListResponse
from applepy.services.base import BaseService
from applepy.session import get_session

# Type variables for generic CRUD routes
K = TypeVar("K")  # ID type
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
RecordSchemaT = TypeVar("RecordSchemaT", bound=BaseModel)


class CrudRoutes(Generic[CreateSchemaT, RecordSchemaT, K]):
    """Base class for generating CRUD REST endpoints.

    This class automatically generates list, get, create, update, and delete
    endpoints for a domain entity. Subclasses need to specify:
    - path: URL prefix for the routes (e.g., '/offices')
    - service_class: The service class to use for business logic
    - create_schema: Pydantic schema for POST/PUT requests
    - record_schema: Pydantic schema for responses
    - id_param_name: Name of the URL parameter for the ID (e.g., 'office_code')

    Type parameters:
        CreateSchemaT: Pydantic schema for create/update operations
        RecordSchemaT: Pydantic schema for responses
        K: Type of the primary key (str, int, etc.)
    """

    # These must be set by subclasses
    path: str
    service_class: Type[BaseService]  # type: ignore[type-arg]
    create_schema: Type[CreateSchemaT]
    record_schema: Type[RecordSchemaT]
    id_param_name: str

    def __init__(self) -> None:
        """Initialize the CRUD routes and create the blueprint."""
        self.blueprint = self._create_blueprint()

    def _create_blueprint(self) -> Blueprint:
        """Create and configure the Flask blueprint with all CRUD endpoints."""
        bp = Blueprint(
            self._get_blueprint_name(),
            __name__,
            url_prefix=self.path,
        )

        # Register all CRUD endpoints
        bp.add_url_rule("", "list", self.list_all, methods=["GET"])
        bp.add_url_rule("", "create", self.create, methods=["POST"])
        bp.add_url_rule(
            f"/<{self.id_param_name}>",
            "get",
            self.get_by_id,
            methods=["GET"],
        )
        bp.add_url_rule(
            f"/<{self.id_param_name}>",
            "update",
            self.update,
            methods=["PUT"],
        )
        bp.add_url_rule(
            f"/<{self.id_param_name}>",
            "delete",
            self.delete,
            methods=["DELETE"],
        )

        return bp

    def _get_blueprint_name(self) -> str:
        """Generate blueprint name from class name (e.g., OfficeRoutes -> office)."""
        class_name = self.__class__.__name__
        # Remove 'Routes' suffix and lowercase
        if class_name.endswith("Routes"):
            class_name = class_name[:-6]
        return class_name.lower()

    def _get_service(self, session: Session) -> BaseService:  # type: ignore[type-arg]
        """Get a service instance for the given session."""
        return self.service_class(session)  # type: ignore[call-arg, arg-type]

    def list_all(self) -> FlaskApiResponse:
        """List all records.

        Returns:
            200: List of all records
            500: Server error
        """
        try:
            with get_session() as session:
                service = self._get_service(session)
                records = service.get_all()
                list_response: ListResponse[RecordSchemaT] = ListResponse(
                    items=list(records), count=len(records)
                )
                response: ApiResponse[ListResponse[RecordSchemaT]] = ApiResponse(
                    data=list_response
                )
                return response.model_dump(), 200
        except Exception as e:
            error_response: ApiResponse[None] = ApiResponse(error=str(e))
            return error_response.model_dump(), 500

    def get_by_id(self, **kwargs: Any) -> FlaskApiResponse:
        """Get a single record by ID.

        Args:
            **kwargs: URL parameters including the ID

        Returns:
            200: The requested record
            404: Record not found
            500: Server error
        """
        try:
            id_value = kwargs[self.id_param_name]
            with get_session() as session:
                service = self._get_service(session)
                record = service.get_by_id(id_value)
                response: ApiResponse[RecordSchemaT] = ApiResponse(data=record)
                return response.model_dump(), 200
        except NotFoundException as e:
            error_response: ApiResponse[None] = ApiResponse(error=str(e))
            return error_response.model_dump(), 404
        except Exception as e:
            error_response = ApiResponse(error=str(e))
            return error_response.model_dump(), 500

    def create(self) -> FlaskApiResponse:
        """Create a new record.

        Returns:
            201: Record created
            400: Invalid request
            500: Server error
        """
        try:
            data = request.get_json()
            if not data:
                error_response: ApiResponse[None] = ApiResponse(
                    error="No JSON data provided"
                )
                return error_response.model_dump(), 400

            # Validate request data using schema
            create_data = self.create_schema(**data)

            with get_session() as session:
                service = self._get_service(session)
                created_record = service.create(create_data)
                session.commit()
                response: ApiResponse[RecordSchemaT] = ApiResponse(data=created_record)
                return response.model_dump(), 201
        except Exception as e:
            error_response = ApiResponse(error=str(e))
            return error_response.model_dump(), 500

    def update(self, **kwargs: Any) -> FlaskApiResponse:
        """Update an existing record.

        Args:
            **kwargs: URL parameters including the ID

        Returns:
            200: Record updated
            400: Invalid request
            404: Record not found
            500: Server error
        """
        try:
            id_value = kwargs[self.id_param_name]
            data = request.get_json()

            if not data:
                error_response: ApiResponse[None] = ApiResponse(
                    error="No JSON data provided"
                )
                return error_response.model_dump(), 400

            # Validate request data using schema
            record_data = self.record_schema(**data)

            # Validate that ID in URL matches ID in body
            id_in_body = getattr(record_data, self.id_param_name, None)
            if id_in_body != id_value:
                error_response = ApiResponse(
                    error=f"{self.id_param_name} in URL must match "
                    f"{self.id_param_name} in request body"
                )
                return error_response.model_dump(), 400

            with get_session() as session:
                service = self._get_service(session)
                updated_record = service.update(record_data)
                session.commit()
                response: ApiResponse[RecordSchemaT] = ApiResponse(data=updated_record)
                return response.model_dump(), 200
        except NotFoundException as e:
            error_response = ApiResponse(error=str(e))
            return error_response.model_dump(), 404
        except Exception as e:
            error_response_2: ApiResponse[None] = ApiResponse(error=str(e))
            return error_response_2.model_dump(), 500

    def delete(self, **kwargs: Any) -> FlaskApiResponse:
        """Delete a record by ID.

        Args:
            **kwargs: URL parameters including the ID

        Returns:
            204: Record deleted
            404: Record not found
            500: Server error
        """
        try:
            id_value = kwargs[self.id_param_name]
            with get_session() as session:
                service = self._get_service(session)
                service.delete_by_id(id_value)
                session.commit()
                response: ApiResponse[None] = ApiResponse(
                    message="Record deleted successfully"
                )
                return response.model_dump(), 204
        except NotFoundException as e:
            error_response: ApiResponse[None] = ApiResponse(error=str(e))
            return error_response.model_dump(), 404
        except Exception as e:
            error_response = ApiResponse(error=str(e))
            return error_response.model_dump(), 500
