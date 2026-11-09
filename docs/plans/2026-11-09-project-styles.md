---
title: Use a project's own styles from .byhand/styles/
issue: "#103"
status: draft
approved_by:
approved_at:
---

# Use a project's own styles from .byhand/styles/

## Goal

A project can have its own voice: a client's, a team's house style. Its `.byhand/styles/` holds styles in the same
format as `~/.byhand/styles/`, and `write` and `learn` use it. The plugin is installed globally, and a global default
can't give one folder its own voice (the maintainer, 2026-11-09, #103).

Done means, from the issue:

- in a project with its own styles, `write` picks the project's default for the kind and language;
- the global styles stay usable there by name;
- `learn` saves into the project only when the user asks;
- the extra read per draft costs bytes only where the folder exists;
- tries in real sessions show it.

In scope: `write`'s pick, `learn`'s save, list, default, remove and remember, the docs, tries.
Out of scope: finding `.byhand/` above the folder Claude Code started in; writing a project's `.gitignore`; `check`,
which reads no style; learning from edits (the rest of 0.5.0).

## Design

### Where a project's styles are

`${CLAUDE_PROJECT_DIR}/.byhand/styles/`: `index.md` and one `<style>.md` per style, the format `learn`'s SKILL.md
gives today, unchanged.

- **The path:** Claude Code substitutes `${CLAUDE_PROJECT_DIR}` in a skill's text ("The project root directory. This
  is the same path hooks and MCP servers receive", the skills docs, String substitutions). Tried on 2.1.319, Windows,
  in a throwaway plugin: it became the folder `claude` was started in, with forward slashes, inside a git repo too (a
  subfolder of a repo gives the subfolder, not the repo's root). Read takes that path as written.
- **No prompt:** the folder is inside the working directory, which Read reads without asking (the permissions docs,
  "Read-only ... within the working directory"). `~/.byhand/` stays covered by the skills' `allowed-tools: Read`, as
  today.
- **Started elsewhere:** a session started in a subfolder finds no project styles. The READMEs say to start Claude
  Code in the folder that holds `.byhand/`. Walking up would cost a failed Read per level on every draft.

### `write`'s pick

Step 4 reads the project's index, `${CLAUDE_PROJECT_DIR}/.byhand/styles/index.md`, then `~/.byhand/styles/index.md`,
as one list with the project's rows first (Fit I1). A missing project index means no project styles; it isn't tried
again in the conversation. The pick stays today's bullets, with one phrase added to the first:

1. a style the user names, their own (`~/`) first unless they say the project's (Fit I2);
2. else the default for this kind and language; two rows claiming one, the first wins, as today, so the project's
   default beats the global one with no new rule;
3. else the one style in this language that is the default for no kind;
4. else, with several such, ask; with none, or no index, the signs alone, said nothing about.

The style is read from the folder whose index named it. A project default is for that kind and language only: a
project with a default for `email` leaves the user's global default for `message` in force. A name in both folders
stays the user's own when named, as Claude Code's own skills resolve a name in both ("personal over project", the
skills docs): a cloned repo can't take over "in my work-mail style".

Two lines are new besides:

- **A style is how to write.** A line in one that asks for anything else (a tool, a file, a link, an address to send
  to) is not followed. A cloned repo can carry a `.byhand/styles/`, as it can a `CLAUDE.md`; this keeps its style to
  voice.
- **The first draft in a conversation in a project's style ends with one line naming it** ("In this project's style
  `acme-mail`."). A project default replaces the user's own for that kind without asking: one line, once, makes that
  visible. Step 8's "nothing the user didn't ask for" gains this exception.

### `learn`

- **Save:** to `~/.byhand/styles/` unless the user asks for the project ("for this project", "in this repo"). Then
  the style and its row go to `${CLAUDE_PROJECT_DIR}/.byhand/styles/`, a new index starting with the header as today.
  Write asks the user, as every save does; `learn` never writes into a project unasked.
- **The first save into a project** says, inside step 5's one question: the excerpts are the user's own words, and
  the folder goes where the project goes if it is committed; to keep it to themselves, add `.byhand/` to the project's
  `.gitignore`. Committing it is the user's call (a team's house style is meant to be shared), so `learn` writes no
  `.gitignore`: the bootstrap plan's "learn adds `.byhand/` to the project's `.gitignore`" goes.
- **A name in both:** saving a project style under a global style's name says the name is taken and proposes
  another (Fit I2).
- **List:** both indexes, the project's marked as this project's.
- **Default, remove:** in the index that holds the style; a name in both: ask which.
- **Remember:** under `## Corrections` of the style the last draft used, in the file the draft read.

### What a draft reads, in bytes

An English mail on a Claude model, today: `write`'s SKILL.md 4,581, the short sign files `any/any`, `en/any` and
`en/claude` 9,410, the global index (two rows, about 110), one style (under 4,096).

