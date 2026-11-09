"""Plain Turkish work text, invented, against the real catalogue. A strong or usual sign counts alone, so one that fires
on any of these accuses a person of writing like a machine. A weak sign may fire, but plain work text must not reach a
cluster. The text, and what it is seeded from, is in `office_tr.toml` beside this file: ruff reads Turkish's dotless i
as a confusable one, and Turkish writes it in nearly every word."""

import re
import tomllib
import unicodedata
from pathlib import Path

import pytest

from byhand import signs

TEXT = tomllib.loads((Path(__file__).parent / "office_tr.toml").read_text(encoding="utf-8"))
MAIL, REPLIES, CHAT, NOTES = TEXT["mail"], TEXT["replies"], TEXT["chat"], TEXT["notes"]
REPORTS, SPEECHES, POSTS, TYPOGRAPHY = TEXT["reports"], TEXT["speeches"], TEXT["posts"], TEXT["typography"]
DOTLESS, DOTTED = (
    unicodedata.lookup("LATIN SMALL LETTER DOTLESS I"),
    unicodedata.lookup("LATIN CAPITAL LETTER I WITH DOT ABOVE"),
)
# What a Turkish draft loads: the `any` signs and Turkish's, never another language's.
TURKISH = ("any", "tr")

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


def test_the_text_holds_turkish_letters_and_marks():
    # so the tests below can't pass on text that lost its letters or marks on the way
    for name in ("EM DASH", "EN DASH", "LEFT DOUBLE QUOTATION MARK", "RIGHT SINGLE QUOTATION MARK"):
        assert any(unicodedata.lookup(name) in text for text in OFFICE), name
    assert sum(DOTLESS in text for text in OFFICE) >= 50
    assert sum(DOTTED in text for text in OFFICE) >= 10
    assert len(OFFICE) >= 60


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_turkish_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


def test_each_i_in_a_turkish_pattern_stands_with_its_capital(catalogue):
    # Python's re folds the four Turkish i letters together under IGNORECASE; Grep folds only i with I, so its dotted i
    # misses a dotted capital and its dotless i a plain capital I. A class of each letter with its own capital finds the
    # capitals in both, as tr.toml's header says.
    letters = f"iI{DOTLESS}{DOTTED}"
    pairs = rf"\[(?:i{DOTTED}|{DOTTED}i|{DOTLESS}I|I{DOTLESS})\]"
    patterns = [form for sign in catalogue.signs.values() for code, form in sign.forms.items() if code == "tr"]
    assert patterns
    bare = [pattern for pattern in patterns if re.search(f"[{letters}]", re.sub(pairs, "", pattern))]
    assert bare == []


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_turkish(catalogue, read_in, sign, text):
    # as a Turkish check runs it: the forms under tr and any, never another language's
    pattern = read_in(catalogue.signs[sign], "tr")
    assert pattern is not None
    assert pattern.search(text), sign


def test_every_turkish_form_of_a_shared_sign_has_a_machine_line(unproven):
    assert unproven(MACHINE + FORMS, "tr") == []


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_plain_turkish_work_text_makes_no_weak_cluster(weak_hits, text, kind):
    for paragraph in text.split("\n\n"):
        assert weak_hits(paragraph, kind, TURKISH) < signs.WEAK_CLUSTER, paragraph


def test_the_weak_counting_counts_a_cluster(weak_hits):
    # so the test above can fail: three different weak habits in one paragraph of a document
    assert weak_hits(TEXT["cluster"], "document", TURKISH) == signs.WEAK_CLUSTER


def test_one_habit_counts_once_per_text(weak_hits):
    # rol oynuyor twice is one hit; a term counts each different text it matches, so rol oynamaya is another (#84)
    assert weak_hits(TEXT["repeated"], "document", TURKISH) == 2


def test_the_turkish_checks_read_no_mail_or_chat(catalogue):
    # the set phrases of mail and chat and the idioms people write in them would add up there: no Turkish sign with a
    # pattern reads mail or chat
    reading_mail = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language == "tr" and sign.pattern and {"any", "email", "message"} & set(sign.kinds)
    ]
    assert reading_mail == []


@pytest.mark.parametrize("text", TYPOGRAPHY)
def test_turkish_typography_meets_no_formatting_check(catalogue, text):
    # of the files a Turkish draft reads: English's and Korean's dash signs fire here, and no Turkish draft loads them
    fired = [
        sign.id
        for sign in catalogue.signs.values()
        if sign.language in TURKISH and sign.category == "formatting" and sign.pattern and sign.pattern.search(text)
    ]
    assert fired == []


@pytest.mark.parametrize(("sign", "text"), FORMS)
def test_a_weak_turkish_check_finds_its_forms(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert pattern.search(text), sign


@pytest.mark.parametrize(("sign", "text"), LEFT_ALONE)
def test_a_weak_turkish_check_leaves_plain_forms_alone(catalogue, sign, text):
    pattern = catalogue.signs[sign].pattern
    assert pattern is not None
    assert not pattern.search(text), sign
