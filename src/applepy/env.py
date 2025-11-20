import os
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
