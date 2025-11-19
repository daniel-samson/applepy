from __future__ import annotations

from applepy.cli import make_parser


def test_flask_command_exists() -> None:
    """Test that the flask command is registered."""
    parser = make_parser()
    args = parser.parse_args(["flask"])
    assert args.command == "flask"


def test_db_migrate_command_exists() -> None:
    """Test that the db:migrate command is registered."""
    parser = make_parser()
    args = parser.parse_args(["db:migrate"])
    assert args.command == "db:migrate"


def test_migration_create_command_exists() -> None:
    """Test that the migration:create command is registered."""
    parser = make_parser()
    args = parser.parse_args(["migration:create", "test migration"])
    assert args.command == "migration:create"
    assert args.message == "test migration"


def test_parser_requires_command() -> None:
    """Test that parser requires a command."""
    parser = make_parser()
    try:
        parser.parse_args([])
        raise AssertionError("Should have raised SystemExit")
    except SystemExit:
        # Expected behavior
        pass
