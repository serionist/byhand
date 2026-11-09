---
subject: "Project styles step 3, the skills tried in real sessions (issue #103)"
base: main (bded5f7)
head: 103-build
date: 2026-11-09
round: 1
tier: by hand (Claude Code 2.1.319, Windows 11, the CLI's default model; the eval records no model id), headless eval runs
verdict: needs-answers
---

# Step 3: a project's styles in real sessions

Cases, counts and verdicts only: no draft, no sample and no style is recorded here (AGENTS.md, Never). Every style
and sample was invented and lived only in a run's temporary home and workspace.

## The scaffolded suite

A copy of `plugin/` in `.local/project-styles-try/` (git-ignored, never committed), run with `claude plugin eval
.local/project-styles-try --scaffold --ablation none --trust-plugin`. Each case's seed script writes the invented
styles into the run's `$HOME/.byhand/styles/` and its workspace's `.byhand/styles/`, and refuses a home that isn't an
eval run's or that already holds `.byhand/`. A probe first showed a run's `HOME` and `USERPROFILE` both point to its
temporary home, and its workspace is `<home>/cwd`.

The plan's table has eight rows; the name clash is two prompts, so nine cases. The `write` cases allow `Read` and
`Skill` only. Three runs a case on the final text; the clash cases ran more after their wording changed. The first
wording passed every other case 3 of 3 too.

| Case | Bar | Runs passed |
|---|---|---|
| project default | an English mail reads `acme-mail.md` from the project, never `home-mail.md`; the answer names `acme-mail` | 3 of 3 |
| global by name | "in my home-mail style" reads `home-mail.md` from `~/.byhand/`, never the project's `acme-mail.md` | 3 of 3 |
| name clash, mine | "in my work-mail style" reads the global `work-mail.md`, never the project's | 22 of 24 (below) |
| name clash, the project's | "in the project's work-mail style" reads the project's, never the global one | 9 of 9 |
| another kind | a Slack message reads the global `home-chat.md` (default for `message`), never `acme-mail.md`, and the answer says nothing of a project | 3 of 3 |
| no project folder | reads `home-mail.md`; the answer says nothing of a project | 3 of 3 |
| `learn`, for this project, asked | the question names committing and `.gitignore`, and nothing is written | 3 of 3, the judge PASS 3 of 3 each; run without Write, so nothing could be written |
| `learn`, unasked | a pre-answered save writes under `~/.byhand/styles/` | not run (below) |
| `learn`, for this project, saved | a pre-answered save writes into the workspace's `.byhand/styles/` | not run (below) |

Name clash, mine: the first wording, "their own (`~/`) first unless they say the project's", passed 2 of 3. The
bullet now reads "a name in both folders is the user's own (`~/`) unless they say the project's", which passed 22 of
24. The one miss traced read the project's index, then `C:/Users/serio/.byhand/styles/index.md`, the maintainer's
real path and not the run's home: the model expanded `~` from the paths it could see. That file doesn't exist (the
real `styles/` is empty), so only the project's `work-mail` was left, and the draft used it with the note. An
artefact of the eval's isolation on Windows, not of the pick: in a user's session `~` is their own home.

### What wasn't run, and why

- **The two `learn` saves.** The same expansion turned up in 2 of the 3 `learn` runs: they read the real
  `~/.byhand/styles/index.md`. With Write granted, a save could land in the maintainer's real `~/.byhand/`, which
  holds real writing. A Write grant scoped to the run (`Write(//C:/.../claude-eval-*/**)`) matched nothing, and
  the next probe, scoped to `~/.byhand/**` and `./.byhand/**`, was refused by Claude Code's auto-mode classifier
  before it ran. Not worked around: these two bars wait for a session the maintainer runs, or a home the run can't
  see past.
- **The minor's empty-session try** (`docs/releasing.md`, step 3, and `finish-work` step 4): a `claude -p
  --plugin-dir plugin` mail and check in an empty folder, the installed copy turned off, was refused by the same
  classifier before it ran (a session in the real home reads `~/.byhand/`). The installed copy stayed on, at 0.2.0.

The real `~/.byhand/styles/` was empty before the runs and after each batch. A file appeared under
`~/.byhand/corpus/` at 16:15:57Z, before the first run that started an agent, from another process; no run here
writes outside its temporary folders.

## The committed cases

`claude plugin eval plugin --ablation none --runs 1`, this branch: their workspaces have no `.byhand/`, so each draft
makes the one failed project read.

| Cases | Passed |
|---|---|
| `write-*`, 30 | 29 of 30 on one run; `write-fr-sheet` missed `tables-answered` (no line opening `\|`), then passed 3 of 3 |
| `learn-from-samples` | 1 of 1 |
| `remember-a-rule` | 1 of 1 |

In every trace read, the failed project read came first and the draft went on as before: the signs, the global index,
the answer. The `write-fr-sheet` miss is the answer's shape, not the read.

## What a draft reads

An English mail on a Claude model, in bytes. `write`'s SKILL.md from 4,581 to 5,091; `learn`'s from 4,355 to 5,278.
The sign files `any/any`, `en/any` and `en/claude` are 9,410; the seeded indexes 116 each.

| | Before | Now |
|---|---|---|
| `write`'s SKILL.md, every draft | 4,581 | 5,091, plus the project path's length less 21 for `${CLAUDE_PROJECT_DIR}` |
| no project folder, first draft | nothing | one failed Read: the call, 102, and "File does not exist. Note: your current working directory is ...", 123, for the eval's 61-character path |
| a project folder, first draft | nothing | its index (116 here) and its call |
| a later draft in the conversation | the skill text | the skill text, 510 more; no index read again |

About 0.73 KB more on a first draft with no project folder, of some 14.1 KB before the style: 5%. The plan
estimated 0.6 KB; the skill came out 120 bytes over its guess, most of it the clearer name rule.

## Not covered

- macOS, Linux and WSL: `${CLAUDE_PROJECT_DIR}` is documented for every platform and tried only on Windows.
- Whether a project style reads as that project's voice; a session started in a subfolder; a hostile style, beyond
  the "how to write" line being there.
