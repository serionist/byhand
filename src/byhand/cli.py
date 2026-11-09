"""The `byhand` command: this repo's own tool, which the gate and contributors run. A user never does."""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from byhand import refresh, render, signs


def _utf8() -> None:
    """Write UTF-8 whatever the platform: on Windows a pipe is cp1252, where a Hungarian or Chinese problem would raise
    UnicodeEncodeError."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def validate() -> int:
    catalogue, problems = signs.load()
    for problem in problems:
        print(problem)
    if problems:
        print(f"the catalogue has {len(problems)} problem(s)")
        return 1
    print(
        f"the catalogue is valid: {len(catalogue.languages)} languages, {len(catalogue.families)} model families, "
        f"{len(catalogue.sources)} sources, {len(catalogue.signs)} signs"
    )
    return 0


def render_signs(check: bool) -> int:
    """Write the plugin's sign files, or with `check` only say what differs. A catalogue with a problem, or files over
    a budget, write nothing."""
    catalogue, problems = signs.load()
    files = render.render(catalogue) if not problems else {}
    problems += render.budget_problems(files, catalogue)
    if not problems and check:
        problems = render.stale(files, render.OUT)
    for problem in problems:
        print(problem)
    if problems:
        print(f"the sign files have {len(problems)} problem(s)")
        return 1
    if not check:
        render.write(files, render.OUT)
    print(f"{len(files)} sign files {'match the catalogue' if check else 'written'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    _utf8()
    parser = argparse.ArgumentParser(prog="byhand", description="Check the catalogue and its sources; render it.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="check the catalogue: its schema, every sign's examples, its sources")
    write = commands.add_parser("render", help="write the catalogue as the plugin's sign files")
    write.add_argument("--check", action="store_true", help="write nothing; exit 1 when the files differ")
    sources = commands.add_parser("refresh", help="check the sources that are due; write an issue body per changed one")
    sources.add_argument("--out", type=Path, default=Path("refresh"), help="where the issue bodies go")
    download = commands.add_parser(
        "fetch", help="download sources' text now and its diff from read_at, to read by hand"
    )
    download.add_argument("ids", nargs="+", help="the sources' ids in sources.toml")
    download.add_argument("--out", type=Path, default=Path(".local/sources"), help="where <id>/ goes")
    args = parser.parse_args(argv)
    if args.command == "refresh":
        return refresh.run(args.out, dt.datetime.now(dt.UTC).date())
    if args.command == "fetch":
        return refresh.fetch(args.ids, args.out)
    return render_signs(args.check) if args.command == "render" else validate()


if __name__ == "__main__":
    sys.exit(main())
