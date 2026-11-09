---
subject: "Count each different phrase a weak check finds (PR #76)"
base: main (26884bc)
head: e99228b
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, read-only; findings checked against the code by the main session)
verdict: clean
---

# Count each different phrase a weak check finds: code review

The reviewer read the change, issue #70, F2 of `2026-11-09-weak-hits-code.md`, the plugin's counting rule, the
catalogue's weak checks and every office test that counts weak signs; it ran nothing. The main session reproduced each
finding with `_weak_hits` on the catalogue and fixed the minors in c6a6975. Only minors were found, so the review ends
with this round.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `src/byhand/render.py`, `_file`; `plugin/skills/check/SKILL.md`, step 7 | The new line named only "a mark such as a dash", but the tests count every formatting check once, and several match different text each time: `hu-english-quotes` takes the quoted word, `any-raw-markdown` the bold label. "A gomb neve “Mentés”, a menüé “Fájl”, az átfogó leírás a súgóban van." counts 2 in the tests; a model reading "two that one sign finds as well" could count the two quotes apart and call it a cluster | fixed in c6a6975: both say "a mark such as a dash, quotes or bold however often it appears and whatever words it holds"; `test_the_cluster_rule_prints_only_where_a_weak_sign_is`; tried in a session, below |
| F2 | minor | `tests/test_office_ko.py`, `_weak_hits` | Older than this change: the Korean office guard kept its own count, one per sign, the rule #70 replaces. "경쟁사가 시장을 잠식하자 실적에 적신호가 켜졌고, 회사는 새 청사진을 내놓았다." counts 1 there (`ko-coined-metaphor`), 3 in the plugin and the shared fixture | fixed in c6a6975: `test_plain_korean_work_text_makes_no_weak_cluster` takes the shared `weak_hits` under every kind; the scenario counts 3 with it; every Korean office text stays below 3 |
| F3 | minor | `tests/conftest.py`, `_count`, the terms branch | A term's inner group counts once, read as spellings, but some list different words: `ja-calques`' `(?:プロジェクト\|リポジトリ\|ワークスペース\|組織)レベルの`, `en`'s `(?:local\|national\|regional) media outlets`, and others in fr, ko and ja. "プロジェクトレベルの設定と組織レベルの権限を見直した瞬間に、作業が止まった。" counts 2 in the tests, 3 in the plugin | wontfix here: counting a term by its matched text would count an ending (átfogó, átfogóbb) twice, which the hu test of one word rejects; the fix is to split those groups in the catalogue, outside #70. A follow-up issue is drafted (opening it with `gh issue create` was refused in this session) |

## Refuted

- The formatting category drawing the wrong line: every weak dash or mark check is `formatting`, and no `phrase` or
  `structure` check matches a bare mark (`zh-first-next-last` takes 首先…其次…最后 as one span).
- An empty match giving two signs one `""` key: a check that can match nothing also matches its `passes`, which
  `_examples` refuses.
- The other-language rule making a draft count less: a call with `languages` has no other language's spans, and a call
  without them takes the higher of that and every language at once.
- A check's text colliding with a term's key: only when the term is that same text, the one phrase two signs find,
  which the rule counts once.
- The marks tests breaking: the ja asides, hu dashes and quotes still count 1, the de dashes 3.
- The new test passing without the change: at 26884bc F2's line counts 2 (`pt-staged-reveal` once, `enfatizando`).

| Improvement | Answer |
|---|---|
| Say "even two from one sign" instead of "two that one sign finds as well", which can read as "also found by" | taken |
| Reword the conftest comment on the staged reveal's overcount | taken |
| Give `write`'s step the same mark exception | left: `write` reads the sign files' line, which has it |

## Live run

`claude -p --plugin-dir plugin` on Claude Code 2.1.319, Opus 5.5, byhand not installed. `/byhand:check` on F2's
Portuguese line counted a cluster of 3 (`pt-staged-reveal` twice, `pt-ai-vocabulary`); on three dash asides in Japanese,
`ja-em-dash` once and no cluster; after c6a6975, on F1's Hungarian line, the two quotes once and no cluster (2). A
request without the slash command did not start the skill in `-p` mode. Not shown: an interactive session.

## Checks

`uv run tools/gate.py full` passed on e99228b and c6a6975; CI passed on e99228b (Checks (Linux) after a rerun, the
first failed downloading gitleaks with a 504). Every `weak_hits` call in the suite (1,055) was logged at 26884bc and
with the change: none differs.
