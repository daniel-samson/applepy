from __future__ import annotations

import argparse
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

    # Example: greet command
    greet_parser = subparsers.add_parser(
        "greet",
        help="Greet someone by name.",
    )
    greet_parser.add_argument(
        "name",
        type=str,
        help="Name of the person to greet.",
    )

    # Example: add command
    add_parser = subparsers.add_parser(
        "add",
        help="Add two integers.",
    )
    add_parser.add_argument("a", type=int, help="First integer.")
    add_parser.add_argument("b", type=int, help="Second integer.")

    return parser


def run_command(args: argparse.Namespace) -> int:
    if args.command == "greet":
        print(f"Hello, {args.name}!")
        return 0

    if args.command == "add":
        result = args.a + args.b
        print(result)
        return 0

    # This should not happen because parser requires a command
    raise RuntimeError(f"Unknown command: {args.command!r}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return run_command(args)


if __name__ == "__main__":
    raise SystemExit(main())
