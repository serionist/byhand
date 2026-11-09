---
subject: "Print each term as a phrase a person writes, and find die Tradition (PR #95)"
base: main (4c0a640)
head: 5c29d11
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, read-only but for scripts over render.words and the patterns; findings checked by the main session)
verdict: clean
---

# Review: Print each term as a phrase a person writes, and find die Tradition

The reviewer read the issues (#92, #93), the PR body, the diff and the touched files, and applied every lens. It ran
main's and the branch's `render.py` over all 397 terms, main's TOML and the branch's: the new rules change seven
prints with main's terms, ten with the respelled ones, as the PR's tables say. It ran the old and new patterns on
6,638 strings (every string literal in `tests/`, every string in the catalogue): only the new office line `Der Ort
pflegt eine reiche Tradition.` changes. Every changed sign file shrinks or keeps its size, as the PR's byte table says.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `render.py` `_class`; the PR body | The body said fr-filler-notice now prints "il convient de noter que", but Python folds `qu(?:['’]|e)` into a class, which the branch rule never sees: the print stayed "qu'" | fixed in 78c0ffb: `_class` prefers a letter to an apostrophe; it changes only this print (same bytes); `test_a_term_prints_one_plain_word_per_alternative` (`noter qu(?:…|e)`) and the real-catalogue test pin it |
| F2 | minor | `tests/test_render.py`, the `[ж-я]{3,} могут` case | Main prints "… могут" for it too: a class with no literal was already the ellipsis, so the case didn't pin the range rule | fixed in 78c0ffb: `[ж-яё]{3,} могут`, which main prints "ёёё могут" |

## Refuted

- The elision rule ignores the next word: `(?:l['’]|le )enjeu` would print "le enjeu". No term has that shape; the rule
  changes only the two fr calques, both now right, and `propose-signs` tells a proposer to read the print.
- The gap rule hides an optional `\w?`: that is the shortest text, and it turns ar "تسليط" into "سلّط", which is right.
- The `traditionelle` office line passes on main too: it guards "nothing it shouldn't" against a looser `tradition\w*`;
  the new `eine reiche Tradition` line fails on main.
- German fragments ("reiche erbe", "lass mich es aufschlüsseln") read as parts of phrases people write; no respelling
  avoids "es" without changing what the term finds.
- The cut `what` text of `fr-calques` and `ru-chat-residue`: the fr examples now print as words, the ru kinds are in
  the brackets.

`ru-chat-residue`'s `помог\w*` also finds помогают, помогут, помогу and помогающий after "надеюсь, это": wider than the
PR body said, harmless; the body now names them.

| Improvement | Answer |
|---|---|
| Prefer a letter to an apostrophe in a class (F1's fix) | taken in 78c0ffb |

## Checks

Only minors, so no second round: the fixes were checked in this session. The prints over the whole catalogue before and
after 78c0ffb differ only in fr-filler-notice; every file's bytes are unchanged by it; `uv run pytest` (4,101 passed)
and `uv run tools/gate.py full` passed on 78c0ffb. CI passed on 5c29d11.
