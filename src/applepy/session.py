"""Database session context manager for automatic resource cleanup."""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from applepy.db import SessionLocal


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager for database sessions with automatic cleanup.

    This context manager provides automatic resource management for database
    sessions. It ensures that sessions are properly closed and cleaned up
    after use, preventing connection leaks.

    Usage:
        with get_session() as session:
            result = service.get_all(session)
            # Session is automatically closed after this block

    Yields:
        SQLAlchemy Session instance for database operations

    Note:
        Transactions must be managed by calling session.commit() or
        session.rollback() as needed. This context manager only ensures
        the session is properly closed.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
