---
subject: "Bootstrap step 4, the Japanese signs (PR #18)"
base: main (70dd6ed)
head: f0ebede
date: 2026-11-07
round: 1
tier: standard (a fresh reviewer per round on Claude Opus 5.5, every lens; the last fix verified by its mutants)
verdict: needs-fixes
---

# Review: Bootstrap step 4, the Japanese signs (PR #18)

Two rounds by fresh reviewers, each writing their own plain Japanese work texts (business mail with its set phrases,
Slack, Chatwork, reports, minutes, essays with ――, Qiita posts) and chatbot lines, running every pattern under Python
and ripgrep, and copycheck over yomiyasu, stop-ai-slop-jp and Zaitsu et al. 2025.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | ja-llm-function-words | Alone it reached a weak cluster on plain mail (に関する, いくつかの): Zaitsu's rates are over whole texts, not terms | fixed: a sign for the model's read, with no terms; a test holds it has no pattern |
| F2 | major | ja-em-dash | A person's essay with ―― reached 3 hits | fixed: a ――…―― pair is one hit; `what` says essay and fiction dashes are a person's |
| F3 | major | ja-chat-residue, ja-instruction-residue | Their `what` left out the source's exception, a writer's own offer or scope note | fixed |
| F4 | major | ja-bold-not-rendered | Counted alone in documents and posts, where a person makes the slip too | fixed: the maintainer's call, usual for `email` and `message` only |
| F5 | blocker | ja-calques, ja-copy-fragments | Examples rebuilt from the MIT sources' own examples | fixed: the maintainer's call, a blocker as for Korean; nine examples written anew |
| F6 | minor | ja-gpt-4-ya-lists | Its scope contradicted its source | gone: the maintainer cut it, with ja-claude-3-connectives |
| F7 | minor | ja-thin-human-markers | Named ため, which its source doesn't | fixed |

The maintainer's rule that a weak cluster needs 3 different words or phrases (#21) came from this review's F1 and F2.

## Round 2

**Where:** `f0ebede..8347fe2`, rebased onto #21. F1 to F5 and F7 held.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| N1 | major | seven weak signs | Plain business chat reached a weak cluster (温度感, 肌感, アグリー, アライン) | fixed in `7c9df76`: ja-texture-words, ja-preface-filler, ja-stiff-wording, ja-noncommittal, ja-copy-fragments, ja-stock-metaphors and ja-calques read posts and documents only; the review's lines and a dev-chat line held to no cluster |
| N2 | minor | tests/test_office_ja.py | `_weak_hits` counted a repeated dash as several hits | fixed: counts as the rule does |

## Closed

`7c9df76`: eight mutants, each sign moved back to every kind and the old counting, each fail a test. The maintainer
merged without a third round.
