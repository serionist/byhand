---
subject: "Bootstrap step 7, the eval suite and the real-session record"
base: main (a3f36ad)
head: 3b7a74d
date: 2026-11-09
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens; the fixes read in the main session and the suite run again)
verdict: clean
---

# Review: Bootstrap step 7, the eval suite and the real-session record

One round by a fresh reviewer, who read the branch against the bootstrap plan's Step 7 and ran the full gate in a
worktree of its own (22 checks). The feedback offer (`2aebcab`) landed after its read and was tried by hand.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | the record, "an id the catalogue has never seen" | Not shown: the catalogue names Opus 5.5, and `write`'s worked example was that very id | fixed: recorded as untried; `write`'s example is a made-up id |
| F2 | minor | the record's verdict, the plan's new decision | "Every bar met" over bars not measured: prompts in manual mode, a draft after `/compact` | fixed: "every measured bar met", the rest listed as untried |
| F3 | minor | the record | The plan's token count per seed language and a verdict per draft were missing | fixed: bytes per seed language, tokens cut (no API key); the six drafts' verdict |
| F4 | minor | the record | Three cases were last run before the skills changed | fixed: the whole suite run again on the final skills |
| F5 | minor | `check` and `learn` SKILL.md | "Each new request starts this skill again" was unscoped and could pull them into another kind of request | fixed: "each new text to check", "each new request about styles" |
| F6 | minor | the plan's step 7 row | "this PR" | fixed: the PR's number |

Refuted: the suite against the plan and plugin-evals.md (every key valid, every grader can fail); the `passes` texts
(the catalogue's own, none of the 8 signs with a check); `check-de`'s preamble line; real text anywhere; the record's
counts against the result files; the backticked-id rule.

Improvements, each taken: three runs for the `passes` cases; the record says the `passes` grader began as a regex on
the id; a `check-not-started` grader in `boundary-rewrite`.

## Closed

No second round: no blocker or major. The suite on the final skills: 51 of 52 cases every run, the one miss within
its bar.
