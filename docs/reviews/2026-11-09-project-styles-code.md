---
subject: "Use a project's own styles from .byhand/styles/ (PR #105)"
base: main (bded5f7)
head: 597a6b7
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer on Opus 5.5, every lens; its findings checked against the skills by the main session)
verdict: clean
---

# Round 1

The reviewer read `AGENTS.md`, `REVIEW.md`, issue #103, the plan, `docs/releasing.md`, `write-skill`, the diff and
the touched files, against every lens in `lenses.md`. It found no blocker or major. It checked the pick in `write`
step 4 against the plan's Design line by line, the new test against the base (it fails there, and for a misspelt
variable or a dropped project read), and every number in the CHANGELOG and the sessions record against the files and
the eval results.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `learn`, The format, and step 5 | "One default per kind and language: setting one takes it from the style that held it" reads across both folders: a project default for `email` would take the user's own global `email` default away, in every other project too, against the plan's "a project default is for that kind and language only" | fixed: one default per kind and language in each index; a project's default leaves the user's own in place |
| F2 | minor | `write` step 4, 8 and 9; `learn` | Started in the home folder, `${CLAUDE_PROJECT_DIR}/.byhand/styles/` is `~/.byhand/styles/`: every style reads as "this project's", the note names it on the first draft, and `learn` lists each style twice and asks which on every default or remove. The plan's Risks row covered the pick only | fixed: the home folder itself means no project styles, in both skills |

Both fixes were tried: the six `write` cases and `learn`, for this project, asked, three runs each, 21 of 21
(`docs/reviews/2026-11-09-project-styles-sessions.md`, Live run). The home folder case can't be staged in an eval
run.

## Refuted

- "Closes #103" claims more than ran: the PR and the record say which tries didn't run, and why.
- `REVIEW.md`'s "data folder" to "style folders" loosens a harness rule: both folders are the one-way door's already,
  and the plan names the edit.
- A lone non-default project style picked for other kinds: today's rule on one list, refuted in the plan's Round 1,
  and the note names it.
- Remember with a name in both folders: "ask when it isn't clear" covers it.
- The name-clash misses are a pick error: both have the grader result the traced one had, which read the real home's
  missing index.

## Not covered

- The catalogue lens: no sign changed.
- The gate: not run by the reviewer (it writes coverage files); it passed in this session on 597a6b7, and CI passed
  on the same commit.
- The second name-clash miss: its trace wasn't kept.

## Improvements

| # | Improvement | Answer |
|---|---|---|
| I1 | Say the second clash miss went untraced, so the isolation finding isn't read as covering both | taken |
| I2 | Say in the PR that the untried learn saves and the minor's empty-session try wait for the maintainer before merge | taken |
| I3 | Put `learn`'s "Read both indexes" above both sections: learning a style needs both too | taken |
| I4 | `write` step 8: "the first draft in this conversation that uses a project's style", not "the conversation's first draft in a project's style" | taken |

The gate and the tries ran again on the fixes; only minors, so no second round (`review-code`, step 7).
