"""What the office tests share: the catalogue, the signs that count alone, and the weak cluster counted as the rendered
files say. The helpers are fixtures, as the tests import no module of their own (`--import-mode=importlib`)."""

import re
from collections.abc import Callable, Collection
from functools import partial

import pytest

from byhand import signs


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


def _weak_hits(catalogue: signs.Catalogue, text: str, kind: str, languages: Collection[str] | None = None) -> int:
    counted: set[str] = set()
    spans: list[tuple[int, int]] = []
    for sign in catalogue.signs.values():
        if not sign.pattern or sign.strength != "weak" or not _reads(sign, kind):
            continue
        if languages is not None and sign.language not in languages:
            continue
        language = catalogue.languages.get(sign.language)
        edge = r"\b" if language is None or language.spaces else ""
        phrases = [
            (phrase, re.compile(rf"{edge}(?:{phrase}){edge}", re.IGNORECASE | re.MULTILINE))
            for term in sign.terms
            for phrase in _alternatives(term.term)
        ]
        for phrase, pattern in phrases or [(sign.id, sign.pattern)]:
            for found in pattern.finditer(text):
                if phrase not in counted and any(found.start() < end and start < found.end() for start, end in spans):
                    continue
                counted.add(phrase)
                spans.append(found.span())
    return len(counted)


@pytest.fixture(scope="session")
def weak_hits(catalogue: signs.Catalogue) -> Callable[..., int]:
    """Hits of the weak signs a kind of writing reads, as the cluster rule counts them: each a different word or phrase.
    Each alternative of a term is a phrase of its own, one phrase however its endings vary; a check is one habit however
    often it fires; one phrase two signs find counts once. A term has word edges in a language written with spaces, as
    `validate` gives it. `languages` limits the count to the signs a draft in those languages loads."""
    return partial(_weak_hits, catalogue)
