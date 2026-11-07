---
subject: "Bootstrap step 4, the Chinese signs (PR #16)"
base: main (70dd6ed)
head: 417f0f7
date: 2026-11-07
round: 1
tier: standard (a fresh reviewer per round on Claude Opus 5.5, every lens; the last fix verified by the main session)
verdict: needs-fixes
---

# Review: Bootstrap step 4, the Chinese signs (PR #16)

Four rounds by fresh reviewers, each writing their own plain Chinese work texts (Simplified and Traditional: mail,
WeChat, DingTalk, notices, reports) and chatbot lines, running every pattern under Python and Claude Code's Grep, and
copycheck over wikipedia-zh, shuorenhua, slop-gate and speak-human-tw. No licence blocker in any round.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | any-assistant-preamble, Chinese branch | Fired strong on a person returning their own revision ("当然可以！这是修改后的版本：") | fixed: only 以下是/下面是 … 修改后的版本 fires; speak-human-tw 30 cited; five lines in `OFFICE` |
| F2 | major | zh-officialese | Plain official notices reached the weak cluster | fixed: the maintainer's call, narrowed to the padded forms; a notice test |
| F3 | minor | zh-holding-space | Fired on things, not people (servers, traffic, a pass) | fixed: a person or a feeling as object |
| F4 | minor | any-ai-self-reference, Chinese branch | Fired on 我们 | fixed in round 4's form, below |
| F5 | minor | several fields | Wording and list order taken from the MIT sources | fixed: rewritten, reordered; copycheck at 6, 5 and 4 |
| F6 | minor | model scopes, citations | Scopes beyond their source | fixed: the maintainer's call, follow the source |
| F7 | minor | any-emoji-markers | Fires on "1. ✅ 合同已盖章" | later: #19, a sign every language shares |

## Round 2

**Where:** `417f0f7..0c975c4`. F1 to F6 held.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F8 | major | zh-officialese, zh-wrap-up-phrases | Plain year-end reports reached 3 weak hits from separate phrases | fixed: the maintainer's call, 关键在于, 核心在于 and the 实现了…的增长 branch dropped; a report test |
| F9 | minor | zh-holding-space | Lost 接住你的情绪 | fixed |
| F10 | minor | any-ai-self-reference | Fired on 我司, 我方 | fixed in round 4's form |
| F11 | minor | any-assistant-preamble | Missed 下面是根据您的要求修改后的版本 | fixed |

## Round 3

**Where:** `0c975c4..6238e63`. F8 to F11 held.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| N1 | major | any-didactic-aside, Chinese branch | A usual sign counting 值得注意的是 alone, standard in reports and news | fixed: the phrases moved to zh-stock-openers, weak |
| N2 | minor | any-ai-self-reference | Fired on 我公司, 我行, 我校 | fixed in round 4's form |

## Round 4

**Where:** `6238e63..87e0508`, rebased onto #21's cluster rule. N1 and N2 held; a person describing their own role
(作为新人，我可以…) passes.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| N3 | major | any-ai-self-reference | The narrowed ending missed common disclaimers (作为一个AI语言模型，我不具备个人情感, …我建议您…) | fixed in `e3c01bb`: a wider ending after AI助手/助理/语言模型; eight lines in `MACHINE` |
| N4 | minor | tests/test_office_zh.py | `_weak_hits` counted a repeated phrase more than once | fixed: counts as the rule does |

## Closed

`e3c01bb` verified in the main session: six chatbot disclaimers fire, and eight human lines stay silent, among them a
person's role (作为新人，我可以…), a company (作为AI助手，我公司…), an engineer (作为一名人工智能工程师，我理解…) and a
team lead (作为AI助手团队的负责人，我很高兴…). The maintainer merged on that, without a fifth round.