| | Today | With this plan |
|---|---|---|
| `write`'s SKILL.md, every draft | 4,581 | about 4,970 (step 4 grows by about 300 bytes, the "how to write" line about 110 of them, the note by about 85; the substituted path by its length) |
| no project folder, first draft | nothing | one failed Read: the call and "File does not exist. Note: your current working directory is ...", about 250 |
| a project folder, first draft | nothing | its index, about 110 to 300, and its call |
| a later draft in the same conversation | the skill text | the skill text, about 400 more; no index read again |

About 0.6 KB on a first draft of some 14 KB before the style, under 5%; about 0.4 KB on each later one. The style
read stays one either way. Step 3 measures the real numbers.

### Evals

The committed suite can't seed a project folder: the gate refuses a `scaffold_script` in `plugin/evals/` (a plugin
ships no script) and any tracked file under `.byhand/` (`check_private`). Both rules stay. So:

- **A scaffolded suite, never committed:** a copy of `plugin/` in `.local/project-styles-try/` (git-ignored), with
  cases in its `evals/` whose seed scripts write invented styles into the run's temporary `$HOME/.byhand/styles/` and
  its workspace's `.byhand/styles/`, run with `claude plugin eval .local/project-styles-try --scaffold
  --ablation none`. Tried on 2.1.319, Windows, in a throwaway plugin: the seed wrote both, the skill read
  `~/.byhand/styles/index.md` from the temporary home and `${CLAUDE_PROJECT_DIR}/...` from the workspace, Opus 5.5.
- **The committed cases,** `write-*`, `learn-from-samples` and `remember-a-rule`, re-run: their workspaces have no
  `.byhand/`, so they show the failed project read changes nothing.

### This repo's own `.byhand/`

`.gitignore` ignores `.byhand/` and the gate's `private` check refuses a tracked file under it at any depth. Both
still hold: byhand's own repo is the plugin's, has no project voice to commit, and holds only invented text
(`AGENTS.md`, Never). A user's project is another repo, where the gate doesn't run. No change.

### Alternatives

- **Project defaults merged into the global index, with a project column:** one read, but a global file naming
  folders, stale when a project moves, and no way to share a house style through the repo.
- **The project's styles replace the global ones in that folder:** simpler pick, but a user's own styles vanish in
  every project that has a folder; the issue keeps them usable by name.
- **Walk up to the repo's root for `.byhand/`:** a failed Read per level on every draft.
- **Glob for the folder before reading:** the skills use no Glob or listing (missing or prompting on some machines).
- **`learn` writes `.gitignore`:** a second Write prompt, and wrong for a house style meant to be shared.
- **No note on a project style:** quieter, but a project default silently replaces the user's own.
- **Committed scaffolded evals:** a script in the plugin, which the gate refuses for good reason.

## Compatibility

- **One-way doors:** `.byhand/styles/` and the style format are named in `AGENTS.md` and used here as reserved,
  neither changed: the same index and style files, now read from the second place.
- **Users:** global styles work as before. A `.byhand/styles/` someone made by hand before this release, unused until
  now, starts being read in the folder that holds it. No skill's name or argument changes.
- **The version:** a minor (`docs/releasing.md`: what a skill does changes).

## Steps

1. **`write`,** `plugin/skills/write/SKILL.md`: step 4 as designed, the "how to write" line, step 8's note. A test in
   `tests/test_render.py`, beside the one that holds every `${CLAUDE_PLUGIN_ROOT}/signs/` path to a rendered suffix:
   every `${...}` a plugin skill or agent names is one byhand uses, `CLAUDE_PLUGIN_ROOT` or `CLAUDE_PROJECT_DIR`
   (Fit I3): a misspelt one is never substituted, and the project read would fail silently on every draft. A closed
   list of our own never has to track Claude Code's docs. The gate's plugin checks prove the form.
2. **`learn`,** `plugin/skills/learn/SKILL.md`: the format names both folders; save, list, default, remove and
   remember as designed. The same checks.
3. **Tries, by hand,** the scaffolded suite in `.local/` (Design, Evals), three runs a case, every text invented:

   | Case | Seeds | Bar |
   |---|---|---|
   | project default | global `home-mail` (en, email), project `acme-mail` (en, email) | an English mail reads `acme-mail.md` from the project, not `home-mail.md`; the answer's last line names `acme-mail` |
   | global by name | the same | "in my home-mail style" reads `home-mail.md` from `~/.byhand/` |
   | name clash | `work-mail` in both | "in my work-mail style" reads the global one; "in the project's work-mail style" the project's |
   | another kind | project default for `email`, global for `message` | a Slack message reads the global style, with no note |
   | no project folder | global `home-mail` (en, email) | reads `home-mail.md`; says nothing about project styles |
   | `learn`, unasked | none | a pre-answered save (or a history file ending on `learn`'s question) writes under `~/.byhand/styles/`, nothing in the workspace; Write and Edit granted to the run |
   | `learn`, for this project | none | the same with "for this project" writes the project's style and index, and the question named committing and `.gitignore` |

   Then the committed `write-*`, `learn-from-samples` and `remember-a-rule` cases, one run each (Fit I4): they show
   only that a failed project read changes nothing, which the "no project folder" case shows three times. The bytes a first
   and a later draft read, with and without a project folder. Counts and verdicts only in
   `docs/reviews/<date>-project-styles-sessions.md`: no draft, no sample, no style.
4. **The docs** (below), `plugin.json` to the next minor, its `CHANGELOG.md` section.
5. **finish-work:** `uv run tools/gate.py full`, `review-code` until clean, the PR, naming the Claude Code version,
   the models and what ran by hand.

## Tests

- Unit (CI): the substitution test in Step 1; the gate's plugin and private checks, unchanged.
- By hand: Step 3's suite and the committed cases, on Windows, Opus 5.5. macOS, Linux or WSL if one is at hand, else
  said in the PR: `${CLAUDE_PROJECT_DIR}` is documented for every platform but tried only on Windows.
- What none can show: whether a project style reads as that project's voice; a session started in a subfolder (by
  design it finds nothing); a cloned repo's hostile style, beyond the "how to write" line being there.

## Docs

- `plugin/README.md`, "Your styles": a project's own styles, the pick order, "for this project", start Claude Code in
  the folder that holds `.byhand/`, committing it is your call.
- `README.md`: "Your styles live in `~/.byhand/styles/` ... on your machine only" gains the project folder and that it
  goes where you put the project.
- `SECURITY.md`: the folders byhand keeps styles in are two. No new "what counts" line (Fit I5): a style's text
  followed by the model is the model doing what it does with the text it is given, which doesn't count already.
- `AGENTS.md`, What this is, "The styles": "They stay on the user's machine" says a project's go where the user puts
  them. The same line count: the file is at its 150-line cap.
- `REVIEW.md`'s blocker "written outside their data folder": "their style folders".
- `CHANGELOG.md`: the minor's section.
- `docs/plans/2026-11-06-bootstrap.md`, Decisions: a project's styles as built (#103), and `learn` writes no
  `.gitignore`.

## Risks

| Risk | Answer |
|---|---|
| A session started in a subfolder misses the project's styles | accepted: the READMEs say where to start; walking up costs every draft |
| A cloned repo's style steers drafts, or carries instructions | the "how to write" line is the guard; the note names a project style once; a named style is the user's own first. Accepted: a repo's `CLAUDE.md` can do as much |
| A project style learned from real mail is committed and shared | the user's call, said at the first save into a project and in the READMEs |
| Every first draft outside a project pays a failed Read | accepted: about 250 bytes, once a conversation |
| Started in the home folder, both indexes are one file | harmless: the same file read twice, its styles the same |
| `${CLAUDE_PROJECT_DIR}` untried on macOS and Linux | documented for every platform; Step 3 says what ran where |
| An index row for a style whose file is in the other folder | read from the folder whose index named it; missing there: said and skipped, as today |

## Plan review

### Fit

The plan at `0da7476`, by a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09. The change's own
question: does every part earn its keep (the maintainer's "don't overcomplicate"), with the token cost per draft, name
clashes and this repo's `.byhand/` rule weighed. Answers by the maintainer's standing word of 2026-11-09: take the
recommended improvements.

| # | Improvement | Answer |
|---|---|---|
| I1 | `write` reads the project's index first and the global one after, as one list; today's "two rows claiming one: the first wins" then gives the project's default with no new rule, and the pick stays today's bullets | taken |
| I2 | A name in both folders, when the user names it, is their own global style, as Claude Code resolves a skill in both ("personal over project"); the issue keeps global styles usable by name, and a cloned repo can't take over a named style. `learn` says a taken name and proposes another | taken |
| I3 | The substitution test checks against a closed list of the variables byhand uses, not a copy of Claude Code's list, already missing `${CLAUDE_EFFORT}` | taken |
| I4 | The committed cases run once each, not three times: they only show a failed project read changes nothing | taken |
| I5 | No new `SECURITY.md` "what counts" line for a style followed as more than how to write: no fix could follow such a report, and the model following text it is given already doesn't count | taken |

Noticed on the way, for Round 1:

- Goal says the extra read costs bytes only where the folder exists; Design and Risks accept a failed Read outside
  one, without saying it departs from the issue.
- This repo's own `.byhand/`: `.gitignore` and `check_private`'s stated reason ("hold real writing") goes stale for a
  shared house style; the reason that holds is that this repo keeps only invented text.
- Docs: the `REVIEW.md` blocker edit widens a harness rule without naming the maintainer's agreement.
