---
subject: "Let a dash that opens speech after a colon pass in Portuguese (PR #68)"
base: main (a430174)
head: 4a960d4
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: clean
---

# Let a dash that opens speech after a colon pass in Portuguese: code review

The reviewer read the diff against `it-dash-pivots` and the Italian review's F1, and ran the Portuguese and Italian
office tests (550 passed) and `byhand validate`. It loaded both signs' checks from the TOML and found them the same
string, and ran the old and new checks over `flags`, both `passes` and the three new lines, then 16 edge lines of its
own, through `signs.as_grep` and Claude Code's ripgrep 14.1.1: the two find the same lines. It confirmed the 12 bytes
(`pt/check.md`, 2,939 to 2,951) and that the Japanese check keeps its 494. No finding.

Refuted: two spaces before a dialogue dash (rare for a weak sign, as the Italian review's round 2 found); a dash right
after a bold label such as `**Nota:**`, which ends in `*` (rarely written, and the sign is weak); a pivot inside speech
opened after a colon, now missed (the class the comment already accepts: a pivot after another dash on the line);
"Prazo: sexta" and a time such as 9:00 before a pivot, which still fire, rightly, as the colon is earlier in the line.
A left side that ends in a colon has no words to pivot from, so the guard drops no real pivot.

## Improvements

| Improvement | Answer |
|---|---|
| A test that `pt-dash-pivots` and `it-dash-pivots` have the same check | left: the two languages may part on purpose, and Italian's comment names the link |

## Not covered

A native speaker's reading of the office lines; a plugin session, as the change is one rendered pattern.
