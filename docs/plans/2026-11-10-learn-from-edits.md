---
title: Learn a style's corrections from the user's edits to a draft
issue: "#106"
status: draft
approved_by:
approved_at:
---

# Learn a style's corrections from the user's edits to a draft

## Goal

When the user changes one of byhand's drafts and gives byhand their version, byhand compares the two, names the habits
behind the changes, and on the user's yes keeps the ones they pick under `## Corrections` in the style the draft used.
This is the bootstrap plan's `0.5.0` (`docs/plans/2026-11-06-bootstrap.md`, Styles: "`0.5.0` learns them from edits
into the same section"). Today a correction comes only from what the user says ("remember: ..."); most people fix the
draft and send it, and the fix is the best evidence of how they write.

- **In scope:** the user's version given in the conversation while byhand's draft is still in context: pasted, as a
  file they point at, or the file the draft became this session, which they only say they changed. Or both versions
  given by the user. The corrections it proposes, one question, the save.
- **Out of scope:**
  - reading what the user sent from a mail or chat app (a connector, a hook): see Design, the alternatives;
  - learning from a draft byhand no longer has and the user can't give;
  - changing a style's body or excerpts from an edit: an edit is a correction, nothing more.

## Design

Two skill changes and a test, no new skill, agent, command, file or key in a style.

### `write`, step 9

