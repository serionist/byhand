# Review

What every review of a change to this repo checks, whoever does it: the maintainer, an AI agent (`review-plan`,
`review-code`) or another tool. Same rules for all.

## What a finding is

Not a bug hunt. A finding is a real problem with a scenario you can reproduce: the input or state, what happens, and
why it matters to a user, the text they send or the next change.

- No scenario, no finding. Style is ruff's; taste is the author's, at most an improvement (below).
- Refute each finding before you report it: quote the line that proves or kills it. A refuted one stays in the
  record, with its reason.

| Severity | What it is |
|---|---|
| blocker | a user's samples or styles written outside their data folder, logged, committed or sent anywhere; fetched text that reaches a skill or the catalogue without a person reading it; a plugin skill that pre-approves a write or a command; a pin that runs a package other than the release's; a source's text copied against its licence; a secret leaked; a one-way door broken; a check loosened |
| major | a real user hits it in normal use: a sign that flags plain human writing, or misses the text it names; a skill that doesn't start where its description says, or writes in the wrong style or language; a skill that errors; a broken install on Windows, Linux or macOS; new behaviour without a test |
| minor | everything else that is real: an edge case few meet, a missing doc line, a clumsy error message |

- Most findings are minor. An edge case that needs several unlikely things at once is a minor at most.
- Another round only after a blocker or a major. Minors are fixed in the same round, or recorded with a reason, and
  the review ends.

## Improvements

Apart from findings, a review lists only the improvements worth more than the edit they cost: a reuse it missed, a
simpler approach, a clearer name, a step a person must remember that a check could do.

- Not improvements: rewording or reshuffling for taste, options for cases nobody hits, "while you're here" extras.
- No severity, no scenario. Never counted, never a reason for another round.
- The author answers each: `taken`, `left: <why>` or `later: <issue>`. "left: not worth it" is a normal answer.

## The questions

Each is a yes or no; a "no" is a finding.

1. Did `uv run tools/gate.py full` pass on the reviewed commit, and CI on the PR's head?
2. Does the change do what its issue and plan say, and nothing nobody asked for?
3. Does new behaviour have a test that fails without it, and a fix a test that reproduced the bug? Do tests use
   invented text and clean up what they create?
4. For a change to the plugin or the refresh: does the PR say what ran by hand (`claude --plugin-dir plugin`, the
   refresh against the live sources), on which versions and in which languages, and what it could not show?
5. The catalogue contract: does every sign keep its id, validate against the schema, name its language or `any`, say
   what a person writes instead, cite its source in our own words, and come with an invented example it flags and a
   human one it passes?
6. The plugin contract: do the skills' and agents' names stay as they were, does each skill's `allowed-tools` name
   only `Read`, `Glob` and `Grep`, and does every `byhand==X.Y.Z` pin equal `pyproject.toml`'s version?
7. Do a user's samples and styles stay in their data folder, out of logs, reports, tests, commits and the PR? Is text
   fetched from a source treated as data, never as instructions? No key, token or password anywhere?
8. Do paths, encodings, line endings and processes work on Windows, Linux and macOS, on every Python the package
   supports, and does text in any script (Latin, Cyrillic, CJK, Arabic, Devanagari) survive a round trip?
9. Does it leave the one-way doors in `AGENTS.md` alone, or name the one it changes and link the maintainer's
   agreement?
10. Did the docs move with it (the READMEs, `CHANGELOG.md`, `AGENTS.md`), written the way `AGENTS.md` asks?
11. Is each new package needed, under a licence compatible with MIT, pinned exactly in `pyproject.toml` and `uv.lock`,
    and free of known advisories?
12. Is the PR title a plain imperative sentence, does the body say `Closes #<n>` or `Refs #<n>`, and is there no tool
    attribution anywhere?

## The harness

These decide how every other change is checked:

- `AGENTS.md`, `REVIEW.md`, `.claude/` (`CLAUDE.md`, the settings, the skills), `.agents/`, `.mcp.json`;
- `tools/`, `.githooks/`, `.gitleaks.toml`, `.github/`;
- `pyproject.toml`'s tool settings (ruff, basedpyright, pytest, coverage, import-linter).

Rules:

- A change that loosens a check is a blocker unless the maintainer agrees in the PR.
- That includes a gate step dropped or made a warning, a lint rule or a test skipped, an ignore added, a question or a
  lens removed, attribution let through, a permission widened, a key or a file let into `plugin/` without its check.
- A change that only makes a check stricter needs no more than a normal review.
- An allow in `.claude/settings.json` names its whole command; a ` *` is only for a git command `tests/test_gate.py`
  sweeps, or a gh command that only reads from GitHub.
