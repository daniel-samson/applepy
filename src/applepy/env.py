import os
import re
from pathlib import Path

# Load .env file from project root if it exists
# This allows developers to use `cp .env.example .env` for local development
try:
    from dotenv import load_dotenv

    env_file = Path.cwd() / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    # python-dotenv is optional (dev dependency)
    pass

# Allow default for testing, but require in production
_default_database_url = "mysql+pymysql://root:example@localhost/applepy?charset=utf8mb4"
_is_testing = os.getenv("TESTING", "").lower() in ("true", "1", "yes")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    if _is_testing:
        # Allow default for testing with isolated transactions
        DATABASE_URL = _default_database_url
    else:
        raise ValueError(
            "DATABASE_URL environment variable is required.\n"
            "\n"
            "To set up your development environment:\n"
            "1. Copy the example environment file: cp .env.example .env\n"
            "2. Edit .env and set DATABASE_URL to your database connection string\n"
            "3. Make sure your database is running (e.g., docker compose up -d)\n"
            "4. Run migrations: uv run applepy db:migrate\n"
            "\n"
            "Example DATABASE_URL formats:\n"
            "- MySQL:  mysql+pymysql://user:password@localhost/database\n"
            "- PostgreSQL: postgresql://user:password@localhost/database\n"
            "- SQLite: sqlite:///./test.db\n"
        )

# Test database configuration
# When testing, we use transaction rollback isolation with the development database.
# The TEST_DATABASE_URL is available but not used - it's here for reference or
# future use cases where a separate test database might be desired.
if _is_testing:
    # Check if TEST_DATABASE_URL is explicitly set in environment
    TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

    if not TEST_DATABASE_URL:
        # Derive test database name from DATABASE_URL by appending '_test'
        # This works for both MySQL and PostgreSQL
        # For MySQL: mysql+pymysql://user:pass@host/dbname?charset=utf8mb4
        #        -> mysql+pymysql://user:pass@host/dbname_test?charset=utf8mb4
        match = re.search(r"(/[^/?]+)(\?.*)?$", DATABASE_URL)
        if match:
            database_name = match.group(1)
            query_string = match.group(2) or ""
            TEST_DATABASE_URL = DATABASE_URL.replace(
                database_name + query_string,
                database_name + "_test" + query_string,
            )
        else:
            # Fallback: just append _test to the URL
            TEST_DATABASE_URL = DATABASE_URL + "_test"

    # Note: DATABASE_URL is NOT overridden with TEST_DATABASE_URL
    # Tests use transaction rollback isolation with the development database
