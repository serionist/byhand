---
subject: "Weigh the new languages' signs on their sources, with no native-review gate (PR #82)"
base: main (ca523f9)
head: bab4faa
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: clean
---

# Weigh the new languages' signs on their sources: code review

The reviewer ran the six office tests (1,387 passed) and `byhand validate`, and ran every Spanish, Portuguese, Arabic,
Vietnamese, Italian and Turkish pattern over every office test's text with a script of its own: the counts in the PR
match, and the three dash signs also fire on other languages' office lines (18, 4 and 4), which `counted_alone` sweeps.
It checked each sign's strength against `propose-signs` step 5 and the bar #72 sets, and agrees that all 30 stay weak.
It read Wang et al.'s text and the downloaded skills at their cited commits; the other papers rest on the citations
earlier reviews checked. No blocker or major: the minors are fixed in this round and the review ends, as `REVIEW.md`
says.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `any.toml`, `any-assistant-preamble`'s Vietnamese comment | Two person's lines that fire the strong sign were "left for a native reader to judge", a deferral #72 ends, as the PR ended "a native reader's call" in `it-dash-pivots` | fixed: accepted, with #62's round-2 F5 reason (narrowing the gap fills the check budget and loses model lines) |
| F2 | minor | the plan's progress log; the PR body | The branch was behind main (#79, the Finnish seed): the log's rows conflicted, #79's row would still read "open", and the PR's Finnish line was stale | fixed: rebased on c686adf, #79's row kept and marked merged, the #72 row says fi came in under the same rule; the PR says Finnish has nothing to drop |
| F3 | minor | the PR table (`es-ai-vocabulary`); `tr.toml`'s header; the plan's #72 row | (a) humanizer-es counts adéntrate and sumérgete alone, not only in a group; (b) the office text writes zemin hazırlama only literally; (c) Hungarian had a native read, so "with no native read" misstates the rule | fixed: (a) "it counts adéntrate and sumérgete alone and the rest only in a group, and none of the six is in its 30 model texts"; (b) "office reports write rol oynamak, and both idioms' strings in their literal sense"; (c) "with no native-review gate" |

## Refuted

- `it-inflated-stakes`: SKILL-IT.md rates the empty opener P0, but its Tier 3 table names this phrase as flagged only
  at density, and the office speech fires it.
- Dropping `propose-signs`' native-speaker line loosens a check: it is a step's instruction, and #72 asks for it.
- Dropping the 12 tests weakened more than asked: each language keeps the test that no strong or usual sign fires on
  its office text, and the forms tests are untouched.
- Rewriting the 0.1.0 "Until a native speaker reads them" lines: 0.1.0 is released, so they stay, and an Unreleased
  line says what changed.
- The PR's other facts (Wang et al.'s 50.06% and 36%, b13-claude's tú and vosotros, VI-HUM-D01's low severity,
  scrittura-italiana §21, humanizer-tr's native read, #55's F14 and F19, the office lines named): as claimed.

## Improvements

| Improvement | Answer |
|---|---|
| Open the follow-up issue for narrowing `es-mixed-address` and `ar-register-drift` now | left: `gh issue create` was refused by this session's permissions; the PR carries the draft for the maintainer |

## Not covered

The papers other than Wang et al., read through their citations; `gate.py full` on the reviewer's side. The privacy,
plugin-contract and compatibility lenses had nothing in scope.

The fixes were checked in the main session on the rebased branch: `byhand validate`, `byhand render` (no change),
the office tests and `gate.py full`.
