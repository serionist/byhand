"""The catalogue: read it from TOML, and say what is wrong with it.

`load` reads every file and collects each problem rather than stopping at the first, so `byhand validate` shows a
contributor all of theirs at once, and a bad value is a problem, never a traceback. An unknown key is a problem too: a
misspelt `untill` would otherwise retire nothing, and a misspelt `[[signs]]` would drop a whole file.
"""

from __future__ import annotations

import datetime
import functools
import re
import tomllib
import unicodedata
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from byhand.models import Family, ModelRange, parse_version

CATALOGUE = Path(__file__).parent / "catalogue"
ANY = "any"
LANGUAGE_COUNT = 100
# Hits of weak signs in a paragraph or section, each a different word or phrase: people do each of them too, and one
# habit repeated, however often, is a person's.
WEAK_CLUSTER = 3
KINDS = ("message", "email", "post", "document", "deck", "sheet")
LAYOUT_KINDS = ("deck", "sheet")
CATEGORIES = ("word", "phrase", "structure", "formatting", "layout", "artefact")
TERM_CATEGORIES = ("word", "phrase")
STRENGTHS = ("strong", "usual", "weak")
SOURCE_KINDS = ("wiki", "repo", "paper", "dataset", "vendor", "review")
DUE = ("daily", "weekly", "monthly", "quarterly", "by-hand")
# What each kind of feed needs for a script to read the source; `none` is a page a person reads.
FEEDS = {
    "mediawiki": ("site", "title"),
    "github": ("repo", "paths"),
    "arxiv": ("query",),
    "hf": ("dataset",),
    "none": (),
}
_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Most signs are about a line in a draft, so `^` and `$` match at each line. Part of the schema: a check is written
# against these flags.
_FLAGS = re.IGNORECASE | re.MULTILINE
# A check also runs through Claude Code's Grep, which is ripgrep: the Rust regex crate, not Python's re. A check uses
# only what both read alike, and `_python_only` refuses the rest, but for a word's letters and edges, which Python is
# given as Grep reads them (`as_grep`). Part of the schema.
#
# A pattern in the pieces where the two differ, and anything else one character at a time. A class is read as Python
# reads it: to its first `]` that isn't escaped or first in it.
_PIECE = re.compile(
    r"(?P<escape>\\b\{|\\.)"
    r"|(?P<set>\[\^?\]?(?:\\.|[^\]\\])*\]?)"
    r"|(?P<group>\(\?(?:[\w-]+[:)=<]?|<?.)?)"
    r"|(?P<count>\{[0-9,]*\}?\+?)"
    r"|(?P<possessive>[*+?]\+)"
    r"|.",
    re.DOTALL,
)
# The groups both read alike: `(?:`, a named group, and the flags i, m, s and u. Grep has no look-around, no
# backreference, no atomic group, no comment, and no flag a, L or x as Python has them (its x skips spaces in a class).
_SHARED_GROUP = re.compile(r"\(\?(?::|P<|(?:[imsu]+(?:-[ims]+)?|-[ims]+)[:)])")
# A count Grep reads, in ASCII digits as Python's is. Python reads `{,3}` as up to three, and a `{` that starts no count
# as itself; Grep refuses both.
_COUNT = re.compile(r"\{[0-9]+(?:,[0-9]*)?\}")
# Python reads these and Grep refuses them: `\Z`, `\N{...}`, a digit (a backreference or an octal), or reads them
# otherwise: `\<`, `\>` and `\b{...}` are a word's edges in Grep and text in Python. Grep also refuses an escaped
# character outside ASCII, such as `\—`, which Python reads as the character.
_PYTHON_ESCAPES = frozenset(("\\b{", *(f"\\{c}" for c in "ZN<>0123456789")))
# In a class, Grep reads a `[` as a class within it, and `&&`, `--` and `~~` as operations on two classes. It refuses
# `\b` there, which Python reads as a backspace. A `\W` there is refused too, but in a negated class: Python's would
# take in every mark, and only `[^\W...]`, a word character but those listed, has a reading for Python.
_CLASS_OPERATORS = ("[", "&&", "--", "~~")
# Grep's word characters that Python's `\w` leaves out: the combining marks (an Indic vowel sign, the nukta, Arabic
# tanween), every connector punctuation, not only `_`, and the joiners ZWNJ and ZWJ. Python's re has no `\p{M}`, so
# `_word_extra` lists them from `unicodedata`. Grep's `\w` also leaves out `No` (², ½) and takes a few `So` (Ⓐ): no
# sign has a term against them.
_WORD_CATEGORIES = ("Mn", "Mc", "Me", "Pc")
_JOINERS = (0x200C, 0x200D)

