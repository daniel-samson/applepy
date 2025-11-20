"""Pytest configuration and shared fixtures for database testing."""

from collections.abc import Generator

import pytest
from sqlalchemy import engine as sa_engine
from sqlalchemy.orm import Session

from applepy.db import engine


@pytest.fixture(scope="function")
def db_connection() -> Generator[sa_engine.Connection, None, None]:
    """Create a database connection with a savepoint for transaction rollback.

    This fixture creates a nested transaction that allows each test to
    run independently without affecting the database state.
    """
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def db_session(db_connection: sa_engine.Connection) -> Generator[Session, None, None]:
    """Create a test database session that rolls back after each test.

    All changes made during the test are rolled back automatically,
    ensuring test isolation and preventing data pollution.
    """
    session = Session(bind=db_connection)

    yield session

    session.close()
