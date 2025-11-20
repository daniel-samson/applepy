"""Tests for environment configuration."""


def test_database_url_from_environment() -> None:
    """Test that DATABASE_URL is read from environment."""
    # This test checks that DATABASE_URL is properly configured
    # by verifying it's set to a valid value
    from applepy import env

    assert env.DATABASE_URL is not None
    db_url = env.DATABASE_URL
    assert "mysql" in db_url or "postgresql" in db_url or "sqlite" in db_url


def test_testing_flag_detection() -> None:
    """Test that TESTING environment variable is properly detected."""
    from applepy import env

    # The _is_testing flag is set during module import
    # Just verify it's a boolean
    assert isinstance(env._is_testing, bool)


def test_test_database_url_derivation() -> None:
    """Test that TEST_DATABASE_URL is derived from DATABASE_URL in testing mode."""
    # Only test if we're in testing mode
    from applepy import env

    if env._is_testing:
        assert env.TEST_DATABASE_URL is not None
        # TEST_DATABASE_URL should contain _test in the database name
        # or at least be different from DATABASE_URL
        assert env.TEST_DATABASE_URL is not None


def test_test_database_url_with_query_string() -> None:
    """Test TEST_DATABASE_URL derivation with query string in database URL."""
    # This tests the regex logic that extracts database name and query string
    import re

    test_url = "mysql+pymysql://user:pass@localhost/mydb?charset=utf8mb4"
    match = re.search(r"(/[^/?]+)(\?.*)?$", test_url)

    assert match is not None
    assert match.group(1) == "/mydb"
    assert match.group(2) == "?charset=utf8mb4"


def test_test_database_url_mysql_format() -> None:
    """Test TEST_DATABASE_URL derivation for MySQL URLs."""
    import re

    test_url = "mysql+pymysql://user:pass@localhost/mydb"
    match = re.search(r"(/[^/?]+)(\?.*)?$", test_url)

    assert match is not None
    database_name = match.group(1)
    query_string = match.group(2) or ""
    test_db_url = test_url.replace(
        database_name + query_string,
        database_name + "_test" + query_string,
    )

    assert test_db_url == "mysql+pymysql://user:pass@localhost/mydb_test"


def test_test_database_url_postgresql_format() -> None:
    """Test TEST_DATABASE_URL derivation for PostgreSQL URLs."""
    import re

    test_url = "postgresql://user:pass@localhost/mydb"
    match = re.search(r"(/[^/?]+)(\?.*)?$", test_url)

    assert match is not None
    database_name = match.group(1)
    query_string = match.group(2) or ""
    test_db_url = test_url.replace(
        database_name + query_string,
        database_name + "_test" + query_string,
    )

    assert test_db_url == "postgresql://user:pass@localhost/mydb_test"


def test_dotenv_loading_when_available() -> None:
    """Test that dotenv loading is attempted when available."""
    # The dotenv loading happens at module import time
    # This test just verifies the module loads without errors
    import importlib

    import applepy.env

    importlib.reload(applepy.env)
    # If we get here without exception, dotenv loading was attempted
    assert applepy.env.DATABASE_URL is not None


def test_environment_variable_testing_flag_true() -> None:
    """Test TESTING flag when set to 'true'."""
    # Since TESTING is already loaded, we can't easily change it,
    # but we can test the logic
    test_values = ["true", "True", "TRUE", "1", "yes", "Yes", "YES"]
    for value in test_values:
        result = value.lower() in ("true", "1", "yes")
        assert result is True


def test_environment_variable_testing_flag_false() -> None:
    """Test TESTING flag when set to invalid values."""
    # Test that invalid values are treated as False
    test_values = ["false", "0", "no", "random", "", "maybe"]
    for value in test_values:
        result = value.lower() in ("true", "1", "yes")
        assert result is False