Table = dict[str, Any]


@dataclass(frozen=True)
class Language:
    code: str
    name: str
    native: str = ""
    rank: int = 0  # 0 for a script variant, which `of` ties to its base language
    of: str = ""
    spaces: bool = True  # False for a language written without spaces between words


@dataclass(frozen=True)
class Source:
    id: str
    languages: tuple[str, ...]


@dataclass(frozen=True)
class Term:
    term: str
    instead: str


@dataclass(frozen=True)
class Sign:
    id: str
    language: str
    category: str
    kinds: tuple[str, ...]
    models: tuple[ModelRange, ...]  # empty for a sign of every model
    what: str
    instead: str
    strength: str
    flags: str
    passes: str
    pattern: re.Pattern[str] | None  # None for a sign only the model's own read can find; else `grep`, read as Grep
    grep: str = ""  # the pattern as written, in NFC: what Grep runs, and what a check file prints
    terms: tuple[Term, ...] = ()
    until: datetime.date | None = None  # set, the sign is retired: it keeps its id and renders nowhere


@dataclass
class Catalogue:
    languages: dict[str, Language] = field(default_factory=dict)
    families: dict[str, Family] = field(default_factory=dict)
    sources: dict[str, Source] = field(default_factory=dict)
    signs: dict[str, Sign] = field(default_factory=dict)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _read(path: Path, problems: list[str]) -> Table:
    try:
        with path.open("rb") as f:
            return tomllib.load(f)
    except OSError as exc:
        problems.append(f"{path.name}: {exc.strerror or exc}")
    except UnicodeDecodeError:
        problems.append(f"{path.name}: not UTF-8; save it as UTF-8")
    except tomllib.TOMLDecodeError as exc:
        problems.append(f"{path.name}: not valid TOML: {exc}")
    return {}


def _keys(where: str, table: Table, required: tuple[str, ...], optional: tuple[str, ...] = ()) -> list[str]:
    missing = [f"{where}: `{key}` is missing" for key in required if key not in table]
    unknown = [f"{where}: unknown key `{key}`" for key in table if key not in (*required, *optional)]
    return missing + unknown


def _rows(file: str, data: Table, key: str, problems: list[str]) -> list[Table]:
    """The tables of `[[key]]`. A `[key]` is a table, not a list of them, and a row that isn't a table is no row."""
    rows = data.get(key, [])
    if not isinstance(rows, list):
        problems.append(f"{file}: `{key}` must be [[{key}]], a list of tables")
        return []
    tables = [row for row in rows if isinstance(row, dict)]
    if len(tables) != len(rows):
        problems.append(f"{file}: every `{key}` must be a table")
    return tables


def _id(file: str, row: Table, problems: list[str], key: str = "id") -> str:
    value = row.get(key, "?")
    if isinstance(value, str):
        return value
    problems.append(f"{file}: `{key}` must be text, not {value!r}")
    return "?"


def _text(where: str, table: Table, key: str) -> list[str]:
    value = table.get(key)
    return [] if isinstance(value, str) and value.strip() else [f"{where}: `{key}` must be text"]


def _one_of(where: str, value: object, allowed: tuple[str, ...], key: str) -> list[str]:
    return [] if value in allowed else [f"{where}: `{key}` is {value!r}; it must be one of {', '.join(allowed)}"]


