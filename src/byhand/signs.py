"""The catalogue: read it from TOML, and say what is wrong with it.

`load` reads every file and collects each problem rather than stopping at the first, so `byhand validate` shows a
contributor all of theirs at once. An unknown key is a problem too: a misspelt `untill` would otherwise retire nothing.
"""

from __future__ import annotations

import datetime
import re
import tomllib
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from byhand.models import Version, parse_version

CATALOGUE = Path(__file__).parent / "catalogue"
ANY = "any"
LANGUAGE_COUNT = 100
KINDS = ("message", "email", "post", "document", "deck", "sheet")
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
_FLAGS = re.IGNORECASE

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
class Family:
    id: str
    name: str
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class Source:
    id: str
    languages: tuple[str, ...]


@dataclass(frozen=True)
class ModelRange:
    family: str
    since: Version
    to: Version | None = None  # None holds every later version, so a newer model is covered


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
    pattern: re.Pattern[str] | None  # None for a sign only the model's own read can find


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
    except tomllib.TOMLDecodeError as exc:
        problems.append(f"{path.name}: not valid TOML: {exc}")
    return {}


def _keys(where: str, table: Table, required: tuple[str, ...], optional: tuple[str, ...] = ()) -> list[str]:
    missing = [f"{where}: `{key}` is missing" for key in required if key not in table]
    unknown = [f"{where}: unknown key `{key}`" for key in table if key not in (*required, *optional)]
    return missing + unknown


def _text(where: str, table: Table, key: str) -> list[str]:
    value = table.get(key)
    return [] if isinstance(value, str) and value.strip() else [f"{where}: `{key}` must be text"]


def _one_of(where: str, value: object, allowed: tuple[str, ...], key: str) -> list[str]:
    return [] if value in allowed else [f"{where}: `{key}` is {value!r}; it must be one of {', '.join(allowed)}"]


def _compile(where: str, pattern: str) -> tuple[re.Pattern[str] | None, list[str]]:
    try:
        return re.compile(_nfc(pattern), _FLAGS), []
    except re.error as exc:
        return None, [f"{where}: not a regular expression: {exc}"]


