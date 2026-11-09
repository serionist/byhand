"""Every list in a sign runs in alphabetical order, in every language.

A source's list order is its own: copied, or reversed, it is still the source's (the review of #24, F8 and F12). One
order that no source chose, alphabetical with accents and case ignored, holds it mechanically, so no review has to
judge an order again. The order of a regex's alternatives changes which one is tried first, never whether a text
matches, so sorting changes no sign's finds.
"""

import re
import unicodedata

import pytest

from byhand import signs

# A group of plain words, with no regex syntax nested in it: the groups the rule can be checked on mechanically.
SIMPLE_GROUP = re.compile(r"\(\?:([^()\[\]\\?*+{}^$.]+)\)")


@pytest.fixture(scope="module")
def catalogue() -> signs.Catalogue:
    found, problems = signs.load()
    assert problems == []
    return found


def plain(text: str) -> str:
    """A text as the rule reads it: accents and case ignored."""
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def term_key(term: str) -> str:
    """A term's plain start: its first word or words, up to the first group or class, or a leading group's first
    alternative."""
    term = term.replace("['\u2019]", "'")
    if term.startswith("(?:"):
        return plain(re.split(r"[|)]", term[3:], maxsplit=1)[0])
    return plain(re.split(r"[(\[]", term, maxsplit=1)[0])


def regexes(catalogue: signs.Catalogue) -> list[tuple[str, str]]:
    found = []
    for sign in catalogue.signs.values():
        if sign.pattern:
            found += [(sign.id, term.term) for term in sign.terms] or [(sign.id, sign.grep)]
    return found


def test_plain_word_groups_run_in_alphabetical_order(catalogue):
    groups = [(sign, group.split("|")) for sign, regex in regexes(catalogue) for group in SIMPLE_GROUP.findall(regex)]
    assert len(groups) >= 200  # the parse finds the groups, so the test can fail
    wrong = [(sign, items) for sign, items in groups if [plain(item) for item in items] != sorted(map(plain, items))]
    assert wrong == []


def test_term_lists_run_in_alphabetical_order(catalogue):
    lists = [sign for sign in catalogue.signs.values() if len(sign.terms) >= 2]
    assert len(lists) >= 50
    wrong = [
        sign.id
        for sign in lists
        if [term_key(t.term) for t in sign.terms] != sorted(term_key(t.term) for t in sign.terms)
    ]
    assert wrong == []


def test_the_rule_reads_an_unsorted_group():
    # The group test fails on a list out of order, so it can't pass by finding nothing.
    regex = r"\b(?:seulement|juste|simplement)\b"
    items = SIMPLE_GROUP.findall(regex)[0].split("|")
    assert [plain(item) for item in items] != sorted(map(plain, items))
