---
subject: "Seed the Italian signs (PR #63)"
base: main (c2b4841)
head: 0349234
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: clean (round 2, c3d2639)
---

# Seed the Italian signs: code review

The reviewer ran the Italian office test and the whole suite, `byhand validate`, the budgets in memory (Japanese's
check at 32,740 bytes, 28 free), and Python against ripgrep 14.1.1 on every Italian and `any` pattern over 236 lines
(they agree). It compared the old and new Chinese alternations by brute force over 67,112 generated lines: the preamble
matches the same lines with the same spans, and the self-reference adds only two mixed-script lines. It ran the Italian
checks over humanizer-it's own human fixtures (Pinocchio, Manzoni, Verga, 24 Wikipedia texts): nothing fires. It
scanned `it.toml` and the office test for 4-word runs shared with the three Italian lists (only fixed phrases, and
F5). No blocker or major: the minors are fixed in this round and the review ends, as `REVIEW.md` says.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `it.toml`, `it-dash-pivots` | Speech opened after a colon fired as a pivot: "Marta disse: — Va bene.", "Il falegname rispose: — Niente." The sign's comment says a line of dialogue is not found | fixed: the left side may not end in a colon; both lines in `LEFT_ALONE`, "Nota: il server è fermo — torna domani." in `FORMS`. Portuguese has the same miss |
| F2 | minor | `it.toml`, `it-dash-pivots` | The check counts a lone pivot, which scrittura-italiana 21 and humanizer-it's false positives call Italian (the burst is the tell); the citation said "not a lone dash" | fixed: the comment says Grep reads a line, not a paragraph's count, so a lone pivot counts once as a weak hit, a native reader's call; the citation says what 21 says. Item 2 of the PR's native-read list |
| F3 | minor | `any.toml`, `any-ai-self-reference`, the Italian branch | Three of its four lacks (non ho opinioni, non posso accedere, non posso navigare) are in no Italian source, against #55's F13 | fixed: only non ho accesso (SKILL-IT 30); the `MACHINE` lines use it, and "In quanto IA, non ho opinioni…" is in `REPLIES` |
| F4 | minor | `any.toml`, `any-generic-over-specific`; `it.toml`, `it-even-sentences` | Wang et al.'s few quotes and numbers are in E.5, not D.5; Farrell's 5.4 is about English influence, the cue is in 5.3.4 | fixed: E.5; 5.3.2, 5.3.3 and 5.3.4 |
| F5 | minor | `it.toml`, `it-staccato-fragments` | The `what` and `instead` followed avoid-ai-writing's wording (three or more fragments in a row, each…; keep a fragment that earns its emphasis) and scrittura-italiana 77's order | fixed: rewritten on our own words and order |
| F6 | minor | `it.toml`, `it-staccato-fragments`, `it-even-sentences` | The rendered text described a flyer's or a job ad's run of facts ("Pizzeria Da Gino. Forno a legna."), and `it-even-sentences` could read the same run, a third hit by the rendered rule (#55's F29 class) | fixed: staccato's fragments claim nothing, and a list of items or requirements is not one; `it-even-sentences` reads full sentences |
| F7 | minor | PR #63's description | "A line mixing the two scripts now does too" holds for the self-reference only; `any-negative-parallelism` holds the set-up foil, not non solo… ma anche itself | fixed: the description says so |
| F8 | minor | `any.toml`, `any-ai-self-reference` | It misses "Come modello di IA, non ho accesso", "… sviluppato da OpenAI", "Però, in quanto IA", "In qualità di IA", "non sono in grado di" | wontfix: a strong sign wants precision, as #53's round 4 accepted; with F3 it misses more, and item 1 of the native-read list asks for the forms |

## Refuted

- The self-reference on a person's "as for" line: "Come modello di intelligenza artificiale, non ho accesso a niente:
  l'azienda li blocca tutti." fires, the class #53's rounds 4 and 5 accepted for "Como modelo de lenguaje, no tengo…".
  The branch keeps only the source's roles; "Come IA…", contrasts and the third person pass; a quoted bot reply fires
  by design.
- Weak clusters on plain text: of 13 plain paragraphs only two reach 3, a bold Markdown list where two `any` checks hit
  one label, and three stacked tells, both classes #55 refuted. Mail reaches 2 at most.
- The Chinese rewrite: no change beyond two mixed-script self-reference lines; Grep agrees.
- The other citations, the order, the docs, the `read_at` revisions, the budget figures: as claimed.
- The Italian preamble and knowledge-cutoff forms left out: a departure from the plan's move 2, said in the PR with the
  budget's reason and left to the maintainer.
- "Milano—Roma" and "9:00 — Apertura lavori." fire: edge cases for a weak sign.

## Improvements

| Improvement | Answer |
|---|---|
| Cite scrittura-italiana 69 on `it-inflated-stakes`, which lists "In un mondo sempre più X…" too | taken |
| Apply F1's colon guard to `pt-dash-pivots` | later: its own issue, as it changes another language's sign |

## Not covered

Whether a native speaker finds the signs and the office lines natural; the plugin sessions, which the main session
ran; `gate.py full` on the reviewer's side (CI passed on 0349234). The privacy, plugin-contract and harness lenses had
nothing in scope.

The fixes were checked in the main session: the office test, `byhand validate` and `render` (Japanese's check at 32,695
bytes, 73 free), ripgrep against Python on the two changed patterns, and `copycheck` at 5 words (only the fixed term).

## Round 2

A fresh reviewer, on c3d2639: the round-1 fixes, rebased on the Vietnamese seed (af235ef, #62), and the room that
rebase needed in the check budget. With #62 the Japanese check (`any/check.md` beside `ja/check.md`) would have been
24 bytes over before the Russian rewrite; c3d2639 also regroups the English branch of `any-assistant-preamble`, which
had written its noun list four times and its linking words three. Verdict: clean. F1 to F7 and the improvement hold,
each with the line that covers it: the two colon lines in `LEFT_ALONE` fail on 0349234's dash check; the `REPLIES` line
"In quanto IA, non ho opinioni…" fails on its self-reference. The reviewer rebuilt the old and new English branch from
named pieces: both are the union of the same six branches, each anchored at the line's start and end, so a regrouping
changes no match. Over 165,233 lines the two find the same 7,081 lines with the same spans, and over 450,030 the
Russian rewrite changes none; ripgrep 14.1.1 agrees with Python on every line. The budget: 32,274 bytes, 494 free.
The suite (3,415) and gate quick passed on c3d2639.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| N1 | minor | `it.toml`, `it-staccato-fragments`, `what` | F6's exemption, "a list of items or requirements is not one", left out the tic the source flags: scrittura-italiana 77's own example is a list of items ("Consegna al piano. Zero plastica. Disdetta senza penali."), as is two thirds of the sign's `flags` | fixed: the fragments echo a sentence for a punchy beat, and a flyer's, menu's or job ad's list of facts standing on its own is not one |

Refuted: two spaces before a dialogue dash, "«Va bene» — disse Marta." and a pivot right after a colon (edge cases for
a weak sign, rare); a bold role before the self-reference (a model doesn't write it); the PR body's 21.3 KB (21.0 at
c3d2639, now said).

| Improvement | Answer |
|---|---|
| The staccato `instead` said "what changes", which fits only the library example | taken: "Say it in one sentence with a verb" |
| The note on the Chinese and Russian rewrites sat in `any-ai-self-reference`, though most of it is about `any-assistant-preamble` | taken: the preamble's comment names all three rewrites, the self-reference's names its Chinese classes |

The fixes were checked in the main session: `byhand validate` and `render` (the Japanese check unchanged at 32,274),
`copycheck` at 5 words (no hit on the staccato sign), gate quick. The review ends here: no blocker or major is open.
