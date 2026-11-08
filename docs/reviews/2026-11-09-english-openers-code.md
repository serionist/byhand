---
subject: "More English chatbot openers in the preamble sign, and bare foster (PR #43)"
base: main (a3f36ad)
head: 7b914c4
date: 2026-11-09
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens; fixes verified by the main session, with mutants)
verdict: needs-fixes
---

# Review: More English chatbot openers in the preamble sign, and bare foster (PR #43)

Round 1 by a fresh reviewer. It probed the change with about 26 invented person lines and 16 chatbot lines under
Python, and ran the opener and one full branch under Claude Code's Grep tool. Python and Grep agreed.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | any-assistant-preamble, English branch, the bare "below is" opener | The new openers reached the text-to-send branch too, which needs no reader's text and no more or less, so a person's template to colleagues fired strong: "Below is a friendly message you can share with your team:", "Below is a formal letter you can send to your landlord:", "Happy to help! Here's a polite reply you can use if a customer asks for a refund:". On main that branch came only after an eager yes, which is why #35's review let the colleague case stand | fixed: the text-to-send branch keeps main's opener alone (an eager yes, then here's or here is); the other branches take the new openers. Two lines join `OFFICE` |
| F2 | minor | the same opener | "I'd be happy to help! Here's a more polished version of your email:" was missed, as `^\W*` can't reach "happy" past "I'd be" | fixed: "i'd be happy to help" joins the openers, alphabetically, with a `MACHINE` line. "Sure, happy to help!" left: rare |

## Refuted

- "Below is a more formal version for the board:" fires: the rule's letter, a register word after more or less, as
  F5 in #35's review (wontfix). The bare opener only makes it commoner.
- Person lines around the new openers pass: "Below is your revised offer letter:", "a revised version of your
  proposal:", "my revised email to the board:", "Sure thing - here's my updated CV:", "Of course - below is the
  revised quote:", "Below is a draft email you can send to parents:".
- `sure|sure thing`: "sure" is tried first, fails on " thing", then "sure thing" matches, in both engines; the list is
  alphabetical. The `-` leading `[-–—]` is literal in both.
- Grep safety: no look-around or backreference in the new text.
- Bare "foster" over-firing ("foster care", "Jodie Foster"): `en-ai-vocabulary` is weak and counts only with other
  words in a cluster; "fostering" already matched on main, and `\b` keeps "Fosterville" out.
- The `MACHINE` test now reads every sign: a weak sign has a pattern, and `counted_alone` still guards `OFFICE`.
- CHANGELOG: no entry needed, as for #35's sign change.

## Improvements

None beyond the fixes.

Not covered: privacy-and-sources, plugin-contract and harness-integrity had nothing in scope; under `plugin/` only
rendered sign files changed.

## Checks

- The fixes, one mutant each: the text-to-send branch back after the new openers fails the two new `OFFICE` lines;
  no "i'd be happy to help" fails its `MACHINE` line.
- The first commit's 7 mutants (foster needing a suffix; no happy to help; no sure thing; no dash; no below is after a
  yes; no bare below is; a bare below is taking any line) each failed `tests/test_office.py`.

