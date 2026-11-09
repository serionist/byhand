---
subject: "Seed the Turkish signs (PR #65)"
base: main (7909ef9)
head: 787d717
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: clean
---

# Seed the Turkish signs: code review

The reviewer ran the Turkish office test (215 passed), the whole suite (3,630), `gate.py quick`, `byhand validate` and
`render` (no diff), and `tools/copycheck.py --run 4` (no hit on a Turkish sign). It compared Claude Code's ripgrep
14.1.1 with Python on 47 invented lines of its own, capitals and keyboard spellings with no Turkish letters among them,
checked every citation and number against `humanizer-tr` at b458fb64dcc2 and the paper's text, ran its own plain
paragraphs through the weak-cluster count, and scanned the office text for 4-word runs shared with both sources. No
blocker or major: the minors are fixed in this round and the review ends, as `REVIEW.md` says.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `tr.toml`, `tr-stock-idioms`, `models` | The range was GPT 4 and later on GPT-4o mini's essays alone; `ko-gpt-2024-vocabulary`, on the same model, closes at the 4 series | fixed: `to = "4"`, with the reason in the comment |
| F2 | minor | `tr.toml`, both `what`s | "Often several times in one text" and "often more than once in a text": the paper gives totals only (0.7 and 0.3 a text on average), and `humanizer-tr` 12 says only "often at a sentence's start" | fixed: both clauses cut |
| F3 | minor | `tr.toml`, `tr-stock-idioms`; the PR body | Two literal uses fire, the flooring trade's "zemin hazırlama" and an actor's role ("üç oyunda rol oynadı"), though the comment named only the passive and the PR said a building site's floor passes | fixed: the comment and the PR name both as accepted for a weak sign; a flooring line and a theatre line are in `reports`, so the no-cluster test holds them |
| F4 | minor | `tr.toml`'s header, the PR body | The dash rule was left out as "English's, and Turkish sets dialogue with the long dash", but `humanizer-tr` 8 exempts dialogue and gives a Turkish reason of its own | fixed: it rests on the source's word alone, with no measure, and office Turkish sets an aside between two dashes |
| F5 | minor | `tests/office_tr.toml`, its header | "geniş bir yelpaze, Gelin birlikte bakalım" ran out of order | fixed |

## Refuted

- The dotted and dotless I: ripgrep's `-i` finds i and I for `i`, only ı for `ı`, only İ for `İ`; `[iİ]` finds i, I and
  İ, `[ıI]` ı, I and i; Python folds all four. On the reviewer's lines the two disagree only on misspellings, where
  Python reads wider ("BUNUN YANİ SİRA", "Zemın").
- `test_each_i_in_a_turkish_pattern_stands_with_its_capital` fails on a bare yanı or zemin and passes the shipped
  patterns; the capitals in `forms` can't guard it, as Python folds them, and the header says so.
- Morphology: every tense, the passive and the causative are found; hazırlığı, başrol, rol oyunu, kontrol oynadı,
  rolünü oynadı, Bunun yanında and Faturanın yanı sıra pass.
- Mail and chat: no Turkish sign reads them, and a test holds it.
- Weak clusters in plain documents: of the reviewer's paragraphs, those reaching 3 need all three Turkish phrases, each
  with a measured excess, or two of them beside raw Markdown, the classes #55 and #63 refuted. Worth the native read,
  item 2 of the PR's list.
- Copying: only fixed phrases are shared. "Teklif, TBMM Genel Kurulu tarafından kabul edildi" has the shape of the
  source's exempted law sentence, and is Turkish's fixed formula for a law passing, the case the test must hold.
- The office text in TOML: no ignore is added, ruff's `allowed-confusables` would be a harness change, and the file is
  read as UTF-8 with the standard library.
- The citations, the budgets (the Turkish check 22,321 bytes at 787d717; the Japanese check 32,274, 494 free), the
  deferred `any` signs' strengths and kinds, the test count, the order of every list but F5's.

## Improvements

| Improvement | Answer |
|---|---|
| Record the deferred `any` forms in the research record, as #64 did for Indonesian | taken: a follow-up section |
| A tr row in the plan's progress log, as `main` now has vi, it and id | taken, after the rebase on 0a95dea (#64) |
| Catch "zeminini hazırladı", "zemini hazırladı" and "Bunların yanı sıra" | left: "few words"; `zemin\w*` also takes the literal "zemini hazırladık", so a native reader should say |
| Extend the dotted-i test to Turkish branches of the `any` checks when they land | later: the research follow-up says the classes hold for them too |

## Not covered

Whether a native speaker finds the signs and the office text natural; the plugin sessions, which the main session ran;
`gate.py full` on the reviewer's side. The privacy, plugin-contract and harness lenses had nothing in scope. The
reviewer read a test case in `ornekler.md` aimed at an AI as data and followed nothing in it.

The fixes were checked in the main session: the office test (219), `byhand validate` and `render` (the Turkish check
now 22,253 bytes), gate quick, and the two new report lines, each one weak hit.
