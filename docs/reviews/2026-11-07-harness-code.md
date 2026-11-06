---
subject: "Bootstrap step 1, the harness and the plan (PR #9)"
base: main (42373e1)
head: d0285ec
date: 2026-11-07
round: 1
tier: split (three fresh reviewers on Claude Opus 5.5, by lens; findings checked and fixes verified by the main session)
verdict: clean
---

# Review: Bootstrap step 1, the harness and the plan (PR #9)

60 files and 6,596 diff lines, so the lenses went to three fresh reviewers in parallel: the harness and its port
(harness-integrity, compatibility), the docs (plan-and-intent, docs-freshness, simplicity), and the code (implementation,
tests, plugin-contract, catalogue-contract, privacy-and-sources). `uv run tools/gate.py full` passed on `d0285ec`, and
CI on the PR's head. No blocker or major: every finding below was fixed in this round, each fix checked in the main
session, and the review ends.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `.github/workflows/ci.yml`, `tests` | The Windows leg on Python 3.14 from omniverse-mcp's layout was dropped: a skill run with `--no-project` takes the machine's newest Python, which CI never tested on Windows | fixed: the leg is back; ci.yml's header and AGENTS.md's row name it |
| F2 | minor | `.github/ISSUE_TEMPLATE/bug_report.yml` | The required "no secrets" box simready-forge's form ends with was dropped; a bug report is where a user would paste their real mail | fixed: the box, worded for keys, tokens and anyone's real mail or messages |
| F3 | minor | repo settings | Auto-merge was off, so `dependabot-auto-merge.yml` would fail on Dependabot's first PR | fixed: on |
| F4 | minor | repo settings | A squash commit took the commits' messages, not the PR's title and description that `pr-text.yml` checks | fixed: `PR_TITLE` and `PR_BODY` |
| F5 | minor | repo settings | Private vulnerability reporting was off, though SECURITY.md and the issue chooser send reporters there | fixed: on |
| F6 | minor | repo settings | Dependabot alerts and security updates were off | fixed: on |
| F7 | minor | `AGENTS.md`, `README.md` | The refresh was described as proposing signs from the workflow, which needs a model in CI, the alternative the plan rejected; "a default per kind" missed Q1's language | fixed: the workflow fetches, diffs and opens an issue, and a maintainers' skill drafts the PR; a default per kind and language |
| F8 | minor | `.claude/skills/write-skill/SKILL.md` | The pin form `uv run --with` that the plan's round 1 retired (P4): the first plugin skill written from it would write a `.venv` into the user's project | fixed: `uv run --no-project --with`, with why |
| F9 | minor | `review-code/SKILL.md`, `finish-work/SKILL.md` | "The live tests", simready-forge's, which byhand has none of; review-code's SKILL.md and its lenses disagreed on what a refuter may run | fixed: the live sources and someone's real writing, in both |
| F10 | minor | `.claude/skills/fit-plan/SKILL.md` | "On #7", another repo's precedent; byhand's #7 is Step 7 | fixed: the bootstrap plan's own Fit |
| F11 | minor | `pyproject.toml`, the sdist | The sdist shipped `tests/` and `tools/` without `.claude/`, so its tests failed to collect; an unanchored `README.md` pulled in every README | fixed: `/src`, `/tests/test_package.py` and the three root files, each anchored |
| F12 | minor | `tools/gate.py`, `_TOOL_TRAILER` | No test failed without it: its one case was also a session link | fixed: `Claude-Session: 0000example` and `Codex-Task: task_0000example` refused; a never-matching regex now fails 4 tests |
| F13 | minor | `tools/gate.py`, `_TOOL_NAME` | `Co-authored-by: Claude Fable 5 <claude@example.org>` passed | fixed: `fable` among the model words; removing it fails 4 tests |
| F14 | minor | `tools/gate.py`, the plugin check | Only `byhand==` was read, so `uvx byhand` or `--with byhand>=0.1.0` in a skill passed and would run whatever PyPI serves | fixed: `loose_pin_problems`; dropping it fails 2 tests |
| F15 | minor | `tools/gate.py`, `plugin_file_problems` | A reference-style link out of `plugin/` passed, and a `mailto:` link was refused | fixed: reference definitions read, `mailto:` a URL; each fails a test without it |
| F16 | minor | `tests/test_gate.py` | Comments cited simready-forge's #9 and #19 as if they were byhand's | fixed: the side file named, and "simready-forge #19" |

## Refuted

- The plugin check with zero skills and agents passes: right for Step 1, and now pinned by a test.
- The variables check with no `BYHAND_` variable passes: its reader sets are empty, so any doc naming one would fail.
- `byhand.__version__` from the wheel and the sdist: both read the version; the wheel holds only the package.
- The sed-renamed fixtures: each still tested its logic (the old names acted as wrong names).
- `cli.py` and `docs/USAGE.md` cited before they exist: pointers to Steps 2 to 6, and the gate reads only files that
  exist.
- The plugin README's "Updating" line names a pin that doesn't exist yet: the page says it isn't released.
- The port's departures: `release.yml` (Step 8), hosted runners (a public repo), simready-forge's markers, ignores and
  import contract, `requires-python` without simready-forge's cap. Each is explained or stricter.
- The repo's own writing rules: no em dash, the banned words only as quoted examples.

## The maintainer's call

The plugin's version: Claude Code keeps a user on a plugin's version until it changes, so an install before the
release would sit on an empty `0.1.0` for good. The maintainer chose `0.0.0` until the release PR sets `0.1.0`
(`pyproject.toml`, `plugin.json`, the plan's Step 8).

## Improvements

| Improvement | Answer |
|---|---|
| The harness-integrity lens points at REVIEW.md's list instead of copying it | taken |
| fit-plan's Reuse example named the CLI-per-draft design the plan rejected; it names the rendered signs | taken |
| README and plugin/README link the bootstrap plan itself, not issue #1 | taken |
| Step 1's row in the plan's progress log names #9 | taken |
| A gate test for a plugin with no skills and no agents, the repo's state today | taken |
| The GitHub settings the house's repos run with, listed once | taken: `SETTINGS` in `tools/setup.py` |
| `uv run tools/setup.py settings` compares them through read-only `gh api` calls | taken; byhand passes |
| test_gate.py's simready-forge fixture text (Isaac Sim, the lamp's joint, the `make` skill, the `critic` agent) in byhand's words | taken |

## Checks

- `uv run tools/gate.py full` after the fixes: 18 checks, 352 tests.
- Each new test run against the gate with its fix removed (the five mutations above): each fails.
- `uv run tools/setup.py settings` against GitHub after the settings change: every setting as the house's repos have it.
