---
title: Key the shared signs' checks by language in the catalogue's schema, and give the patterns only to scan
issue: "#71"
status: draft
approved_by:
approved_at:
---

# Key the shared signs' checks by language in the catalogue's schema, and give the patterns only to scan

## Goal

A check reads less than half of what it reads today, in every language, and a new language's forms of the shared
signs no longer cost every other language's check. Today every `/byhand:check` reads `any/check.md`, 20,991 bytes,
whose patterns hold every language's forms of the shared signs; a Japanese check reads 32,274 of its 32,768-byte
budget, and the Turkish and Indonesian forms wait for room (`docs/research/2026-11-09-sources-it-tr-vi-id-he-th-fi.md`).
The two changes #71 names, both agreed by the maintainer on 2026-11-09:

1. An `any` sign holds its check per language, so a scan runs only its language's forms.
2. The main session reads check files without patterns; only the `scan` agent reads them.

In scope: the schema of `check` on an `any` sign, `signs.py`, `render.py` and its budgets, the `check` skill, the
`scan` agent, `any.toml`'s checks split into forms, the tests, the docs.

Out of scope: the Turkish and Indonesian forms the research record defers, each in its own PR once this lands; a
language sign's `check`, which stays one pattern; `write`'s files, which hold no pattern and do not change; decks and
sheets (`0.4.0`).

### The measure

Bytes read per check, from `render.render` on `origin/main` at `26884bc` and a prototype of this design (the forms
split by hand in a script, not committed). The main session's files are exact: they are today's lines without
`Pattern:`. The scan files are near: the build's split sets them.

| Language | Today: check files, main session | After: `check.md`, main session | Saved | After: `scan.md`, scan | Saved in scan |
|---|---|---|---|---|---|
| `ar` | 22,385 | 8,435 | 13,950 | 2,402 | 19,983 |
| `de` | 27,582 | 11,579 | 16,003 | 6,743 | 20,839 |
| `en` | 28,600 | 12,433 | 16,167 | 8,201 | 20,399 |
| `es` | 26,279 | 11,140 | 15,139 | 4,894 | 21,385 |
| `fr` | 29,697 | 12,945 | 16,752 | 6,116 | 23,581 |
| `hu` | 27,157 | 11,808 | 15,349 | 3,536 | 23,621 |
| `it` | 22,642 | 8,633 | 14,009 | 2,047 | 20,595 |
| `ja` | 32,274 | 15,184 | 17,090 | 5,550 | 26,724 |
| `ko` | 28,930 | 13,017 | 15,913 | 4,164 | 24,766 |
| `pt` | 23,942 | 9,656 | 14,286 | 4,355 | 19,587 |
| `ru` | 30,199 | 13,150 | 17,049 | 7,395 | 22,804 |
| `tr` | 22,253 | 8,309 | 13,944 | 1,810 | 20,443 |
| `vi` | 22,146 | 8,196 | 13,950 | 1,961 | 20,185 |
| `zh` | 29,914 | 13,414 | 16,500 | 5,327 | 24,587 |
| `zh-Hant` | 31,027 | 14,263 | 16,764 | 5,805 | 25,222 |
| a language with no signs of its own (`hi`) | 20,991 | 7,282 | 13,709 | 1,405 | 19,586 |

- **Pasted text:** the main session reads the second column, 54 to 65% less.
- **A file:** today the main session and `scan` each read the first column; after, the main session reads the second,
  plus `scan`'s `ran` line (below, 244 to 740 bytes), and `scan` reads the fourth. A Japanese file: 64,548 bytes
  today, about 21,300 after.
- **A draft:** unchanged, to the byte. `write`'s files print no pattern, and the `any` signs' lines in them do not
  change: the largest mail read stays 12,834 bytes (`zh-Hant`), the largest post or document 15,203 (`ja`).
- **The budgets:** `check` drops from 32 KB to 16 KB; a new `scan` budget of 9 KB; `mail`, `document` and `layout`
  stay, as nothing frees them. Each new one is the largest read at the build plus at least 512 bytes, rounded up to a
  whole KB, as `document` was set over its 15,203: the build sets them from its own render.

## Design

### The schema

`check` on an `any` sign is one pattern or a table of forms:

```toml
[[sign]]
id = "any-closing-summary"
# ... the other keys, as today; a language's note sits above its own form
check.en = '^\W*(?:in conclusion|in summary)\b'
check.de = '^\W*zusammenfassend\b'
check.ru = '^\W*(?:в заключение|подводя итог)\b'
flags = "..."
```

