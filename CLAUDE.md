# CLAUDE.md

## Project overview

zwemmr is a Python application that helps people find swimming pool opening hours and available time slots in Dutch cities, starting with Amsterdam.

## Tech stack

- **Python 3.12+** with **uv** for package and project management
- **ruff** for linting and formatting
- **ty** for type checking
- **pytest** for testing
- **pre-commit** for local git hooks

## Project structure

```
src/zwemmr/        # Main package (src layout)
tests/             # Test suite
data/              # Data files (xlsx)
.github/workflows/ # CI/CD
```

## Development commands

```bash
uv sync                              # Install all dependencies
uv run pytest                        # Run tests
uv run pytest --cov=zwemmr           # Run tests with coverage
uv run ruff check                    # Lint
uv run ruff check --fix              # Auto-fix lint issues
uv run ruff format                   # Format code
uv run ruff format --check           # Check formatting
uv run ty check                      # Type check
```

## Code conventions

- All functions and methods must have type annotations
- Immutable data structures preferred (frozen dataclasses, tuples)
- Domain terms use Dutch names where they match the source data (e.g., `baanzwemmen`)
- Never create unnecessary `__init__.py` files — Python 3.3+ namespace packages don't need them
- Tests use class-based grouping with descriptive method names
