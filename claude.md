# Claude Code Guidelines for ApplePy

This document provides guidelines for Claude Code when working on the ApplePy project. It covers project structure, coding standards, testing requirements, and git workflows.

## Project Overview

**ApplePy** is a Python API for a model cars shop. It's a modern Python package with strict type checking, comprehensive testing, and automated code quality checks.

- **Version:** 0.1.0
- **Python Version:** >=3.10 (targets 3.11)
- **Package Entry Point:** `applepy = "applepy.cli:main"`
- **License:** MIT

## Project Structure

```
apple-py/
├── src/applepy/              # Main package source code
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Core business logic
│   └── cli.py               # CLI interface
├── tests/                    # Test suite
│   ├── test_main.py         # Unit tests for main module
│   └── test_cli.py          # CLI integration tests
├── docs/                     # Documentation
│   ├── index.md             # Main documentation
│   ├── api.md               # API reference
│   └── mkdocs.yml           # MkDocs configuration
├── Makefile                  # Development task automation
├── pyproject.toml           # Python project configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .github/workflow/ci.yaml # GitHub Actions CI
├── .gitignore               # Git ignore rules
└── README.md                # Project README
```

## Coding Standards

All code must adhere to strict standards enforced by automated tools running in CI/CD and pre-commit hooks.

### Code Formatting

**Tool:** Black & Ruff Format
- **Line Length:** 88 characters
- **Quote Style:** Double quotes (`"string"`)
- **Indentation:** 4 spaces
- **Python Version:** 3.11

**To Format Code:**
```bash
make format
```

This runs:
1. `black src tests` - Auto-format Python files
2. `ruff format src tests` - Additional formatting

### Linting

**Tool:** Ruff Linter
- **Enabled Rules:** E (errors), F (Pyflakes), I (isort), B (flake8-bugbear)
- **Line Length:** 88 characters

**To Lint Code:**
```bash
make lint
```

### Type Checking

**Tool:** MyPy (Strict Mode)
- **Python Version:** 3.11
- **Strict Settings:**
  - `disallow_untyped_defs = true` - All functions must have type hints
  - `disallow_incomplete_defs = true` - Complete type annotations required
  - `check_untyped_defs = true` - Check untyped function bodies
  - `no_implicit_optional = true` - No implicit Optional types
  - `strict_optional = true` - Strict Optional handling
  - `ignore_missing_imports = true` - Allow third-party imports without stubs

**To Type Check:**
```bash
make check
```

**Type Hints Requirements:**
- All function parameters must have explicit type annotations
- All function return types must be specified
- Use proper types from `typing` module when needed
- Example:
  ```python
  def add(a: int, b: int) -> int:
      """Add two integers and return the result."""
      return a + b
  ```

## Testing

All code changes must be covered by tests. The project uses **pytest** with coverage tracking.

### Test Structure

- **Test Location:** `tests/` directory
- **Test Pattern:** `test_*.py` files
- **Framework:** pytest
- **Coverage Tool:** pytest-cov

### Running Tests

```bash
make test
```

This runs `uv run pytest` with the following configuration:
- Python path: `src/` directory added automatically
- Output: Quiet mode (`-q`)

### Test Requirements

1. **All new functions must have tests** covering:
   - Happy path (normal usage)
   - Edge cases
   - Error conditions when applicable

2. **Test Naming Convention:**
   - Test files: `test_<module_name>.py`
   - Test functions: `test_<function_name>` or `test_<function_name>_<scenario>`
   - Descriptive test names for clarity

3. **Test Example:**
   ```python
   def test_add_positive_numbers():
       """Test adding two positive integers."""
       result = add(2, 3)
       assert result == 5

   def test_add_negative_numbers():
       """Test adding negative integers."""
       result = add(-2, -3)
       assert result == -5
   ```

4. **Coverage Expectations:**
   - Aim for high coverage of new code
   - Use `pytest-cov` for coverage reports

## Git Workflow

Follow a standard Git Flow for all changes.

### Branch Naming Convention

- **Main branch:** `main` - Production-ready code
- **Feature branches:** `feature/<issue-number>-<description>`
  - Example: `feature/1-add-checkout-flow`
- **Bugfix branches:** `fix/<issue-number>-<description>`
  - Example: `fix/5-handle-negative-prices`
- **Docs branches:** `docs/<description>`
  - Example: `docs/update-api-reference`

### Commit Message Format

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring without feature changes
- `test:` - Adding or updating tests
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `chore:` - Build, dependencies, tooling

**Example:**
```
#42 feat(cli): add product search command

Add a new search command to the CLI that allows users to search
for products by name and category.

Closes #42
```

