"""Custom exceptions for ApplePy application."""


class AppPyException(Exception):
    """Base exception for all ApplePy exceptions."""

    pass


class NotFoundException(AppPyException):
    """Raised when a requested resource is not found."""

    pass


class ValidationError(AppPyException):
    """Raised when data validation fails."""

    pass


class DuplicateKeyError(AppPyException):
    """Raised when attempting to create a resource with a duplicate key."""

    pass


class DatabaseError(AppPyException):
    """Raised when a database operation fails."""

    pass


class AuthenticationError(AppPyException):
    """Raised when authentication fails."""

    pass


class AuthorizationError(AppPyException):
    """Raised when a user lacks required permissions."""

    pass
