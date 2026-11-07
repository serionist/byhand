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

# A number after a family's name, its size or its minor beside it. A minor is one or two digits and then the number's
# end: `gpt-4-0314` is 4, and `llama-3-70b` is 3, not 3.70.
_NUMBER = re.compile(r"(\d+)([bkmx](?![a-z]))?(?:[.-](\d{1,2})(?![\da-z]))?")
_WRITTEN = re.compile(r"^(\d+)(?:\.(\d+))?$")
_MAJOR_DIGITS = 2  # more is a date, `mistral-large-2411` or `qwen-max-2025-01-25`, not a version


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


@dataclass(frozen=True)
class Family:
    """A model family: its id, which names its rendered files, and the patterns that name it in a model's id."""

    id: str
    name: str
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class ModelRange:
    """The versions of a family a sign holds for."""

    family: str
    since: Version
    to: Version | None = None  # None holds every later version, so a newer model is covered

    def holds(self, version: Version) -> bool:
        """True when the range holds version. A `to` with no minor holds its whole major: `to = "5"` holds 5.6, where
        `to = "5.0"` stops at 5.0. It is what an author means by it."""
        if version < self.since:
            return False
        if self.to is None:
            return True
        return version.major <= self.to.major if self.to.minor is None else version <= self.to


@dataclass(frozen=True)
class ModelId:
    """What a model's id names. `version` is None when the id holds no number that is a version."""

    family: str
    version: Version | None


def parse_version(text: str) -> Version | None:
    """A version as a sign writes it, `5` or `4.6`; None for anything else."""
    match = _WRITTEN.match(text)
    if match is None:
        return None
    major, minor = match.groups()
    return Version(int(major), None if minor is None else int(minor))


def _version(text: str) -> Version | None:
    """The version in what follows a family's name: its first number, unless that number is a size or a date."""
    number = _NUMBER.search(text)
    if number is None:
        return None
    major, size, minor = number.groups()
    if size or len(major) > _MAJOR_DIGITS:
        return None
    return Version(int(major), None if minor is None else int(minor))


def read_id(model_id: str, families: Iterable[Family]) -> ModelId | None:
    """The family and version in an id, whatever wraps it (`us.anthropic.claude-opus-4-6-v1:0`), or None when no family
    matches: an unknown or empty id, for which a draft reads the `any` signs alone. The family named first in the id
    wins: `deepseek-r1-distill-llama-70b` is a DeepSeek model."""
    text = model_id.strip().lower()
    found = [
        (match.start(), match.end(), family.id)
        for family in families
        for pattern in family.patterns
        if (match := re.search(rf"(?<![a-z]){re.escape(pattern)}", text))
    ]
    if not found:
        return None
    _, end, family = min(found)
    return ModelId(family, _version(text[end:]))
