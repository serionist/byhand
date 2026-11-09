---
subject: "Seed the deck and sheet signs, read the slide-text signs for decks, and lower the layout budget (PR #90)"
base: main (8c5f659)
head: 4437832
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked by the main session)
verdict: clean
---

# Review: the deck and sheet signs (PR #90)

Step 3 of `docs/plans/2026-11-09-decks-and-sheets.md`: 89 files, most of them rendered sign files. One fresh Claude
Code agent on Opus 5.5 read the ground truth (`AGENTS.md`, `REVIEW.md`, #66, the plan, `propose-signs` and the
research record), the diff and the touched files in full, and applied every lens. It ran read-only probes against
`byhand.signs` and `byhand.render`: no catalogue problem, no budget problem, nothing stale, each new form finding its
`flags` and passing its `passes`. No blocker or major; its six minors were fixed in this session (7c6fdaf).

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `ja.toml`, `ja-count-titles` | The class took 一 and 1, so `## 1. 一つのアプリで受付から会計まで`, a single app, fired as a count | fixed: two to nine only; `test_a_deck_check_leaves_plain_titles_alone` in `tests/test_office_ja.py` |
| F2 | minor | `any.toml`, `any-formula-separators` | `=RACINE(B2*1,5)` and `=ARRONDI(RACINE(B2*1,5);2)` fire, and the comment said a decimal comma beside a semicolon passes | fixed: the comment says what fires and accepts it as weak, since English Excel reads such a comma as two arguments |
| F3 | minor | `any-emoji-markers`'s departure, `CHANGELOG.md` | Keeping the sign off decks drops emoji before slide titles too, which the count's emoji tell (each line's symbol) doesn't measure and `jinba-consulting-pptx` names for headings; CHANGELOG said list items only | fixed: `ja-emoji-titles` (weak, from that source), with machine and left-alone lines; CHANGELOG and the progress log say titles left decks elsewhere |
| F4 | minor | `any-takeaway-bar`, `any-invented-figures`, `ja-count-titles` | Examples in `what` and `instead` not in alphabetical order (`propose-signs` step 3) | fixed: reordered |
| F5 | minor | `CHANGELOG.md` | "until now read only for posts and documents": three of the 49 read mail already | fixed: "read for posts and documents but not decks until now" |
| F6 | minor | the PR and the progress log | No skip reason for flight-check's filler slides and agenda-restating close, or for groups of three | fixed: `any-generic-over-specific`, `any-closing-summary` and `any-rule-of-three` read decks already |

## Not verified by the reviewer, checked by the main session

- The count's figures it couldn't find in the research record (fake stats 80% against 53%, uniform bullet walls 21%
  against 17%, the section names and tell numbers) and `jinba-consulting-pptx`'s 2.4 and 4.103: read on the pages
  themselves while drafting, 2026-11-09.
- The `any-label-above-title` labels ("WHY NOW", "HOW IT WORKS"): invented; neither stands as a label on the
  downloaded Analyst Academy or Plus AI pages.

## Refuted

- The preamble and the closing offer firing on people's title and closing slides now that they read decks: nine
  closing slides and nine titles in four languages passed.
- `any-colon-titles`' English form firing on a French title: only `en/scan.layout.md` holds it.
- Grep and Python disagreeing on `[^;]*` across lines: Python finds as much or more, so the pass tests hold.
- The budget: 6,778 bytes plus 4,096, rounded up to 11 KB (after F3, 6,913 bytes, still 11 KB).
- The count of 49, the stated rule against what was done, the `any` rule's two languages, the header comments, the
  changed tests (each still holds its point), and the writing rules.

## Improvements

| Improvement | Answer |
|---|---|
| `any-label-above-title`'s `flags` and `passes` in the outline form | taken |
| `ja-count-titles`' `flags` not built on the source's own 3つの理由 | taken |
| Say why `de-dive-in` gains `deck` and `fr-article-rituals` doesn't | taken, in the PR: the French sign is about an article's frame |
| `test_office_de`'s test name says "only documents" | taken: "only documents and decks" |

## Checks

`uv run tools/gate.py full` passed on 4437832 and again on the fixes; CI passed on 4437832.
