---
subject: "Draft the refresh's sign changes with an agent every two weeks (PR #98)"
base: main (8d2f857)
head: 187edc3
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, read only; a fresh refuter for the blocker, which reproduced it with the CLI)
verdict: clean
---

# Review: Draft the refresh's sign changes with an agent every two weeks (PR #98)

Round 1 by a fresh Claude Code agent on Opus 5.5, read only, from the pack's diff, every touched file, the plan and
the issue, with every lens in `lenses.md`. It ran throwaway repros in a scratch folder: `git diff` with
`diff.external`, a planted `json.py` against `python -`, and a cut-short tarball. It graded F1 a blocker it could not
settle without running `claude`. A fresh refuter ran the CLI and refuted it. The five minors were fixed in `f656dee`
and checked in this session; with no blocker or major left, there is no second round.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | blocker, refuted | `.github/refresh-agent.json`, the model's step | The model writes `src/byhand/catalogue/tools/gate.py`, runs `cd src/byhand/catalogue` on its own, then the allowed `uv run tools/gate.py quick`, which would run the planted script. That code could set `diff.external` in `.git/config`, which runs in the next step, where the OAuth token is | refuted: with 2.1.285, the workflow's flags and the scrub, `cd src/byhand/catalogue`, `cd ./...` and `pushd` were denied ("cd names a path that is computed at run time, which cannot be checked against the read block"). The one absolute spelling allowed left the next call in the checkout's root. The real gate ran every time, and the planted script never did, with `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` and without. Kept as hardening in `f656dee`: the variable, `git diff --no-ext-diff --no-textconv`, and the token grep in a step that runs nothing from the checkout. Shown on Windows only |
| F2 | minor | `refresh-agent.yml`, publish, the check step | `python3 -` runs after `git apply` has put the hand-off in the working folder, so a planted `json.py` at the root would load on `import json` before the path check refuses it | fixed in `f656dee`: `python3 -I -` in both steps; the hand try's planted `json.py` is refused with no import |
| F3 | minor | `refresh-agent.yml`, draft, "What to do" | Any open PR whose branch starts `refresh-agent/`, a fork's included, stops every run | fixed in `f656dee`: `gh pr list --author app/github-actions` |
| F4 | minor | `refresh-agent.yml`, publish | A draft closed unmerged keeps `refresh-agent/<date>`, so a second run that day can't push | fixed in `f656dee`: `refresh-agent/<date>-<run id>` |
| F5 | minor | `refresh.py`, `fetch` | A gzip stream cut short raises `EOFError`, which wasn't caught, so every later source went unfetched | fixed in `f656dee`: `EOFError` and `zlib.error` caught; `test_fetch_a_broken_tarball_is_unreadable_and_the_rest_are_fetched` fails without the fix |
| F6 | minor | `AGENTS.md`, Where the work stands | It named `byhand refresh` and `refresh.yml` only | fixed in `f656dee` |

Refuted by the reviewer:
- SIGPIPE in the open-PR check: 1,000 branch names fit the pipe's buffer.
- `python3 -` in "What to do": it runs on main's checkout before any model.
- A planted `.py` in the catalogue run by the gate: the catalogue is read by path, and pytest's `testpaths` is `tests`.
- A planted bare repository: it needs F1's `cd` too.
- A GitHub token in the model's reach: none is in its step.
- `${{ }}` injection: every value goes through `env`.
- Two issues for one id: `refresh.yml` opens an issue only when no open issue has its title.
- The setting's API field: it is right.
- `splitlines` on U+2028: it makes a stray marker in a diff that is only read.
- A read-only tar member: codeload uses 0664 and 0775.

Not covered: the catalogue and plugin contracts, since neither changed. The runs on GitHub's runners and the scrub's
Linux PID namespace wait for the first dispatches.

| Improvement | Answer |
|---|---|
| Hold `.github/refresh-agent.json` to its keys, since `--settings` would load hooks or `env` as readily | taken in `f656dee`: `test_the_refresh_agent_edits_four_folders_and_reads_only_the_checkout` |
| In publish, check that each moved `read_at` equals the revision `byhand fetch` wrote | left: the plan's rule is that a moved `read_at` closes its issue, and the maintainer reads that line in the draft before it lands |
| `--no-ext-diff`, and the token grep in a step of its own | taken in `f656dee` |

## Checks

- `uv run tools/gate.py full` on `f656dee`: 22 checks, 4124 tests, 99.16% coverage.
- The publish job's checks were run again on the invented hand-offs, all refused as before, and on a planted root
  `json.py`, which was refused by the path check with no import. The real hand-off from the try still passes.
