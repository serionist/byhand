"""The versions a sign holds for.

A model released after the catalogue works out of the box: a range with no `to` holds every later version. A skill
reads the family from the model's own id; nothing here looks an id up.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import total_ordering

_WRITTEN = re.compile(r"^(\d+)(?:\.(\d+))?$")


@total_ordering
@dataclass(frozen=True)
class Version:
    """A model's version. `minor` is None when only the major is written, as in a range's `to = "4"`."""

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
    """A model family. Its id names its rendered files, `plugin/signs/<language>/<id>.signs.md`."""

    id: str
    name: str


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


def parse_version(text: str) -> Version | None:
    """A version as a sign writes it, `5` or `4.6`; None for anything else."""
    match = _WRITTEN.match(text)
    if match is None:
        return None
    major, minor = match.groups()
    return Version(int(major), None if minor is None else int(minor))
