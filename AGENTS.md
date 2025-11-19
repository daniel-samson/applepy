# Repository Guidelines

## Project Structure & Module Organization
Business logic lives under `src/applepy`, with `main.py` exposing simple helpers and `cli.py` providing the `applepy` CLI (run it via `uv run python -m applepy.cli ...`). The `tests/` folder mirrors the module layout (`tests/test_cli.py`, `tests/test_main.py`) to keep unit scope tight. Top-level configs (`pyproject.toml`, `pytest.ini`, `Makefile`) define tooling, while `docs/` and `mkdocs.yml` power the MkDocs site. Keep assets and fixtures close to the code that consumes them; prefer module-local directories over new top-level roots.

## Build, Test, and Development Commands
- `uv sync` – create/update the pinned `.venv` using `uv.lock`.
- `make test` – run `python -m pytest` with `pythonpath=src` for fast feedback.
- `make lint` / `make format` – invoke Ruff, Mypy, Black, and Isort with the repository defaults; avoid ad-hoc flags.
- `uv run python -m applepy.cli add 1 2` – example invocation of the CLI without manual activation.
- `make docs` or `uv run mkdocs serve` – build or preview the documentation site.

## Coding Style & Naming Conventions
Code targets Python 3.11 (see `pyproject.toml`). Use 4-space indentation, 88-character lines, and double quotes—Black and Ruff enforce these choices. Modules, packages, and filenames are lowercase_with_underscores; classes are `PascalCase`; functions and variables are `snake_case`. Keep functions small, type annotated (`mypy` runs in strict-ish mode), and prefer explicit imports sorted by Isort. Configuration should live in TOML/YAML rather than hard-coded constants when feasible.

## Testing Guidelines
Pytest is the sole test framework (`pytest -q` by default). Place new tests in `tests/` mirroring the module path (e.g., `tests/cli/test_new_command.py`). Name files `test_*.py` and functions `test_<behavior>` to keep auto-discovery simple. Use parametrization for edge cases instead of multiple similar tests. `pytest-cov` is available—run `uv run pytest --cov=src` for coverage before large changes. Avoid hitting real external services; mock or stub instead.

## Commit & Pull Request Guidelines
The existing history uses short, imperative summaries (“Initial commit”). Follow that style, keeping the first line ≤72 characters and referencing issues (`Fixes #123`) when relevant. Each pull request should describe motivation, implementation notes, and validation steps (commands run, new tests). Attach CLI output snippets or screenshots when UI/CLI behavior changes. Keep PRs focused; split refactors and feature work when possible to simplify reviews.
