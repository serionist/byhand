---
subject: "Split the terms whose group lists different words (PR #89)"
base: main (63c88f0)
head: 9d2da9b
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, read-only; findings checked against the code by the main session)
verdict: clean
---

# Split the terms whose group lists different words: code review

The reviewer read the change, issue #84, F3 of #70's review, `weak_hits`, `render.words` and the order tests, and
applied every lens. It compared each changed sign's old and new pattern on 34,824 strings generated from every term,
bare and in three contexts: none differ. It recounted the PR's tables and budgets, and checked that main's new
`render.py` (#87) passes the branch's catalogue. The main session reproduced F1's lines with `_weak_hits`.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `zh.toml`, `zh-Hant.toml`: `zh-Hant-mainland-terms`, `zh-gpt-5-register`, `zh-wrap-up-phrases` | Three character classes list different words: `[軟硬]件`, `[揪抠摳]出[来來]`, `[总總]的[来來][说說看]`. "軟件和硬件都要升級。", "我把错误揪出来，又把漏洞抠出来。" and "总的来说，总的来看，问题不大。" each count 1 in the tests and 2 in the plugin | fixed in 79f2da7: `軟件` and `硬件` (each with its own Taiwan word), `揪出[来來]` and `[抠摳]出[来來]`, `[总總]的[来來][说說]` and `[总總]的[来來]看`; each line counts 2 |
| F2 | minor | `.claude/skills/propose-signs/SKILL.md`, step 5 | The new sentence said a group holds only one word's endings or spellings, but the change keeps articles, particles and pronouns grammar picks; a proposer would split `im herzen (?:der|des|von)`. Nor did it name classes, which is how F1 slipped through | fixed in 79f2da7: "a group or class … or the article, particle or pronoun grammar picks" |
| F3 | minor | `CHANGELOG.md` | `write` now sees every phrase (`hu-calque-phrases` showed one verb of 15), which users may notice; no line said so | fixed in 79f2da7: a line under Changed |

## Refuted

- Reordering changing a match's text: the generated strings match identically, and the word edges wrap the whole body.
- Budgets breaking after a rebase on #87: `budget_problems` with main's `render.py` is empty, and the merged files equal
  a fresh render.
- The `ja-preface-filler` and `zh-gpt-5-register` reorders breaking the order rule: their keys tie (`^`, `''`).
- A `usual` or `strong` sign split, or an `instead` changed: every changed sign is weak, every new `instead` an old one.

| Improvement | Answer |
|---|---|
| Top-level alternatives in one term (`プロジェクトレベルの|組織レベルの`) in place of terms of their own: one `instead` per sign, which would fit the six Japanese groups left | left: the issue asks for terms of their own; the PR offers the other form to the maintainer |
| Align ja `(?:ここ|そこ)` and fr `(?:ici|là)` | taken in 79f2da7: both stay grouped as demonstratives, which cuts 4 of `fr-staged-reveal`'s terms |
| ja `解像度(?:が上が|が高|を上げ)` is one idiom only loosely: が高 is another word | left: ja's document has 56 bytes, not enough to split it |
| ru `(?:все|существующие|эти)`: существующие is no pronoun | left: no paragraph realistically holds two of them beside two other weak hits |

## Checks

The minors were fixed and checked in this session, with no second round (`review-code`, step 7): the by-hand
comparison over flags, passes and office text (42 signs, 17,840 lines, the same matches), `_weak_hits` on F1's
three lines (2 each), `uv run pytest` (4,065 passed), and `uv run tools/gate.py full` on 79f2da7. Main moved twice
during the round (#87, #88); after each rebase the sign files re-rendered within the budgets, and the comparison
held.

## Round 2

**Where:** PR #89, c49b936 against round 1's fixes: `tests/conftest.py`, read by one fresh reviewer (read-only).
**Verdict:** clean.

CI's coverage leg (Tests, Linux, Python 3.12) was cancelled at its 15-minute timeout on cfd6b87 and c92f074, while
main's takes about a minute. The split takes the weak phrases `_count` compiles from 423 to 600, past the 512 patterns
`re` keeps, so every `weak_hits` call compiled each phrase again: five calls took 7.5 s, against 1.7 s on main.
c49b936 cached them: 0.02 s, and pytest under coverage 24 s in place of 137 s.

The reviewer found nothing: `as_grep` is pure, a compiled pattern is safe to share, no test patches what it reads,
and each xdist worker has its own cache.

| Improvement | Answer |
|---|---|
| Use the conftest's existing `_compiled` cache rather than a second one | taken in ee0c70c |

CI passed on c49b936, every leg; `uv run tools/gate.py full` passed on ee0c70c.

## Round 3

**Where:** PR #89, 98c2384 on main f3ba1b4 (#90), read by one fresh reviewer (read-only), who also checked a186694 on
8c5f659. **Verdict:** clean once the minors below were fixed; no round 4, as none is a blocker or a major.

The maintainer turned down the byte cost of terms of their own. 98c2384 writes each former group as one term of
top-level alternatives with its one `instead`. The tests count each alternative as its own phrase, and the sign
files print the `instead` once. The branch was rebuilt as one commit on #90, 9a0a820 with this round's fixes, so
the commits rounds 1 and 2 name (79f2da7, c49b936, ee0c70c) are folded into it. #90 put 98 more bytes in a Japanese
document, so three ja groups now stay grouped in place of two.

The reviewer compared main's and the head's patterns on 52,710 generated texts: the same spans and the same text. Two
different alternatives of each of the 78 rewritten terms in one paragraph count one more than on main. The order tests
pass, and the sign files equal a fresh render within every budget.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F4 | minor | `zh-Hant.toml`, `zh-Hant-mainland-terms` | `硬件|軟件` with `instead = "軟體, 硬體"` printed "硬件, 軟件: 軟體, 硬體", which reads as hardware → software | fixed in 9a0a820: `instead = "硬體, 軟體"` |
| F5 | minor | `fr.toml` `fr-calques` `(?:à travers|dans)`, `vi.toml` `vi-article-opener` `(?:ở|trong)` | Two preposition groups list different words: "naviguons dans ces incertitudes … naviguons à travers ces incertitudes" and "Ở bài viết này … Trong bài viết này" each count 1 with two different matches | wontfix: a preposition the verb or noun picks is grammar, like the articles and particles that stay grouped; propose-signs now names prepositions with them |

Framing and optional words around one core phrase (de `(?:dabei ist es|es ist|hierbei ist es)`, ru
`(?:живым |ярким )?`, zh `(?:很|要)?`) stay grouped as before: a reader takes each as the same phrase.

| Improvement | Answer |
|---|---|
| CHANGELOG: "most weak signs", and drop "count as two", the plugin's rule since #76 | taken |
| A TOML comment by the three ja terms left grouped, so a later proposer meets the budget reason, not the failure | taken |
| Sort zh-wrap-up's new pair: `[总總]的[来來]看|[总總]的[来來][说說]` | taken |

Bytes, main f3ba1b4 → head: a document +870 (de), +905 (fr), +1,228 (ru), +452 (ja: 16,329 of 16,384); the scan
+1,116 (de), +1,384 (ru: 9,003 of 9,216). About 5.3 KB over all languages is the phrases `write` and `check` now
see, and 5.9 KB is the scan pattern spelling each phrase in full. Nothing in the catalogue or tests brings it nearer
main without grouping different words again.

`uv run tools/gate.py full` passed on 9a0a820.

## Round 4

**Where:** PR #89, b4f7a03 on main f3ba1b4 (7ef2679 after the rebase on #91), read by one fresh reviewer
(read-only). **Verdict:** clean once the minors below were fixed in b1d76b5; no round 5, as none is a blocker or a
major.

The maintainer turned down the catalogue fixes of rounds 1 to 3: even as one term of alternatives they cost up to
1.2 KB more in every draft. b4f7a03 leaves the catalogue and the sign files as on main, and fixes the tests alone: a
weak term counts each different text it matches, casefolded, as a check does. A word's other ending then counts
again, more than the plugin's rule, which is the safe side for a guard. Five counting tests that rested on endings
counting once say the stricter count.

The reviewer compared main's `_count` and the head's over 3,179 strings (every string in the office tests, every
`flags` and `passes`) in five kinds: only the edited test texts and `ko-policy-verbs`' `flags` (1 → 2) change, no
`passes` string changes, and nothing new reaches 3. It found no case where the tests count less than the plugin.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F6 | minor | `tests/test_office_ar.py`, `test_one_habit_counts_once_per_text` | Its three texts were all different (يسلط التقرير الضوء, ويسلط الضوء, يسلط الضوء), so the test no longer checked that a repeat counts once, and its comment misread why ويسلط الضوء differs (the `\w{0,2}` prefix) | fixed in b1d76b5: "…، ثم يسلط الضوء …، ثم يسلط الضوء …" counts 2 (main 1): the repeat once, the words-between form again |
| F7 | minor | `tests/conftest.py`, `_compiled`'s comment | It said the weak patterns are more than the 512 `re` keeps; on main's catalogue the phrases are 423 and fit | fixed in b1d76b5: the cache guards the catalogue's growth past 512 |
| F8 | minor | PR #89's title and body | They described the catalogue split, which this head no longer carries; squashed, they would become main's commit message | fixed: retitled and rewritten for the test-only fix, saying why the catalogue fix was declined |

| Improvement | Answer |
|---|---|
| Say "more than the rule" in the hu test's comment, as it now asserts 2 | taken in b1d76b5 |
| Compile each term whole rather than each top-level alternative, now that keys are texts | left: no count changes, and it touches the overlap rule for no user gain |

`uv run tools/gate.py full` passed on b1d76b5.
