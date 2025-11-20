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

**Option 1: Default (Transaction Isolation)**
Tests use the development database with automatic transaction rollback:

```sh
make test
```

Benefits:
- No additional setup needed
- Fast iteration
- Transaction rollback prevents test pollution

**Option 2: Separate Test Database (Complete Isolation)**
If you started `docker compose up -d`, the test database (`applepy_test`) is already available:

```sh
# Run tests with complete database isolation
TESTING=true make test
```

This uses the separate test database service running on port 3307.

**GitHub Actions**
Tests automatically use a separate test database service to ensure CI tests don't affect development data.

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
