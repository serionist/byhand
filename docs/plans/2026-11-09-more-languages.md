---
title: Seed signs for more languages, by their own sources
issue: "#49"
status: draft
approved_by:
approved_at:
---

# Seed signs for more languages, by their own sources

## Goal

The most spoken languages with sources that show their own signs get signs of their own, one language per PR, the way
Step 4 of the bootstrap plan seeded ten. A draft in Spanish or Hindi then reads its language's signs, not only the
`any` ones, and costs no more than a draft in English does today. The maintainer's first ask: the top 100 languages.

In scope: Spanish, Portuguese, Hindi and Arabic, in that order (rank 4, 9, 3 and 5 in `languages.toml`, ordered by
the sources each has), then each further language `find-sources` finds evidence for, most spoken first, while the
milestone is open. #13, Python reading a term's edges as Grep does, before Hindi.

Out of scope: a language with no source that shows its own signs: the `any` signs carry it (the bootstrap plan's
Risks, "Thin sources"). Translating another language's signs (AGENTS.md, Traps). Measuring excess words from datasets,
which the bootstrap's Risks named for `0.3.0`: a script and its own plan once two languages rest only on datasets. No
schema, render or skill change.

## Design

Each language is the same three moves, with the tools that exist:

1. **Sources:** `find-sources` for the language, when it has fewer than two that name signs; a PR of `sources.toml`
   entries and a research record (Spanish has three since #48).
2. **Signs:** `propose-signs` on them, structure first, as in Step 4. A sign is `strong` only when two sources show it
   or one shows it with model-labelled evidence; otherwise `usual` or `weak`. Every `passes` text is office text in
   that language.
3. **Plain work text:** `tests/test_office_<code>.py`, as `test_office_hu.py` is: invented mail, messages and
   documents in the language's office register and typography, which no strong or usual sign may fire on. It is what
   keeps a sign from accusing a person, and the only guard where no native speaker reads the PR.

Steps 1 and 2 may share a PR when the sources are few. The PR names the signs a native speaker should read first,
and one standing issue, "Native review wanted", lists each language seeded without one and those signs: one issue
for all, edited, never one per language. A native speaker's answers become a source of kind `review`, as the
maintainer's were for Hungarian.

Each language needs none of the budgets raised: a draft reads its language's files only. Over a budget, cut words
first (`propose-signs`, step 7).

### Alternatives

- **Wait for native speakers for every language:** none has offered; the `test_office` text, the `passes` texts and
  the conservative strengths stand in until one does, and the standing issue says so.
- **Many languages per PR:** faster, but a reviewer can't judge eight languages' signs at once, and one bad language
  holds back the rest.
- **The `any` signs only for the rest:** they're what every language already gets; this adds a language's own.

## Compatibility

None. New sign ids, new files under `plugin/signs/<code>/`; nothing a user has changes. No one-way door.

## Steps

1. **Spanish:** `propose-signs` on `humanizer-es`, `alonso-simon-2025-spanish` and `resende-castilho-2026-style`, plus
   any `find-sources` adds; `tests/test_office_es.py`.
2. **Portuguese:** `find-sources` (the pt Wikipedia translation, the Wikidata lead from #48, B18 of the research),
   then `propose-signs`; `tests/test_office_pt.py`.
3. **#13:** a term's edge in the tests reads combining marks as word characters, as Grep does; a Hindi and a Bengali
   case in `tests/test_catalogue.py`.
4. **Hindi:** `find-sources`, then `propose-signs`; `tests/test_office_hi.py`.
5. **Arabic:** the same; `tests/test_office_ar.py`, right-to-left text and Arabic punctuation among it.
6. **Each further language,** most spoken first, that `find-sources` finds evidence for: the same, a PR each; the
   progress log below lists them.

Each step ends with `finish-work`: the gate, `review-code` until clean, a PR.

## Tests

- Unit (CI): `byhand validate` (every `flags` and `passes`), `tests/test_office_<code>.py` per language,
  `tests/test_order.py`, the render budgets; #13's cases.
- By hand: for each language, `/byhand:write` once on a mail in it and `/byhand:check` once on its `flags` texts, in
  a session from this clone, recorded in the PR; the eval suite gains a `write-<code>` case per language.
- What none can show: whether a native reader finds the signs right. The standing issue stays open for that.

## Docs

`AGENTS.md`'s "Where the work stands" (the languages seeded), `README.md`'s list of languages, `CHANGELOG.md` under
Unreleased, Added (a line per language), this plan's progress log.

## Risks

| Risk | Answer |
|---|---|
| A sign written without a native speaker accuses plain writing | `test_office_<code>.py`, `passes` texts, strengths kept low without two sources; accepted until a native review |
| Sources are ports of English skills, so their signs are English's translated | `find-sources` and `propose-signs` take facts only and drop forks that add nothing; a sign needs the language's own evidence |
| A script without spaces (none planned here) or Indic marks break the word edges | #13 before Hindi; a language without spaces has no edges, as zh and ja |

## Progress log

| Step | Language | PR | State |
|---|---|---|---|
| 1 | es | | |
| 2 | pt | | |
| 3 | #13 | | |
| 4 | hi | | |
| 5 | ar | | |

## Plan review

None yet.
