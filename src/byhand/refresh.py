"""`byhand refresh`: which of the catalogue's sources changed since `read_at`, for the scheduled workflow to open an
issue on. No model and no key. An issue holds our own ids, dates, paths and links, never a fetched page's text, a commit
message or a source's file name (AGENTS.md, Traps)."""

from __future__ import annotations

import datetime as dt
import http.client
import json
import os
import re
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from byhand import signs

USER_AGENT = "byhand-catalogue/0.0 (https://github.com/serionist/byhand)"
# How long after `read_at.date` a source is read again; `by-hand` never is.
DAYS = {"daily": 1, "weekly": 7, "monthly": 30, "quarterly": 90}
# GitHub's compare lists at most this many changed files; a list that long may have dropped a watched one.
GITHUB_FILES = 300
_SHA = re.compile(r"^[0-9a-f]{40}$")

Get = Callable[[str], Any]


class UnreadableError(Exception):
    """The source couldn't be read, as distinct from read and unchanged."""


@dataclass(frozen=True)
class Change:
    now: str  # the revision or commit live now
    link: str  # where a person reads the change
    matched: tuple[str, ...] = ()  # which of our own `paths` it touched
    cut: bool = False  # GitHub cut the file list


def get_json(url: str) -> Any:
    """GET a JSON document. The GitHub token goes to api.github.com only."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and urllib.parse.urlsplit(url).hostname == "api.github.com":
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:  # noqa: S310
        return json.load(response)


def _mediawiki(feed: Mapping[str, Any], read_at: Mapping[str, Any], get: Get) -> Change | None:
    site, old = feed["site"], str(read_at["revision"])
    query = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "ids",
        "titles": feed["title"],
        "redirects": "1",
        "format": "json",
        "formatversion": "2",
    }
    page = get(f"https://{site}/w/api.php?{urllib.parse.urlencode(query)}")["query"]["pages"][0]
    if page.get("missing") or not page.get("revisions"):
        raise UnreadableError("no such page")
    now = str(int(page["revisions"][0]["revid"]))
    if now == old:
        return None
    return Change(now, f"https://{site}/w/index.php?{urllib.parse.urlencode({'diff': now, 'oldid': old})}")


def _under(name: str, path: str) -> bool:
    path = path.rstrip("/")
    return name == path or name.startswith(f"{path}/")


def _github(feed: Mapping[str, Any], read_at: Mapping[str, Any], get: Get) -> Change | None:
    repo, old = feed["repo"], read_at["commit"]
    data = get(f"https://api.github.com/repos/{repo}/compare/{old}...HEAD")
    files = data["files"]
    names = {f["filename"] for f in files} | {f["previous_filename"] for f in files if "previous_filename" in f}
    matched = tuple(path for path in feed["paths"] if any(_under(name, path) for name in names))
    cut = len(files) >= GITHUB_FILES
    if not matched and not cut:
        return None
    # Unpaged, compare lists the newest commit last.
    head = data["commits"][-1]["sha"]
    if not isinstance(head, str) or not _SHA.match(head):
        raise UnreadableError("no commit id")
    now = f"{head[:12]}, {int(data['ahead_by'])} commits ahead"
    return Change(now, f"https://github.com/{repo}/compare/{old}...{head[:12]}", matched, cut)


def _hf(feed: Mapping[str, Any], read_at: Mapping[str, Any], get: Get) -> Change | None:
    dataset, old = feed["dataset"], read_at["commit"]
    sha = get(f"https://huggingface.co/api/datasets/{dataset}")["sha"]
    if not isinstance(sha, str) or not _SHA.match(sha):
        raise UnreadableError("no commit id")
    if sha.startswith(old):
        return None
    return Change(sha[:12], f"https://huggingface.co/datasets/{dataset}/commits/main")


READERS: dict[str, Callable[[Mapping[str, Any], Mapping[str, Any], Get], Change | None]] = {
    "mediawiki": _mediawiki,
    "github": _github,
    "hf": _hf,
}


def due(source: Mapping[str, Any], today: dt.date) -> bool:
    days = DAYS.get(source.get("due", "by-hand"))
    read_at = source.get("read_at", {})
    return days is not None and "date" in read_at and (today - read_at["date"]).days >= days


def body(source: Mapping[str, Any], change: Change) -> str:
    read_at = source["read_at"]
    old = read_at.get("revision") or read_at.get("commit")
    lines = [
        f"The source `{source['id']}` ({source['url']}) changed since the catalogue last read it.",
        "",
        f"- Read at: `{old}`, {read_at['date']}",
        f"- Now: `{change.now}`",
    ]
    if change.matched:
        lines.append("- Watched paths changed: " + ", ".join(f"`{path}`" for path in change.matched))
    if change.cut:
        lines.append(f"- GitHub listed only {GITHUB_FILES} changed files, so any watched path may have changed")
    lines += [
        f"- The change: {change.link}",
        "",
        f"Run `propose-signs` on `{source['id']}`. Its PR carries `Closes #<this issue>` and moves `read_at`, even when"
        " the change gives no sign. Closing this issue without moving `read_at` brings it back on the next run.",
        "",
    ]
    return "\n".join(lines)


def run(out: Path, today: dt.date, get: Get = get_json, root: Path = signs.CATALOGUE) -> int:
    """Check each source that is due, write `<out>/<id>.md` for each changed one, and return 1 if any source with a
    feed couldn't be read."""
    with (root / "sources.toml").open("rb") as f:
        sources = tomllib.load(f).get("source", [])
    out.mkdir(parents=True, exist_ok=True)
    counts = {"changed": 0, "unchanged": 0, "unreadable": 0}
    for source in sources:
        api = source.get("feed", {}).get("api", "none")
        if api == "none" or not due(source, today):
            continue
        reader = READERS.get(api)
        try:
            if reader is None:
                raise UnreadableError(f"no reader for the feed {api!r}")
            change = reader(source["feed"], source["read_at"], get)
        except (UnreadableError, OSError, http.client.HTTPException, LookupError, TypeError, ValueError) as exc:
            # OSError holds urllib's errors and timeouts; HTTPException, a reply cut short; ValueError, bad JSON; the
            # rest, a reply of another shape.
            print(f"{source['id']}: unreadable ({type(exc).__name__}: {exc})")
            counts["unreadable"] += 1
            continue
        if change is None:
            print(f"{source['id']}: unchanged")
            counts["unchanged"] += 1
            continue
        print(f"{source['id']}: changed")
        counts["changed"] += 1
        (out / f"{source['id']}.md").write_text(body(source, change), encoding="utf-8", newline="\n")
    print(", ".join(f"{n} {what}" for what, n in counts.items()))
    return 1 if counts["unreadable"] else 0