Step 9 already turns feedback on a draft into "Save this as a rule for <style>?". One sentence joins it: the user's
own version of the draft (pasted, a file they changed, or "I changed it" for the file the draft became) is feedback
too. `write` doesn't rewrite it. When the user's words already ask to learn from it ("this is what I sent, learn from
it"), `write` starts `learn` at once; for a bare version it offers, in step 9's own wording, to learn from the changes
for <style>, and starts `learn` on a yes. The offer comes only when the draft used a style, as step 9's does, and it
takes the project wording #105 gives that offer if #105 merges first.

### `learn`, Remember gains the edit

Remember already picks the style the last draft used or the one the user names, asks when it isn't clear, offers to
learn a style from samples when there is none, dates each rule and names the kind of text it came from. Learning from
an edit is Remember with rules it finds itself:

1. **The two versions:** byhand's draft, from the conversation, and the user's; or both from the user. The file the
   draft became this session is read again by its path; a deck or a sheet as `check` step 1 reads one. No draft to
   compare with: say so, and offer to learn a style from samples instead.
2. **The style,** as Remember picks it. No style: say so and offer to learn one from samples, without comparing: the
   user's version can't be a sample, so the rules would have nowhere to go. The style file is in context from
   `write`'s step 4 unless the conversation was compacted; then it is read again.
3. **The changes that are habits:** compare the two line by line, and keep a change only when it would hold for the
   next text of this kind: a greeting or sign-off swapped, a word or phrase cut or replaced, sentences shortened or
   joined, the register moved, formatting removed (bold, bullets, headings). A change to a fact of this text (a date,
   a name, a number, a point added or cut) is no correction. A change the style's rules or corrections already hold
   is no new one.
4. **Show them with one question:** each as a short rule with its before and after, numbered, and which to keep
   (all, some by number, or none). A change that puts in what a sign names (the sign files are in context from the
   draft) says so beside its rule, so the user keeps it knowingly, as the bootstrap plan has it for a learned rule
   that matches a sign. Nothing is saved on silence.
5. **Save the picks** as Remember saves a rule.

Remember gains two rules, for both ways in: a rule that repeats an older correction replaces it, with the new date;
and a style that would pass 4 KB says so, and asks which old corrections to drop or fold into the rules.

Only the changes reach the style, as rules in the skill's own words. The user's version is never an excerpt or a
sample: the lines they left as byhand wrote them are byhand's text, and learn never takes a style from AI text.

`learn`'s description stays as it is: `write`'s step 9 starts `learn` by name, and a direct "learn from my changes"
is a request to learn how the user writes, which the description already names. The eval's `learn-started` grader
(Steps) tries that first; words are added only if it fails.

### Alternatives

| Alternative | Why not |
|---|---|
| A hook that sees the sent mail or the changed file | The plugin runs no command, and the gate refuses a `hooks` key in the plugin (the bootstrap plan) |
| A connector that reads the sent mail or message | A connector is the user's to add; it would read the user's mailbox for every draft, at a cost in every session |
| byhand keeps each draft on disk to compare later | `write` would need Write, which no plugin skill pre-approves, and every draft would leave the user's text in a new folder |
| Claude Code's auto memory, which already keeps "corrections you give Claude" | Per repository, not per style or language; saved without a question; loaded into every session |
| A new skill for it | The format, the index and the corrections already live in `learn`; a new skill is one more description in every session's context |
| Learn every change, no question | A style changes only on the user's yes (the bootstrap plan, Styles) |

### Cost

- **A session with no edit:** one sentence more in `write`'s step 9, read with each draft, about 150 bytes; nothing
  in any description. A test holds `write`'s SKILL.md under a byte ceiling, set at the size this PR leaves.
- **An edit:** `learn`'s SKILL.md, already read for "remember", grows by about 800 bytes; the style and the sign files
  are in context from the draft.

## Compatibility

The style's format is a one-way door, and this keeps it as it is: corrections already go under `## Corrections`,
dated, with the kind of text they came from (`plugin/skills/learn/SKILL.md`, The format). No skill is renamed; no
sign, schema or kind changes. A style a project holds (#103, if it merges first) takes its corrections in its own
file, as Remember does.

## Steps

1. **`learn`:** Remember gains the edit and its two rules. The eval `plugin/evals/learn-from-an-edit/`: a `case.yaml`
   whose `context.history_file` is a recorded session in which `write` drafted an invented mail in an invented
   style; the prompt is the user's version, with a sign-off swapped, bold cut and a date changed, and "learn from my
   changes". Graders: `learn` started; an `llm` grader that the sign-off and the bold are proposed and the date is
   not; no Write or Edit, since no one said yes. A second, one-prompt eval gives a version with no draft before it:
   the offer to learn from samples. The recording is scrubbed of the recording machine's paths before it is
   committed.
2. **`write`:** step 9's sentence. The eval `plugin/evals/write-offers-learning-from-an-edit/`: the same recording,
   then a bare version; graders: an `llm` grader that the offer is made and no new draft written, no Write or Edit.
   The byte ceiling test for `write`'s SKILL.md in `tests/test_render.py`.
3. **The release:** a minor, `plugin.json` and its `CHANGELOG.md` section (`docs/releasing.md`); `README.md`'s Use it
   and Next; `plugin/README.md`.

## Tests

- **Unit (CI):** the gate's plugin and skill checks over both skills; the byte ceiling on `write`'s SKILL.md.
- **Evals,** run by hand (`claude plugin eval`), on Claude Opus 5.5 and Sonnet 5.5: the three above.
- **By hand, in a real session** (`claude --plugin-dir plugin`), with invented styles in a temporary home, never the
  maintainer's `~/.byhand/`, in English and Hungarian, for what saves:
  - a yes to one of two: one dated line under `## Corrections`, nothing else in the file changed;
  - a change the style's corrections already hold: not proposed again;
  - "no": the file unchanged;
  - a style near 4 KB: the question about old corrections;
  - a document written to a file, changed by hand, then "I changed it": the file read again, its changes proposed.
- **What none can show:** whether the proposed rules are the habits the user means, over weeks of real mail. The
  maintainer's own use is that test.

## Docs

`README.md` (Use it: "Tell it what you don't like" gains the edit; Next drops `0.5.0`), `plugin/README.md`,
`CHANGELOG.md`'s section, and the bootstrap plan's progress log (its log alone: a merged plan changes only that).

## Risks

| Risk | Answer |
|---|---|
| A fact taken for a habit ("we meet Tuesdays" becomes a rule) | Accepted: step 3's test, and the user picks each rule by number |
| Corrections pile up and push the style past 4 KB, costing every draft | Resolved: a repeat replaces the older line, and past 4 KB learn asks what to drop |
| The user's version keeps byhand's lines, which would teach the style AI text | Resolved: only the changes become rules, and the version is never an excerpt |
| A long document compared line by line costs many tokens | Accepted: it happens only when the user asks or says yes, once |
| `write` offers on text that isn't an edit of its draft (a new mail pasted to reply to) | Accepted: the offer is one line, and a no costs nothing |
| A direct "learn from my changes" doesn't start `learn` with its description unchanged | Resolved: the eval's `learn-started` grader shows it, and words are added only then |
| A recorded session committed with a path or a name from the recording machine | Resolved: it is recorded on invented text and scrubbed before the commit; gitleaks runs over it |

## Plan review

### Fit

The plan at `f16a31f`, by a fresh general-purpose agent on Claude Opus 5.5 (`claude-opus-5-5`), 2026-11-10, with the
change's own question: does the design keep the cost to a user who never edits a draft at (nearly) zero, and is there
a simpler way to get the user's version than a paste or a path? Answers by the maintainer, 2026-11-10.

| # | Improvement | Answer |
|---|---|---|
| I1 | Design, Cost: leave `learn`'s description as it is, try the eval's `learn-started` grader first, add words only if it fails; every session's skill list pays for a description | taken |
| I2 | Design, `write` step 9: one sentence in step 9 instead of a new case with its own offer, reusing step 9's wording (and #105's project wording with it); half the bytes every draft reads | taken |
| I3 | Design, `write` step 9: when the user already asks to learn from their version, start `learn` at once; offer only for a bare version ("Ask nothing you can judge yourself") | taken |
| I4 | Goal, `learn` step 1: the file the draft became this session is read again by its path, so the user only says "I changed it" | taken |
| I5 | Steps 2, Tests: make step 9's case a committed eval with `context.history_file`, a recorded session; keep by hand only what saves | taken |
| I6 | Tests: a byte ceiling test on `write`'s SKILL.md, so "no cost for a user who never edits" is a check CI keeps | taken |
| I7 | Design, `learn` steps 2 and 5: save the picks as Remember does, and move the two new rules into Remember so both ways in keep them | taken |
| I8 | Design, `learn` steps 3 and 4: a change that puts in what a sign names says so beside its rule (the bootstrap plan: a learned rule that matches a sign is kept only on the user's yes) | taken |
| I9 | Design, `learn` step 2: with no style, say so and offer samples without comparing; the rules would have nowhere to go | taken |
| I10 | Design, Alternatives: a row for Claude Code's auto memory, the first "why not" a reviewer asks | taken |

Noticed on the way, for Round 1: Alternatives row 1 gave the wrong reason a hook is out (a hook isn't a skill); Steps
2 and Tests said an eval is one prompt, but `context.history_file` resumes a transcript; `write` step 9's new offer had
no project wording; `learn` step 2's no-style path couldn't be reached from `write`; Cost said the style file is read
again, though it is in context from the draft.