- A key is a language code from `languages.toml`, a variant's included, or `any` for a form every language reads.
  A form goes under the language it is written in; one written for both scripts (`[为為]`) under the base, `zh`.
  A chatbot's leftover that turns up in text of every language stays under `any`, even when its words are English:
  `any-unfilled-placeholder`'s `[Your Name]` branch, `insert_…_here` and `20\d\d-xx-xx`, which the de, hu and ja
  office tests find in their own mail. It costs every scan about 60 bytes more than The measure counts.
- A string stays what it is today: one pattern, read in every language. A language-free check (a Markdown artefact,
  an emoji, a tool's token) is written so and needs no change. `check.any` alone is allowed, not needed.
- A sign mixing both, `any-chatgpt-citation-markup` with its German `gehe zu suche nr`, has `any` and `de`.
- A table on a language's own sign is refused: its language is its file's, so its `check` stays one string. A table
  with no form, a form that isn't text, or an unknown key is a problem, as an unknown key is today.
- The forms are dotted keys, `check.en = '…'`, where `check` stands today: `tomllib` reads them as one table, so no
  key moves, no line holds two forms, and each language's comment stays above its form. An inline table would put a
  2 KB pattern and its neighbours on one line.

`flags` and `passes` stay one text each, and `validate` checks them against every form: `flags` must be found by the
forms together, `passes` by none of them. That is today's proof exactly, as today's one alternation is the forms
together. Per-language examples are left out:

- the per-language proof is already in `tests/test_office_<code>.py`: a machine line per branch, and plain work text
  in the language that no sign counting alone may find, which is a stronger `passes` than one sentence;
- after this change those machine lines read each sign through the forms a check in their language runs, so a form
  under the wrong key fails there; and a test in each office file holds that every `any` form under its code has a
  machine line there that the form alone finds, so a new language's forms can't land unproven;
- per-language `flags` and `passes` would add about 120 texts in eleven languages, rendered nowhere and duplicating
  those tests, and a second table shape in a one-way-door schema for no reader.

The forms with no machine line in their language's office test today get one in this change (13 in the prototype's
split, most of them weak signs' and English forms'): that test fails until they do.

### The package

`signs.py`:

- `Sign.forms`: each form as written, in NFC, by its key, in place of `grep`. A language sign's one pattern is
  under its language, an `any` sign's string under `any`, a `terms` pattern under its language: render reads one
  field for every sign.
- `Sign.pattern`: Python's reading of every form together, through `as_grep`, as today; `validate`, `copycheck` and
  the tests that name no language use it.
- Each form passes `_checked` on its own, and a problem names its key: `signs/any.toml: any-x: de: Grep can't run …`.
  Grep gets each form as written, in NFC, as today.

`tests/conftest.py`: a fixture beside `weak_hits` reads a sign as a check in a language runs it, `as_grep` on its
forms under `render._scopes(catalogue, code)`, or None. The office tests use it, and `weak_hits` given its languages
too, in place of conftest's hand-built `{"any", code, _base(...)}`: the tests read exactly the scopes `scan_files`
renders, and the package gains no method only tests call.

`render.py`, under `plugin/signs/<scope>/`, where a scope is `any`, a variant's base or the language (`_scopes`):

| File | Holds | Read by |
|---|---|---|
| `check.md` | every prose sign of the scope, its line as today's without ` Pattern: …`; the header loses the pattern line | the main session, `check` and `learn`'s screen |
| `scan.md` (new) | one line per form under the scope's key: `- <id> (<strength; ranges; kinds>): `<form>``; for a language, its own signs' patterns and the `any` signs' forms under its code; for `any`, the forms under `any` | `scan` only |

- `scan.md`'s brackets are `check.md`'s, so `scan` filters by kind and family as it does today. Its header says
  what a pattern is; the weak-cluster and versions lines stay in `check.md`, which the main session counts with.
- `scan_files(catalogue, language)`, beside `check_files`; `Budgets.scan`; `budget_problems` names a scan over its
  budget as it names a check.
