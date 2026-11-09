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

## Round 2

**Where:** PR #57 at df57f26 (the fixes since dd566cd, in 67bfae9), one fresh reviewer, read-only; the main session
reproduced each finding with `_weak_hits`. **Verdict:** clean. F1's three lines count 3 at df57f26 and 2 at dd566cd,
each worked through by the reviewer; F2's reason holds (one check finding two phrases is not one sign taking another's
text, and the ja asides and hu dashes rest on a check counting once).

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F3 | minor | `tests/conftest.py`, `_weak_hits`, another language's checks | With every language loaded, as the fr, de, hu and ja guards call it, a check whose every match overlaps another language's check is dropped, even when it finds something else. "Et si notre synergie pourrait potentiellement — enfin — changer tout ?" counted 2: `de-em-dash`'s letters beside the dashes overlap `fr-hedge-stack` and `fr-engagement-lines`. A French draft counts 3. The comment said "the same mark" | fixed in c208375: a call without `languages` takes the higher of every language at once and each language's own draft (`any`, the language, its base), so it is never below a draft's count and stays as strict as before; `test_another_language_s_dash_check_takes_no_french_check`, which counts 2 at 2786619 and at df57f26. The comment says "overlaps" |
| F4 | minor | `tests/conftest.py`, `_weak_hits`, the checks of one draft | `any-bold-lead-in-list` and `any-raw-markdown` on one label now count twice: "- **Prazo:** sexta-feira — antes do almoço." counts 3, the plugin 2 ("one phrase two signs find counts once") | wontfix: more than the rule is what #56 allows ("at least what the plugin counts"), and no office line in a weak count has a bold label in a list. A containment rule would merge the dash pivot with the label it runs over, F1 again. The comment names the overcount |

| Improvement | Answer |
|---|---|
| Pass each draft's `languages` in the de, fr, hu and ja guards instead, and drop the other-language rule | left: those guards would stop counting other languages' signs, looser than before; F3's fix keeps both counts |
| Take the base language from `Language.of`, not by splitting the code | taken: `_base` |
| Write the condition as `base != "any" and other not in ("any", base)` | taken |
| Record the gate on the fixes | taken: below |

Every `weak_hits` call in the suite was counted at 2786619, at df57f26 and at c208375: only the new tests' five lines
differ, none of them lower. The review ends with this round: only minors were found, each fixed or answered here.

## Checks

`uv run tools/gate.py full` passed on dd566cd, df57f26 and c208375; CI passed on dd566cd and df57f26.
