"""Write the catalogue as Markdown into the plugin: lean files `write` reads, check files `check` reads, and scan files
its `scan` agent reads.

The plugin's skills run no command: they read these files. A draft reads only what its kind of writing needs, a mail
or a message the short files, a post or a document the long ones too, a deck or a sheet the layout ones, so a hundred
languages cost a draft no more than one. `write`'s and `check`'s files hold no regex, only plain words: a pattern is
for Grep, which `check` runs through its `scan` agent from the scan files, each holding only its language's forms. The
signs only a deck or a sheet needs have check and scan files of their own, so a mail's check pays nothing for them.
Nothing is rendered that a skill doesn't act on, no citation and no example, and nothing here reads the clock, so a
file can't go stale overnight.
"""

from __future__ import annotations

import re
import re._parser as regex_parser  # pyright: ignore[reportMissingModuleSource]
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

from byhand import signs
from byhand.models import ModelRange
from byhand.signs import ANY, Catalogue, Sign

OUT = Path(__file__).resolve().parents[2] / "plugin" / "signs"
KB = 1024


@dataclass(frozen=True)
class Budgets:
    """The bytes each reader may take, set from the catalogue of 2026-11-08 with a margin, and only ever lowered.
    `check` and `scan` were set on 2026-11-09 (#71), once the shared signs' forms moved to each language's scan
    file: the largest read then, Japanese's check and English's scan, plus at least 512 bytes, rounded up to a whole
    KB."""

    mail: int = 14 * KB  # the short files a mail or a message reads, together
    document: int = 16 * KB  # the short and long files a post or a document reads, together
    layout: int = 16 * KB  # the layout files a deck or a sheet adds, together; and those a check or a scan of one adds
    check: int = 16 * KB  # the check files one check reads: `any`, a variant's base language, the language
    scan: int = 9 * KB  # the scan files `scan` reads for one check, from the same scopes


BUDGETS = Budgets()
MAX_LINES = 2000  # Claude Code's `Read` default: past it, a file is read only in part
# Not `<family>.md`: on Windows and macOS `claude.md` is a CLAUDE.md, which Claude Code loads as project instructions.
SHORT = ".short.md"
LONG = ".long.md"
LAYOUT = ".layout.md"
CHECK = "check.md"
SCAN = "scan.md"
# A layout-only sign's check and scan lines: only a check of a deck or a sheet reads them.
CHECK_LAYOUT = "check.layout.md"
SCAN_LAYOUT = "scan.layout.md"
SHORT_KINDS = ("email", "message")
LONG_KINDS = ("document", "post")
ELLIPSIS = "…"
_ORDER = {strength: n for n, strength in enumerate(signs.STRENGTHS)}
_SUFFIX = {"short": SHORT, "long": LONG, "layout": LAYOUT}


def is_layout(sign: Sign) -> bool:
    """A sign only a deck or a sheet needs: every message would pay for it otherwise."""
    return set(sign.kinds) <= set(signs.LAYOUT_KINDS)


def parts(sign: Sign) -> tuple[str, ...]:
    """Which files a sign goes to: `short` alone when a mail or a message reads it, as every draft reads the short
    files; else `long` when a post or a document does, and `layout` when a deck or a sheet does, both when both."""
    if ANY in sign.kinds or set(sign.kinds) & set(SHORT_KINDS):
        return ("short",)
    return tuple(
        where for where, kinds in (("long", LONG_KINDS), ("layout", signs.LAYOUT_KINDS)) if set(sign.kinds) & set(kinds)
    )


def _class(items: list[tuple[Any, Any]]) -> str:
    """A character class's word: its first literal, a space for `\\s`, else the ellipsis. A negated class's literals
    are what it excludes, so it prints the ellipsis."""
    if any(op.name == "NEGATE" for op, _value in items):
        return ELLIPSIS
    for op, value in items:
        if op.name == "LITERAL":
            return chr(value)
    if any(op.name == "CATEGORY" and value.name == "CATEGORY_SPACE" for op, value in items):
        return " "
    return ELLIPSIS


