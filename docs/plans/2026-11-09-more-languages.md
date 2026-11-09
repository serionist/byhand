---
title: Seed signs for more languages, by their own sources
issue: "#49"
status: approved
approved_by: serionist
approved_at: 2026-11-09
---

# Seed signs for more languages, by their own sources

## Goal

The most spoken languages with sources that show their own signs get signs of their own, one language per PR, the way
Step 4 of the bootstrap plan seeded ten. A draft or a check in Spanish then reads Spanish signs, not only the `any`
ones, within the budgets every language already has (`Budgets` in `render.py`: 14 KB a mail). The maintainer's first
ask: the top 100 languages.

In scope: Spanish, Portuguese, Hindi and Arabic (rank 4, 9, 3 and 5 in `languages.toml`), each seeded or recorded as
having no source to seed from; then #49 closes. #13, Python reading `\w` and `\b` as Grep does, before the first of
them written with combining marks. A later language gets its own issue and follows this plan's moves without a new
plan.

Out of scope: a language with no source that shows its own signs: the `any` signs carry it (the bootstrap plan's
Risks, "Thin sources"). Translating another language's signs (AGENTS.md, Traps). Measuring overused words from
model-labelled datasets, which the bootstrap's Risks put in `0.3.0`: #50, with its own plan once two languages rest
only on datasets. No schema or skill change, and no change to what `render` writes.

## Design

Each language is the same three moves, with the tools that exist:

1. **Sources:** one `find-sources` run for pt, hi and ar together (Spanish has three since #48): one PR of
   `sources.toml` entries and a research record. It also notes each source's list of false positives, if it has one,
   and the language's own style guide (Fundéu for Spanish): what people write, which the plain-text guard starts from.
   What it finds sets the order of the rest, most evidence first.
2. **Signs:** `propose-signs` on them, structure first, as in Step 4. Until a native speaker reads them:
   - a language's sign with a pattern (`terms` or a `check`) is `weak`; a `usual` or `strong` one has neither and is
     for the model's own reading of a draft. A native review can raise one later (Round 1's Q1, as the de, fr and ko
     seeds ended);
   - a calque of English is translationese, which people write too: no sign without evidence that models write it
     more (the Korean seed's rule);
   - the `any` checks that list each language's forms (`any-ai-self-reference`, `any-knowledge-cutoff`,
     `any-assistant-preamble` among them) gain this language's, cited from its sources, with a machine line in its
     office test, as every seed PR did.
3. **Plain work text:** `tests/test_office_<code>.py`, invented mail, messages and documents in the language's office
   register and typography, seeded from the false positives and the style guide of move 1, and the test that no check
   of the language counts alone. It shares its helpers with the other office tests in `tests/conftest.py` and reads
   each sign's pattern from `signs.py`, never building its own.

Moves 1 and 2 may share a PR when the sources are few; never two languages in one. A PR names the signs a native
speaker should read first (`propose-signs`, step 8). Which languages no native speaker has read is in `sources.toml`:
a language with signs and no source of kind `review`; `CONTRIBUTING.md` says so, and asks for that read.

A draft reads only its language's files, so a new language costs other languages' drafts nothing. `any/check.md`,
which every check reads, grows with each language's `any` forms: 17.7 KB of the 32 KB check budget today, room for
these four. Over a budget, cut words first (`propose-signs`, step 7).

### Alternatives

- **Wait for native speakers for every language:** none has offered; the office text, the `passes` texts and checks
  that never count alone stand in until one does.
- **Many languages per PR:** a reviewer can't judge several languages' signs at once, and one bad language holds back
  the rest.
- **A `find-sources` run per language:** the skill takes a handful per run; one run lets the evidence set the order.
- **A standing "native review" issue:** someone would edit it on every PR; `sources.toml` already holds the answer.
- **A `write-<code>` eval case per language:** they grade only that `write` starts, which a sign file can't change,
  at three runs a case; the try by hand checks that `signs/<code>/` was read.

## Compatibility

No new language code: a sign for one variety (pt-BR, es-MX) is for the language as a whole, or waits for its own plan,
as `zh-Hant` had. New sign ids and files under `plugin/signs/<code>/`; nothing a user has changes. No one-way door.

## Steps

1. **Spanish:** `propose-signs` on `humanizer-es`, `alonso-simon-2025-spanish` and `resende-castilho-2026-style`; the
   `any` forms; `tests/test_office_es.py`, and the shared helpers moved to `tests/conftest.py` as the office tests'
   first change.
