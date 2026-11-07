---
subject: "Bootstrap step 2, the catalogue's schema (PR #12)"
base: main (64fb1d1)
head: 7a32a5d
date: 2026-11-07
round: 1
tier: standard (one fresh reviewer on Claude Opus 5.5, every lens; findings checked and fixes verified by the main session)
verdict: clean
---

# Review: Bootstrap step 2, the catalogue's schema (PR #12)

One fresh reviewer read the change at `7a32a5d`, ran probes in a scratch folder, and tried each mutant on a scratch copy.
No blocker or major, so no second round: each finding below was fixed in this round and checked in the main session.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `models.py`, `read_id` | A number that is no version was read as one: `mistral-large-2411` as 2411, `qwen-max-2025-01-25` as 2025.1, `mistral-7b` as 7, `gpt-oss-120b` as 120 | fixed: a number of more than two digits, or with a size, is no version; tests for each. Kept, in the plan's Decisions: `gpt-35-turbo` reads 35, `grok-code-fast-1` reads 1 |
| F2 | minor | `models.py`, `read_id` | The family was the first in the file, not the first in the id: `deepseek-r1-distill-llama-70b` read llama | fixed: the earliest match in the id; a test, and a mutant killed |
| F3 | minor | `signs.py` | `byhand validate` gave a traceback, not a problem, on a file in cp1250, `models = ["gpt"]`, `[sign]`, `term = 3`, `id = 3`, `family = ["gpt"]`, and a datetime beside a date | fixed: `_rows`, `_id`, `_is_date` and type guards; a case for each |
| F4 | minor | `signs.py` | A misspelt `[[signs]]` dropped a whole file with `validate` green | fixed: each file's top-level keys are checked |
| F5 | minor | `signs.py`, `_range` | `from = 4.10` loaded as 4.1 | fixed: a version must be text, in quotes |
| F6 | minor | `signs.py` | Rules left to a reviewer: a `word` sign with no `terms` or `check`, an `artefact` with no `check`, `kinds = ["any", "deck"]` and repeated kinds, a `layout` sign for mail, an empty `instead` or `where`, a variant repeating a language, `spaces = "false"` | fixed: a check and a case for each |
| F7 | minor | `signs.py`, `_terms` | `\w` excludes combining marks, so in Indic scripts a term can match part of a longer word | later: #13, for `0.3.0`. No seeded language has it, and the pattern is derived, so a later fix breaks no door |
| F8 | minor | `signs.py`, `_terms` | An `any` sign's terms took the spaced edge, so they missed in Chinese, Japanese and Thai text | fixed: an `any` sign writes its own `check` |
| F9 | minor | `languages.toml` | `tts`, written in Thai script, lacked `spaces = false` | fixed |
| F10 | minor | `tests/` | Five mutants survived: `main` not calling `_utf8`, `__lt__` ignoring the minor, the left edge dropped, a variant ignoring `spaces`, `_compile` skipping NFC | fixed: each is now killed; the pipe test runs `cli.main` |
| F11 | minor | `AGENTS.md`, `ci.yml` | "The harness only" was stale, and ci.yml's list of the quick lane missed the catalogue | fixed |

## Refuted

- `Version(4) == Version(4, 0)` is unsound: `claude-opus-4` and `claude-opus-4-0` are one model.
- A legitimate Step 4 sign is refused: a `zh-Hant` file, Japanese and Thai terms, a stem with `\w*`, an artefact with a
  `check`, two ranges in two families and a layout sign all load clean.
- The language data is wrong: recomputed from CLDR's `territoryInfo.json`, all 100 ranks match.
- The codes aren't valid BCP 47: each is an active ISO 639 code in its shortest form.
- The gate imports the package: `tool()` runs it through `uv run`, and gate.py's imports are the standard library's.
- The keyword `multilingual` is misspelt (improvement 7 of the review): spelt letter by letter it is multi and lingual,
  in `pyproject.toml` and `plugin.json` alike. The maintainer took the fix before this was checked; there was none to
  make.

## The maintainer's calls

| Call | Answer |
|---|---|
| What `to = "5"` means | the whole 5 series; `to = "5.0"` stops at 5.0. `ModelRange.holds` comes here, as `validate` needs it |
| The flags a `check` runs with | case-insensitive and line by line, `re.MULTILINE`, in the schema's comment |
| `gpt-4o` reads gpt 4, `deepseek-r1` deepseek 1 | kept, in the plan's Decisions |
| `lah` beside `pa`, as CLDR counts it | kept, in the plan's Decisions |

## Improvements

| Improvement | Answer |
|---|---|
| `byhand models` loads only the families, so a bad sign can't stop it | taken |
| `Family` moves into `models.py`, which drops a one-caller Protocol | taken |
| `_DATE` goes: F1 covers it, and no test needed it | taken |
| `_terms`' `_nfc` duplicated `_compile`'s | taken |
| A language sign cites a source in its language, or its base language's | taken |
| The gate's `sign ids`: each id at a base stays in the tree, read with `tomllib` so the gate stays free of the package | taken |

## Checks

- `uv run tools/gate.py full` after the fixes: 20 checks, 532 tests, coverage 99.68 %.
- Eight mutants, run one at a time: the five above, dropping `re.MULTILINE`, dropping `holds`' lower bound, and taking the
  first family in the file. Each fails a test.
- A wheel built by hand holds the catalogue's files and the entry point.
