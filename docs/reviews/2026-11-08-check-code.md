---
subject: "Bootstrap step 5, the check skill, its scan agent and the split sign files"
base: main (c49fc74)
head: 8291265
date: 2026-11-08
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens; the fixes verified by their tests and a new eval run)
verdict: needs-fixes
---

# Review: Bootstrap step 5, the check skill, its scan agent and the split sign files

One round by a fresh reviewer, who read the branch against the approved plan, ran the gate in a worktree of its own,
mutated `render.py` six ways (each caught by a test), and ran its own headless session with the plugin outside the
working directory: `scan` read the check files and ran about 33 Grep calls with no permission denial.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `plugin/skills/check/SKILL.md`, step 6 | Pasted text has no scan, and step 6 read only the signs with no pattern and then scan's hits, so a literal reading skipped every word and pattern sign; each failed eval grader was such a sign | fixed: pasted text is read for every sign, the patterned ones by their Words and Pattern |
| F2 | minor | `src/byhand/render.py`, `words` | Python's parser folds a prefix two alternatives share, so five terms lost a word (不可否认的是, "underscore a"); an optional group ending in a space printed a word the bare form lacks ("im digitalen zeitalter"); a negated class could print a character it excludes; a stem read as a typo ("служ") | fixed: alternatives split on the term's own text; an optional group prints only with no letter; a negated class and a stem's open end print "…"; a test that every top-level alternative of the catalogue has its word |
| F3 | minor | `check` SKILL.md, Answer | Said the patterns don't run for a language with no signs, though steps 4 and 5 scan its file with `any` | fixed |
| F4 | minor | `plugin/evals/` | The cases hold less than Step 4 listed (a strong sign and a weak cluster in each) | fixed in the plan: Step 4 says what each case holds and why |
| F5 | minor | `CHANGELOG.md` | "Nothing to use yet" beside the new `check` line | fixed |

Refuted: `scan` prompting for the check files outside the working directory (the reviewer's own try: no denial);
`allowed-tools: Read` falling short (`check` calls Read and Agent, which asks nothing); `scan`'s Grep call; the
no-check grader; `words` crashing on any op the catalogue uses; the gate's agent check; the maintainer's three calls;
the budgets (largest reads 12.5, 14.8 and 28.1 KB of 14, 16 and 32); eval results committed (`.gitignore`).

Improvements: `scan`'s unused patterns input, taken (dropped); the en code-block grader as an `llm` grader, so a right
answer naming the id it left out passes, taken; the hard-coded family list in `check` step 3, taken (the check files'
ranges name them); "foster" missed by `en-ai-vocabulary`'s term, later: #38.

## Closed

The fixes are pinned by `tests/test_render.py` and checked by a new eval run, in the PR. No second round: no major is
left.
