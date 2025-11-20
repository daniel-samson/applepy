"""Pytest configuration and shared fixtures for database testing."""

from collections.abc import Generator, Iterator
from contextlib import contextmanager

import pytest
from flask import Flask
from sqlalchemy import engine as sa_engine
from sqlalchemy.orm import Session
from werkzeug.test import Client

from applepy import db as db_module
from applepy.db import engine
from applepy.flask import app as applepyflask


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


class SessionProxy:
    """Proxy object that wraps a test session for Flask-SQLAlchemy compatibility.

    This allows Flask-SQLAlchemy's teardown logic to work while using our
    transactional test session.
    """

    def __init__(self, session: Session):
        self._session = session

    def __call__(self) -> Session:
        """Allow this proxy to be called like db.session()."""
        return self._session

    def __getattr__(self, name: str) -> object:
        """Delegate attribute access to the wrapped session."""
        return getattr(self._session, name)

    def remove(self) -> None:
        """No-op remove() to satisfy Flask-SQLAlchemy's teardown."""
        # Don't actually remove the session since it's managed by the fixture
        pass


@contextmanager
def get_test_session(test_session: Session) -> Iterator[Session]:
    """Context manager that yields the test session.

    This mimics the behavior of get_session() but uses the test session
    to ensure transaction rollback works in Flask tests.
    """
    try:
        yield test_session
    finally:
        # Don't close the test session - it's managed by the fixture
        pass


@pytest.fixture()
def app(db_session: Session) -> Generator[Flask, None, None]:
    """Flask app fixture with test database session.

    Patches db.session and get_session() to use the transactional test session,
    ensuring all database changes are rolled back after each test.
    """
    app = applepyflask
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # Patch db.session with our test session proxy
    original_session = db_module.db.session
    db_module.db.session = SessionProxy(db_session)  # type: ignore[assignment]

    # Patch get_session in the routes module where it's imported and used
    # This must be patched where get_session is USED, not where it's defined
    import applepy.routes.base as routes_module

    original_get_session = routes_module.get_session
    routes_module.get_session = lambda: get_test_session(db_session)  # type: ignore[assignment]

    yield app

    # Restore original functions
    db_module.db.session = original_session
    routes_module.get_session = original_get_session


@pytest.fixture()
def client(app: Flask) -> Client:
    """Test client for making requests to the Flask app."""
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> object:
    """CLI runner for testing CLI commands."""
    return app.test_cli_runner()


@pytest.fixture()
def test_office(client: Client) -> dict:  # type: ignore[name-defined]
    """Create a test office for employee tests."""
    import uuid

    office_data = {
        "office_code": f"TST{uuid.uuid4().hex[:5]}",
        "city": "Test City",
        "state": "MA",
        "country": "USA",
        "phone": "(617) 555-0100",
        "address_line_1": "100 Test Street",
        "address_line_2": None,
        "postal_code": "02108",
        "territory": "1",
    }
    response = client.post(
        "/offices", json=office_data, content_type="application/json"
    )
    return response.json["data"]  # type: ignore[return-value, index]