- A language with forms and no signs of its own (Turkish's deferred forms, say, had Turkish no signs) gets a
  `scan.md` and no `check.md`.

### The plugin

- **`check`, step 4:** read the `check.md` files, as today. **Step 5:** start `scan` with the file, the kind, the
  families and the `scan.md` paths of the same scopes (`any`, a variant's base, the language), which may not all
  exist. **Step 6:** a sign in `scan`'s `ran` line is found where `scan` hit it and nowhere else, as a patterned sign
  is today; read the text for every other sign. Pasted text had no scan: read it for every sign, by its description
  and its Words. No `ran` line: read for every sign.
- **`scan`:** reads the `scan.md` files it is given, skipping one that isn't there; one line per form, the pattern
  in the backticks after the brackets; runs Grep as today. It ends its answer with `ran` and the ids it ran, so the
  main session knows which signs the patterns covered in this language: the main session no longer sees which have
  one.
- **`learn`:** no change. Its screen reads `check`'s `SKILL.md` and follows steps 1 to 7, so it passes `scan` the new
  paths and reads its `ran` line with them; a pasted sample is read by descriptions, as `check` reads pasted text.

Today a Hindi file meets `any-closing-summary` as patterned, so the main session leaves it to `scan`, whose
alternation holds no Hindi form: no one looks. With the `ran` line, a sign with no form in the text's language is
read for.

### Alternatives

- **The `any` forms in each language's `check.md`, patterns kept:** only change 1. A Japanese check would still read
  every Japanese pattern in the main session, about 20 KB.
- **Only change 2:** `scan` would read every language's forms of the `any` signs, 14 KB a scan and growing with each
  language; the issue names both.
- **The `any` signs' language-free patterns copied into each language's `scan.md`:** one file fewer per scan, a
  hundred copies in the repo. `_scopes` already lists the files a check reads.
- **A language sign per form (`de-closing-summary`):** a new id for each, and a style's `keeps` would need every
  language's. Ids are a one-way door.
- **A marker in `check.md` on each sign with a pattern, in place of `ran`:** `any/check.md` is shared, and whether an
  `any` sign has a form depends on the language; `scan` knows, so it says.
- **`scan.md` lines without the strength:** 8 bytes a line, and `scan` would need a second bracket format.

## Compatibility

- **The catalogue's schema,** a one-way door (AGENTS.md): `check` on an `any` sign also takes a table of forms keyed
  by language code. Agreed by the maintainer in #71 (2026-11-09). It only adds: every row of today's catalogue
  validates unchanged before the split, and a string `check` keeps its meaning. The code PR names the schema in its
  title.
- **A sign's id:** none changes; a style's `keeps` holds as it is.
- **Language codes, kinds, the skills' and agents' names:** unchanged.
- **The rendered files** are the contract the skills read: `check.md` loses its patterns and `scan.md` is new.
  Users never see the catalogue, and the skills ship with the files in one plugin version, so no user meets one
  without the other; the gate's `render --check` holds the files equal to the catalogue.
- **CHANGELOG:** under Unreleased, Changed; nothing for a user to move.

## Steps

One PR, a commit per step.

1. **The schema and the loader.** `signs.py` (`forms`, `pattern`, the rules above), `copycheck.py`'s
   `pattern` reading a table's forms, the users of `grep` in the tests moved to `forms`. Render's output does not
   change: every sign still has one form. Proven by `tests/test_catalogue.py`'s new cases and `tests/test_copycheck.py`.
2. **The files and the plugin.** `render.py` (`check.md` without patterns, `scan.md`, `scan_files`, `Budgets.scan`
   at 32 KB for now), the `check` skill's steps 4 to 6 and the `scan` agent, in one commit, since neither works
   without the other. `any/scan.md` holds every `any` form until step 3. Proven by `tests/test_render.py`.
3. **The split.** `any.toml`'s multilingual checks into `check.<code>` forms, the leftovers under `any`; the comments that cite the check budget
   (`any-assistant-preamble`'s, the Vietnamese closing offer "waits for room") reworded; a machine line for each form
   with none, and each office file's test that every form under its code has one; the office tests' machine lines,
   and `weak_hits` given its languages, read through conftest's new fixture. Then
   the budgets: `check` and `scan` from the render by the rule in The measure, 16 KB and 9 KB if it agrees. Proven by
   `byhand validate`, the office tests and `budget_problems`.
4. **By hand,** then the docs, then `finish-work`: `uv run tools/gate.py full`, `review-code` until clean, a PR.

## Tests

- **Unit (CI):**
  - `tests/test_catalogue.py`: a table loads as forms and a string as the `any` form; a table on a language sign, an
    empty one, a form that isn't text and an unknown key are each refused; a form Grep can't run is named with its
    key; `flags` found by one form passes and by none fails; `passes` found by any form fails; `pattern` reads every
    form; dotted `check.de` keys load as a table; the nukta case reads its pattern from `hi/scan.md`.
  - `tests/test_render.py`: `check.md` holds no pattern; a `de` form renders in `de/scan.md` only, an `any` form in
    `any/scan.md` only; a `zh` form reaches a `zh-Hant` scan through `scan_files`; a `scan.md` line's pattern is its
    form's NFC text; a language with forms and no signs gets `scan.md` alone; `budget_problems` names a scan over
    budget; no form holds a backtick.
  - `tests/test_office*.py`: every machine line read through its language's forms, the 13 new ones among them, and
    in each file a test that every `any` form under its code has a machine line there that the form alone finds.
  - The gate: `byhand validate`, `byhand render --check`, the budgets.
- **By hand,** `claude --plugin-dir plugin` from this clone, on the current Claude Code, the main session on Opus
  and `scan` on its Haiku: `/byhand:check` on the `check-en` and `check-ja` cases' pasted texts, and on a file in
  `en`, `de`, `ja` and `zh-Hant`. From each transcript's Read calls: the main session read only `check.md` files,
  `scan` only `scan.md` ones, `scan` ended with `ran`, and the hits are those `origin/main`'s plugin finds on the same file, but for another
  language's forms. Then the `learn-from-samples` case, and `learn` on one sample given as a file: its screen starts `scan` with the `scan.md`
  paths. The eval cases `check-de`, `check-hu`, `check-zh` and `learn-from-samples`, with `claude plugin eval`.
- **What none can show:** whether a reader of descriptions alone, on pasted text, finds what the patterns found; the
  pasted eval cases are the nearest.

## Docs

- `docs/USAGE.md`: the table of files (`check.md` without patterns, `scan.md`) and the budgets (`check` 16 KB, a
  `scan` row).
- `any.toml`'s header: the example sign's `check` comment names the table of forms.
- `.claude/skills/propose-signs/SKILL.md`, step 5: an `any` sign's check is a form per language, `check.<code>`,
  `check.any` for a chatbot's leftover every language meets; a new language's forms go under its code, each with a
  machine line in `tests/test_office_<code>.py`.
- `CHANGELOG.md`, Unreleased, Changed: `/byhand:check` reads less than half as much, in every language.
- `plugin/README.md` already says `scan` runs the patterns and pasted text gets a reading: no change. `AGENTS.md`: no
  path, command or rule changes. The bootstrap plan's schema table is a dated record and stays.

## Risks

| Risk | Answer |
|---|---|
| A text in one language quoting a chatbot line in another (a German mail with "As an AI language model"): `scan` runs only German and `any` forms, and the `ran` line leaves the sign to it | Accepted: a check judges one language per text (step 2), as a language's own signs already do; the main session reads the quoted line too |
| Pasted text loses the patterns: a tool's token the description doesn't spell (`oaicite`) | Accepted, the maintainer's call; the description names the tool, and the pasted eval cases are tried |
| A form split under the wrong key | Each form's machine line, read through its language's forms, fails; the 13 forms with none get one |
| `scan` (Haiku) drops the `ran` line or lists a sign it didn't run | No `ran` line: the main session reads for every sign. A wrong id: that sign is missed, as a missed Grep hit is today; tried by hand |
| 16 KB leaves Japanese about 1.2 KB of descriptions to grow | Accepted: over it, cut words first (`propose-signs`, step 7), as today |
| A missing `scan.md` path costs a failed Read | `scan` skips it, as the check files' missing paths are skipped today |

## Plan review

### Fit

The plan at `a7d8b7a`, by a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, with the change's own
question: does it free the most bytes a session reads, for every language and the 80 to come, with the simplest
schema and the fewest new parts? It found yes, with I3 and I4 trimming it; the one `flags` and `passes` per sign, the
`ran` line and the strength in `scan.md` kept. Prior art from the repo's research records only; no live repo or
Context7 read. Answers by the author on the maintainer's standing word ("take recommended improvements"), 2026-11-09.

| # | Improvement | Answer |
|---|---|---|
| I1 | A chatbot's leftover written in English (`[Your Name]`, `insert_…_here`, `20\d\d-xx-xx`) stays under `any`: the de, hu and ja office tests find it in their mail, and under `en` their scans would stop | taken |
| I2 | A lasting test in each office file, every `any` form under its code with a machine line the form alone finds, in place of a one-off sweep: a new language's forms can't land unproven | taken |
| I3 | No `Sign.pattern_in`: a conftest fixture reads a sign under `render._scopes`, so the tests read the scopes `scan_files` renders and the package gains no method only tests call | taken |
| I4 | Dotted keys, `check.en = '…'`, where `check` stands today, in place of a `[sign.check]` sub-table after `sources`: no key moves, and each language's comment stays above its form | taken |

Noticed on the way, for Round 1: `test_office.py`'s `MACHINE` holds German, Russian and Chinese lines that English's
forms won't find (Steps, Tests); `scan.md`'s "answer `none`" beside the new `ran` line (The plugin); `weak_hits` takes
its languages from `sign.language`, so a language with forms and no signs of its own gets no count of its own (The
package); propose-signs' step 5 names no machine line (Docs, moot with I2); `check.any` alone gives one check two
spellings, with no test of it (The schema).
