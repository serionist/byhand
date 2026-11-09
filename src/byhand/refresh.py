"""`byhand refresh`: which of the catalogue's sources changed since `read_at`, for the scheduled workflow to open an
issue on. No model and no key. An issue holds our own ids, dates, paths and links, never a fetched page's text, a commit
message or a source's file name (AGENTS.md, Traps).

`byhand fetch`: a changed source's text now, and its diff from `read_at`, for `propose-signs` to read as data."""

from __future__ import annotations

import datetime as dt
import difflib
import http.client
import io
import json
import os
import re
import shutil
import tarfile
import tempfile
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import zlib
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from byhand import signs

USER_AGENT = "byhand-catalogue/0.0 (https://github.com/serionist/byhand)"
# How long after `read_at.date` a source is read again; `by-hand` never is.
DAYS = {"daily": 1, "weekly": 7, "monthly": 30, "quarterly": 90}
# GitHub's compare lists at most this many changed files; a list that long may have dropped a watched one.
GITHUB_FILES = 300
_SHA = re.compile(r"^[0-9a-f]{40}$")

Get = Callable[[str], Any]
GetBytes = Callable[[str], bytes]


class UnreadableError(Exception):
    """The source couldn't be read, as distinct from read and unchanged."""


@dataclass(frozen=True)
class Change:
    now: str  # the revision or commit live now
    link: str  # where a person reads the change
    matched: tuple[str, ...] = ()  # which of our own `paths` it touched
    cut: bool = False  # GitHub cut the file list


def _request(url: str, accept: str) -> urllib.request.Request:
    """A GET with our user agent. The GitHub token goes to api.github.com only, and as an unredirected header, so a
    redirect to another host never carries it."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})  # noqa: S310
    token = os.environ.get("GITHUB_TOKEN")
    if token and urllib.parse.urlsplit(url).hostname == "api.github.com":
        request.add_unredirected_header("Authorization", f"Bearer {token}")
    return request


def get_json(url: str) -> Any:
    """GET a JSON document."""
    with urllib.request.urlopen(_request(url, "application/json"), timeout=30) as response:  # noqa: S310
        return json.load(response)


def get_bytes(url: str) -> bytes:
    """GET a file: a page's text, a tarball."""
    with urllib.request.urlopen(_request(url, "*/*"), timeout=120) as response:  # noqa: S310
        return response.read()


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


# `byhand fetch`. Each fetcher writes the source's text at `read_at` into `old` and as it is now into `new`, and returns
# the revision now, the value `read_at` moves to.
Fetcher = Callable[[Mapping[str, Any], Mapping[str, Any], Path, Path, GetBytes], str]
WIKITEXT = "page.wikitext"


def _wikitext(site: str, query: Mapping[str, str], get: GetBytes) -> tuple[str, str]:
    """The revision id and wikitext a MediaWiki query for one revision answers."""
    params = {"action": "query", "prop": "revisions", "rvprop": "ids|content", "rvslots": "main", **query}
    params |= {"format": "json", "formatversion": "2"}
    pages = json.loads(get(f"https://{site}/w/api.php?{urllib.parse.urlencode(params)}"))["query"].get("pages") or []
    if not pages or pages[0].get("missing") or not pages[0].get("revisions"):
        raise UnreadableError("no such page or revision")
    revision = pages[0]["revisions"][0]
    content = revision["slots"]["main"].get("content")
    if not isinstance(content, str):
        raise UnreadableError(f"no text for revision {revision.get('revid')}")
    return str(int(revision["revid"])), content


def _fetch_mediawiki(feed: Mapping[str, Any], read_at: Mapping[str, Any], old: Path, new: Path, get: GetBytes) -> str:
    site = feed["site"]
    _, before = _wikitext(site, {"revids": str(read_at["revision"])}, get)
    now, text = _wikitext(site, {"titles": feed["title"], "redirects": "1"}, get)
    (old / WIKITEXT).write_text(before, encoding="utf-8", newline="\n")
    (new / WIKITEXT).write_text(text, encoding="utf-8", newline="\n")
    return now


def _sha(value: object) -> str:
    if not isinstance(value, str) or not _SHA.match(value):
        raise UnreadableError("no commit id")
    return value


def _extract(tarball: bytes, paths: list[str], dest: Path) -> None:
    """Extract the regular files under `paths` from a GitHub tarball into `dest`, its top folder cut off. A member named
    with `..` or an absolute path refuses the whole tarball, and tarfile's data filter anything else that would land
    outside `dest`."""
    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as tar:
        members = []
        for member in tar.getmembers():
            name = PurePosixPath(member.name)
            if name.is_absolute() or ".." in name.parts or "\\" in member.name:
                raise UnreadableError(f"the tarball names a path outside its folder: {member.name!r}")
            inner = "/".join(name.parts[1:])
            if member.isfile() and inner and any(_under(inner, path) for path in paths):
                members.append(member.replace(name=inner, deep=False))
        try:
            tar.extractall(dest, members=members, filter="data")
        except tarfile.FilterError as exc:
            raise UnreadableError(f"the tarball names a path outside its folder: {exc}") from exc


