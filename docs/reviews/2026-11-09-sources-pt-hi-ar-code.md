---
subject: "Add the first sources for Portuguese, Hindi and Arabic (PR #52)"
base: main (52331c8)
head: 1db9fce
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, every lens; F1 checked against the repo by the main session)
verdict: clean
---

# Review: Add the first sources for Portuguese, Hindi and Arabic (PR #52)

One fresh reviewer read the pack (`files.txt`, `scope.diff`), issue #49, the plan's Step 2 and move 1, the
find-sources skill and the earlier research records, and checked each new source against the work itself: licences,
commits, revisions, feed paths, and the record's numbers and findings. Five minors, no blocker or major, so no second
round. The main session confirmed F1 with `gh api` (the prompt in `eval/textos/ia/01-email-relatorio/meta.yaml` and
the README's "Como foi feito") before fixing it. The dated record is never edited after merge, so the minors were
fixed now.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | the record, `humanizer-pt-br` row and the order's pt row; the PR body | The 5.93 against 0.03 was presented as measured, but every prompt asked Grok 4.7 to pack the text with tics, the control is pre-1930 fiction, and a model wrote the repo unreviewed: Step 4 would draft `grok` signs on no evidence of Grok's own habit | fixed in `02dc2f7`: the limits said, no model scope, pt's place rests on its two studies |
| F2 | minor | the record, `humanizer-pt-br` row | "two other pt skills": its originality check compares one pt skill and one zh one | fixed in `02dc2f7` |
| F3 | minor | the record, `wang-2026-human-detection` row and the order's hi row | The Hindi English-word cue (formal news only) contradicts the record's own note that Hinglish is normal: a sign from it would flag code-mixed office mail | fixed in `02dc2f7`: the news scope and the clash written beside the cue |
| F4 | minor | the record, `wang-2026-human-detection` row | The paper's caveat that human texts' plain blocks may come from collection was left out, so a "short sections" sign would flag normal paragraphed Arabic | fixed in `02dc2f7`: the caveat carried, Markdown preferred over paragraph count |
| F5 | minor | the PR body | "about 35 finds dropped": the table names more | fixed in the PR body: no count |

## Refuted

- The licences: each read on the work and holds (evitar's LICENSE is MIT although GitHub reads NOASSERTION; the three
  arXiv licences; Andrade's paper says only ©2026 ACL, so the stricter is kept; pt.wikipedia CC BY-SA 4.0).
- `read_at`: pt.wikipedia's latest revision is 73274816; each repo's head and each arXiv version match; every feed
  path exists at its commit.
- A version on a `none` feed's `read_at`: `lee-2026-korean` already does it and the loader allows it.
- Keeping `evitar-escrita-ia` without evidence: the plan asked for B18 once its licence was found, and the record
  limits it to pairing with a second source and to its false-positive list.
- Detector evasion among the kept repos: none; `MrBridgeHQ/human-writer-hi`'s drop is confirmed.
- Writing rules: no em dashes, banned words or American spellings; NFC, LF, no zero-width characters.

## Improvements

| Improvement | Answer |
|---|---|
| Give the `-I` trap its own row in the skill | taken in `02dc2f7` |
| Add Gemma and AceGPT to the families `models.toml` lacks | taken in `02dc2f7` |
| Say Andrade's terms are fake-news genre and its generation method shapes them | taken in `02dc2f7` |
| Step 6 of the skill: a paper's version in `read_at` | taken in `02dc2f7` |
| Fill the plan's progress log row 2 | left: the brief for this step said not to edit the plan; at merge |

## Not covered

- `gate.py full` was not rerun by the reviewer; it passed on `1db9fce` in the main session and CI was green.
- The refresh run, the style-guide URLs and every dropped repo were not re-checked by the reviewer.
