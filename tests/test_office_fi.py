"""Plain Finnish work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that fires
on any of these accuses a person of writing like a machine. A weak sign may fire, but plain work text must not reach a
cluster. The text, and what it is seeded from, is in `office_fi.toml` beside this file: ruff reads Finnish's short dash
as a confusable hyphen, and Finnish writes it in every range."""

import tomllib
import unicodedata
from pathlib import Path

import pytest

from byhand import signs

TEXT = tomllib.loads((Path(__file__).parent / "office_fi.toml").read_text(encoding="utf-8"))
MAIL, REPLIES, CHAT, NOTES = TEXT["mail"], TEXT["replies"], TEXT["chat"], TEXT["notes"]
REPORTS, SPEECHES, POSTS, TYPOGRAPHY = TEXT["reports"], TEXT["speeches"], TEXT["posts"], TEXT["typography"]
# What a Finnish draft loads: the `any` signs and Finnish's, never another language's.
FINNISH = ("any", "fi")

OFFICE = MAIL + REPLIES + CHAT + NOTES + REPORTS + SPEECHES + POSTS + TYPOGRAPHY

KINDS = [
    *((text, "email") for text in MAIL + REPLIES),
    *((text, "message") for text in CHAT),
    *((text, "document") for text in NOTES + REPORTS + SPEECHES + TYPOGRAPHY),
    *((text, "post") for text in POSTS),
]

MACHINE = [(row["sign"], row["text"]) for row in TEXT["machine"]]
FORMS = [(row["sign"], row["text"]) for row in TEXT["forms"]]
LEFT_ALONE = [(row["sign"], row["text"]) for row in TEXT["left_alone"]]


def test_the_text_holds_finnish_letters_and_marks():
    # so the tests below can't pass on text that lost its letters or marks on the way
    for name in ("EN DASH", "RIGHT DOUBLE QUOTATION MARK", "RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK"):
        assert any(unicodedata.lookup(name) in text for text in OFFICE), name
    assert sum("ä" in text for text in OFFICE) >= 50
    assert sum("ö" in text for text in OFFICE) >= 10
    assert len(OFFICE) >= 60


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_finnish_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_finnish(counted_alone, sign, text):
    pattern = {found.id: found.pattern for found in counted_alone}[sign]
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_finnish_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind, FINNISH) < signs.WEAK_CLUSTER, paragraph


def test_the_weak_counting_counts_a_cluster(weak_hits):
    # so the test above can fail: three different weak habits in one paragraph of a document
    assert weak_hits(TEXT["cluster"], "document", FINNISH) == signs.WEAK_CLUSTER


def test_one_habit_repeated_counts_once(weak_hits):
    assert weak_hits(TEXT["repeated"], "document", FINNISH) == 1


@pytest.mark.parametrize("text", TYPOGRAPHY)
def test_finnish_typography_meets_no_formatting_check(catalogue, text):
    # of the files a Finnish draft reads: English's and Korean's dash signs fire on other dashes, and no Finnish draft
    # loads them
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language in FINNISH and sign.category == "formatting" and sign.pattern and sign.pattern.search(text)
    ]
    assert fired == []


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_finnish_check_finds_its_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_finnish_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
