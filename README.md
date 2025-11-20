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
# Start MariaDB/MySQL via Docker
docker compose up -d

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

By default, tests use the development database with transaction rollback for isolation:

```sh
# Run tests (uses development database with transaction isolation)
make test
```

For complete database separation (optional):

```sh
# Option 1: Create separate test database
mysql -u root -p -e "CREATE DATABASE applepy_test;"

# Option 2: Run tests with test database isolation
TESTING=true make test
```

**GitHub Actions** automatically runs tests with a separate test database service to ensure CI tests don't affect development data.

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
