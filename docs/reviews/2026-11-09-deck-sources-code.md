---
subject: "List the sources for deck and sheet signs (PR #83)"
base: main (c686adf)
head: 368e83c
date: 2026-11-09
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, read only; its findings checked against the sources by the main session)
verdict: clean
---

# Review: List the sources for deck and sheet signs (PR #83)

Round 1 by a fresh reviewer, read only. It checked every new entry against `load_sources`, the licences at the
commits and pages named, the six GitHub paths at their `read_at` commits, and the record's figures against the live
pages and papers (Analyst Academy's counts, Leinonen et al., both MBABench papers, Grossman et al., the Japanese,
Chinese and Korean files). Six minors, all on what the record says its sources show; each was checked at its source by
the main session and fixed in `468e401`. Only minors, so no second round.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | the record, Searched | A paragraph between the `ko` and `de` rows cut the table: the rows for ten languages rendered as one run of pipes | fixed: the paragraph sits below the table (`468e401`) |
| F2 | minor | the record, `poeltl-2026-mbabench-2`, Summary 5, Seeding; the PR body | The "rounded to" label was offered as a sign a sheet's text shows, but the paper's house standard (Appendix G) asks for a "rounded to" note; the habit is its mismatch with formulas that don't round, which no text shows. A person's sheet following such a convention would be flagged. Opus 5 also writes "shown to" | fixed: the mismatch is the habit, the label no sign, Opus 5 named (`468e401`) |
| F3 | minor | the record, `flight-check`; the PR body | Filler titles ("Overview", "Context") were offered as a sign, against the record's own Summary 2 (topic titles commoner in real decks) and the plan's I2 | fixed: a slide with no finding of its own is the content candidate; the title form gives none (`468e401`) |
| F4 | minor | the record, `futura-2023-chatgpt-excel`, Summary 7, Seeding | The Portuguese page shows commas with a Portuguese function (FILTRO), not English names; only the French page shows English names, so two languages hold for the separator alone | fixed (`468e401`) |
| F5 | minor | the record and `sources.toml`, `decksmith-2026-seven-signs` | DEV labels the post "AI-assisted", the reason borncity was dropped, and the record said more about its render checks than the post does | fixed: dropped, with its reason; 17 sources (`468e401`) |
| F6 | minor | the PR body | The plan's Step 2 names E6 as entries; uxdesign.cc was dropped without a line in the PR | fixed: the PR body says why |

Refuted, each checked: `lt-slide-skills` listed as MIT (its LICENSE.txt says "MIT License", and a comment records
it); `anthropic-skills` not open (both LICENSE.txt files at `2c5958ecac7c` are Apache 2.0); Finnish not searched (the
seed languages are those the plan names, all searched); vendor translations counted as English against AGENTS.md's
"a translated page counting" (stricter, not looser); three cards cited beside a count that rates three boxes weak (the
count's "groups of three by habit" holds it); Kimi K3's "displayed to" (the paper's paraphrase); report-de-ai-voice's
licence without its lineage (already facts only).

Not covered, nothing in scope: implementation, tests, compatibility, plugin contract, harness integrity. The reviewer
did not re-read the dropped pages beyond the record's reasons, uxdesign.cc, or Plus AI's page history.

Improvements:

- I1, say in the record why a vendor's own translations don't count as other languages: taken (`468e401`).
- I2, name report-de-ai-voice's Wikipedia lineage in its licence, as `humanizer-ru` does: taken (`468e401`).
- I3, the Open line called all three sheet sources finance models, which Grossman's small exercises are not: taken
  (`468e401`).

## Checks

`uv run tools/gate.py full` passed on `368e83c` (3,845 tests); CI passed on `368e83c`; `uv run byhand validate` and
gate quick passed on `468e401`.