def _is_date(value: object) -> bool:
    """A date and only a date: TOML's datetime is a subclass, and comparing the two raises."""
    return isinstance(value, datetime.date) and not isinstance(value, datetime.datetime)


def _python_escape(piece: str) -> bool:
    return piece in _PYTHON_ESCAPES or not piece[1:].isascii()


def _python_set(piece: str) -> bool:
    escapes = re.findall(r"\\.", piece)
    # An escape stands as one plain character, so `[-\d-]` doesn't read as `--`.
    rest = re.sub(r"\\.", "e", piece[1:])
    refused = (r"\b",) if piece.startswith("[^") else (r"\b", r"\W")
    return any(_python_escape(escape) or escape in refused for escape in escapes) or any(
        op in rest for op in _CLASS_OPERATORS
    )


_PYTHON_ONLY = {
    "escape": _python_escape,
    "set": _python_set,
    "group": lambda piece: not _SHARED_GROUP.fullmatch(piece),
    "count": lambda piece: not _COUNT.fullmatch(piece),
    "possessive": lambda _: True,
}


def _python_only(pattern: str) -> str | None:
    """The first piece of a pattern that Python's re reads and Grep refuses or reads otherwise, or None."""
    for match in _PIECE.finditer(pattern):
        if match.lastgroup and _PYTHON_ONLY[match.lastgroup](match.group()):
            return match.group()
    return None


@functools.cache
def _word_extra() -> str:
    """The ranges, inside a class beside `\\w`, of Grep's word characters that Python's leaves out. Each is the
    character itself: none of them is one a class reads as syntax (`[`, `]`, `\\`, `^`, `-`, `&`, `~` or `|`). Found
    once, from every code point."""
    found = [n for n in range(0x110000) if unicodedata.category(chr(n)) in _WORD_CATEGORIES or n in _JOINERS]
    ranges: list[list[int]] = []
    for n in found:
        if ranges and ranges[-1][1] == n - 1:
            ranges[-1][1] = n
        else:
            ranges.append([n, n])
    return "".join(chr(low) if low == high else f"{chr(low)}-{chr(high)}" for low, high in ranges)


@functools.cache
def _as_grep_escapes() -> dict[str, str]:
    """What Python is given for each escape it reads otherwise than Grep. Its `\\b` is look-around, which Grep refuses:
    only Python ever compiles it, and the check files print the pattern as written."""
    word = rf"[\w{_word_extra()}]"
    return {
        r"\w": word,
        r"\W": rf"[^\w{_word_extra()}]",
        r"\b": rf"(?:(?<!{word})(?={word})|(?<={word})(?!{word}))",
        r"\B": rf"(?:(?<={word})(?={word})|(?<!{word})(?!{word}))",
    }


def _in_class(escape: re.Match[str]) -> str:
    return {r"\w": rf"\w{_word_extra()}", r"\W": ""}.get(escape.group(), escape.group())


def _as_grep_class(piece: str) -> str:
    """A class as Grep reads it. A `\\W` stands only in a negated class, as `_python_set` holds: `[^\\W\\d_]` is a
    word character but a digit or `_`, which Python reads as one that the class without its `\\W` lets through."""
    read = re.sub(r"\\.", _in_class, piece)
    if r"\W" not in re.findall(r"\\.", piece):
        return read
    word = _as_grep_escapes()[r"\w"]
    return word if read == "[^]" else f"(?:(?={word}){read})"


def as_grep(pattern: str) -> re.Pattern[str]:
    """A pattern Grep runs, compiled for Python to read as Grep does: in NFC, with the schema's flags, and with `\\w`,
    `\\W`, `\\b` and `\\B` taking marks and joiners as word characters wherever they stand, a class included.
    `validate` and the tests search with this, on patterns `validate` passes."""
    pieces = []
    for match in _PIECE.finditer(_nfc(pattern)):
        piece = match.group()
        if match.lastgroup == "escape":
            piece = _as_grep_escapes().get(piece, piece)
        elif match.lastgroup == "set":
            piece = _as_grep_class(piece)
        pieces.append(piece)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)  # as in `_checked`: a class such as `[a||b]` is no problem
        return re.compile("".join(pieces), _FLAGS)