def load_languages(root: Path, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    data = _read(root / "languages.toml", problems)
    bases = data.get("language", [])
    for row in bases:
        code = row.get("code", "?")
        where = f"languages.toml: {code}"
        problems += _keys(where, row, ("code", "name", "rank"), ("native", "speakers_millions", "spaces"))
        if code in catalogue.languages:
            problems.append(f"{where}: repeated")
        catalogue.languages[code] = Language(
            code, row.get("name", ""), row.get("native", ""), row.get("rank", 0), spaces=row.get("spaces", True)
        )
    if len(bases) != LANGUAGE_COUNT:
        problems.append(f"languages.toml: {len(bases)} languages; the catalogue holds {LANGUAGE_COUNT}")
    if sorted(row.get("rank", 0) for row in bases) != list(range(1, len(bases) + 1)):
        problems.append("languages.toml: the ranks must run from 1 with no gap")
    for row in data.get("variant", []):
        code = row.get("code", "?")
        where = f"languages.toml: {code}"
        problems += _keys(where, row, ("code", "name", "of"), ("spaces",))
        if row.get("of") not in catalogue.languages:
            problems.append(f"{where}: `of` names no language")
        catalogue.languages[code] = Language(
            code, row.get("name", ""), of=row.get("of", ""), spaces=row.get("spaces", True)
        )
    return problems


def load_families(root: Path, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    for row in _read(root / "models.toml", problems).get("family", []):
        family = row.get("id", "?")
        where = f"models.toml: {family}"
        problems += _keys(where, row, ("id", "name", "patterns"))
        if family in catalogue.families:
            problems.append(f"{where}: repeated")
        if not _SLUG.match(family):
            problems.append(f"{where}: an id takes lowercase letters, digits and hyphens: it names a file")
        catalogue.families[family] = Family(family, row.get("name", ""), tuple(row.get("patterns", ())))
    return problems


def _feed_problems(where: str, feed: object) -> list[str]:
    if not isinstance(feed, dict):
        return [f"{where}: `feed` must be a table"]
    api = feed.get("api")
    if api not in FEEDS:
        return [f"{where}: `feed.api` is {api!r}; it must be one of {', '.join(FEEDS)}"]
    return _keys(f"{where}: feed", feed, ("api", *FEEDS[api]))


def _read_at_problems(where: str, read_at: object, api: object) -> list[str]:
    """When a source was last read: the refresh diffs from here, so a source that yielded no sign has one too. A page
    with no feed has only its date."""
    if not isinstance(read_at, dict):
        return [f"{where}: `read_at` must be a table"]
    problems = _keys(f"{where}: read_at", read_at, ("date",), ("revision", "commit"))
    if not isinstance(read_at.get("date"), datetime.date):
        problems.append(f"{where}: `read_at.date` must be a date")
    if api != "none" and not ({"revision", "commit"} & read_at.keys()):
        problems.append(f"{where}: `read_at` needs the `revision` or `commit` last read")
    return problems


def load_sources(root: Path, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    for row in _read(root / "sources.toml", problems).get("source", []):
        source = row.get("id", "?")
        where = f"sources.toml: {source}"
        problems += _keys(where, row, ("id", "url", "kind", "languages", "licence", "due", "feed", "read_at"))
        if source in catalogue.sources:
            problems.append(f"{where}: repeated")
        problems += _one_of(where, row.get("kind"), SOURCE_KINDS, "kind")
        problems += _one_of(where, row.get("due"), DUE, "due")
        problems += _text(where, row, "url") + _text(where, row, "licence")
        languages = tuple(row.get("languages", ()))
        problems += [f"{where}: the language {c!r} isn't one" for c in languages if c not in catalogue.languages]
        if "feed" in row and "read_at" in row:
            problems += _feed_problems(where, row["feed"])
            feed = row["feed"]
            problems += _read_at_problems(where, row["read_at"], feed.get("api") if isinstance(feed, dict) else None)
        catalogue.sources[source] = Source(source, languages)
    return problems


def _kinds_problems(where: str, kinds: object) -> list[str]:
    if not isinstance(kinds, list) or not kinds:
        return [f"{where}: `kinds` must list {ANY} or the kinds of writing"]
    return [problem for kind in kinds for problem in _one_of(where, kind, (*KINDS, ANY), "kinds")]


def _range(where: str, row: Table, catalogue: Catalogue) -> tuple[ModelRange | None, list[str]]:
    problems = _keys(f"{where}: models", row, ("family", "from"), ("to",))
    if row.get("family") not in catalogue.families:
        problems.append(f"{where}: `models` names no family {row.get('family')!r}")
    since = parse_version(str(row.get("from", "")))
    to = parse_version(str(row["to"])) if "to" in row else None
    if since is None:
        problems.append(f'{where}: `from` must be a version, such as "4.6"')
    if "to" in row and to is None:
        problems.append(f'{where}: `to` must be a version, such as "4.6"')
    if since and to and to < since:
        problems.append(f"{where}: `to` {to} comes before `from` {since}")
    return (ModelRange(row.get("family", ""), since, to) if since and not problems else None), problems


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


def _terms(where: str, row: Table, spaces: bool) -> tuple[re.Pattern[str] | None, list[str]]:
    """The one pattern a sign's terms make. In a language written with spaces a term stands as a word of its own, so
    `delve` doesn't match inside another word; in one written without, there is no such edge to look for."""
    terms = row.get("terms")
    if terms is None:
        return None, []
    if row.get("category") not in TERM_CATEGORIES:
        return None, [f"{where}: only a {' or '.join(TERM_CATEGORIES)} sign holds `terms`"]
    if not isinstance(terms, list) or not terms:
        return None, [f"{where}: `terms` must list {{ term, instead }}"]
    problems = [problem for term in terms for problem in _keys(f"{where}: terms", term, ("term", "instead"))]
    if problems:
        return None, problems
    body = "|".join(f"(?:{_nfc(term['term'])})" for term in terms)
    return _compile(where, rf"(?<!\w)(?:{body})(?!\w)" if spaces else body)


def _sign_sources(where: str, row: Table, language: str, catalogue: Catalogue) -> list[str]:
    cited = row.get("sources")
    if not isinstance(cited, list) or not cited:
        return [f"{where}: `sources` must cite at least one"]
    problems = []
    for entry in cited:
        problems += _keys(f"{where}: sources", entry, ("source", "where", "seen"))
        if entry.get("source") not in catalogue.sources:
            problems.append(f"{where}: cites no source {entry.get('source')!r}")
        if not isinstance(entry.get("seen"), datetime.date):
            problems.append(f"{where}: `seen` must be a date")
    known = (catalogue.sources[e["source"]] for e in cited if e.get("source") in catalogue.sources)
    if language == ANY and len({code for source in known for code in source.languages}) < 2:
        problems.append(f"{where}: an {ANY} sign needs sources in at least two languages (AGENTS.md, Traps)")
    return problems


def _dates(where: str, row: Table) -> list[str]:
    since, until = row.get("since"), row.get("until")
    if since is None and until is None:
        return []
    if row.get("models") != ANY:
        return [f"{where}: a model-scoped sign retires by its range's `to`, not by a date"]
    problems = [
        f"{where}: `{key}` must be a date"
        for key, value in (("since", since), ("until", until))
        if value is not None and not isinstance(value, datetime.date)
    ]
    if not problems and since and until and until < since:
        problems.append(f"{where}: `until` comes before `since`")
    return problems


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


def _pattern(where: str, row: Table, spaces: bool) -> tuple[re.Pattern[str] | None, list[str]]:
    """A sign's own `check`, which wins over its terms: it is how a term that can't stand alone is matched."""
    built, problems = _terms(where, row, spaces)
    if "check" not in row:
        return built, problems
    if not isinstance(row["check"], str):
        return None, [*problems, f"{where}: `check` must be text"]
    own, wrong = _compile(where, row["check"])
    return own, problems + wrong


def _sign(language: str, row: Table, catalogue: Catalogue) -> list[str]:
    sign = row.get("id", "?")
    where = f"signs/{language}.toml: {sign}"
    required = ("id", "category", "kinds", "models", "what", "instead", "strength", "flags", "passes", "sources")
    problems = _keys(where, row, required, ("terms", "check", "since", "until"))
    slug = sign.removeprefix(f"{language}-")
    if slug == sign or not _SLUG.match(slug):
        problems.append(f"{where}: an id is {language}-<slug>, in lowercase letters, digits and hyphens")
    if sign in catalogue.signs:
        problems.append(f"{where}: repeated")
    problems += _one_of(where, row.get("category"), CATEGORIES, "category")
    problems += _one_of(where, row.get("strength"), STRENGTHS, "strength")
    problems += _kinds_problems(where, row.get("kinds"))
    problems += _text(where, row, "what") + _text(where, row, "instead")
    models, wrong = _models(where, row.get("models"), catalogue)
    entry = catalogue.languages.get(language)
    pattern, wrong_pattern = _pattern(where, row, entry.spaces if entry else True)
    problems += wrong + wrong_pattern + _examples(where, row, pattern)
    problems += _sign_sources(where, row, language, catalogue) + _dates(where, row)
    catalogue.signs[sign] = Sign(
        sign,
        language,
        row.get("category", ""),
        tuple(row.get("kinds") or ()),
        models,
        row.get("what", ""),
        row.get("instead", ""),
        row.get("strength", ""),
        row.get("flags", ""),
        row.get("passes", ""),
        pattern,
    )
    return problems


def load_signs(root: Path, catalogue: Catalogue) -> list[str]:
    problems: list[str] = []
    for path in sorted((root / "signs").glob("*.toml")):
        language = path.stem
        if language != ANY and language not in catalogue.languages:
            problems.append(f"signs/{path.name}: the file's name is no language")
        for row in _read(path, problems).get("sign", []):
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
