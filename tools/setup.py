"""Set up a clone once, and link skills for Codex. Safe to run again.

Usage:
  uv run tools/setup.py                 turn on the hooks, make `git blame` skip reformats, check out the skill
                                        links as symlinks where this machine can make them, and check the tools
  uv run tools/setup.py link [skill]    write .agents/skills/<skill> into git's index as a link to
                                        .claude/skills/<skill>; every skill when none is named
  uv run tools/setup.py settings        compare the GitHub repo's settings and main's ruleset with the house's
                                        (SETTINGS below), through gh; reads only

Every setting is this repo's own (`git config --local`), shared by its worktrees; nothing global changes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import cast

import gate
from gate import LINK_MODE, ROOT, SKILL_LINKS_DIR, SKILLS_DIR

CONFIG = (
    ("core.hooksPath", ".githooks", "the hooks in .githooks/: commit-msg, pre-push, post-checkout, post-merge"),
    ("blame.ignoreRevsFile", ".git-blame-ignore-revs", "git blame skips the reformat commits listed there"),
)
TOOLS = (
    ("uv", True, "runs the hooks and the gate: https://docs.astral.sh/uv/getting-started/installation/"),
    ("gitleaks", False, "the gate's secret scan, skipped without it: https://github.com/gitleaks/gitleaks"),
    ("gh", False, "the skills' issues and PRs: https://cli.github.com, then gh auth login"),
)


def set_config(root: Path, key: str, value: str) -> str:
    """Set a value in this repo's git config; say whether it changed."""
    if gate.git("config", "--local", "--get", key, cwd=root).stdout.strip() == value:
        return f"{key}={value} (already set)"
    done = gate.git("config", "--local", key, value, cwd=root)
    if done.returncode != 0:
        return f"TO DO: git config --local {key} {value} failed: {done.stderr.strip()}"
    return f"{key}={value} (set)"


def make_hooks_executable(root: Path) -> list[str]:
    """On Linux and macOS git skips a hook without the executable bit; git stores them as 100755, but a copy or an
    unzip may drop it."""
    if os.name == "nt":
        return []
    done = []
    for hook in sorted((root / ".githooks").glob("*")):
        mode = hook.stat().st_mode
        if hook.is_file() and not mode & stat.S_IXUSR:
            hook.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            done.append(f"made {hook.relative_to(root).as_posix()} executable")
    return done


def symlinks_work() -> bool:
    """True when this machine lets this user make a symlink; on Windows that takes Developer Mode."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "target").mkdir()
        try:
            (Path(tmp) / "link").symlink_to("target", target_is_directory=True)
        except (OSError, NotImplementedError):
            return False
    return True


def changed_links(root: Path) -> list[str]:
    """Paths under .agents/skills that differ on disk from git's index, or that git doesn't track. A link only
    staged, as `link` leaves it, is no change: checking it out writes what the index holds."""
    status = gate.git("status", "--porcelain", "--", SKILL_LINKS_DIR, cwd=root).stdout
    # Each line is "XY path": Y is the working tree's side, " " when the file on disk is what the index holds.
    return [line[3:] for line in status.splitlines() if len(line) > 3 and line[1] != " "]


def checkout_links(root: Path, can_symlink: Callable[[], bool]) -> list[str]:
    """Where symlinks work, have git check the skill links out as real symlinks, which Codex follows. Elsewhere they
    stay plain files holding their target: git's index still has them as links, so every commit keeps them."""
    if not can_symlink():
        return [
            f"this machine can't make symlinks (Windows without Developer Mode), so {SKILL_LINKS_DIR} holds plain "
            "files and Codex finds no skills there; AGENTS.md names them, and each is a SKILL.md to read"
        ]
    # A checkout overwrites what differs on disk from git's index, so a changed link is left for the developer to look
    # at. Checked before core.symlinks changes: with it false, a plain file holding the target is no change.
    changed = changed_links(root)
    if changed:
        return [
            f"warning: {SKILL_LINKS_DIR} has local changes, so it was not checked out again: "
            f"{', '.join(changed)}; see git status -- {SKILL_LINKS_DIR}, then run this again"
        ]
    lines = [set_config(root, "core.symlinks", "true")]
    if not gate.git("ls-files", "--", SKILL_LINKS_DIR, cwd=root).stdout.strip():
        return lines
    done = gate.git("checkout", "--", SKILL_LINKS_DIR, cwd=root)
    if done.returncode != 0:
        return [*lines, f"TO DO: git checkout -- {SKILL_LINKS_DIR} failed: {done.stderr.strip()}"]
    return [*lines, f"{SKILL_LINKS_DIR} checked out as symlinks"]


