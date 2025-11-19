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


def test_run_command_db_migrate() -> None:
    """Test that db:migrate command executes."""
    from unittest.mock import patch

    from applepy.cli import run_command

    with patch("applepy.cli.subprocess.run") as mock_run:
        parser = make_parser()
        args = parser.parse_args(["db:migrate"])
        result = run_command(args)
        assert result == 0
        mock_run.assert_called_once_with(["alembic", "upgrade", "head"])


def test_run_command_migration_create() -> None:
    """Test that migration:create command executes."""
    from unittest.mock import patch

    from applepy.cli import run_command

    with patch("applepy.cli.subprocess.run") as mock_run:
        parser = make_parser()
        args = parser.parse_args(["migration:create", "add_new_table"])
        result = run_command(args)
        assert result == 0
        mock_run.assert_called_once_with(
            ["alembic", "revision", "--autogenerate", "-m", "add_new_table"]
        )


def test_run_command_unknown_command() -> None:
    """Test that unknown command raises RuntimeError."""
    import argparse

    from applepy.cli import run_command

    args = argparse.Namespace(command="unknown_command")
    try:
        run_command(args)
        raise AssertionError("Should have raised RuntimeError")
    except RuntimeError as e:
        assert "Unknown command" in str(e)


def test_run_command_flask() -> None:
    """Test that flask command executes."""
    from unittest.mock import patch

    from applepy.cli import run_command

    with patch("applepy.flask.app") as mock_flask_app:
        parser = make_parser()
        args = parser.parse_args(["flask"])
        result = run_command(args)
        assert result == 0
        mock_flask_app.run.assert_called_once()


def test_main_function() -> None:
    """Test main function with db:migrate command."""
    from unittest.mock import patch

    from applepy.cli import main

    with patch("applepy.cli.subprocess.run") as mock_run:
        result = main(["db:migrate"])
        assert result == 0
        mock_run.assert_called_once_with(["alembic", "upgrade", "head"])
