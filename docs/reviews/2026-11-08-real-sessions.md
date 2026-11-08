---
subject: "Bootstrap step 7, byhand tried in real sessions"
base: main (a3f36ad)
head: 7-real-sessions
date: 2026-11-09
round: 1
tier: by hand (Claude Code 2.1.319, Opus 5.5, Windows), and the maintainer's own session
verdict: clean
---

# Step 7: byhand in real sessions

Cases, counts and verdicts only: no draft, no sample and no style is recorded here (AGENTS.md, Never).

## The eval suite

`claude plugin eval --ablation none`, Claude Code 2.1.319, Opus 5.5, three runs a case, every text invented and pasted
(a case gets no file the model can find; the Step 5 plan's decision). One run of the whole suite on the branch's final
skills: 52 cases, 156 runs, about $19.70.

| Bar (bootstrap plan, Step 7) | Cases | Result |
|---|---|---|
| `write` starts on writing requests: 21 of 23 | en 7, hu 4, de 3, zh 3, fr 3, ja, ko and ru 1 each; mail, chat, posts, documents, a slide | 23 of 23, every run |
| `write` starts on at most 1 of 10 others | a commit message, a README, a docstring, a PR description, a code comment, a function, an explanation, a regex, SQL, a git question | 1 of 10: the commit message, in 1 of its 3 runs |
| 6 of the 7 `check` and boundary cases | `check` in en, hu, zh, ja and de; a rewrite request (`write`, not `check`); "which lines give it away" (`check`, not `write`) | 7 of 7, every run, after `check` was told to print a sign's id in every language |
| A sign's own human text (`passes`) that `check` flags is a finding | 8 signs with no pattern | none: 8 of 8, every run |

Also passing every run: `learn` from pasted samples leaving the AI-written one out; "remember: …" starting `learn`;
a Hungarian mail from `write`, formal and with no strong sign; `write` starting on a plain Slack request and never on
`check`'s cases.

The `passes` grader began as a regex on the sign's id. It failed 4 of 8 because the answers named the sign as a near
miss and said why it didn't apply; an `llm` grader that fails only when the sign is counted replaced it.

## By hand

- **A second draft in the same session** (headless, `--continue`): before the fix, `write` was not started again, its
  read grant had lapsed and the Hungarian sign files were denied; each skill now starts itself again for its own kind
  of request. After it: `write` started, read only the two Hungarian files, no denial.
- **Feedback kept as a rule** (headless, a throwaway style, removed after): feedback that is a habit ended the rewrite
  with "Save this as a rule for work-mail?"; on yes `learn` added a dated line under `## Corrections`.

## The maintainer's session

The maintainer's own session, with their usual plugins, on Windows, 2026-11-08:

| Bar | Result |
|---|---|
| `write` starts on 9 of 10 writing requests in a crowded session | 10 of 10 |
| The maintainer's style learned from their own writing, drafts read in English and Hungarian | learned; all six drafts, three in each, read as the maintainer's own |

## What a draft reads

The largest read per seed language, across model families, in bytes (`render`'s budgets: 14, 16 and 32 KB). Tokens
were not counted: an exact count needs an Anthropic API key, which this repo doesn't hold, so the plan's token column
is cut and the bytes stand in for it.

| Language | Mail or message | Post or document | Check |
|---|---|---|---|
| en | 10,714 | 11,427 | 25,168 |
| zh | 11,975 | 13,972 | 26,482 |
| zh-Hant | 12,834 | 14,831 | 27,595 |
| de | 7,816 | 11,879 | 24,150 |
| fr | 7,363 | 13,245 | 26,265 |
| hu | 10,585 | 11,901 | 23,725 |
| ko | 11,530 | 13,388 | 25,498 |
| ja | 9,517 | 15,203 | 28,842 |
| ru | 9,450 | 13,451 | 26,767 |

## Not tried

- **Permission prompts in manual mode:** the maintainer's session ran in auto mode, which asked nothing; the one-time
  Skill allow and no prompt on later drafts stay unmeasured, as does a draft after `/compact`.
- **An id the catalogue has never seen:** none was available. The catalogue already names Opus 5.5
  (`ja-claude-version-calque` holds from 5.5), and `write`'s worked example is now a made-up id, `claude-opus-9-1`,
  so it no longer hands the model its own answer.
- **macOS, Linux and WSL.**

## Verdict

Every measured bar met. The `SessionStart` hook is not needed before the release (bootstrap plan, Q4): the crowded
session started `write` on 10 of 10.