def _checked(where: str, pattern: str) -> tuple[str | None, list[str]]:
    """The pattern in NFC, as Grep gets it, or None and why not. Python first: what it can't read is its error, not
    Grep's. Its warning on a class such as `[[` goes unshown, as `_python_only` refuses that class with a problem of its
    own."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            re.compile(_nfc(pattern), _FLAGS)
    except re.error as exc:
        return None, [f"{where}: not a regular expression: {exc}"]
    if piece := _python_only(pattern):
        return None, [f"{where}: Grep can't run `{piece}` as Python's re does: {pattern}"]
    return _nfc(pattern), []


def load_languages(root: Path, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    file = "languages.toml"
    data = _read(root / file, problems)
    problems += _keys(file, data, (), ("language", "variant"))
    bases = _rows(file, data, "language", problems)
    for row in bases:
        code = _id(file, row, problems, "code")
        where = f"{file}: {code}"
        problems += _keys(where, row, ("code", "name", "rank"), ("native", "speakers_millions", "spaces"))
        problems += _language_problems(where, row, catalogue)
        native = row.get("native", "")
        catalogue.languages[code] = Language(
            code, str(row.get("name", "")), str(native), _rank(row), spaces=row.get("spaces") is not False
        )
    if len(bases) != LANGUAGE_COUNT:
        problems.append(f"{file}: {len(bases)} languages; the catalogue holds {LANGUAGE_COUNT}")
    if sorted(_rank(row) for row in bases) != list(range(1, len(bases) + 1)):
        problems.append(f"{file}: the ranks must run from 1 with no gap")
    for row in _rows(file, data, "variant", problems):
        code = _id(file, row, problems, "code")
        where = f"{file}: {code}"
        problems += _keys(where, row, ("code", "name", "of"), ("spaces",))
        problems += _language_problems(where, row, catalogue)
        of = row.get("of")
        if not isinstance(of, str) or of not in catalogue.languages:
            problems.append(f"{where}: `of` names no language")
        catalogue.languages[code] = Language(
            code, str(row.get("name", "")), of=str(of), spaces=row.get("spaces") is not False
        )
    return problems


def _rank(row: Table) -> int:
    rank = row.get("rank")
    return rank if isinstance(rank, int) else 0


def _language_problems(where: str, row: Table, catalogue: Catalogue) -> list[str]:
    problems = _text(where, row, "name")
    if row.get("code") in catalogue.languages:
        problems.append(f"{where}: repeated")
    if "spaces" in row and not isinstance(row["spaces"], bool):
        problems.append(f"{where}: `spaces` must be true or false")
    return problems


def load_families(root: Path, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    file = "models.toml"
    data = _read(root / file, problems)
    problems += _keys(file, data, (), ("family",))
    for row in _rows(file, data, "family", problems):
        family = _id(file, row, problems)
        where = f"{file}: {family}"
        problems += _keys(where, row, ("id", "name")) + _text(where, row, "name")
        if family in catalogue.families:
            problems.append(f"{where}: repeated")
        if not _SLUG.match(family):
            problems.append(f"{where}: an id takes lowercase letters, digits and hyphens: it names a file")
        catalogue.families[family] = Family(family, str(row.get("name", "")))
    return problems


def _feed_problems(where: str, feed: object) -> list[str]:
    if not isinstance(feed, dict):
        return [f"{where}: `feed` must be a table"]
    api = feed.get("api")
    wrong = _one_of(where, api, tuple(FEEDS), "feed.api")
    return wrong or _keys(f"{where}: feed", feed, ("api", *FEEDS[str(api)]))


def _read_at_problems(where: str, read_at: object, api: object) -> list[str]:
    """When a source was last read: the refresh diffs from here, so a source that yielded no sign has one too. A page
    with no feed has only its date."""
    if not isinstance(read_at, dict):
        return [f"{where}: `read_at` must be a table"]
    problems = _keys(f"{where}: read_at", read_at, ("date",), ("revision", "commit"))
    if not _is_date(read_at.get("date")):
        problems.append(f"{where}: `read_at.date` must be a date")
    if api != "none" and not ({"revision", "commit"} & read_at.keys()):
        problems.append(f"{where}: `read_at` needs the `revision` or `commit` last read")
    return problems


def load_sources(root: Path, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    file = "sources.toml"
    data = _read(root / file, problems)
    problems += _keys(file, data, (), ("source",))
    for row in _rows(file, data, "source", problems):
        source = _id(file, row, problems)
        where = f"{file}: {source}"
        problems += _keys(where, row, ("id", "url", "kind", "languages", "licence", "due", "feed", "read_at"))
        if source in catalogue.sources:
            problems.append(f"{where}: repeated")
        problems += _one_of(where, row.get("kind"), SOURCE_KINDS, "kind")
        problems += _one_of(where, row.get("due"), DUE, "due")
        problems += _text(where, row, "url") + _text(where, row, "licence")
        languages = row.get("languages", ())
        if not isinstance(languages, list) or not languages:
            problems.append(f"{where}: `languages` must list the languages it covers")
            languages = []
        problems += [f"{where}: the language {c!r} isn't one" for c in languages if c not in catalogue.languages]
        if "feed" in row and "read_at" in row:
            feed = row["feed"]
            problems += _feed_problems(where, feed)
            problems += _read_at_problems(where, row["read_at"], feed.get("api") if isinstance(feed, dict) else None)
        catalogue.sources[source] = Source(source, tuple(languages))
    return problems


def _kinds_problems(where: str, row: Table) -> list[str]:
    kinds = row.get("kinds")
    if not isinstance(kinds, list) or not kinds:
        return [f"{where}: `kinds` must list {ANY} or the kinds of writing"]
    problems = [problem for kind in kinds for problem in _one_of(where, kind, (*KINDS, ANY), "kinds")]
    if problems:
        return problems
    if len(set(kinds)) != len(kinds):
        problems.append(f"{where}: `kinds` repeats a kind")
    if ANY in kinds and len(kinds) > 1:
        problems.append(f"{where}: `kinds` is {ANY} or a list of kinds, not both")
    if row.get("category") == "layout" and not set(kinds) <= set(LAYOUT_KINDS):
        problems.append(f"{where}: a layout sign is for {' and '.join(LAYOUT_KINDS)}: only they read the layout files")
    return problems


def _range(where: str, row: object, catalogue: Catalogue) -> tuple[ModelRange | None, list[str]]:
    if not isinstance(row, dict):
        return None, [f"{where}: a `models` range must be a table"]
    problems = _keys(f"{where}: models", row, ("family", "from"), ("to",))
    family = row.get("family")
    if not isinstance(family, str) or family not in catalogue.families:
        problems.append(f"{where}: `models` names no family {family!r}")
    # Written as text: TOML reads a bare 4.10 as the number 4.1.
    written = {key: row[key] for key in ("from", "to") if key in row}
    versions = {key: parse_version(value) if isinstance(value, str) else None for key, value in written.items()}
    problems += [
        f'{where}: `{key}` must be a version in quotes, such as "4.6"'
        for key, value in versions.items()
        if value is None
    ]
    since = versions.get("from")
    if problems or since is None:
        return None, problems
    span = ModelRange(str(family), since, versions.get("to"))
    if not span.holds(since):
        return None, [f"{where}: `to` {span.to} comes before `from` {since}"]
    return span, []


def _models(where: str, models: object, catalogue: Catalogue) -> tuple[tuple[ModelRange, ...], list[str]]:
    if models == ANY:
        return (), []
    if not isinstance(models, list) or not models:
        return (), [f"{where}: `models` must be {ANY!r} or a list of ranges"]
    ranges, problems = [], []
    for row in models:
        found, wrong = _range(where, row, catalogue)
        problems += wrong
        if found:
            ranges.append(found)
    return tuple(ranges), problems


def _terms(where: str, row: Table, language: str, spaces: bool) -> tuple[str | None, list[str]]:
    """The one pattern a sign's terms make. In a language written with spaces a term stands as a word of its own, so
    `delve` doesn't match inside another word; in one written without, there is no such edge to look for. An `any` sign
    has no one edge, so it writes its own `check`."""
    terms = row.get("terms")
    if terms is None:
        return None, []
    if row.get("category") not in TERM_CATEGORIES:
        return None, [f"{where}: only a {' or '.join(TERM_CATEGORIES)} sign holds `terms`"]
    if language == ANY:
        return None, [f"{where}: an {ANY} sign writes its `check`: a word's edge differs between languages"]
    if not isinstance(terms, list) or not terms:
        return None, [f"{where}: `terms` must list {{ term, instead }}"]
    if not all(isinstance(term, dict) for term in terms):
        return None, [f"{where}: every term must be a table"]
    problems = []
    for term in terms:
        problems += _keys(f"{where}: terms", term, ("term", "instead"))
        problems += _text(f"{where}: terms", term, "term") + _text(f"{where}: terms", term, "instead")
    if problems:
        return None, sorted(set(problems))
    body = "|".join(f"(?:{term['term']})" for term in terms)
    return _checked(where, rf"\b(?:{body})\b" if spaces else body)


def _pattern(where: str, row: Table, language: str, spaces: bool) -> tuple[str | None, list[str]]:
    """A sign's own `check`, which wins over its terms: it is how a term that can't stand alone is matched."""
    built, problems = _terms(where, row, language, spaces)
    category = row.get("category")
    if "check" not in row:
        if category in TERM_CATEGORIES and "terms" not in row:
            problems = [*problems, f"{where}: a {category} sign needs `terms` or a `check`"]
        if category == "artefact":
            problems = [*problems, f"{where}: an artefact sign needs a `check`: it is a string a script can find"]
        return built, problems
    if not isinstance(row["check"], str):
        return None, [*problems, f"{where}: `check` must be text"]
    own, wrong = _checked(where, row["check"])
    return own, problems + wrong


def _examples(where: str, row: Table, pattern: re.Pattern[str] | None) -> list[str]:
    """Both texts present and different; with a pattern, it finds the first and not the second. Without one, CI can't
    prove the sign: only the model's own read can, in the eval suite."""
    problems = _text(where, row, "flags") + _text(where, row, "passes")
    if problems:
        return problems
    flags, passes = _nfc(row["flags"]), _nfc(row["passes"])
    if flags == passes:
        return [f"{where}: `flags` and `passes` must differ"]
    if pattern is None:
        return []
    if not pattern.search(flags):
        problems.append(f"{where}: its check doesn't find `flags`")
    if pattern.search(passes):
        problems.append(f"{where}: its check finds `passes`, a human text")
    return problems


