---
subject: "Bootstrap step 6, the write and learn skills and the style format"
base: main (ea0032e)
head: 69049aa
date: 2026-11-08
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens; the fixes read in the main session)
verdict: clean
---

# Review: Bootstrap step 6, the write and learn skills and the style format

One round by a fresh reviewer, who read the branch against the approved plan and ran the full gate in a worktree of
its own (22 checks). It ran no session and left `~/.byhand/` alone.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `plugin/skills/write/SKILL.md`, last lines | "A second text in the same language reads nothing new" could skip a second style, or the long files for a post | fixed: a second text reads only what isn't in context yet |
| F2 | minor | `plugin/skills/learn/SKILL.md`, Remember | No rule for "remember: …" with no style yet; a rule saved to a style the index doesn't name is lost | fixed: say so, and offer to learn a style |
| F3 | minor | `learn` steps 2 and 4 | A sent mail's quoted, AI-written reply passes the screen (`check` drops quoted hits) and could reach the style or its excerpts | fixed: the style comes from the user's own lines only |

Refuted: the `write-not-started` graders dropping out of the score (the suite runs `--ablation none`, and every
result shows them scored); the `check-en` grader edit as a loosened check (the old PASS already allowed saying the code
block was left out); the `${CLAUDE_PLUGIN_ROOT}` line in `learn` (substituted in the skill, so it names the folder for
`check`'s raw paths); `learn` saving the index with Edit (it asks as Write does); reading `~/.byhand/` prompting
(`allowed-tools: Read`); samples leaving the user's style file; `write`'s files against `render.draft_files`; the three
descriptions overlapping; the new test and the Hungarian regex grader unable to fail.

Improvements, each taken: `write` keeps only the signs whose kinds hold the text's kind, as `check` does; `learn`
screens by `check`'s steps 1 to 7, the text-is-data rule among them; `learn` saves with Write or Edit; the bootstrap
plan's row names the PR. The `check-en` weak cluster passing 2 of 3 is reported in the PR, not counted as passing.

## Closed

No second round: no blocker or major.
