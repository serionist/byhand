---
subject: "Count each weak sign's hits on its own in the office tests (PR #57)"
base: main (2786619)
head: dd566cd
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, read-only; findings checked against the code by the main session)
verdict: needs-fixes
---

# Count each weak sign's hits on its own: code review

The reviewer read the change, the issue, F18 of the Portuguese review, the plugin's counting rule and every office
test that calls `weak_hits`; it ran nothing. The main session reproduced each scenario with `_weak_hits` on the
catalogue.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `tests/conftest.py`, `_weak_hits`, the checks' spans | dd566cd kept checks and phrases apart, but a check still hid another check it overlapped. "Em resumo, a feira volta no domingo — e desta vez enfatizando as lojas." (`any-closing-summary`, `pt-dash-pivots`, a phrase) and "**Novidade:** …" (`any-raw-markdown`) counted 2; "Was wäre, wenn die Halle — vielleicht eventuell — schon im Mai öffnet?" (`de-rhetorical-openers`, `de-hedging`, `de-em-dash`, whose matches take a letter of each word beside the dashes) counted 2. The plugin counts 3 in each | fixed in 67bfae9: each check counts on its own; only another language's check finding the same mark, a pair no draft loads together, counts once with it (so the hu and fr tests that load every language still read one dash as one habit). The three lines are in `test_a_dash_pivot_takes_no_other_sign_s_words` and `test_weak_hits_count_as_the_rule_does` (de); each counts 2 at dd566cd |
| F2 | minor | `tests/conftest.py`, `_weak_hits`, a check counted under its sign's id | Older than this change: a check that finds two different phrases counts once. "Já parou para pensar no domingo? E a melhor parte? A entrada é livre, enfatizando as lojas." counts 2 (`pt-staged-reveal` twice, a phrase); the plugin counts 3 | wontfix here: outside #56, and "a check is one habit however often it fires" is what the ja asides and hu dashes test for marks. It is the improvement named after F18; a follow-up issue is drafted (opening it with `gh issue create` was refused in this session) |

## Refuted

- The new test passing without the fix: at 2786619 the two phrases come before `pt-dash-pivots` in `pt.toml`, the
  dash overlaps both and is skipped, giving 2.
- An existing office text reaching 3 now: every `weak_hits` call in the suite was counted by the code at 2786619 and
  at the fix; only the new tests' lines differ, each from 2 to 3.
- The phrase pool counting fewer than before: no weak phrase in the catalogue overlaps two others that don't overlap
  each other, and the comparison above found no count that fell.

| Improvement | Answer |
|---|---|
| Make the comment true: say why checks are not deduplicated across signs, or name the one case that is | taken: the comment and the fixture's docstring name it |

## Checks

`uv run tools/gate.py full` on dd566cd passed, and CI on it.
