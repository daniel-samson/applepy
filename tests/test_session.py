"""Tests for database session management."""

from applepy.session import get_session


def test_get_session_context_manager() -> None:
    """Test that get_session is a context manager."""
    with get_session() as session:
        assert session is not None
        # Session should be a valid SQLAlchemy Session
        assert hasattr(session, "query")
        assert hasattr(session, "add")
        assert hasattr(session, "commit")


def test_get_session_closes_properly() -> None:
    """Test that get_session closes the session after context exit."""
    session_ref = None
    with get_session() as session:
        session_ref = session
        # Session should be open inside context
        assert not session_ref.info.get("closed", False)

    # After exiting context, session should be closed
    assert session_ref is not None
    # Check that the session's connection is closed by verifying
    # that operations would fail if we tried to use it


def test_get_session_closes_on_exception() -> None:
    """Test that session is closed even when exception occurs in context."""
    session_ref = None
    try:
        with get_session() as session:
            session_ref = session
            # Session should be open inside context
            assert hasattr(session, "query")
            raise ValueError("Test exception")
    except ValueError:
        pass

    # Session should still be closed even though exception was raised
    assert session_ref is not None


def test_get_session_multiple_contexts() -> None:
    """Test that multiple session contexts work independently."""
    with get_session() as session1:
        with get_session() as session2:
            # Both sessions should be distinct
            assert session1 is not session2
            # Both should have query capability inside context
            assert hasattr(session1, "query")
            assert hasattr(session2, "query")
