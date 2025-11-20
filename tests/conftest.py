"""Pytest configuration and shared fixtures for database testing."""

from collections.abc import Generator

import pytest
from sqlalchemy import engine as sa_engine
from sqlalchemy.orm import Session

from applepy.db import engine


@pytest.fixture(scope="function")
def db_connection() -> Generator[sa_engine.Connection, None, None]:
    """Create a database connection with a savepoint for transaction rollback.

    This fixture creates an outer transaction on the connection. The test
    session will use begin_nested() to create savepoints within this transaction,
    allowing all changes to be rolled back after each test.
    """
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def db_session(db_connection: sa_engine.Connection) -> Generator[Session, None, None]:
    """Create a test database session with savepoint rollback isolation.

    Each test runs within a savepoint that is rolled back after the test,
    ensuring test isolation and preventing data pollution. The connection's
    outer transaction allows the savepoint to work correctly.
    """
    session = Session(bind=db_connection)

    # Begin a savepoint (nested transaction) for this test
    # This allows session.commit() calls within the test to work while still
    # allowing automatic rollback of all changes after the test
    nested_transaction = session.begin_nested()

    yield session

    # Rollback the savepoint if it's still active, undoing all changes made in this test
    # If the test already committed/rolled back the transaction, it will be closed
    if nested_transaction.is_active:
        nested_transaction.rollback()

    session.close()
