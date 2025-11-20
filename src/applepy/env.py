import os

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
            "DATABASE_URL environment variable is required. "
            "Example: mysql+pymysql://user:password@localhost/database"
        )
