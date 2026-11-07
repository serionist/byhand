"""The versions a sign holds for, for models that exist and for models that don't yet."""

import pytest

from byhand import models
from byhand.models import ModelRange, Version


@pytest.mark.parametrize(
    ("text", "expected"), [("5", Version(5)), ("4.6", Version(4, 6)), ("4.6.1", None), ("x", None)]
)
def test_a_written_version(text, expected):
    assert models.parse_version(text) == expected


def test_versions_order_by_number_not_by_text():
    assert Version(4, 9) < Version(4, 10)
    assert Version(4, 10) > Version(4, 9)
    assert Version(5) > Version(4, 99)
    assert Version(4) == Version(4, 0)
    assert hash(Version(4)) == hash(Version(4, 0))
    assert Version(4) != "4"
    assert str(Version(4)) == "4"
    assert str(Version(4, 6)) == "4.6"


@pytest.mark.parametrize(
    ("since", "to", "version", "expected"),
    [
        (Version(4), None, Version(9, 1), True),  # no `to`: a model newer than the catalogue is covered
        (Version(4), None, Version(3, 9), False),
        (Version(4, 6), Version(5), Version(5, 6), True),  # a `to` with no minor holds its whole major
        (Version(4, 6), Version(5), Version(6), False),
        (Version(4, 6), Version(5, 0), Version(5), True),
        (Version(4, 6), Version(5, 0), Version(5, 6), False),  # `to = "5.0"` stops at 5.0
        (Version(4, 6), Version(4, 6), Version(4, 6), True),
        (Version(4, 6), Version(4), Version(4, 7), True),
    ],
)
def test_a_range_holds_a_version(since, to, version, expected):
    assert ModelRange("gpt", since, to).holds(version) is expected
