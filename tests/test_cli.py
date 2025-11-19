from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from typing import Sequence

from applepy.cli import main


def run_cli(args: Sequence[str]) -> str:
    buf = StringIO()
    with redirect_stdout(buf):
        exit_code = main(args)
    assert exit_code == 0
    return buf.getvalue().strip()


def test_greet() -> None:
    output = run_cli(["greet", "Alice"])
    assert output == "Hello, Alice!"


def test_add() -> None:
    output = run_cli(["add", "1", "2"])
    assert output == "3"
