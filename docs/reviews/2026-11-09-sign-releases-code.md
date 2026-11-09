---
subject: "Release a new version with each change to the plugin, signs included (PR #102)"
base: main (359d0b3)
head: 8353141
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer on Opus 5.5, read-only; its finding checked against the code by the main session)
verdict: clean
---

# Release a new version with each change to the plugin, signs included: code review

The reviewer read the change, issue #31, the approved plan with its review, the gate's version and range code, the
pre-push hook, both workflows and the catalogue's language names. In its own scratch folder it ran the publish job's
new step on a throwaway repo and `frozen_problems` from a copy of the gate; it ran nothing in the worktree. It checked
CI's logged bases for how `base.sha` moves.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `tools/gate.py`, `frozen_problems` | Only main's newest released section was frozen. PR B forks at `0.2.0`; PR A merges `0.2.1`; B, pushed without hooks, adds a line under `## 0.2.0`. Git merges the two without a conflict (A inserts above the heading, B about 30 lines lower), and CI's base is main's tip, whose newest section is `0.2.1`, unchanged, so B's line merges under a version users already have. Pre-push catches it, so it needs a missing hook too | fixed in ac3e52e: every section released on the base is frozen; `test_frozen_problems` gains "under an older one, a newer released since", and "an older one" now fails |

## Refuted

- The pre-push range refusing a PR's own reworded section: `main_bases` reads where the last push meets `origin/main`;
  `test_a_branch_rewords_its_own_section_but_not_mains` holds it, and fails with `fork_points`.
- CI comparing the wrong base for the newest section: with `base.sha` at main's tip, the tree is the merge result, the
  right comparison; a rebase that keeps two PRs' lines under one version fails.
- The publish step: run with `de` and `any`, it moved 0.2.0 to 0.2.1, wrote the line and staged both files; the
  runner's Python 3.12 has `tomllib` and `datetime.UTC`; `-I` keeps a planted module out; `HEAD` is the base, so the
  names are the base's; every rendered file sits under a `<code>/` folder; no model text reaches `CHANGELOG.md`.
- `release.yml`: a re-run keeps `GITHUB_SHA`; `gh release view` failing inside `if` doesn't stop the script; `GH_TOKEN`
  is in the step's env; no tag ruleset; `v0.2.0` exists, so this PR's own merge stops; no `${{ }}` in a `run:`.
- `contents: write` as a widened permission: the approved plan names it (Design, `release.yml`).
- Several releases pushed in a row: costs a release page, not an update (the plan's Round 2).

Not covered: the auto-update path the READMEs name was not checked against Claude Code's docs by the reviewer; the
plan's Fit read it ("Turn on auto-update" in the hosting docs).

## Improvements

| # | Improvement | Answer |
|---|---|---|
| 1 | `release_problems`' message named "the release PR", which is gone | taken (ac3e52e) |
| 2 | The PR body names `release.yml`'s `contents: write` and the plan's approval of it | taken |
| 3 | Correct Round 1's note that CI's `base.sha` is the head's merge base: it is main's tip when the run starts | taken: the plan's `tools/gate.py` section records it with F1 |

## Checks

- `uv run tools/gate.py full` passed on 8353141 and on ac3e52e (4133 tests, coverage 99.16%).
- CI passed on 8353141: Checks (Linux), the six test legs, CodeQL's actions and python scans, and PR text.
- By hand: `release.yml`'s notes extract gives v0.2.0's own notes, and fails for a version with no section; the
  publish step, in a scratch clone, for `de`, `zh-Hant` and `any`, `any` alone, an unknown folder and `sources.toml`
  alone.