def _shortest(items: Iterable[tuple[Any, Any]]) -> str:
    """The shortest text a parsed pattern matches, with a required run of `\\w` or of a class as the ellipsis: a
    filler letter would read as part of the word ("aként" for `\\w+ként`)."""
    out: list[str] = []
    for op, value in items:
        name = op.name
        if name == "LITERAL":
            out.append(chr(value))
        elif name in ("NOT_LITERAL", "ANY"):
            out.append(ELLIPSIS)
        elif name == "IN":
            out.append(_class(value))
        elif name == "SUBPATTERN":
            out.append(_shortest(value[-1]))
        elif name == "BRANCH":
            # A word before an ellipsis: "delve" says more than "…".
            out.append(min((_shortest(branch) for branch in value[1]), key=lambda word: (ELLIPSIS in word, len(word))))
        elif name in ("MAX_REPEAT", "MIN_REPEAT"):
            low, high, inner = value
            word = _shortest(inner)
            if low:
                out.append(ELLIPSIS if ELLIPSIS in word else word * low)
            elif word == ELLIPSIS and high > 1 and out:
                out.append(ELLIPSIS)  # a stem's open end: "служ…", not "служ", which reads as a typo
            elif high == 1 and word and not any(char.isalpha() for char in word):
                out.append(word)  # an optional apostrophe or space prints: "today's", not "todays"; a word doesn't
        elif name != "AT":  # `\b`, `^` and `$` print nothing; `validate` refuses what else Grep can't run
            raise ValueError(f"no word for {name}")
    return re.sub(f"{ELLIPSIS}+", ELLIPSIS, "".join(out))


def alternatives(term: str) -> list[str]:
    """A term's top-level alternatives, split on its own text: Python's parser pulls a prefix the alternatives share
    out of them (`a b|a c` becomes `a (?:b|c)`), which would leave one word for two."""
    found, depth, start, index = [], 0, 0, 0
    while index < len(term):
        char = term[index]
        if char == "\\":
            index += 1
        elif char == "[":
            index = term.index("]", index + 2 if term[index + 1 : index + 2] in ("]", "^") else index + 1)
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "|" and depth == 0:
            found.append(term[start:index])
            start = index + 1
        index += 1
    return [*found, term[start:]]


def words(term: str) -> list[str]:
    """A term's plain words for `write`: one per top-level alternative, each the shortest text it matches."""
    return list(
        dict.fromkeys(_shortest(regex_parser.parse(alternative).data).strip() for alternative in alternatives(term))
    )


def _span(span: ModelRange) -> str:
    """A range as the model reads it: no `to` is every later version, and a `to` with no minor its whole series."""
    if span.to is None:
        return f"{span.family} {span.since} and later"
    return f"{span.family} {span.since} to {span.to}{'.x' if span.to.minor is None else ''}"


def _notes(sign: Sign, family: str | None) -> str:
    """What the brackets after a sign's id hold: its strength, its ranges in `family` or all of them, its kinds."""
    notes = [sign.strength]
    notes += [_span(span) for span in sign.models if family is None or span.family == family]
    if ANY not in sign.kinds:
        notes.append(", ".join(sign.kinds))
    return "; ".join(notes)


def _line(sign: Sign, family: str | None) -> str:
    """A sign as the model acts on it: its ranges in `family`, or all of them in a check file."""
    line = f"- {sign.id} ({_notes(sign, family)}): {sign.what} Instead: {sign.instead}"
    if sign.terms:
        line += " Words: " + "; ".join(f"{', '.join(words(term.term))}: {term.instead}" for term in sign.terms)
    return line


def _scan_line(sign: Sign, code: str) -> str:
    """A sign's form under `code`, after the same brackets as its check line, so `scan` keeps a sign by kind and family
    as `check` does."""
    return f"- {sign.id} ({_notes(sign, None)}): `{sign.forms[code]}`"


def _title(catalogue: Catalogue, language: str, family: str, what: str) -> str:
    who = catalogue.languages[language].name if language in catalogue.languages else "every language"
    model = catalogue.families[family].name if family in catalogue.families else "every model"
    return f"# Signs of AI writing: {who}, {model}, {what}"