def _citation(where: str, entry: object, catalogue: Catalogue) -> list[str]:
    if not isinstance(entry, dict):
        return [f"{where}: every entry of `sources` must be a table"]
    problems = _keys(f"{where}: sources", entry, ("source", "where", "seen")) + _text(where, entry, "where")
    source = entry.get("source")
    if not isinstance(source, str) or source not in catalogue.sources:
        problems.append(f"{where}: cites no source {source!r}")
    if not _is_date(entry.get("seen")):
        problems.append(f"{where}: `seen` must be a date")
    return problems


def _sign_sources(where: str, row: Table, language: str, catalogue: Catalogue) -> list[str]:
    """Each citation, and what the citations cover: a sign comes from sources in its own language, so English's signs
    aren't carried over into another, and an `any` sign from at least two (AGENTS.md, Traps). An artefact with a `check`
    needs one: a tool's string looks the same in every language."""
    cited = row.get("sources")
    if not isinstance(cited, list) or not cited:
        return [f"{where}: `sources` must cite at least one"]
    problems = [problem for entry in cited for problem in _citation(where, entry, catalogue)]
    if problems:
        return problems
    covered = {code for entry in cited for code in catalogue.sources[entry["source"]].languages}
    if language == ANY:
        if len(covered) < 2 and not (row.get("category") == "artefact" and "check" in row):
            problems.append(f"{where}: an {ANY} sign needs sources in at least two languages (AGENTS.md, Traps)")
        return problems
    entry = catalogue.languages.get(language)
    if not ({language, entry.of if entry else ""} & covered):
        problems.append(f"{where}: no source it cites covers {language} (AGENTS.md, Traps)")
    return problems


