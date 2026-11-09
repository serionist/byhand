---
subject: "Seed the Vietnamese signs (PR #62)"
base: main (c2b4841)
head: f0b9c51
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: needs-fixes
---

# Seed the Vietnamese signs: code review

The reviewer ran `byhand validate`, `byhand render` (no diff), the full test suite (3,174 passed) and
`tools/copycheck.py --run 4` (no Vietnamese hit), and scanned the office test for 5-word runs shared with
vietnamese-humanizer (only the fixed phrases it names as left alone, and one common phrase). It probed the preamble
branch with 46 lines (32 a person's, 14 a model's), the weak terms' syllable edges with 27, and 13 plain paragraphs for
clusters, and compared Python with Claude Code's Grep on 170 line and pattern pairs: no disagreement. The main session
reproduced F1 before fixing it.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `any.toml`, `any-assistant-preamble`, the Vietnamese branch | The gap before the reader's text took any relation, so a colleague who calls the reader bạn fired the strong sign with a version made from their mail or sent to it: "Dưới đây là phiên bản đã sửa theo email của bạn:", "…hợp đồng mình đã gửi vào email của bạn:", "…slide mình làm dựa trên email của bạn:" (13 of 32 such lines outside the class #24 accepts) | fixed: the text must follow của (phiên bản … của email của bạn:), +4 bytes within the check budget; the five lines are in `REPLIES`, and the `MACHINE` line with "cho tin nhắn" now reads "của tin nhắn" |
| F2 | minor | `vi.toml`, `vi-emphasise`'s citation and the header | "The one ratio above the 2022 control's 4.0" is wrong: tối ưu hóa (9.5), then chốt (8.3) and nhân tạo (7.6) are above it too; the paper names only nhấn mạnh's ratio outside the control. The skip list left out tối ưu hóa, tích hợp, thách thức, phản ánh and mở ra | fixed: "the ratio the paper names outside the control's 4.0"; the five words are in the header's skip list, with the reason |
| F3 | minor | `vi.toml`'s header, the PR description | vietnamese-humanizer rates its dense connectors (S03) medium for false positives, not high; only S04 is high | fixed: "medium and high" |
| F4 | minor | PR #62's description | The ratio (F2), the rating (F3), and "a textbook's Trong bài này" passing, while a textbook's "Trong phần này, chúng ta sẽ…" is one weak hit, as the office test's own line shows | fixed: the description is updated for the head |

## Refuted

- Weak clusters in plain Vietnamese: only `vi-article-opener`, `vi-emphasise` and `any`'s formatting checks can add up,
  so plain text reaches 2 at most; of 13 paragraphs, two reach 3 only through Markdown, one a bold word stacked on two
  weak hits (the class #55 and #58 refuted), one a bold-label list conftest counts twice where the rendered rule counts
  2.
- Syllable edges: `vi-emphasise` passes "nhấn nút mạnh", "nhấn mạnhh", "nhan manh"; "nhấn mạnh tay" fires, accepted and
  written in the sign's comment. `vi-article-opener` passes "chúng tôi", "mình", "Bài viết này…", "Trong bài này".
  Misses on a no-break space or two spaces are minor at most for a weak sign.
- NFC and case: every touched file is NFC; combining form is unmatched in Python and Grep alike, as the header says;
  Vietnamese capitals fold alike in both.
- Order: every alternation sorts by `tests/test_order.py`'s rule; no alternation holds đ.
- Citations: the skill's "Đầu ra" line, VI-HUM-D01, slop-gate's ten rules, the 2022 control's 9.1 pp on "bài viết",
  Wang et al.'s D.9 and the exceptions of S01, L01, L02 and D02 are as cited.
- Copying: the term is VI-HUM-D01's short regex narrowed, a fixed string; `flags` and `passes` are on our own subjects.
- The rendered "Words:" line (display only, #58's class); the budget's description; the docs.

## Improvements

| Improvement | Answer |
|---|---|
| Write down for the next seeds that the check budget is full at ja (4 bytes left after F1), so it, tr and id must start by cutting, the English preamble branch's repeated noun lists the cheapest place | taken: the PR says so; the follow-up issue for the cut is drafted for the maintainer, as `gh issue create` was refused in this session |
| `vi.toml` line 18 was 121 characters | taken: the header is rewrapped to 120 |
| The header named slop-gate's lưu trú, and its rule is "lưu trú\|cư trú" | taken |

## Not covered

privacy-and-sources, plugin-contract and harness-integrity: no skill, agent, refresh or harness file is in scope. The
plugin sessions, which the main session ran. Whether a native speaker finds the signs and the person's lines natural.

## Round 2

A fresh reviewer, on bfde69c (the fixes since f0b9c51). Verdict: clean. F1 to F4 hold: the five `REPLIES` lines F1
added fire under f0b9c51's branch and pass now (`test_no_sign_that_counts_alone_fires_on_plain_vietnamese_work_text`),
the three `MACHINE` lines still fire, Python and Grep agree on 51 probe lines, and a Japanese check reads 32,764 of
32,768 bytes. The citation now says what Lee et al. 5.7 says, and VI-HUM-S03 and S04 are medium and high.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F5 | minor | `any.toml`, `any-assistant-preamble`, the Vietnamese branch and its comment | Still fires on a version made from the reader's mail with a second của ("…theo nội dung của email của bạn:") and on a converted copy ("Dưới đây là phiên bản PDF của văn bản của bạn:"); the comment said all such versions pass | fixed in part: the comment names both as still firing, left for a native reader; "…theo nội dung email của bạn:", which passes, is in `REPLIES`; the PR asks the native reader. Narrowing the gap to `{0,20}` would fill the budget to its last byte and lose model lines with long modifiers: left |
| F6 | minor | `vi.toml`'s header, the PR description | Lee et al.'s other words were called "a field's or a year's"; the paper calls them a register group mirroring Korean and English, and sets only topic words such as chuyển đổi số aside | fixed: register words with no ratio the paper names outside its control, ordinary office words; chuyển đổi số apart |
| F7 | minor | PR #62's description | Stale test count, cư trú missing, and the plugin try not tied to a commit | fixed: the description is updated, and `/byhand:check` ran again on the head's rendered files |

Refuted: the `MACHINE` line moved from "cho tin nhắn" to "của tin nhắn" (recorded in F1; `(?:của|cho)` costs 7 bytes
with 4 left, and lets in "phiên bản chữ ký cho email của bạn"); "names outside its control" (the paper names only nhấn
mạnh's ratio so); no `\b` before của (no Vietnamese syllable ends in của); `^\W*` on quoted lines (every branch does
it); CRLF (`\s*$` takes the `\r` in both).

| Improvement | Answer |
|---|---|
| Narrow the gap to `[^:\n]{0,20}` | left: it fills the check budget to the last byte before the cut it needs, and loses model lines; a native reader can say whether the doubled của is common |
| Pin the line between what passes and what fires with "…theo nội dung email của bạn:" | taken |

The rerun of `/byhand:check` on the head, with a pasted text, read the preamble into "Dưới đây là phiên bản đã sửa theo
email của bạn:" by hand, though the pattern passes it: the model's own read of a pasted text follows the sign's `what`,
which every language shares, and is wider than the Vietnamese pattern. On a file the pattern decides. Recorded in the
PR; not this change's to fix.

The review ends here: no blocker or major is open.
