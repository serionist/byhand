---
subject: "Bootstrap step 7, byhand tried in real sessions"
base: main (a3f36ad)
head: 7-real-sessions
date: 2026-11-08
round: 1
tier: by hand (Claude Code 2.1.319, Opus 5.5, Windows), and the maintainer's own session
verdict: clean
---

# Step 7: byhand in real sessions

Cases, counts and verdicts only: no draft, no sample and no style is recorded here (AGENTS.md, Never).

## The eval suite

`claude plugin eval --ablation none`, Claude Code 2.1.319, Opus 5.5, three runs a case unless named, every text
invented and pasted (a case gets no file the model can find; the Step 5 plan's decision).

| Bar (bootstrap plan, Step 7) | Cases | Result |
|---|---|---|
| `write` starts on writing requests: 21 of 23 | en 7, hu 4, de 3, zh 3, fr 3, ja, ko and ru 1 each; mail, chat, posts, documents, a slide | 23 of 23, every run |
| `write` starts on at most 1 of 10 others | a commit message, a README, a docstring, a PR description, a code comment, a function, an explanation, a regex, SQL, a git question | 0 of 10 |
| 6 of the 7 `check` and boundary cases | `check` in en, hu, zh, ja and de; a rewrite request (`write`); "which lines give it away" (`check`) | 7 of 7, every run, after `check` was told to print a sign's id in every language |
| A sign's own human text (`passes`) that `check` flags is a finding | 8 signs with no pattern, one run each | none: 8 of 8 left their sign uncounted, some naming it as a near miss |

Also in the suite and passing: `learn` from pasted samples leaving the AI-written one out; "remember: …" starting
`learn`; a Hungarian mail from `write` with no strong sign; `check` never starting on a plain writing request.

## By hand

- **A second draft in the same session** (headless, `--continue`): before the fix, `write` was not started again, its
  read grant had lapsed and the Hungarian sign files were denied; each skill now starts itself again per request.
  After it: `write` started, read only the two Hungarian files, no denial.
- **An id the catalogue has never seen:** Opus 5.5's id, `claude-opus-5-5`, is newer than every closed range in the
  catalogue; it read its family's open ranges and the `any` files.

## The maintainer's session

The maintainer's own session, with their usual plugins, on Windows, 2026-11-08:

| Bar | Result |
|---|---|
| `write` starts on 9 of 10 writing requests in a crowded session | 10 of 10 |
| Permission prompts on later drafts: none | not measured: the session ran in auto mode, which asked nothing; the one-time Skill allow in manual mode stays untried |
| The maintainer's style learned from their own writing, drafts read in English and Hungarian | learned; the drafts read as the maintainer's own |

Not tried: macOS, Linux and WSL.

## Verdict

Every bar met. The `SessionStart` hook is not needed before the release (bootstrap plan, Q4).