def _dates(where: str, row: Table) -> list[str]:
    until = row.get("until")
    if until is None:
        return []
    if row.get("models") != ANY:
        return [f"{where}: a model-scoped sign retires by its range's `to`, not by a date"]
    return [] if _is_date(until) else [f"{where}: `until` must be a date"]


def _term_list(row: Table) -> tuple[Term, ...]:
    terms = row.get("terms")
    if not isinstance(terms, list):
        return ()
    return tuple(
        Term(term["term"], term["instead"])
        for term in terms
        if isinstance(term, dict) and isinstance(term.get("term"), str) and isinstance(term.get("instead"), str)
    )


def _sign(language: str, row: Table, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    sign = _id(f"signs/{language}.toml", row, problems)
    where = f"signs/{language}.toml: {sign}"
    required = ("id", "category", "kinds", "models", "what", "instead", "strength", "flags", "passes", "sources")
    problems += _keys(where, row, required, ("terms", "check", "until"))
    slug = sign.removeprefix(f"{language}-")
    if slug == sign or not _SLUG.match(slug):
        problems.append(f"{where}: an id is {language}-<slug>, in lowercase letters, digits and hyphens")
    if sign in catalogue.signs:
        problems.append(f"{where}: repeated")
    problems += _one_of(where, row.get("category"), CATEGORIES, "category")
    problems += _one_of(where, row.get("strength"), STRENGTHS, "strength")
    problems += _kinds_problems(where, row)
    problems += _text(where, row, "what") + _text(where, row, "instead")
    models, wrong = _models(where, row.get("models"), catalogue)
    entry = catalogue.languages.get(language)
    grep, wrong_pattern = _pattern(where, row, language, entry.spaces if entry else True)
    pattern = None if grep is None else as_grep(grep)
    problems += wrong + wrong_pattern + _examples(where, row, pattern)
    problems += _sign_sources(where, row, language, catalogue) + _dates(where, row)
    kinds = row.get("kinds")
    catalogue.signs[sign] = Sign(
        sign,
        language,
        str(row.get("category", "")),
        tuple(kinds) if isinstance(kinds, list) else (),
        models,
        str(row.get("what", "")),
        str(row.get("instead", "")),
        str(row.get("strength", "")),
        str(row.get("flags", "")),
        str(row.get("passes", "")),
        pattern,
        grep or "",
        _term_list(row),
        row.get("until") if _is_date(row.get("until")) else None,
    )
    return problems


def load_signs(root: Path, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    for path in sorted((root / "signs").glob("*.toml")):
        language = path.stem
        file = f"signs/{path.name}"
        if language != ANY and language not in catalogue.languages:
            problems.append(f"{file}: the file's name is no language")
        data = _read(path, problems)
        problems += _keys(file, data, (), ("sign",))
        for row in _rows(file, data, "sign", problems):
            problems += _sign(language, row, catalogue)
    return problems


def load(root: Path = CATALOGUE) -> tuple[Catalogue, list[str]]:
    """The catalogue under root, and what is wrong with it. Languages and families come first: sources and signs name
    them."""
    catalogue = Catalogue()
    problems = load_languages(root, catalogue) + load_families(root, catalogue)
    problems += load_sources(root, catalogue)
    problems += load_signs(root, catalogue)
    return catalogue, problems