def link(root: Path, name: str) -> tuple[bool, str]:
    """Write `.agents/skills/<name>` into git's index as a symlink (mode 120000) to the skill, then check it out.

    git puts a symlink on disk where it can, and otherwise a plain file holding the target; either way the commit has
    the link. Git Bash's `ln -s` copies the folder instead, which is why this writes the index directly.
    """
    if not (root / SKILLS_DIR / name / "SKILL.md").is_file():
        return False, f"no skill {name}: {SKILLS_DIR}/{name}/SKILL.md doesn't exist"
    path = f"{SKILL_LINKS_DIR}/{name}"
    on_disk = root / path
    if on_disk.is_dir() and not on_disk.is_symlink():
        return False, f"{path} is a folder (a copy, as Git Bash's ln -s makes): delete it, then run this again"
    target = f"../../{SKILLS_DIR}/{name}"
    blob = gate.git("hash-object", "-w", "--stdin", cwd=root, stdin=target)
    if blob.returncode != 0:
        return False, f"linking {path} failed: {blob.stderr.strip()}"
    sha = blob.stdout.strip()
    listed = gate.git("ls-files", "-s", "--", path, cwd=root).stdout.split()
    if listed[:2] == [LINK_MODE, sha] and (on_disk.is_symlink() or on_disk.is_file()):
        return True, f"{path} -> {target} (already linked)"
    added = gate.git("update-index", "--add", "--cacheinfo", f"{LINK_MODE},{sha},{path}", cwd=root)
    if added.returncode != 0:
        return False, f"linking {path} failed: {added.stderr.strip()}"
    done = gate.git("checkout", "--", path, cwd=root)
    if done.returncode != 0:
        return False, f"{path} is staged as a link, but git couldn't check it out: {done.stderr.strip()}"
    kind = "a symlink" if on_disk.is_symlink() else "a plain file holding the target (git makes no symlinks here)"
    return True, f"{path} -> {target} (linked in git's index; on disk {kind}). Commit it with the skill."


def link_all(root: Path, names: list[str]) -> int:
    """Link each named skill, or every skill in .claude/skills; 1 when one failed."""
    names = names or list(gate.skill_folders(root))
    failed = 0
    for name in names:
        ok, line = link(root, name)
        print(line)
        failed += not ok
    return 1 if failed else 0


def run(
    root: Path, which: Callable[[str], str | None] = shutil.which, can_symlink: Callable[[], bool] = symlinks_work
) -> int:
    """Configure the repo at root and print what was done; 1 when something is left for you to do."""
    if gate.git("rev-parse", "--git-dir", cwd=root).returncode != 0:
        print(f"not a git repository: {root}")
        return 1
    done = []
    for title, lines in (
        ("git config (this repo only)", [f"{set_config(root, k, v)}: {why}" for k, v, why in CONFIG]),
        ("hooks", make_hooks_executable(root) or ["executable as stored"]),
        ("skill links", checkout_links(root, can_symlink)),
    ):
        print(f"{title}:")
        for line in lines:
            print(f"  {line}")
        done += lines
    todo = sum(line.startswith("TO DO") for line in done)
    print("tools:")
    for name, needed, why in TOOLS:
        if which(name):
            print(f"  {name}: found")
        elif needed:
            todo += 1
            print(f"  TO DO: {name} is missing; the hooks skip themselves without it. Install: {why}")
        else:
            print(f"  {name}: missing (optional: {why})")
    print("done." if not todo else f"done, with {todo} thing(s) to do above.")
    return 1 if todo else 0


