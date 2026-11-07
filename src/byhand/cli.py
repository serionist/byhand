"""The `byhand` command."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from byhand import models, render, signs


def _utf8() -> None:
    """Read and write UTF-8 whatever the platform: on Windows a pipe is cp1252, where Hungarian or Chinese text raises
    UnicodeEncodeError or comes through mangled."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
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


def read_model(model_id: str) -> int:
    catalogue = signs.Catalogue()
    problems = signs.load_families(signs.CATALOGUE, catalogue)
    if problems:
        print(*problems, sep="\n")
        return 1
    found = models.read_id(model_id, catalogue.families.values())
    if found is None:
        print(f"{signs.ANY}: no family the catalogue knows, so the {signs.ANY} signs alone")
    elif found.version is None:
        print(f"{found.family}: no version in the id")
    else:
        print(f"{found.family} {found.version}")
    return 0


def render_signs(out: Path, check: bool) -> int:
    """Write the plugin's sign files, or with `check` only say what differs. A catalogue with a problem, or files over
    the budget, write nothing."""
    catalogue, problems = signs.load()
    files = render.render(catalogue) if not problems else {}
    problems += render.budget_problems(files, catalogue)
    if not problems and check:
        problems = render.stale(files, out)
    for problem in problems:
        print(problem)
    if problems:
        print(f"the sign files have {len(problems)} problem(s)")
        return 1
    if not check:
        for path in render.write(files, out):
            print(f"{path}: not render's, so left alone")
    print(f"{len(files)} sign files {'match the catalogue' if check else f'written to {out.as_posix()}'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    _utf8()
    parser = argparse.ArgumentParser(prog="byhand", description="Write like a person, in your own voice and language.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="check the catalogue: its schema, every sign's examples, its sources")
    model = commands.add_parser("models", help="the family and version the catalogue reads from a model's id")
    model.add_argument("id", help="a model's id, such as claude-opus-5-5")
    write = commands.add_parser("render", help="write the catalogue as the plugin's sign files")
    write.add_argument("--check", action="store_true", help="write nothing; exit 1 when the files differ")
    write.add_argument("--out", type=Path, default=render.OUT, help=f"the folder (default {render.OUT.as_posix()})")
    args = parser.parse_args(argv)
    if args.command == "render":
        return render_signs(args.out, args.check)
    return validate() if args.command == "validate" else read_model(args.id)


if __name__ == "__main__":
    sys.exit(main())
