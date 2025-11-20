"""Generic API response models for CRUD operations."""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

# Flask response type alias for type-safe API endpoints
FlaskApiResponse = tuple[dict[str, Any], int]


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper for single resource operations."""

    data: Optional[T] = None
    error: Optional[str] = None
    message: Optional[str] = None


class ListResponse(BaseModel, Generic[T]):
    """Wrapper for list/collection responses."""

    items: list[T]
    count: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Wrapper for paginated list responses."""

    items: list[T]
    count: int
    page: int
    page_size: int
    total_pages: int