# The GitHub settings the house's repos run with (omniverse-mcp's, 2026-11-07), which no file in the repo can hold:
# (what, the API path, the key in its answer, the value). A key of None reads only whether the path answers, as
# vulnerability-alerts does: 204 when on, 404 when off.
SETTINGS = (
    ("squash merges only", "", "allow_squash_merge", True),
    ("no merge commits", "", "allow_merge_commit", False),
    ("no rebase merges", "", "allow_rebase_merge", False),
    ("a squash commit's subject is the PR's title", "", "squash_merge_commit_title", "PR_TITLE"),
    (
        "a squash commit's body is the PR's description, which pr-text.yml checks",
        "",
        "squash_merge_commit_message",
        "PR_BODY",
    ),
    ("auto-merge, which dependabot-auto-merge.yml turns on", "", "allow_auto_merge", True),
    ("a merged branch is deleted", "", "delete_branch_on_merge", True),
    (
        "private vulnerability reporting, where SECURITY.md sends reporters",
        "/private-vulnerability-reporting",
        "enabled",
        True,
    ),
    ("Dependabot's security updates", "/automated-security-fixes", "enabled", True),
    ("Dependabot alerts", "/vulnerability-alerts", None, True),
    # refresh-agent.yml's publish job opens its draft PR with the workflow's token; every other job keeps it read-only.
    (
        "Actions may open a PR, for refresh-agent.yml",
        "/actions/permissions/workflow",
        "can_approve_pull_request_reviews",
        True,
    ),
    (
        "the workflow token reads only, unless a workflow asks for more",
        "/actions/permissions/workflow",
        "default_workflow_permissions",
        "read",
    ),
)
RULESET_CHECKS = ("CI", "PR text")


def settings_problems(answers: Mapping[str, object], rules: list[dict[str, object]]) -> list[str]:
    """What differs from SETTINGS, given each setting's answer by its what, and main's rules from
    `repos/<repo>/rules/branches/main`: main takes squash-merged PRs only, and requires RULESET_CHECKS."""
    problems = [
        f"{what}: expected {want!r}, GitHub says {answers.get(what)!r}"
        for what, _, _, want in SETTINGS
        if answers.get(what) != want
    ]
    pr = next((rule for rule in rules if rule.get("type") == "pull_request"), None)
    params = cast(dict[str, object], (pr or {}).get("parameters") or {})
    if pr is None or params.get("allowed_merge_methods") != ["squash"]:
        problems.append("main's ruleset: a PR is required, squash-merged only")
    checks = next((rule for rule in rules if rule.get("type") == "required_status_checks"), None)
    found = cast(
        list[dict[str, object]],
        cast(dict[str, object], (checks or {}).get("parameters") or {}).get("required_status_checks") or [],
    )
    contexts = {str(check.get("context")) for check in found}
    problems += [
        f"main's ruleset: the check {name!r} is not required" for name in RULESET_CHECKS if name not in contexts
    ]
    return problems


def gh_api(path: str) -> tuple[int, object]:
    """GET path through gh: (0, the parsed answer), or gh's exit code and None. Reads only."""
    exe = shutil.which("gh") or "gh"
    done = gate.run([exe, "api", path])
    if done.returncode != 0:
        return done.returncode, None
    return 0, json.loads(done.stdout) if done.stdout.strip() else None


def check_settings(root: Path = ROOT, api: Callable[[str], tuple[int, object]] = gh_api) -> int:
    """Read the repo's GitHub settings with gh and print what differs from SETTINGS; 1 when anything does."""
    remote = gate.git("remote", "get-url", "origin", cwd=root).stdout.strip()
    match = re.search(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?/?$", remote)
    if not match:
        print(f"origin is not a GitHub repository: {remote or 'none'}")
        return 1
    repo = f"repos/{match.group(1)}"
    answers: dict[str, object] = {}
    for what, path, key, _ in SETTINGS:
        status, answer = api(repo + path)
        if key is None:
            answers[what] = status == 0
        elif isinstance(answer, dict):
            answers[what] = cast(dict[str, object], answer).get(key)
    status, rules = api(f"{repo}/rules/branches/main")
    problems = settings_problems(answers, cast(list[dict[str, object]], rules if isinstance(rules, list) else []))
    for line in problems or ["every setting is as the house's repos have it"]:
        print(f"  {line}")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    gate.utf8_streams()
    parser = argparse.ArgumentParser(description="Set up this clone: hooks, git blame, skill links, tools.")
    commands = parser.add_subparsers(dest="command")
    link_parser = commands.add_parser("link", help=f"link {SKILLS_DIR}/<skill> into {SKILL_LINKS_DIR} for Codex")
    link_parser.add_argument("skill", nargs="*", help="the skills to link; every skill when none is named")
    commands.add_parser("settings", help="compare the GitHub repo's settings with the house's, through gh; reads only")
    args = parser.parse_args(argv)
    if args.command == "link":
        return link_all(ROOT, args.skill)
    if args.command == "settings":
        return check_settings()
    return run(ROOT)


if __name__ == "__main__":
    sys.exit(main())
