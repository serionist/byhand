---
subject: "The emoji sign on a progress list's ticks (PR #34)"
base: main (5a1905b)
head: ca08df8
date: 2026-11-08
round: 1
tier: standard (one fresh reviewer on Claude Opus 5.5, every lens; the fixes checked by their mutants in the main session)
verdict: clean
---

# Review: The emoji sign on a progress list's ticks (PR #34)

Round 1 read `any-emoji-markers` at `ca08df8` against issue #19, `AGENTS.md`, `REVIEW.md`, `propose-signs` and every
lens, and ran 18 invented lines of its own under Python and Claude Code's Grep tool: they agreed on each. The new check
finds a subset of what the old one found, so it accuses no new line. No blocker or major; the two minors are fixed in
`06a51ea`, "Fix the emoji sign from review round 1".

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | any-emoji-markers, `what` | It called a ✅ or ❌ on a list item a person's, while the check still fires on one before a bold label (`- ✅ **Faster builds:** ...`). The plugin's model reads `what`, not the check, so it would let such a chatbot list pass this sign | fixed in `06a51ea`: "a ✅ or ❌ ticking off a list item, with no bold label, is a person's"; re-rendered |
| F2 | minor | `tests/test_office.py`, OFFICE | No passing line held a tick before bold text with no label, so a mutant dropping the label's colon from the bold branch would flag `- ✅ **Contract** signed` and every test would pass | fixed in `06a51ea`: that list is in OFFICE; the mutant now fails one test |

Refuted:

- Ticked lists with no bold label are missed now: issue #19 asks for that.
- `- ✅ **Mon:** stand-up done` still fires: the old check fired too, and the PR says a tick leading a bold label still
  counts.
- `\s*` after the tick crosses a newline in Python but not in Grep: it needs a bare tick line followed by a bold-label
  line, too unlikely to matter.
- `- 🟢 Contract signed` and other status emoji still count: old behaviour #19 doesn't name.
- `- ✅ 🚀 Shipped` is missed now: a tick followed by a second emoji is rare.
- ✅ with a variation selector, and ✔️: both pass, as the PR says.
- Alphabetical order: `✅ or ❌` and `[✅❌]` run in code-point order; `tests/test_order.py` reads only groups of plain
  words.
- Own words and invented examples: `flags` and `passes` are invented, near each other; the sources are unchanged.
- The lines sit in `tests/test_office.py`, not each `test_office_<lang>.py`: that file runs every sign that counts alone
  on every line, so the coverage is the same.
- CHANGELOG: before `0.1.0` Unreleased holds only the groundwork, so no entry is due.

Improvements:

- An en dash as a bullet, as `any-bold-lead-in-list` reads one: taken in `06a51ea`. `– 🚀 Launch day` and
  `– ✅ **Speed:** ...` are in MACHINE, and a ticked en-dash list in OFFICE; a mutant without the en dash fails two tests.

Not covered: privacy-and-sources and harness-integrity had no files in scope; plugin-contract had only a rendered sign
line, as no skill exists yet. The reviewer read only, so the gate and the author's mutants are the author's.

## Checks

- `uv run tools/gate.py full --base origin/main` passed on `ca08df8` (1995 tests) and on `06a51ea` (1999 tests).
- Mutants of the check, each killed by `tests/test_office.py`: ✅ and ❌ back after a marker (with the old `passes`),
  no ticks in headings, no bold-label branch, a bold label with ✅ only, the label without its colon-outside form, no
  other list emoji, the bold branch without the label's colon, no en dash.
- The check on 54 invented lines, the new tests' own, under Python's `re` and Claude Code's Grep tool with `-i` (no rg
  on PATH): both find the 13 that should fire and none of the 41 that should pass.
- CI on `ca08df8`: every check green.
