.PHONY: all env run docs uv sync test format lint check ci pre-commit
ARGS ?= --help

all: test

env:
	. .venv/bin/activate

run:
	uv run applepy $(ARGS)

docs:
	uv run mkdocs build

docs-serve:
	uv run mkdocs serve

uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

sync:
	uv sync

test:
	uv run pytest

format:
	uv run black src tests
	uv run ruff format src tests

lint:
	uv run mypy src tests
	uv run ruff check src tests

check:
	uv run mypy src tests
	uv run ruff check src tests

ci:
	uv run pytest
	uv run ruff check .
	uv run ruff format .
	uv run black .
	uv run mypy src tests

pre-commit:
	uv run pre-commit install