def _fetch_github(feed: Mapping[str, Any], read_at: Mapping[str, Any], old: Path, new: Path, get: GetBytes) -> str:
    repo = feed["repo"]
    head = _sha(json.loads(get(f"https://api.github.com/repos/{repo}/commits/HEAD"))["sha"])
    for sha, dest in ((read_at["commit"], old), (head, new)):
        _extract(get(f"https://codeload.github.com/{repo}/tar.gz/{sha}"), feed["paths"], dest)
    return head[:12]


def _fetch_hf(feed: Mapping[str, Any], read_at: Mapping[str, Any], old: Path, new: Path, get: GetBytes) -> str:
    dataset = feed["dataset"]
    head = _sha(json.loads(get(f"https://huggingface.co/api/datasets/{dataset}"))["sha"])
    for sha, dest in ((read_at["commit"], old), (head, new)):
        card = get(f"https://huggingface.co/datasets/{dataset}/resolve/{sha}/README.md")
        (dest / "README.md").write_bytes(card)
    return head[:12]


FETCHERS: dict[str, Fetcher] = {"mediawiki": _fetch_mediawiki, "github": _fetch_github, "hf": _fetch_hf}


def _files(folder: Path) -> dict[str, bytes]:
    return {path.relative_to(folder).as_posix(): path.read_bytes() for path in folder.rglob("*") if path.is_file()}


def change_diff(old: Path, new: Path) -> str:
    """A unified diff of every file under `old` against `new`; a file holding a NUL byte is named, not diffed."""
    before, after = _files(old), _files(new)
    out: list[str] = []
    for name in sorted(before.keys() | after.keys()):
        a, b = before.get(name, b""), after.get(name, b"")
        if a == b:
            continue
        if b"\0" in a or b"\0" in b:
            out.append(f"Binary file {name} differs\n")
            continue
        for line in difflib.unified_diff(
            a.decode("utf-8", "replace").splitlines(keepends=True),
            b.decode("utf-8", "replace").splitlines(keepends=True),
            f"a/{name}" if name in before else "/dev/null",
            f"b/{name}" if name in after else "/dev/null",
        ):
            out.append(line if line.endswith("\n") else f"{line}\n\\ No newline at end of file\n")
    return "".join(out)


def fetch(ids: list[str], out: Path, get: GetBytes = get_bytes, root: Path = signs.CATALOGUE) -> int:
    """For each source, write `<out>/<id>/new/` (its text now), `<out>/<id>/change.diff` (from `read_at` to now) and
    `<out>/<id>/revision` (the value `read_at` moves to). Return 1 if any id couldn't be fetched; the rest still are."""
    with (root / "sources.toml").open("rb") as f:
        sources = {source["id"]: source for source in tomllib.load(f).get("source", [])}
    failed = 0
    for source_id in ids:
        source = sources.get(source_id)
        api = (source or {}).get("feed", {}).get("api", "none")
        fetcher = FETCHERS.get(api)
        if source is None or fetcher is None:
            reason = "not in sources.toml" if source is None else f"the feed {api!r} has no fetcher: a person reads it"
            print(f"{source_id}: not fetched ({reason})")
            failed += 1
            continue
        # What an earlier fetch left goes first, so a failed fetch leaves no old diff to read.
        folder = out / source_id
        new, diff_file, revision_file = folder / "new", folder / "change.diff", folder / "revision"
        shutil.rmtree(new, ignore_errors=True)
        diff_file.unlink(missing_ok=True)
        revision_file.unlink(missing_ok=True)
        new.mkdir(parents=True)
        try:
            with tempfile.TemporaryDirectory() as old:
                revision = fetcher(source["feed"], source["read_at"], Path(old), new, get)
                diff = change_diff(Path(old), new)
        except (
            UnreadableError,
            OSError,
            http.client.HTTPException,
            tarfile.TarError,
            EOFError,
            zlib.error,
            LookupError,
            TypeError,
            ValueError,
        ) as exc:
            # As in `run`; TarError, EOFError and zlib.error are a tarball cut short or garbled.
            print(f"{source_id}: unreadable ({type(exc).__name__}: {exc})")
            shutil.rmtree(new, ignore_errors=True)
            failed += 1
            continue
        diff_file.write_text(diff, encoding="utf-8", newline="\n")
        revision_file.write_text(f"{revision}\n", encoding="utf-8", newline="\n")
        print(f"{source_id}: fetched at {revision}, a diff of {len(diff.encode())} bytes")
    print(f"{len(ids) - failed} fetched, {failed} not")
    return 1 if failed else 0
