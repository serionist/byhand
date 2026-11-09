---
subject: "Release 0.1.0 (PR #45)"
base: main (4cfd111)
head: f27452f
date: 2026-11-09
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens with something in scope; fixes by the main session)
verdict: approved
---

# Review: Release 0.1.0 (PR #45)

Round 1 by a fresh reviewer, read only. It checked every README claim against the skills, the agent and the rendered
signs, and the release steps against the gate and Claude Code's plugin docs. No blocker or major; every minor fixed in
this round, so no second.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `tools/gate.py` `release_problems` | A release dated in the changelog without `plugin.json`'s version moved passed the gate; Claude Code updates on the version, so users would stay on the old one | fixed: the version must be the newest dated section; a test for it |
| F2 | minor | `docs/releasing.md` | "The tag is the release": a marketplace install takes `main`'s head, so the merge is | fixed: the merge is the release, the tag marks it, and what merges after reaches new installs under the same version |
| F3 | minor | `README.md`, `plugin/README.md`, `releasing.md` | No way to update in the README; the one given refreshes the marketplace, not the plugin | fixed: `claude plugin update byhand@byhand` and a new session, in all three (checked against `claude plugin update --help`) |
| F4 | minor | `plugin/README.md`, `docs/USAGE.md`, `SECURITY.md` | "Not released yet" | fixed |
| F5 | minor | `README.md`, both manifests | Layout and decks promised; no layout sign ships and decks are `0.4.0` | fixed: "formatting", "posts and documents"; the `presentations` keyword dropped |
| F6 | minor | `README.md` | "Commit messages … are left alone"; Step 7 saw `write` start on one in 1 of 3 runs | fixed: "isn't meant for … and seldom starts on it" |
| F7 | minor | `README.md` | The feedback offer comes only after a draft in a style | fixed |
| F8 | minor | both READMEs | "Claude Code asks you to allow it" once: unmeasured in Step 7 | fixed: "may ask", and saving a style always asks; `releasing.md` step 3 counts the prompts |
| F9 | minor | `releasing.md` | The `gh release create` line wrapped inside its title and named no notes file | fixed: one fenced line, a full SHA, `.local/notes.md` |
| F10 | minor | the PR | `gate quick` reported, not `full` | fixed: `full` run and said |
| I1 | improvement | the gate | the stricter check of F1 | taken |
| I2 | improvement | `CHANGELOG.md` | the release notes left out listing styles, defaults, "remember", the feedback offer, the languages | taken |
| I3 | improvement | `README.md` | the styles' path on Windows | taken |

Refuted: the token claim (the largest draft reads about 15 KB plus a style, 4 to 5 thousand tokens), the language list,
the Next milestones, the skill claims, the styles path as a one-way door, and the Writing rules over both new files.
