---
subject: "Pick a style by what its name says (PR #111)"
base: main (ba26c2f)
head: 5f52de2
date: 2026-11-12
round: 1
tier: standard (one fresh reviewer on Claude Fable 5.2; findings checked against the code by the main session)
verdict: clean
---

# Review: Pick a style by what its name says (PR #111)

One fresh agent read the pack (`git diff origin/main...HEAD` at `5f52de2`), AGENTS.md, REVIEW.md, issue #110 and every
touched file, with every lens. There is no plan: the PR says `Trivial:`. Minors only: **clean**. The main session
fixed them in `2f79506`, and the tries in real sessions (Live run) changed the rule further, so a second round read
that commit.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `plugin/skills/write/SKILL.md`, step 4 | The pick by name had no word on the kind: with `clients` the default for email and `work-decks` the default for deck, a deck for a client kickoff is drafted from the mail style | fixed: only a style that is the default for no kind is picked by its name. `2f79506`; `test_write_picks_a_style_by_its_name_before_the_users_default` holds the wording. In sessions after the fix the own default for deck was read in 5 of 6 runs of this case; in the sixth `write` did not start |
| F2 | minor | the release, `docs/releasing.md` step 3 | The PR did not say whether the minor's empty-session try ran or waits | wontfix here: it installs from the marketplace, which serves `main`, so it runs right after the merge, and the PR says so |
| F3 | minor | `tests/test_render.py` | The new test held the order of the picks and not the rule's guards, so a trim to the byte ceiling could cut "never a stretch" with CI green | fixed: the test asserts each guard. `2f79506` |
| F4 | minor | `write` step 4, in a session | A mail to a landlord opened the style `vendor` before it settled on the default: a second style in one draft's context | better, and not provable by reading: with the pool narrowed to styles that are the default for no kind, the 8 landlord runs after `2f79506` opened one style each |

Refuted: raising the byte ceiling weakens a test (its comment says a change that needs more raises it there, and
`CHANGELOG.md` names the number); new behaviour without a test (the test fails on `main`, and the gate refuses a seed
script in `plugin/evals/`); a plan was needed (`docs/plans/README.md` lists how styles are learned or kept, not how
one is picked); a cloned repo's style named `friends` takes the user's mail (the first draft in a project's style
names it, and a style is followed for how to write only); the styles' format (untouched); the version step (a minor,
the newest dated section, no other open PR); the user's styles in the PR (it holds no text of one); the root README
(still true; see I2); the issue's milestone (none covers it); the byte test on Windows (`eol=lf`, and CI's Windows
jobs passed).

Not covered: catalogue-contract, harness-integrity and compatibility had nothing to read. What the pick does in a
session cannot be reviewed by reading: see Live run.

| Improvement | Answer |
|---|---|
| I1: "of several, this kind's default, else the first" can be read as "use the kind's default, whichever it is" | taken: the tie reads "the first whose name is what" |
| I2: the root README describes defaults only | later: #109, which rewrites it |
| I3: one line under a draft whose style was picked by its name; a wrong pick is silent | taken, on the maintainer's yes: "In your style `<style>`." under a style's first draft. `ff69394` |

## Round 2

**Where:** PR #111 at `2f79506`. One fresh agent on Claude Fable 5.2 read `git diff 5f52de2..2f79506`, the whole
diff and the touched files, and worked five cases through step 4 as written. **Verdict:** clean. F1, F3 and I1 fixed,
F2 said in the PR, F4 better. Two new minors, fixed in `ff69394` and checked by the main session.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F5 | minor | `plugin/README.md` and `CHANGELOG.md` against `write` step 4's fourth pick | The docs said "with no plain fit the default holds", and not what happens with no default for the kind: with `work-mail` the default for email and `friends` the default for nothing, a Slack message to a manager is written in `friends`, the one style that is the default for nothing. The behaviour is `main`'s, and a style named for a reader makes it sharper | fixed in the docs: `plugin/README.md` names the fallback. The behaviour stays, as the issue keeps the old order below the pick by name. `ff69394` |
| F6 | minor | `plugin/skills/learn/SKILL.md`, step 3 | "`write` picks a style by it when the user names none" stopped being true for a style that is a default, once F1 was fixed: `learn` proposes `clients`, the user makes it the default for email, and no deck for a client is written in it | fixed: "and the style is the default for no kind". `ff69394` |
| F7 | minor | `write` step 8, in a session | Found by the main session in the live run: a draft in the user's default carried "In your style `<style>`." in 2 of 6 runs, though the line is for a pick by name | wontfix: the style and the draft are right and the line names the right style. "never for their default" moved it from 2 of 4 to 2 of 6; another wording was not tried |