def _rules(found: list[Sign]) -> list[str]:
    """The rules a reader of signs counts by: the weak cluster, and what a range holds."""
    lines = []
    if any(sign.strength == "weak" for sign in found):
        lines.append(
            f"A weak sign counts only with {signs.WEAK_CLUSTER} or more hits of weak signs in a paragraph or section, "
            "each a different word or phrase, even two from one sign: the same one repeated, a mark such as a dash, "
            "quotes or bold however often it appears and whatever words it holds, or one phrase two signs find, "
            "counts once."
        )
    if any(sign.models for sign in found):
        lines.append(
            "A sign holds for the versions it names: `5.x` is the whole 5 series, `and later` every newer one."
        )
    return lines


_SCAN_RULE = (
    "A pattern, in backticks after a sign's brackets, is what Grep runs on a file, case-insensitive and line by line."
)


def _file(title: str, found: list[Sign], line: Callable[[Sign], str], rules: list[str] | None = None) -> str:
    """A file of signs: its title, the rules its reader counts by (by default `_rules`'), then a line per sign."""
    rules = _rules(found) if rules is None else rules
    lines = [title, "", "Generated by `byhand render` from the catalogue; a change here is lost.", *rules, ""]
    lines += [line(sign) for sign in sorted(found, key=lambda sign: (_ORDER[sign.strength], sign.id))]
    return "\n".join(lines) + "\n"


_WHAT = {
    "short": "for every kind of writing",
    "long": "for posts and documents",
    "layout": "for decks and sheets",
    CHECK: "to check a text",
    CHECK_LAYOUT: "to check a deck or a sheet",
    SCAN: "to scan a file",
    SCAN_LAYOUT: "to scan a deck or a sheet",
}


def render(catalogue: Catalogue) -> dict[str, str]:
    """Each rendered file, by its path under plugin/signs. A sign with an `until` is retired and renders nowhere; a
    sign with ranges in two families renders in both, a sign of a document and a deck in the long and the layout file,
    and either once in its language's check file. Each of its forms renders once, in the scan file of the language it
    is under: an `any` sign's German form is read by a German scan only. A layout-only sign's check and scan lines go
    to `check.layout.md` and `scan.layout.md`, which only a check of a deck or a sheet reads."""
    groups: dict[tuple[str, str, str], list[Sign]] = {}
    checks: dict[tuple[str, str], list[Sign]] = {}
    scans: dict[tuple[str, str], list[Sign]] = {}
    for sign in catalogue.signs.values():
        if sign.until is not None:
            continue
        for where in parts(sign):
            for family in {span.family for span in sign.models} or {ANY}:
                groups.setdefault((sign.language, family, where), []).append(sign)
        layout = is_layout(sign)
        checks.setdefault((sign.language, CHECK_LAYOUT if layout else CHECK), []).append(sign)
        for code in sign.forms:
            scans.setdefault((code, SCAN_LAYOUT if layout else SCAN), []).append(sign)
    files = {
        f"{language}/{family}{_SUFFIX[where]}": _file(
            _title(catalogue, language, family, _WHAT[where]), found, partial(_line, family=family)
        )
        for (language, family, where), found in groups.items()
    }
    files |= {
        f"{language}/{name}": _file(_title(catalogue, language, ANY, _WHAT[name]), found, partial(_line, family=None))
        for (language, name), found in checks.items()
    }
    files |= {
        f"{code}/{name}": _file(
            _title(catalogue, code, ANY, _WHAT[name]), found, partial(_scan_line, code=code), [_SCAN_RULE]
        )
        for (code, name), found in scans.items()
    }
    return dict(sorted(files.items()))


def _scopes(catalogue: Catalogue, language: str) -> list[str]:
    """Where a text's signs come from: every language's, then its base language's if it is a variant, then its own."""
    entry = catalogue.languages.get(language)
    return list(dict.fromkeys([ANY, *([entry.of] if entry and entry.of else []), language]))


def draft_files(catalogue: Catalogue, language: str, family: str, kind: str) -> list[str]:
    """The files one draft reads, whether they exist or not: the short ones for every kind, the long ones too for a
    post or a document, the layout ones too for a deck or a sheet."""
    suffixes = (SHORT, LONG) if kind in LONG_KINDS else (SHORT, LAYOUT) if kind in signs.LAYOUT_KINDS else (SHORT,)
    return [
        f"{scope}/{name}{suffix}"
        for suffix in suffixes
        for scope in _scopes(catalogue, language)
        for name in dict.fromkeys((ANY, family))
    ]


