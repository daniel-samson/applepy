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

### Other Useful Commands

```sh
# Run tests
make test

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