**Issue References:**
- Reference issues using `Closes #<issue-number>` for closing issues
- Use `Relates to #<issue-number>` for related issues

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/<issue-number>-<description>
   ```

2. **Make Changes**
   - Write code following coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Quality Checks**
   ```bash
   make check    # Type checking and linting
   make format   # Format code
   make test     # Run tests
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat(scope): description

   Detailed explanation of changes.

   Closes #<issue-number>"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/<issue-number>-<description>
   ```

6. **CI/CD Checks**
   - GitHub Actions runs automatically on PR
   - All checks must pass:
     - Tests pass (`pytest`)
     - Linting passes (`ruff`)
     - Formatting passes (`ruff format`)
     - Type checking passes (`mypy`)

7. **Merge**
   - Merge to `main` only after CI passes
   - Use "Squash and merge" for clean history

## Pre-commit Hooks

Pre-commit hooks automatically run before each commit to catch issues early.

### Installed Hooks

- **Ruff Linter** - Syntax and style checking
- **Ruff Format** - Code formatting
- **Black** - Alternative code formatter
- **MyPy** - Type checking
- **Standard Hooks:**
  - Check for merge conflicts
  - Fix end of files
  - Trim trailing whitespace
  - Validate YAML

### Installing Hooks

```bash
make pre-commit
```

This installs all hooks defined in `.pre-commit-config.yaml`.

If a hook fails:
1. Review the error message
2. Fix the issues
3. Re-stage files if modified by hooks
4. Retry commit

## Development Workflow

### Starting Development

```bash
# Install dependencies
make sync

# Install pre-commit hooks
make pre-commit

# Run all checks to ensure environment is ready
make check
make test
```

### During Development

```bash
# Run tests frequently
make test

# Format code before committing
make format

# Check types and linting
make check

# Build documentation locally
make docs
```

### Before Pushing

```bash
# Run full CI suite
make ci
```

This runs:
1. Tests (`pytest`)
2. Linting (`ruff check .`)
3. Formatting validation (`ruff format . && black .`)
4. Type checking (`mypy src tests`)

## Documentation

Documentation is built with MkDocs and Material theme.

### Documentation Files

- **Main Docs:** `docs/index.md`
- **API Reference:** `docs/api.md`
- **Configuration:** `docs/mkdocs.yml`

### Building Documentation

```bash
make docs
```

Builds documentation to `site/` directory.

### Documentation Standards

- Document all public functions and classes
- Provide usage examples
- Keep API reference updated with new features
- Follow Markdown best practices

## CLI Development

The CLI is implemented in `src/applepy/cli.py` using Python's `argparse` module.

### Adding CLI Commands

1. Add command function to `cli.py`
2. Register command with argument parser
3. Add corresponding tests in `tests/test_cli.py`
4. Update CLI documentation

### Example:
```python
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

# In main():
parser.add_argument("command", choices=["greet", "add"])
parser.add_argument("args", nargs="*")

if args.command == "greet":
    print(greet(args.args[0]))
```

## Troubleshooting

### Type Checking Failures

If MyPy fails:
1. Add explicit type hints to function signatures
2. Use `typing` module for complex types
3. Run `mypy src tests` for detailed errors

### Formatting Issues

If formatting fails:
1. Run `make format` to auto-fix
2. Review changes
3. Commit formatted code

### Test Failures

If tests fail:
1. Run `make test` to see detailed output
2. Check test file names follow `test_*.py` pattern
3. Ensure test functions are named `test_*`
4. Verify test discovery in pytest configuration

### Pre-commit Hook Failures

If hooks fail:
1. Check error message from hook
2. Fix the issue
3. Some hooks auto-fix; re-stage if modified
4. Retry commit

## Tools and Commands Reference

### Available Make Commands

| Command | Purpose |
|---------|---------|
| `make all` | Run all tests (default target) |
| `make env` | Activate virtual environment |
| `make run` | Run CLI application |
| `make docs` | Build documentation |
| `make uv` | Install uv package manager |
| `make sync` | Install dependencies |
| `make test` | Run pytest |
| `make format` | Format code with Black and Ruff |
| `make lint` | Lint code with MyPy and Ruff |
| `make check` | Type check and lint (no formatting) |
| `make ci` | Run full CI suite |
| `make pre-commit` | Install pre-commit hooks |

### Package Manager

**uv** is used for dependency management:
- Install: `make uv`
- Sync dependencies: `make sync`
- Run commands: `uv run <command>`

### Key Files for Configuration

- `pyproject.toml` - Python project metadata and tool configuration
- `.pre-commit-config.yaml` - Pre-commit hook definitions
- `Makefile` - Development task automation
- `.github/workflow/ci.yaml` - GitHub Actions CI pipeline
- `pytest.ini` - Pytest configuration
- `.gitignore` - Git ignore patterns

## Questions and Support

For questions about project structure or guidelines:
1. Check this document first
2. Review project configuration files
3. Look at existing code examples
4. Check GitHub issues for context

## Updates to This Document

This document should be updated when:
- Coding standards change
- New tools are added
- Git workflow changes
- Major project structure changes
- New development practices are adopted

Keep this document in sync with actual project configuration and practices.
