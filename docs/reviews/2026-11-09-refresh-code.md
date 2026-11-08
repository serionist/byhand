---
subject: "Check the catalogue's sources daily and open an issue when one changes (PR #44)"
base: main (4cfd111)
head: 1d479f0
date: 2026-11-09
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens with something in scope; fixes by the main session)
verdict: approved
---

# Review: Check the catalogue's sources daily and open an issue when one changes (PR #44)

Round 1 by a fresh reviewer, read only. It ran the tests and the gate, mutated a copy of `refresh.py` to find what
the tests miss, and called the three APIs live to check the replies the code assumes. No blocker or major; every minor
fixed in this round, so no second.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `tests/test_refresh.py` | `>=` mutated to `>` in `due` passed every test: the day a source falls due was untested | fixed: one case per boundary, the day before and the day of each `due`; `formatversion=2` asserted too |
| F2 | minor | `refresh._github` | The issue gave a GitHub source's commit count, not the commit live now, as the plan's Goal says | fixed: the newest commit from the same reply (compare lists it last; checked live), with the count beside it, and the link compares to it |
| F3 | minor | `refresh.run` | `http.client.HTTPException` (a reply cut short) isn't an `OSError`: it would end the run with a traceback | fixed: caught, and tested |
| F4 | minor | `docs/USAGE.md` | Nothing said the command reads `GITHUB_TOKEN`, so a run by hand over 60 calls an hour reads as unreadable | fixed |
| F5 | minor | `AGENTS.md` | "Where the work stands" left out the refresh | fixed |
| I1 | improvement | `refresh.yml` | `--locked`, and the install in a step with no token, so the build backend never sees it | taken |
| I2 | improvement | `refresh._github` | A reply with no file list read as unchanged | taken: unreadable, tested |

Refuted, each checked: fetched text reaching the issue body (every field traced to the catalogue, an `int` or a hex
id), a workflow command in the log from fetched text, the 300-file cap (live, a 471-commit compare lists exactly 300),
renames and prefixes, `HEAD` and a 12-character base, missing and invalid wiki pages, an unknown dataset, an error
hiding a source as unchanged, the workflow's shell under `bash -e`, the token's host, the timeout.

Open for the maintainer: `issues: write` is a new workflow permission, in a plan approved on the maintainer's word for
the night; the workflow runs once by hand after the merge.
