---
subject: "Render a deck's and a sheet's signs from the short and layout files, with layout check and scan files (PR #87)"
base: main (63c88f0)
head: 82d2a96
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked by the main session)
verdict: clean
---

# Review: the render for decks and sheets (PR #87)

Six files, Step 1 of `docs/plans/2026-11-09-decks-and-sheets.md`. One fresh Claude Code agent on Opus 5.5 read the
ground truth (`AGENTS.md`, `REVIEW.md`, #66, the plan and `2026-11-09-check-budget.md`), the diff and the touched files
in full, and applied every lens. It ran read-only probes against `byhand.render`: `stale` against `plugin/signs/`
returns nothing, `budget_problems` nothing, and only `hu/any.layout.md` and `fi/any.layout.md` are new. No blocker or
major; its two minors were fixed in this session.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `tests/test_render.py`, `test_every_pattern_prints_as_written_in_nfc` | The `written` side took layout-only signs once the `deck` filter went, but `printed` chose paths ending in `scan.md`, which `scan.layout.md` doesn't: Step 3's first layout-only sign with a pattern would fail it on a correct change | fixed: the file's name is `scan.md` or `scan.layout.md` (4e9449b); checked by hand that the filter keeps `en/scan.layout.md` |
| F2 | minor | the plan's progress log | Step 1's row had no PR, and Step 2's said `open` though #83 is merged (1d270df) | fixed: #87, and Step 2 merged (4e9449b) |

## Refuted

- `parts` returning nothing: `signs.py` refuses an empty `kinds` and any kind outside the six and `any`.
- `check.layout.md` colliding with a `<family>.layout.md` or the budget's suffix filter: no family is named `check`
  or `scan`, and `draft_files` lists no check file.
- A deck's check unbounded: `check` bounds `check.md`, `layout` bounds `check.layout.md`; 32 KB at most, as the plan's
  cost table accepts.
- `scan.layout.md` under the 16 KB `layout` budget, past `scan`'s 9 KB: a departure the progress log records; Step 3
  lowers `layout`.
- Dropping the `deck` filter in the NFC test loosens it: it widens what is compared.
- No test pinning the unchanged files: the progress log records it; `byhand render --check` and the diff show it.
- No CHANGELOG or AGENTS.md line: no skill or agent reads the layout files yet, so users see nothing.
- A skill naming `check.layout.md` failing the sign-file names test: it ends in `render.LAYOUT`.

## Improvements

| # | Improvement | Answer |
|---|---|---|
| I1 | The module docstring's "a deck or a sheet the layout ones" reads as the old behaviour: "the layout ones too" | taken (4e9449b) |
| I2 | `docs/USAGE.md`: say `check` reads `check.layout.md` and its `scan` agent `scan.layout.md` | taken (4e9449b) |

## Not covered

Privacy-and-sources and harness-integrity: no style, sample, source or harness file touched. The reviewer ran no gate
or session; CI on 82d2a96 passed, and `gate.py full` passed in the main session.

## Checks

`uv run tools/gate.py quick` and `tests/test_render.py` on 4e9449b; `gate.py full` on the head before the PR is
marked ready. The plugin was not tried in a session: no skill reads the new files until Step 4.
