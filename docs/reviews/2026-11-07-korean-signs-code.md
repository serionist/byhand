---
subject: "Bootstrap step 4, the Korean signs (PR #17)"
base: main (70dd6ed)
head: 3bad4a2
date: 2026-11-07
round: 1
tier: standard (a fresh reviewer per round on Claude Opus 5.5, every lens; the last change verified by the main session)
verdict: needs-fixes
---

# Review: Bootstrap step 4, the Korean signs (PR #17)

Three rounds by fresh reviewers, each writing their own plain Korean work texts (합쇼체 and 해요체 mail, KakaoTalk,
Slack, reports, corrections with X가 아니라 Y) and the lines each sign is for, running every pattern under Python and
ripgrep, and copycheck over im-not-ai, slop-gate and Lee et al. 2026.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | blocker | nine signs | `what`, `instead` or `flags` carried im-not-ai's wording into English, which copycheck can't see across languages | fixed: the maintainer's call, a blocker under the repo's own rule whatever the licence; rewritten from what each sign does in a draft |
| F2 | major | ko-beyond-mere | Fired on the "exceeds" sense of 넘어서다 ("단순한 오타 수준을 넘어서는 오류는 발견되지 않았다") | narrowed, then made weak in round 3 |
| F3 | minor | ko-comma-after-ending | Matched sentence-initial 하지만, 그렇지만 | fixed |
| F4 | minor | six weak signs | Inflected forms missed | fixed, held by `FORMS` |
| F5 | minor | three signs | Claims beyond Lee and im-not-ai | fixed |
| F6 | minor | tests | A mutant to a bare 넘어 passed | fixed |
| F7 | minor | docs | The plan's row; AGENTS.md shared with #16 | fixed |

The maintainer cut ko-gemini-hype, which its own source says is no signal.

## Round 2

**Where:** `3bad4a2..616e255`. F1 and F3 to F7 held.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F2 | major | ko-beyond-mere | Still fired on the limit sense with 범위 | narrowed again, then made weak in round 3 |
| N1 | minor | the check's comment | It claimed every 넘어서는 is a limit | fixed |
| N2 | minor | ko-wrap-up-words | Missed -다고 할 수 있습니다 | fixed |

## Round 3

**Where:** `616e255..c498f32`, rebased onto #21's cluster rule. N1 and N2 held.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F3 (r3) | major | ko-beyond-mere | Limit nouns are an open set: 선, 권한, 영역, 조건, 역할 still fired on plain mail ("단순한 실수의 선을 넘어선 일이라 공식적으로 보고하겠습니다") | fixed in `3ceb336`: the maintainer's call, the sign is weak, which REVIEW.md counts as loosening a check and the maintainer agreed to; the noun exceptions go; six limit lines held to no weak cluster |
| F4 (r3) | minor | ko-beyond-mere | The 도 exception hid "단순한 제도를 넘어" | fixed: the exceptions are gone |

## Closed

`3ceb336` verified in the main session: no Korean sign counts alone, and the test that says so fails if
ko-beyond-mere goes back to `usual`. The maintainer merged without a fourth round.
