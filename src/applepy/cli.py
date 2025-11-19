from __future__ import annotations

import argparse
import subprocess
from typing import Sequence


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="applypy-cli",
        description="An applepy CLI tool.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Sub-command to run",
    )

    # flask command
    subparsers.add_parser(
        "flask",
        help="Run as a Flask application.",
    )

    # db:migrate command
    subparsers.add_parser(
        "db:migrate",
        help="Run database migrations.",
    )

    # migration:create
    migration_create = subparsers.add_parser(
        "migration:create",
        help="Create a new migration.",
    )
    migration_create.add_argument(
        "message",
        help="Message for the migration.",
    )

    return parser


def run_command(args: argparse.Namespace) -> int:
    if args.command == "flask":
        from applepy.flask import app

        app.run()
        return 0

    if args.command == "db:migrate":
        # run alembic upgrade head
        subprocess.run(["alembic", "upgrade", "head"])
        return 0

    if args.command == "migration:create":
        message = args.message
        # run `alembic revision --autogenerate -m {message}``
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])

        return 0

    # This should not happen because parser requires a command
    raise RuntimeError(f"Unknown command: {args.command!r}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return run_command(args)


if __name__ == "__main__":
    raise SystemExit(main())
