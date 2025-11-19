# 🍏🥧 ApplePy
API for a model car shop

## Status
[![CI](https://github.com/daniel-samson/applepy/actions/workflows/ci.yaml/badge.svg)](https://github.com/daniel-samson/applepy/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/daniel-samson/applepy/graph/badge.svg?token=BI1vE1160e)](https://codecov.io/gh/daniel-samson/applepy)

## Requirements
- Python 3.6+
- [UV](https://github.com/astral-sh/uv)

## Implementations

This project explores different implementations:

- [flask](https://github.com/daniel-samson/applepy/tree/env-flask)
- [fast-api](https://github.com/daniel-samson/applepy/tree/env-api)

## Setup Development Environment

### Install UV

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
# or on Windows PowerShell:
# irm https://astral.sh/uv/install.ps1 | iex
```

### Virtual Environment

```sh
source .venv/bin/activate
uv sync
```
### Documentation

```sh
uv run mkdocs serve
```

## Run CLI

```sh
uv run applepy
```
