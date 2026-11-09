"""What the office tests share: the catalogue, the signs that count alone, a sign read as a check in one language runs
it, and the weak cluster counted as the rendered files say. The helpers are fixtures, as the tests import no module of
their own (`--import-mode=importlib`)."""

import functools
import re
from collections.abc import Callable, Collection, Iterable
from functools import partial

import pytest

from byhand import render, signs


@pytest.fixture(scope="session")
def catalogue() -> signs.Catalogue:
    found, problems = signs.load()
    assert problems == []
    return found


@pytest.fixture(scope="session")
def counted_alone(catalogue: signs.Catalogue) -> list[signs.Sign]:
    """The strong and usual signs with a pattern: one that fires on plain work text accuses a person."""
    found = [sign for sign in catalogue.signs.values() if sign.pattern and sign.strength != "weak"]
    assert found
    return found


@functools.cache
def _compiled(pattern: str) -> re.Pattern[str]:
    return signs.as_grep(pattern)


def _read_in(sign: signs.Sign, scopes: Collection[str]) -> re.Pattern[str] | None:
    forms = [form for code, form in sign.forms.items() if code in scopes]
    return _compiled(signs.together(forms)) if forms else None


@pytest.fixture(scope="session")
def read_in(catalogue: signs.Catalogue) -> Callable[[signs.Sign, str], re.Pattern[str] | None]:
    """A sign as a check in a language runs it: its forms under the scopes that language's scan files are rendered
    for, `any`, a variant's base and the language, read together; or None, when it has none there. A form under another
    language's code is never read, as scan never reads it."""
    return lambda sign, code: _read_in(sign, render._scopes(catalogue, code))


@pytest.fixture(scope="session")
def unproven(catalogue: signs.Catalogue) -> Callable[[Iterable[tuple[str, str]], str], list[str]]:
    """The forms under `code` that no line of `machine` for their sign finds with that form alone: a form split under
    the wrong language, or one that stopped finding, fails its language's office test. English's covers `any` too."""

    def found(machine: Iterable[tuple[str, str]], code: str) -> list[str]:
        lines = list(machine)
        codes = {code, "any"} if code == "en" else {code}
        return [
            f"{sign.id}: {key}"
            for sign in catalogue.signs.values()
            if sign.until is None
            for key, form in sign.forms.items()
            if sign.language == "any" and key in codes
            if not any(name == sign.id and _compiled(form).search(text) for name, text in lines)
        ]

    return found


def _reads(sign: signs.Sign, kind: str) -> bool:
    return bool({"any", kind} & set(sign.kinds))


def _alternatives(term: str) -> list[str]:
    """A term's top-level alternatives: `a|b` is two phrases, `(?:a|b)c` one phrase with two spellings."""
    found, depth, start, escaped, in_class = [], 0, 0, False, False
    for n, char in enumerate(term):
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif in_class:
            in_class = char != "]"
        elif char == "[":
            in_class = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "|" and depth == 0:
            found.append(term[start:n])
            start = n + 1
    return [*found, term[start:]]


@pytest.fixture(scope="session")
def reads() -> Callable[[signs.Sign, str], bool]:
    """Whether a sign reads a kind of writing."""
    return _reads


@pytest.fixture(scope="session")
def alternatives() -> Callable[[str], list[str]]:
    return _alternatives


def _overlaps(span: tuple[int, int], spans: list[tuple[int, int]]) -> bool:
    return any(span[0] < end and start < span[1] for start, end in spans)


def _base(catalogue: signs.Catalogue, code: str) -> str:
    """The language a sign's draft is in: a script variant's draft loads its base language's signs too."""
    language = catalogue.languages.get(code)
    return language.of if language and language.of else code


def _weak_hits(catalogue: signs.Catalogue, text: str, kind: str, languages: Collection[str] | None = None) -> int:
    if languages is not None:
        return _count(catalogue, text, kind, languages)
    # Every language's signs at once overlap where no draft does (a dash two languages' checks find), so the count
    # is also taken as each language's draft would load it, and the higher one stands.
    codes = {code for sign in catalogue.signs.values() for code in (sign.language, *sign.forms)} - {"any"}
    each = [_count(catalogue, text, kind, render._scopes(catalogue, code)) for code in codes]
    return max(_count(catalogue, text, kind, None), *each)


def _count(catalogue: signs.Catalogue, text: str, kind: str, languages: Collection[str] | None) -> int:
    counted: set[str] = set()
    phrase_spans: list[tuple[int, int]] = []
    marks: dict[str, list[tuple[int, int]]] = {}  # each check's matches, by the language a draft loads it with
    for sign in catalogue.signs.values():
        # In a language, a sign's check is its forms there, as that language's scan runs them.
        pattern = sign.pattern if languages is None else _read_in(sign, languages)
        if not pattern or sign.strength != "weak" or not _reads(sign, kind):
            continue
        if languages is not None and sign.language not in languages:
            continue
        language = catalogue.languages.get(sign.language)
        edge = r"\b" if language is None or language.spaces else ""
        phrases = [
            (phrase, signs.as_grep(rf"{edge}(?:{phrase}){edge}"))
            for term in sign.terms
            for phrase in _alternatives(term.term)
        ]
        if not phrases:
            # Grep runs each check on its own, and a dash's match may run from the line's start over other signs'
            # words and marks, so a check takes no other sign of its draft's text. Two of `any`'s checks on one bold
            # label then count twice, more than the rule, which a guard may. Only a check whose every match overlaps
            # another language's check, a pair no draft loads together, is dropped as the one habit twice.
            # A formatting check finds a mark, one however often it appears; any other check counts each different
            # phrase it finds, as the rule says. The phrase is the match's text, so a staged reveal, whose match takes
            # the next word's first letter, counts twice when two different words follow it: more than the rule.
            base = _base(catalogue, sign.language)
            found = list(pattern.finditer(text))
            elsewhere = [
                span for other, spans in marks.items() if base != "any" and other not in ("any", base) for span in spans
            ]
            for match in found:
                if not _overlaps(match.span(), elsewhere):
                    phrase = " ".join(match.group().casefold().split())
                    counted.add(sign.id if sign.category == "formatting" else phrase)
            marks.setdefault(base, []).extend(match.span() for match in found)
            continue
        for phrase, pattern in phrases:
            for found in pattern.finditer(text):
                if phrase not in counted and _overlaps(found.span(), phrase_spans):
                    continue
                counted.add(phrase)
                phrase_spans.append(found.span())
    return len(counted)


@pytest.fixture(scope="session")
def weak_hits(catalogue: signs.Catalogue) -> Callable[..., int]:
    """Hits of the weak signs a kind of writing reads, as the cluster rule counts them: each a different word or phrase.
    Each alternative of a term is a phrase of its own, one phrase however its endings vary; a check counts each
    different phrase it finds, but a mark (a dash, quotes, bold) once however often it appears; one phrase two signs
    find counts once. Each sign counts on the text on its own, as Grep runs it: a check's match hides no other sign's of
    the same draft. A term has word edges in a language written with spaces, as `validate` gives it. `languages` limits
    the count to the signs a draft in those languages loads; without it, the count is the higher of every language's
    signs at once and each language's draft."""
    return partial(_weak_hits, catalogue)