2. **Sources for pt, hi and ar:** one `find-sources` run (the pt Wikipedia translation, A7 of the research; B18 a
   pointer until its licence is found; the research's P18 for Arabic and P19 for Hindi).
3. **#13:** Python reads `\w`, `\W` and `\b` as Rust's regex does, wherever they stand, a class included: combining
   marks and the joiners ZWJ and ZWNJ as word characters, in a term and in a `check`. Grep gets the pattern as
   written, in NFC as today: `Sign.pattern` is Python's reading, which every search uses; the text as written is a
   field of its own, which `render` and the fr and hu order tests read, and a test holds that a rendered `Pattern:`
   equals that NFC text. `signs.py` exposes the compile, and the office tests' per-phrase patterns use it; a `\W`
   inside a class is refused, as `\b` there already is (Round 3's I8). Cases in `tests/test_catalogue.py`, each
   failing before the fix, the nukta and the Arabic code points written as escapes: `महत्व`
   not inside `महत्वाकांक्षी`; `बड़ी` found in `यह बड़ी बात है`; `कर\w*ना` found in `करवाना`; Bengali `কাজ` not
   inside `কাজী`; Arabic `شكراً` (alef, then fathatan) found before ` لك`. Before hi or ar, whichever comes first.
4. **Each of pt, hi and ar** that step 2 found sources for, most evidence first, a PR each: `propose-signs`, the `any`
   forms, `tests/test_office_<code>.py`. One with none is recorded here as such.

Each step ends with `finish-work`: the gate, `review-code` until clean, a PR.

## Tests

- Unit (CI): `byhand validate` (every `flags` and `passes`), `tests/test_office_<code>.py` per language with no check
  of it counting alone, `tests/test_order.py`, the render budgets; #13's cases.
- By hand, in each language's PR: `/byhand:write` on a mail in it and `/byhand:check` on its `flags` texts, from this
  clone, checking that it read `signs/<code>/`; for es and pt, once more asked in es-MX and pt-BR, to see that the
  base language's signs load (Round 1's Q2: a skill line only if they don't).
- What none can show: whether a native reader finds the signs right. `sources.toml` says which languages still need
  that read.

## Docs

`AGENTS.md`'s "Where the work stands" (the languages seeded), `README.md`'s list of languages in How it works (from
#45), `CONTRIBUTING.md` (one line: a language with no `review` source wants a native read), `CHANGELOG.md` under
Unreleased, Added (a line per language), this plan's progress log.

## Risks

| Risk | Answer |
|---|---|
| A sign written without a native speaker accuses plain writing | No check of the language counts alone until a native review, tested; the office text and `passes`; accepted |
| Sources are ports of English skills, so their signs are English's translated | Facts only; forks that add nothing dropped; a calque needs evidence that models write it more |
| Combining marks (Indic vowel signs, Arabic tanween) make Python and Grep disagree | Step 3, before hi or ar |
| A variety's request (es-MX, pt-BR) reads no folder | Tried in Steps 1 and 4; a skill line only if it fails |

## Progress log

| Step | What | PR | State |
|---|---|---|---|
| 1 | es | #53 | merged 2026-11-09 |
| 2 | sources for pt, hi, ar | #52 | merged 2026-11-09; the order, from its research record: pt, ar, hi |
| 3 | #13 | #54 | merged 2026-11-09; a `\W` in a negated class, `[^\W\d_]` in `es-dash-pivots` and `fr-hashtag-block`, is read as Grep reads it, not refused as I8 had it: refusing it would change two signs' patterns |
| 4 | pt | #55 | merged 2026-11-09 |
| 4 | ar | #58 | merged 2026-11-09 |
| 4 | hi | #59 | recorded 2026-11-09 as having no source to seed from: SHAKTI's longer model texts stand against human texts of about one sentence, Wang et al. found GPT-4o's Hindi news shorter, and their other cues are held by an `any` sign or clash with office Hindi, Sanskritised, and with Hinglish. No `hi.toml`; the `any` signs carry Hindi. The research record's follow-up has the detail |
| #60 | vi | #62 | merged 2026-11-09, by these moves under #60 |
| #60 | it | #63 | merged 2026-11-09 |
| #60 | id | #64 | recorded 2026-11-09 as having no source to seed from: `humanizer-indonesia` is the only Indonesian source; its light verbs and even sentences are measured only in English and Portuguese, which no language sign cites, and its author's own human writing misses some of its bars; the other patterns rest on it alone or are held by `any` signs. No `id.toml`; the research record of #61 has the detail and the deferred `any` forms |

## Plan review

### Fit

The plan at `7efaead`, by a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, read cold, with prior
art from the repo's research records only (searching is `find-sources`' job in each step). Answers by the author on
the maintainer's word for the night ("take the improvements that are recommended"), 2026-11-09.

| # | Improvement | Answer |
|---|---|---|
| I1 | One `find-sources` run for pt, hi and ar, the evidence setting the order | taken |
| I2 | #49 closes once the four are seeded or recorded; Step 6, "each further language", cut | taken |
| I3 | No `write-<code>` eval case per language: they can't fail on a sign file | taken |
| I4 | No standing native-review issue: `sources.toml` and a line in `CONTRIBUTING.md` | taken |
| I5 | Each sign's pattern from `signs.py` only; the office tests' helpers shared in `conftest.py` | taken |
| I6 | The plain-text guard seeded from sources' false positives and the language's style guide | taken |
| I7 | Datasets work untracked in `0.3.0` | later: #50 |

### Round 1

The same agent, 2026-11-09. Verdict: needs-fixes; fixed in place by the author.

| # | Finding | Severity | Fix |
|---|---|---|---|
| P1 | #13 fixed only at the edges leaves `\w` inside a stem reading marks as Python does, a false green against Grep | major | Step 3: `\w` and `\b` as Grep reads them, in terms and checks, one place, with cases |
| P2 | The moves left out each language's forms in the `any` checks, which every seed PR added | major | move 2's third bullet; the check budget's growth said |
| P3 | `usual` counts alone too, so one source could still accuse a person | major | Q1: checks `weak` until a native review, tested |
| P4 | Arabic tanween is a combining mark too | minor | Risks and Step 3 name it; an Arabic case |
| P5 | `README.md` had no list of languages | minor | #45's README lists them in How it works; that line moves |
| P6 | "No more than a draft in English" was untestable and already false | minor | the budgets every language has |
| P7 | The pt leads counted one page twice | minor | A7 once; B18 a pointer |
| P8 | A variety code would be a one-way door | minor | Compatibility: no new language code |

Owner calls, answered on the maintainer's word for the night with the reviewer's recommendation: Q1 (checks `weak`
until a native review) yes; Q2 (a variety's request) try first, a skill line only if it fails. Round 2 reads the fixes.

### Round 2

A fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, on `8f6d145`, which compared Python 3.12's `re`
with ripgrep 14.1.1 on each case. Verdict: needs-fixes; fixed in place by the author.

| # | Finding | Severity | Fix |
|---|---|---|---|
| P9 | Compiling a rewritten pattern would change the `Pattern:` `render` writes, and ripgrep refuses look-around: `scan` would fail on every sign with `\b`; the office tests' own per-phrase patterns would keep Python's reading | major | Step 3: Grep gets the pattern as written, a render test holds it; the office helpers use `signs.py`'s compile |
| P10 | `\W`, a `\w` in a class, and ZWJ and ZWNJ read differently too | minor | Step 3 names them |
| P11 | The stem case passed without the fix | minor | `कर\w*ना` in `करवाना`; each case fails before the fix |
| P12 | Q1 said "with a `check`", but a `terms` sign has a pattern too | minor | "with a pattern (`terms` or a `check`)" |
| P13 | "Fit Q1" and "Fit Q2" pointed at the wrong section | minor | "Round 1's Q1" and "Q2" |

### Round 3

A fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, on `9a20380`, narrowly on Step 3. It built the
fix as a prototype (8 ms to compile, 4 ms over 22 KB) and checked each case against Python 3.12.10 and rg 15.0.0:
each fails today and passes with the fix, agreeing with rg. Verdict: approved.

| # | Finding | Severity | Fix |
|---|---|---|---|
| P14 | "As written" dropped the NFC `render` applies today: a precomposed nukta would reach Grep unsplit | minor | "in NFC as today", the render test compares the NFC text, the nukta written as an escape |
| P15 | Rust's `\w` differs from Python's plus marks on `No` (², ½) and `So` letters (Ⓐ) too | minor | accepted: it needs a term against a superscript ("m²"), which no sign has; the cost is a property table |
| P16 | Which field holds which reading was unsaid, and "no render change" contradicted keeping them apart | minor | `Sign.pattern` is Python's reading; the text as written a field of its own; Out of scope says "no change to what `render` writes" |
| I8 | Refuse `\W` inside a class rather than translate it | improvement | taken |

### Approval

Treated as approved on the maintainer's word for the night ("go autonomously … take improvements that are
recommended"): Round 3 found no blocker or major. Recorded in `.local/NIGHT.md` for the maintainer to see.
