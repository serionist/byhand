---
subject: "Read word edges in the tests as Grep does (PR #54)"
base: main (daa41b0)
head: 889f213
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, reading only; findings checked against the code by the main session)
verdict: clean
---

# Read word edges in the tests as Grep does: code review

The reviewer read the nine changed files, issue #13, the plan's Step 3 and its Rounds 2 and 3, and ran nothing. CI on
889f213 was green on every platform. It traced each of the nine cases on `origin/main` and here. No blocker or major.
The main session fixed the three minors in 4792b18, each with a case that fails without its fix.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `signs.py`, `_as_grep_escapes` | `\B` was neither given Grep's reading nor refused, so a Hindi `\Bना` would read a mark as Python does; no sign has one | fixed: `\B` as look-around too; the case "no edge between a vowel sign and a letter" (`करवा\Bना`), which fails on 889f213 |
| F2 | minor | `signs.py`, `as_grep` | The compile of Python's reading ran outside the FutureWarning guard `_checked` keeps; under pytest's `filterwarnings = error` a class such as `[a\|\|b]` beside a `\b` would be a traceback, not a problem | fixed: the same guard; `\bdelve [i\|\|x]nto` in `SHARED`, which fails on 889f213 with the warning; ripgrep 15.0.0 finds its `flags` |
| F3 | minor | `tests/test_catalogue.py`, `MARKS` | No case held the joiners or a connector other than `_`: dropping `_JOINERS` or `Pc` from the table left the suite green | fixed: "no edge before a joiner" (ZWNJ) and "no edge before a connector" (`‿`), as escapes; both fail on `origin/main` |

## Refuted

- `\b` at the start and end of a text, and with `MULTILINE`: the look-around agrees with Rust's `\b`, the text's
  edges and `\n` being non-word in both.
- An escaped backslash (`[^\\W]`, `\\W`), a `]` first in a class (`[^]\W]`), a class of `\W` alone (`[^\W]`): each
  read as Grep reads it, the last by its own case.
- The negated-class look-ahead dropped unnoticed: `tests/test_office_es.py`'s lines with a raya after a space would
  fire.
- A translation that fails to compile after `validate` passed it: a range with a `\w` or `\W` end already fails the
  first compile, and no added character is class syntax.
- NFC order, case-insensitivity (U+0345's partners are letters already), and any reader of `sign.pattern.pattern`
  meaning the written text (only the NFC test, on purpose).
- The I8 departure, translating `\W` in a negated class: explained in the progress log and the PR, and refusing it
  would change two signs.
- The docs: no user sees a change, and the propose-signs rule covers the new refusal.

## Improvements

| Improvement | Answer |
|---|---|
| `tools/copycheck.py` could compile with `signs.as_grep`, so a stem across a mark is taken out of `flags` | left: `tools/` is standard library only, and copycheck is by hand; a stray hit is read and waved through |
| `_word_extra`'s docstring could say no added character is `[`, `&`, `~` or `\|` either | taken |

## Not covered

The reviewer ran no code and no ripgrep; the main session's comparison with ripgrep 15.0.0 (23 texts, no disagreement)
and the gate are the author's. The minors' fixes were checked in this session, as the skill has it for minors only:
`gate.py full` passed on 4792b18, 2489 tests.
