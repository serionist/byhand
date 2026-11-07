"""Find sign text that shares a run of words with a downloaded source. Run by hand, with propose-signs.

Usage: uv run tools/copycheck.py [--sources <folder>] [--run <words>]

A sign is our own words and a citation, never a source's text (AGENTS.md, Traps), and that holds whatever the source's
licence. This searches each sign's `what`, `instead`, `flags`, `passes` and each term's `instead` for a run of 6 words
or more shared with any file under the folder, which is `.local/sources` unless named. A word is a word, and in Chinese,
Japanese and Thai, written without spaces, a character. In `flags`, a fixed string the sign's own check or terms find is
left out, the one thing a sign may share; a match longer than a run is no fixed string, and counts. Each hit prints both
texts; a person reads them. Exit 1 on any hit.

It reads downloads, which git ignores and CI doesn't have, so it isn't in the gate. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
import unicodedata
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SIGNS = ROOT / "src" / "byhand" / "catalogue" / "signs"
SOURCES = ROOT / ".local" / "sources"
RUN = 6
FIELDS = ("what", "instead", "flags", "passes")
TEXT = (".md", ".txt", ".json", ".yml", ".yaml", ".wikitext", ".toml", ".py", ".js", ".html", ".csv")
MAX_BYTES = 30_000_000
SKIP = ("human-baseline", ".git")  # the false-positive corpus is no source
# Han, Kana and Thai: a token a character, as these are written without spaces between words.
_CHARACTERS = "\u0e00-\u0e7f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
# A combining mark belongs to its word: Python's \w leaves out a Devanagari vowel sign, which would split a word.
_MARKS = "".join(re.escape(chr(c)) for c in range(0x300, 0x10000) if unicodedata.category(chr(c)) in ("Mn", "Mc"))
_WORD = re.compile(rf"[{_CHARACTERS}]|(?:[^\W_{_CHARACTERS}]|[{_MARKS}])+(?:'(?:[^\W_{_CHARACTERS}]|[{_MARKS}])+)?")
_FLAGS = re.IGNORECASE | re.MULTILINE


@dataclass(frozen=True)
class Field:
    """A piece of a sign's text: `pieces` is it with what the sign's check finds taken out."""

    sign: str
    key: str
    text: str
    pieces: tuple[str, ...]


@dataclass(frozen=True)
class Hit:
    sign: str
    key: str
    text: str
    path: str
    shared: str
    around: str


def words(text: str) -> list[str]:
    """Lower-case words: quotes, case and markup can't hide a shared run."""
    return _WORD.findall(unicodedata.normalize("NFKC", text).lower().replace(chr(0x2019), "'"))


def plain(text: str, suffix: str) -> str:
    """A source's text without wiki or HTML markup, which would split a run."""
    if suffix == ".wikitext":
        text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", text)
        text = re.sub(r"'{2,}", "", text)
        text = re.sub(r"\{\{(?:[^{}|]*\|)?([^{}]*)\}\}", r"\1", text)
    if suffix in (".wikitext", ".html"):
        text = re.sub(r"<[^>]+>", " ", text)
    return text


def pattern(row: dict[str, Any]) -> re.Pattern[str] | None:
    """What a sign's check or terms find, or None. A pattern that won't compile finds nothing: validate reports it."""
    terms = row.get("terms") or []
    text = row.get("check") or "|".join(f"(?:{term['term']})" for term in terms)
    if not text:
        return None
    try:
        return re.compile(unicodedata.normalize("NFC", text), _FLAGS)
    except re.error:
        return None


def fields(rows: Iterable[dict[str, Any]], run: int = RUN) -> list[Field]:
    """Each text of each sign. In `flags`, what the sign's own pattern finds is taken out when it is a run long at
    most: that is the fixed string a check needs. Elsewhere nothing is: `what` and `instead` hold no fixed string."""
    found = []
    for row in rows:
        own = pattern(row)
        texts = [(key, row[key]) for key in FIELDS if isinstance(row.get(key), str)]
        texts += [("terms", term["instead"]) for term in row.get("terms") or []]
        for key, text in texts:
            if own is not None and key == "flags":
                kept = own.sub(lambda match: "\0" if len(words(match.group())) <= run else match.group(), text)
                pieces = tuple(kept.split("\0"))
            else:
                pieces = (text,)
            found.append(Field(row["id"], key, text, pieces))
    return found


def load_signs(folder: Path = SIGNS) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(folder.glob("*.toml")):
        with path.open("rb") as f:
            rows += tomllib.load(f).get("sign", [])
    return rows


def source_files(folder: Path) -> Iterator[Path]:
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or set(path.relative_to(folder).parts) & set(SKIP):
            continue
        if path.suffix.lower() in TEXT and path.stat().st_size < MAX_BYTES:
            yield path


def hits(found: list[Field], documents: Iterable[tuple[str, str]], run: int = RUN) -> list[Hit]:
    """Each sign text sharing a run of `run` words with a document, once per sign, field and document."""
    wanted: dict[tuple[str, ...], list[Field]] = {}
    for field in found:
        for piece in field.pieces:
            tokens = words(piece)
            for i in range(len(tokens) - run + 1):
                wanted.setdefault(tuple(tokens[i : i + run]), []).append(field)
    seen = set()
    out = []
    for path, text in documents:
        tokens = words(text)
        for i in range(len(tokens) - run + 1):
            gram = tuple(tokens[i : i + run])
            for field in wanted.get(gram, ()):
                if (field.sign, field.key, field.text, path) not in seen:
                    seen.add((field.sign, field.key, field.text, path))
                    around = " ".join(tokens[max(i - 8, 0) : i + run + 8])
                    out.append(Hit(field.sign, field.key, field.text, path, " ".join(gram), around))
    return out


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Find sign text that shares a run of words with a downloaded source.")
    parser.add_argument("--sources", type=Path, default=SOURCES, help="the folder of downloads")
    parser.add_argument("--run", type=int, default=RUN, help=f"the shortest run that counts (default {RUN})")
    args = parser.parse_args(argv)
    if not args.sources.is_dir():
        print(f"{args.sources}: no such folder; download the sources there first")
        return 1
    paths = list(source_files(args.sources))
    documents = (
        (
            path.relative_to(args.sources).as_posix(),
            plain(path.read_text(encoding="utf-8", errors="ignore"), path.suffix),
        )
        for path in paths
    )
    found = fields(load_signs(), args.run)
    shared = hits(found, documents, args.run)
    for hit in shared:
        print(f"{hit.sign} {hit.key}: {hit.text!r}\n  {hit.path}: ...{hit.around}...\n  shared: {hit.shared}")
    print(f"{len(found)} sign texts against {len(paths)} files, runs of {args.run} words: {len(shared)} hit(s)")
    return 1 if shared else 0


if __name__ == "__main__":
    sys.exit(main())
