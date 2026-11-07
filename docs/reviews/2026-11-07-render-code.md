---
subject: "Bootstrap step 3, rendering the catalogue, and no command for users (PR #14)"
base: main (2d4ed53)
head: 76a98b3
date: 2026-11-07
round: 1
tier: standard (a fresh reviewer per round on Claude Opus 5.5, every lens; findings checked by the main session, where each major's mutant was run again)
verdict: clean
---

# Review: Bootstrap step 3, rendering the catalogue, and no command for users (PR #14)

Round 1 read the change at `76a98b3`, with 38 mutants on a scratch copy. Two majors, so a second round followed.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `tools/gate.py`, `TREE` | Nothing proved the gate runs `sign files` or `private`: dropping either row left every test green, so a stale render would merge | fixed: `test_the_quick_lane_runs_the_package_as_a_tool_and_fails_with_it`, `test_the_quick_lane_holds_private_and_sign_ids`; each row's mutant killed |
| F2 | major | `signs.py`, `_sign` | Nothing proved `terms` and `until` reach a `Sign`: a rendered line could lose every term, and a retired sign render as live | fixed: `test_terms_and_until_reach_the_rendered_files`; both mutants killed |
| F3 | minor | `render.py`, `write` | `byhand render --out <folder>` emptied any folder | fixed: `--out` is gone; the folder is always the repo's `plugin/signs` |
| F4 | minor | `tools/gate.py`, `_LINK` | A regex term in a rendered file, `[úu](?:ak)?`, failed as a link to nowhere | fixed: code spans skipped in `plugin/signs/` alone, the maintainer's call; a test holds the limit |
| F5 | minor | `tools/gate.py`, `check_private` | A nested `.byhand/` passed | fixed: a glob pathspec, a test |
| F6 | minor | `tools/gate.py`, `plugin_paths` | A tracked file under `plugin/evals/results/` passed | fixed: `private` refuses it |
| F7 | minor | `tools/gate.py`, `eval_file` | A suite's `.yaml` could name a `scaffold_script` | fixed: refused, a test |
| F8 | minor | `tests/` | Edge cases: a variant's unknown read, the budgets' boundaries, a pin under `results/` | fixed |
| F9 | minor | `AGENTS.md` | "Where the work stands" missed the render | fixed |

## The maintainer's calls in round 1

- A third budget, 16 KB, for a deck's or a sheet's layout files.
- The link scan's skip, limited to `plugin/signs/`.
- **byhand is two sets of Markdown files, signs and styles, and the skills that read them, with no command on a user's
  machine.** It came from the maintainer asking what the CLI was for, and it reshaped the rest of this PR.

Improvements taken: the range rule in a file's header, a simpler `is_layout`, each set of files reported once.

## Round 2

**Where:** the delta `76a98b3..55e0fd9`, read by a fresh reviewer, 28 mutants on a scratch copy. **Verdict:** no blocker
or major. F1 to F9 hold, each with the test named above.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F10 | minor | `render.py`, `_ours` | A note quoting render's marker was deleted, and a file at a rendered path overwritten | fixed: `--out` is gone, so nothing but render's own folder is touched |
| F11 | minor | `tests/test_render.py` | `_ours`' `.md` half had no test | gone with F10 |
| F12 | minor | `render.py`, `budget_problems` | A deck of unknown author had no budget: 55 KB across family layout files passed | fixed: a test, its mutant killed |
| F13 | minor | the issue forms, `CHANGELOG.md` | User text still named a package and a command line | fixed |
| F14 | minor | `write-skill`, `start-work`, `finish-work`, both lenses | Repo skills still described skills that run commands | fixed |
| F15 | minor | `ci.yml`, `pyproject.toml` | CI said a release publishes to PyPI | fixed: the job and the metadata are gone, the maintainer's call |
| F16 | minor | `REVIEW.md`, the lenses, the gate | "The pin checks go when the first skill lands" had no owner | fixed: they went here, a ban in their place |
| F17 | minor | issues #5, #6, #7 | Titles and text still named commands | fixed |
| F18 | minor | PR #14 | The text didn't name the one-way door it narrows | fixed: the title and body name it |
| F19 | minor | `tools/gate.py`, `render.py` | A comment had moved off its line, and two stale phrases | fixed |
| F20 | minor | the plan, this record | No PR in the progress log, no record | fixed |

Refuted: a misspelt keyword or `scaffold_script`, each checked letter by letter; a `.yml` or escaped-key way past F7;
`is_layout` on empty `kinds`, which `load` refuses; the range rule printing wrongly; the link skip hiding a real link.

## The maintainer's calls in round 2

| Call | Answer |
|---|---|
| The CI package job and the published-package metadata | cut. Dropping a CI job counts as loosening a check, so this records the maintainer's yes (REVIEW.md, The harness) |
| `byhand models` and reading a family from an id | cut: the model reads its own id; Step 7's evals prove it |
| `render --out` | cut |
| The gate's pin checks | replaced by a ban on a command under `plugin/`, which is stricter: a pinned `uv run` passed before |
| What a `check` may hold | what Grep can run: no look-around, no backreference, held by `validate`; a term's edge is `\b` |
| The version | `plugin.json`'s alone |
| `/byhand:styles` | folded into `learn`: three skills, `write`, `check` and `learn` |

## Checks

- `uv run tools/gate.py full` after the cuts: 22 checks, 530 tests, coverage 99.60 %.
- Round 1's majors, run again in the main session: both gate rows, `terms` and `until`, each mutant killed.
- Twelve mutants of the cuts, one at a time: the ban and each of its spellings, the file types it reads, the Grep rule,
  a term's edges, the unknown deck's budget, the version from `plugin.json`. Each fails a test.
- `gate full` on this branch; a search of the docs, forms and skills for `byhand models`, `byhand styles`, `byhand check`,
  `--out` and `/byhand:styles` finds none.
