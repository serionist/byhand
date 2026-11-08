---
subject: "Refuse regex syntax only Python reads in sign checks (PR #36)"
base: main (5a1905b)
head: e125a48
date: 2026-11-08
round: 1
tier: standard (one fresh reviewer on Claude Opus 5.5, every lens; findings reproduced in ripgrep and checked by the main session)
verdict: clean
---

# Review: Refuse regex syntax only Python reads in sign checks (PR #36)

Round 1 read `_python_only` in `src/byhand/signs.py`, its tests and the `propose-signs` line at `e125a48`. The reviewer
ran every scenario through the ripgrep that Claude Code bundles (14.1.1, `-i`) and through Python 3.12 with `_FLAGS`.
It also ran the new tests against `origin/main`'s `signs.py`: all 22 refused cases fail there. No blocker or major,
so the minors were fixed in this round and the review ends.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `_PYTHON_ONLY["escape"]`, `_python_set` | An escaped character outside ASCII, such as an escaped em dash or `«`, passed `validate`. Python reads it as the character and ripgrep refuses it ("unrecognized escape sequence"). A de or hu sign about dashes and quotes could plausibly escape one | fixed in 6e686e4: `_python_escape` refuses it, in a class too; tests `delve \—` and `[\—-]? delve` |
| F2 | minor | `_python_set` | `[\b]` passed: a backspace to Python, "invalid escape sequence found in character class" to ripgrep | fixed in 6e686e4; test `[\b]delve` |
| F3 | minor | the kept forms, `SHARED` | `validate` reads `flags` and `passes` whole, and Grep reads line by line unless `multiline` is on, when it adds `--multiline-dotall`. `\A`, `(?s)`, `\n` and `.` across lines can find different text. The syntax is read alike, so this is about how Grep is called | left: the bootstrap plan leaves Grep's mode to Step 5 (#5). The `SHARED` comment now says the forms read alike on one line. An issue was drafted for it but not filed: the session had no permission to file it, so it goes to the maintainer |
| F4 | minor | `_python_set` | `[-\d-]x`, `[~\s~]x` and `[&\s&]x` were refused: removing the escape joined its neighbours into `--`, `~~` or `&&`. Both engines read these classes alike | fixed in 6e686e4: an escape stands as one plain character; tests `[-\d-]?delve into` and `[~\s~]?delve into` |
| F5 | minor | `_PIECE`, `_COUNT` | `x{١}` (an Arabic-Indic digit) passed. Python reads the braces as text, and ripgrep says "repetition quantifier expects a valid decimal" | fixed in 6e686e4: counts take ASCII digits; test `del{١}ve` |
| F6 | minor | `_compile` | A Rust escape such as `\x{4c}` was blamed on Grep ("Grep can't run `{4`"). In fact ripgrep reads it and Python refuses it | fixed in 6e686e4: Python compiles first, and its FutureWarning on `[[` is hidden, since the scan refuses that class itself; `(?L)` now gets Python's own error, which names the flag. Both are tested in `BREAKS` |

## Refuted

- Mis-tokenising: `[]]`, `[^]a]`, `[\]]`, `\(?let\)?`, `[(?>]x`, `\[[^\]]*\]`, `\++`, `c\+\+`, `x{2}?`, `#{1,6}`, `[{]`, a
  lone `]` and a lone `}` are all read alike by both engines and pass.
- Escaped ASCII punctuation and spaces (`\'`, `\%`, `\,`, `\/`, `\ `) are read alike by both and pass.
- Unicode group names (`(?P<név>`) and `[a||b]` are read alike by both and pass.
- Case folding: `ſ`, the Kelvin sign and `ẞ` match the same under `-i` in both.
- `(?-u:`, `(?<name>`, `x**` and `[\A]` are already refused by Python. `\z` is refused on 3.12, and on 3.14 both read it
  as the end of the text.

## Improvements

- Python first in `_compile`, so every pattern Python refuses gets Python's own message: taken (F6).
- Python's `\w` and `\b` leave out combining marks, and ripgrep's include them, so `\bकरना\b` differs on Hindi text:
  later: #13.

## Not covered

- The reviewer ran Python 3.12 only. CI runs 3.12 to 3.14.

## Checks

- Mutants of the round's fixes, one at a time, each killed: no non-ASCII escape rule, no `\b` in a class, escapes deleted
  rather than replaced, Unicode digits in a count, the scan before Python's compile.
- `uv run tools/gate.py full --base origin/main` on 6e686e4: 2027 tests passed, coverage 99.61%, `signs.py` 100%.
