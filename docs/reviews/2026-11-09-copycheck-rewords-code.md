---
subject: "Reword three signs that copycheck matches against MIT sources (PR #74)"
base: main (26884bc)
head: 2127290
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, read-only; findings checked against the code by the main session)
verdict: clean
---

# Reword three signs that copycheck matches: code review

The reviewer read the issue, the diff, the three sign files and the six rendered lines, propose-signs step 3,
`tests/test_order.py` and copycheck's runs before and after. It ran nothing. It confirmed no finding.

## Refuted

- The zh `what` losing the shape its `flags` show: both clauses of the example are X是Z的Y, which "X is Z's Y" names
  as well as "X is the Y of Z" did; "the real X is Y" is kept.
- The zh `what` breaking the alphabetical rule for examples: "the real X is Y" before "X is Z's Y" is in order; the
  old text was not.
- The hu `instead` breaking the order rule: its two parts are instructions, not a list of examples.
- "it" with no antecedent in the hu and ja texts: the terms' own `instead`s use the same "it" ("say what it does").
- Rendered files out of step: each of the six lines matches its TOML field, and no copy of the old text is left.
- New copycheck hits: 27 before, 15 after, over the same 1265 texts and 3192 files; the 12 gone are the three signs'
  (zh 4, ja 5, hu 3), and the 15 left are the same lines as before.

## Not covered

- implementation and harness-integrity: no code and no harness file in the change.
- The gate, which a read-only reviewer can't run: the main session ran `gate.py full`, and CI passed on 2127290.

## Improvements

| # | Improvement | Answer |
|---|---|---|
| I1 | hu `instead`: "say what it does or why it matters", as the old text read, not "and" | taken in 18688f6; copycheck gives the same 15 hits |
| I2 | ja `instead`: "what happened" could come back, as no source holds "what it does or what" | left: "what took place" is plain too, and the meaning is the same |
| I3 | An issue for the 15 hits left (`tr-stock-idioms` carries the same vale-ai-tells run; `tr-besides-this`, `en-even-sentences`) and two prose lists out of order (ja-stock-metaphors `what`, ja-texture-words `instead`) | later: drafted; opening it with `gh issue create` was refused in this session |
