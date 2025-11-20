# 🍏🥧 ApplePy
API for a model car shop

## Status
[![CI](https://github.com/daniel-samson/applepy/actions/workflows/ci.yaml/badge.svg)](https://github.com/daniel-samson/applepy/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/daniel-samson/applepy/graph/badge.svg?token=BI1vE1160e)](https://codecov.io/gh/daniel-samson/applepy)

## Requirements
- Python 3.10+
- [UV](https://github.com/astral-sh/uv)
- Docker & Docker Compose (for database)

## Setup Development Environment

### 1. Install UV

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
# or on Windows PowerShell:
# irm https://astral.sh/uv/install.ps1 | iex
```

### 2. Install Project Dependencies

```sh
# Activate virtual environment
source .venv/bin/activate

# Install dependencies and dev tools
uv sync
```

### 3. Configure Environment Variables

```sh
# Copy the example environment file
cp .env.example .env

# Edit .env with your database configuration
# (Optional: defaults work with docker-compose setup)
```

### 4. Start Database

```sh
# Start MariaDB/MySQL via Docker (includes both development and test databases)
docker compose up -d

# This starts:
# - db: Development database (applepy) on port 3306
# - db_test: Test database (applepy_test) on port 3307
# - adminer: Web interface for database management on http://localhost:8080

# Run database migrations
uv run applepy db:migrate
```

### 5. Run the Application

```sh
# Run Flask development server
uv run applepy flask

# Server will be available at http://localhost:5000
```

### Running Tests

**Default: Transaction Rollback Isolation (Recommended)**
Tests use the development database with automatic transaction rollback:

```sh
make test
```

Benefits:
- ✅ No additional setup needed
- ✅ Fastest test execution
- ✅ Complete test isolation via transaction rollback
- ✅ No test data persists to development database
- ✅ Works with `docker compose up -d`

How it works:
1. Each test runs within a database transaction
2. All changes (inserts, updates, deletes) happen in the transaction
3. At the end of each test, the transaction is rolled back
4. Development database is restored to its original state
5. Zero test data pollution

**Separate Test Database (Optional - Manual Testing)**
If you want to use the separate test database for manual testing:

```sh
# The db_test service runs on port 3307 with applepy_test database
# Access via: mysql -h localhost -P 3307 -u root -p

# Inspect via Adminer: http://localhost:8080
```

**GitHub Actions CI**
Automatically uses a separate test database service to mirror production-like environment and prevent any CI data from affecting development database.

### Other Useful Commands

```sh
# Run type checking and linting
make check

# Format code
make format

# Build documentation
uv run mkdocs serve

# View all CLI commands
uv run applepy --help
```


## Documentation

- [Developers documentation](docs/index.md)
- [API documentation](docs/api.md)