Refuted: the new sentence breaks with no project (a missing index is none); a project's style by name before the
project's default breaks 0.3.0's promise (that promise was the project's default against the user's own styles, which
holds, and `CHANGELOG.md` says what moves); the ceiling raised and a pick string dropped loosens a check (the
assertions grew, and tests are not the harness); `suppliers` should beat `vendor` for a mail to a supplier (the rule
says the first, and `vendor` for a supplier is its own example); a cloned repo's style named for a reader now takes
drafts ahead of the user's default (the project styles' plan accepts it, and the draft names the style); a mail to a
friend with `friends` the default for message goes out in `work-mail` (by design: a default stays with its kind).

Two things in `2f79506` and `ff69394` answer no finding. The order in a project, each list read the same way, came
from the live run; round 2 read it and found the skill, the docs, the issue and the PR agree. The line under a draft
is I3; no fresh reviewer read `ff69394`.

## Live run

Claude Code 2.1.321, claude-fable-5-2, English and Hungarian: `claude --plugin-dir plugin -p` with
`--allowedTools Read,Skill`, the installed copy turned off, in empty folders holding invented project styles
(`friends`, `vendor`, `house`, `clients`, `team-notes`). The maintainer's own styles were on the machine, so a run
with no fitting project style read them; none of their text is in the repo or the PR.

Four wordings failed in a session and were changed:

- "none or two: go on" sent a mail to a vendor to the default, with a project `vendor` and an own style that fitted;
- "a clear fit, never a guess" wrote a mail to a landlord in `vendor`;
- with no word on the kind, a deck for a client was drafted in the project's mail style `clients`, in one run of two;
- with the project's default before every name, one run of four took the project's `friends` over the project's
  `house` for a mail to a friend, and said why. The order now says so.

On the rule as it is (`2f79506`), 18 runs:

| Request | Styles there | Runs | Style read |
|---|---|---|---|
| a mail to a friend | project `friends` and `vendor`, no default; an own default for email | 1 | `friends` |
| a mail to a vendor | the same, and an own style whose name fits too | 1 | `vendor`, the first of the two |
| a mail to the CEO | the same, and an own style named for leadership | 1 | the one named for leadership |
| a mail to a landlord | the same | 3 | the own default for email, and no other style opened |
| a mail to a dentist's office | the same | 1 | the own default for email |
| a message to a friend, in Hungarian | the same, an own Hungarian style named for a friend, an own default for message | 1 | the one named for a friend |
| a mail to a friend | project `house`, the default for email, and `friends` | 3 | `friends` |
| a mail to the CEO | project `clients`, the default for email; an own style named for leadership | 3 | `clients` |
| a blog post for the team | project `team-notes`, no default; an own default for post | 1 | `team-notes` |
| a deck for a client kickoff | project `clients`, the default for email; an own default for deck | 3 | the own default for deck twice; once `write` did not start |

With the line (`ff69394`), 8 more runs: the two picks by name (the CEO, the Hungarian friend) each read the same style
and ended "In your style `<style>`."; the 6 runs of the landlord and the dentist read the own default, and 2 of them
carried the line as well (F7). A run before the last wording showed the project's line under both project styles.

What it could not show:

- more than three runs of a request, another model, a language other than English and Hungarian;
- a user with no project index: every run had one, so round 2's cases with own styles only are read, not run;
- whether `main` adds a line naming the default too: not compared;
- the one deck run in which `write` did not start: the session went for the mail connector instead, was refused, and
  wrote an outline by itself. `write`'s description doesn't change here.

## Checks

`uv run tools/gate.py full` passed on `5f52de2`, `2f79506` and `ff69394`: 22 checks, 4,136 tests.
