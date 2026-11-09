---
subject: "Record Indonesian as having no source to seed from (PR #64)"
base: main (7909ef9)
head: 01ea47a
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the source and the catalogue by the main session)
verdict: clean
---

# Record Indonesian as having no source to seed from: code review

A docs-only change: no `id.toml`, and a follow-up in the research record of #61. The reviewer read
`humanizer-indonesia` at `62fe1aed5932` (`references/id-ai-tells.md`, `SKILL.md`, `references/voice-prib-id.md`) and
checked each claim against it and the catalogue, with a script over every `signs/*.toml` for citations across
languages. No sign is backed and dropped; the record's reasoning was loose in places. Minors only, fixed in this
session: no second round.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | the follow-up's lead, the A1 and A4 rows; the commit message | "None clears it" contradicts the record's own bar: A1 has English's measure (`reinhart-2025-pnas`) and A4 Portuguese's (`andrade-2026-portuguese`), "another language's measured one". They are left out for other reasons, and `_sign_sources` checks only that one source covers the language, so "as `_sign_sources` says" rested on its docstring | fixed in 20a3178: both said to meet the bar as written, left out as no language sign cites another language's source (AGENTS.md, Traps; `propose-signs`) and as both would flag plain Indonesian |
| F2 | minor | the second paragraph; the A1 and C1/A5/A3 rows | The essay's failures are against the semiformal preset, not the catalogue's bars: its 0.74 connectors pass C1's 3; the paper's 0.39 light verbs pass A1's 1 and 1.2's 0.40, so "the author's own paper has as many" was wrong; A3 has no bar | fixed in 20a3178: each figure names its bar; "as many" cut; A3 said to be present, not over a bar |
| F3 | minor | the second paragraph | "Not for judging a person's text" widened the source, which says its author's own writing | fixed in 20a3178 |
| F4 | minor | the plan's progress log | The research record's order says to record id in the plan, as #59 recorded hi | fixed in 20a3178: rows for vi (#62), it (#63) and id (#64) under #60 |
| F5 | minor | the D1 and A4 rows | Epoch openers are held by eight languages, not four (de, fr, ru, zh too); even sentences are already signs in en, it and pt | fixed in 20a3178: all named; three languages noted as the start of a case for an `any` sign |
| F6 | minor | the lead, "each pattern" | `SKILL.md`'s own checks (calques, personification, stock openers, fragments, steps 5b to 5d), D11's question headings and E's dash row went unweighed | fixed in 20a3178: a row for them, the read widened to steps 5b to 5d; none clears the bar |
| F7 | minor | the deferred forms | The design fix the forms wait for has no issue, so they could be lost when #60 closes | fixed in 20a3178: the record says no issue tracks it yet and the forms wait in the record |

## Refuted

- Section ids, F7, F8, G1, A3 (a calque of which and where), A6 (people and models alike), D4 (above the author's
  habit): as the source says.
- The fourteenth measurement (31 Oct 2026, an outline from Claude, yang mana, merupakan, nine short sentences, one
  triplet, the conclusion) and calibration 1.2 (a 516-word passage scored fully human, failing four bars): as the
  source says.
- The seven `any` signs: none has a check but `any-emoji-markers`, whose check holds emoji only;
  `any-assistant-closing-offer` reads documents only.
- 494 bytes: `any/check.md` 20,991 and `ja/check.md` 11,283, 32,274 of 32,768.
- The vi, it and ar leave-outs and the it seed's closers: as their files say.
- One source only: `wang-2026-human-detection` has no `id`; the source's head is still `62fe1aed5932`, and its
  `read_at` already says so.
- Copied text: only short phrases named as facts. Writing rules: no em dash, banned word or American spelling.
- AGENTS.md, CHANGELOG.md, README.md and CONTRIBUTING.md need no change, as nothing is seeded.

## Improvements

| Improvement | Answer |
|---|---|
| Link the deferral to the design-fix issue once filed | left: no issue exists; the record says so |
| B2's patut diperhatikan belongs to `any-didactic-aside`, not `any-significance-inflation` | taken in 20a3178 |

## Not covered

implementation, catalogue-contract, privacy-and-sources, plugin-contract, tests, compatibility and harness-integrity:
nothing in scope for them. The reviewer ran no gate; gate full passed on 01ea47a and CI passed on it.
