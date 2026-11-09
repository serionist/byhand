---
subject: "Narrow es-mixed-address and ar-register-drift, both still weak (PR #88)"
base: main (63c88f0)
head: 791a58d
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the files by the main session)
verdict: clean
---

# Narrow es-mixed-address and ar-register-drift: code review

The reviewer read the issue, #82 and its review, `propose-signs` step 5, the diff and the three sources at their cited
commits, and ran `byhand validate` and `byhand render --check`. It found every factual claim in the TOML comments, the
CHANGELOG and the PR borne out, and agrees both signs stay weak. No blocker or major: the minors are fixed in this
round and the review ends, as `REVIEW.md` says.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `es.toml`, `es-mixed-address`'s `instead` | A tú mail closing on a usted set phrase (No dude en contactarme), which the file's header calls a person's, was not among the exceptions, so `check` would count one weak hit on it | fixed: "a set closing in usted (No dude en contactarme)" added, in order |
| F2 | minor | `CHANGELOG.md` | "only in Qwen's drafts" holds for `write`; `check` reads every family unless the user names one | fixed: says `/byhand:write` loads it only for Qwen's drafts |
| F3 | minor | the plan's #85 row; the PR body | (a) the row said "(this PR)", not #88; (b) "four sign files change" where three do and one moves | fixed |

## Refuted

- `ar-register-drift` meets #72's bar: one unmeasured remark on one small model, from annotators at 50.06% who took
  36% of people's tweets for a machine's.
- Scoping it to `qwen` breaks a skill or a test: `write` reads a missing file as no signs, `check` reads `ar/check.md`,
  which still holds it, and only `zh/any.short.md` is named in a test.
- An open range is wrong: the Hungarian Qwen signs are open too.
- Something else still describes the old scope: only dated reviews.
- The cited `omel` file is one the refresh doesn't watch: it is a frozen copy.

## Improvements

| Improvement | Answer |
|---|---|
| Say why `ar-register-drift`'s Qwen range stays open | taken |
| Name usted set phrases in a tú mail as one more reason the Spanish sign is weak | left: F1's `instead` now leaves them alone, which is what the reader needs |

## Not covered

`gate.py full` on the reviewer's side (read-only). Privacy, compatibility beyond `render --check`, and harness
integrity had nothing in scope.

The fixes were checked in the main session: `byhand render`, `gate.py quick`, then `gate.py full` on the head.
