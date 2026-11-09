---
subject: "Add sources for Italian, Turkish, Vietnamese and Indonesian (PR #61)"
base: main (bc8291a)
head: b4056fe
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, every lens; F1 checked against the repo by the main session)
verdict: clean
---

# Review: Add sources for Italian, Turkish, Vietnamese and Indonesian (PR #61)

One fresh reviewer read the pack (`files.txt`, `scope.diff`), issue #60, the plan's move 1, the find-sources skill,
the earlier research records and the pt-hi-ar review, and checked each new source against the work itself: licence
files, commits, feed paths, arXiv versions, the Turkish article's notice and numbers, the three wiki pages' revisions.
Three minors, no blocker or major, so no second round. The main session confirmed F1 with `gh api`
(`eval/corpus/ATTRIBUTION.md` at `51f6e3ed3c7c`) before fixing it. The dated record is never edited after merge, so
the minors were fixed now.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | the record, `humanizer-it` row and the order's it row | Its 11 model texts were written to be saturated with its own markers under nominal model labels, so the 0 against 5 hard bans shows only that the scanner finds what was planted; the row read it as a measure, and named Manzoni and Verga (the literary fixture) as the formal control. `propose-signs` could have drafted `claude`, `gemini` and `gpt` signs on no evidence | fixed in `adce4c9`: the limit said, no model scope, the literary tests kept, Italian's first place resting on the reader study, the cues and the lists |
| F2 | minor | the record, `scrittura-italiana` row | "78 patterns, drawn from Italian manuals": the patterns adapt Wikipedia's page; the manuals back its editorial guides | fixed in `adce4c9` |
| F3 | minor | the record, `humanizer-indonesia` row against the order's id row | One line allowed `usual` signs from the one source, the other asked for a second source, which no run found: two opposite instructions for the id PR | fixed in `adce4c9`: a sign needs a second source showing the same pattern, an `any` sign's or another language's measured one; with none, id is recorded as having nothing to seed from |

## Refuted

- The counts: 50 to 57 sources; 82 to 80 languages with no source (id and tr leave, th stays); the ranks match
  `languages.toml`.
- Hebrew and Finnish: neither code is in `languages.toml`, which calls its set a one-way door; `signs.py` refuses an
  unknown code, so leaving them to the maintainer is right, and he is rightly named nothing to seed from.
- The repos: each `read_at` commit is the default branch's head and every feed path exists at it; each LICENSE file
  matches the entry (humanizer-tr's is MIT although GitHub reads NOASSERTION); the pattern counts match.
- The papers: `farrell-2026-translators` v5 is the latest; arXiv says CC BY-NC-ND 4.0, the PDF CC BY-ND 4.0, and the
  stricter is recorded. `bergin-atasoy-2026-turkish`'s notice says CC BY-NC 4.0 against Zenodo's CC BY 4.0, the
  stricter kept, and every number matches the article. `lee-2026-korean`'s Vietnamese words and its "no prevalence
  bound" match.
- The wiki pages: revisions, revision counts and the translation origins of he and th, fi created as a new page.
- Detector evasion among the kept repos: none; each disclaims it.
- The order: it, vi, tr holds on the evidence; vi before tr weighs source count against one measured study.
- Writing rules: no em dashes, banned words or American spellings; LF, NFC, no zero-width characters. No sign changed.

## Improvements

| Improvement | Answer |
|---|---|
| `avoid-ai-writing-multilingual`: watch `SKILL-RO.md` and `SKILL-SV.md` too, for the same reason as `SKILL-IT.md` | taken in `adce4c9` |
| `farrell-2026-translators`: a comment saying why its licence is the stricter one | taken in `adce4c9` |
| `humanizer-it`: say why it isn't detector evasion | taken in `adce4c9`: its README's line that bypass is the wrong target |
| The Thai `\b` note: `terms` already get no `\b` for a `spaces = false` language; only a hand-written `check` needs care | taken in `adce4c9` |

## Not covered

The implementation, plugin-contract, tests, compatibility and harness lenses had nothing in scope: no code, plugin,
test or harness file changed. The reviewer ran nothing (the gate and CI passed on `b4056fe`), did not check the
style guides' pages, and spot-checked rather than reread most dropped finds.