def _reads(catalogue: Catalogue, language: str, kind: str, names: tuple[str, str]) -> list[str]:
    """Every scope's first file, then for a deck or a sheet every scope's second."""
    found = names if kind in signs.LAYOUT_KINDS else names[:1]
    return [f"{scope}/{name}" for name in found for scope in _scopes(catalogue, language)]


def check_files(catalogue: Catalogue, language: str, kind: str) -> list[str]:
    """The check files one check of `kind` reads, whether they exist or not: a deck's or a sheet's adds the layout
    ones."""
    return _reads(catalogue, language, kind, (CHECK, CHECK_LAYOUT))


def scan_files(catalogue: Catalogue, language: str, kind: str) -> list[str]:
    """The scan files `scan` reads for one check of `kind`, whether they exist or not: a deck's or a sheet's adds the
    layout ones."""
    return _reads(catalogue, language, kind, (SCAN, SCAN_LAYOUT))


def _bytes(files: dict[str, str], paths: Iterable[str]) -> int:
    return sum(len(files[path].encode("utf-8")) for path in paths if path in files)


def budget_problems(files: dict[str, str], catalogue: Catalogue, budgets: Budgets = BUDGETS) -> list[str]:
    """What overruns the budgets: a catalogue that grows past them fails here, before a user pays for it. Each set of
    files is named once: `any/any.short.md` alone over budget is one problem, not one per language and family."""
    problems = [
        f"{path}: {text.count(chr(10))} lines; a file stays under {MAX_LINES}, Claude Code's `Read` default"
        for path, text in files.items()
        if text.count("\n") >= MAX_LINES
    ]
    seen: set[tuple[str, frozenset[str]]] = set()

    def over(what: str, paths: Iterable[str], budget: int) -> None:
        found = frozenset(path for path in paths if path in files)
        size = _bytes(files, found)
        if size > budget and (what, found) not in seen:
            seen.add((what, found))
            problems.append(f"{what} reads {size} bytes, over its {budget}: {', '.join(sorted(found))}")

    def layout(paths: list[str]) -> list[str]:
        return [path for path in paths if path.endswith(LAYOUT)]

    # A deck reads a mail's short files, and its check and scan a mail's check and scan files: the `mail`, `check` and
    # `scan` budgets hold those, and `layout` the layout files each read adds.
    for language in catalogue.languages:
        for family in (ANY, *catalogue.families):
            over("a mail or a message", draft_files(catalogue, language, family, "email"), budgets.mail)
            over("a post or a document", draft_files(catalogue, language, family, "document"), budgets.document)
            over("a deck or a sheet", layout(draft_files(catalogue, language, family, "deck")), budgets.layout)
        over("a check", check_files(catalogue, language, "email"), budgets.check)
        over("a check of a deck or a sheet", layout(check_files(catalogue, language, "deck")), budgets.layout)
        over("a scan", scan_files(catalogue, language, "email"), budgets.scan)
        over("a scan of a deck or a sheet", layout(scan_files(catalogue, language, "deck")), budgets.layout)
    return problems


def stale(files: dict[str, str], out: Path) -> list[str]:
    """What differs between the rendered files and the folder: a file changed, missing, or left over."""
    found = {path.relative_to(out).as_posix() for path in out.rglob("*") if path.is_file()} if out.is_dir() else set()
    problems = [f"{path}: left over; `byhand render` removes it" for path in sorted(found - files.keys())]
    for path, text in sorted(files.items()):
        if path not in found:
            problems.append(f"{path}: missing; run `byhand render`")
        elif (out / path).read_bytes() != text.encode("utf-8"):
            problems.append(f"{path}: differs from the catalogue; run `byhand render`")
    return problems


def write(files: dict[str, str], out: Path) -> None:
    """Make the folder hold the rendered files and nothing else. Bytes, not text: LF on every platform."""
    if out.is_dir():
        for path in sorted(out.rglob("*"), reverse=True):
            if path.is_file() and path.relative_to(out).as_posix() not in files:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    for rel, text in files.items():
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
