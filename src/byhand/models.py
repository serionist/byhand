"""Which family and version a model's id names, so a draft reads the signs of the model writing it.

A model released after the catalogue must work out of the box, so an id is never looked up in a list: its family comes
from a pattern and its version from the first number after it. `claude-opus-9-1` is claude 9.1 though no such model
existed when this was written.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from functools import total_ordering
from typing import Protocol

# A release date in an id, `claude-sonnet-4-5-20250929` or `claude-opus-4-6@20250514`, is not a version.
_DATE = re.compile(r"[-@]\d{8}(?!\d)")
# A minor is one or two digits and then the number's end: `gpt-4-0314` is 4, and `llama-3-70b` is 3, not 3.70.
_VERSION = re.compile(r"(\d+)(?:[.-](\d{1,2})(?![\da-z]))?")
_WRITTEN = re.compile(r"^(\d+)(?:\.(\d+))?$")


@total_ordering
@dataclass(frozen=True)
class Version:
    """A model's version. `minor` is None when only the major is known: gpt-7, or a range's `to = "4"`."""

    major: int
    minor: int | None = None

    def __str__(self) -> str:
        return str(self.major) if self.minor is None else f"{self.major}.{self.minor}"

    def __lt__(self, other: Version) -> bool:
        return (self.major, self.minor or 0) < (other.major, other.minor or 0)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor or 0) == (other.major, other.minor or 0)

    def __hash__(self) -> int:
        return hash((self.major, self.minor or 0))


class Named(Protocol):
    """A model family: its id, and the patterns that name it in a model's id."""

    @property
    def id(self) -> str: ...

    @property
    def patterns(self) -> tuple[str, ...]: ...


@dataclass(frozen=True)
class ModelId:
    """What a model's id names. `version` is None when the id holds no number."""

    family: str
    version: Version | None


def parse_version(text: str) -> Version | None:
    """A version as a sign writes it, `5` or `4.6`; None for anything else."""
    match = _WRITTEN.match(text)
    if match is None:
        return None
    major, minor = match.groups()
    return Version(int(major), None if minor is None else int(minor))


def read_id(model_id: str, families: Iterable[Named]) -> ModelId | None:
    """The family and version in an id, whatever wraps it (`us.anthropic.claude-opus-4-6-v1:0`), or None when no family
    matches: an unknown or empty id, for which a draft reads the `any` signs alone."""
    text = _DATE.sub("", model_id.strip().lower())
    for family in families:
        for pattern in family.patterns:
            found = re.search(rf"(?<![a-z]){re.escape(pattern)}", text)
            if found:
                number = _VERSION.search(text, found.end())
                if number is None:
                    return ModelId(family.id, None)
                major, minor = number.groups()
                return ModelId(family.id, Version(int(major), None if minor is None else int(minor)))
    return None
