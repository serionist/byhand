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

- **In scope:** the user's version given in the conversation, pasted or as a file they point at, while byhand's draft
  is still in context; or both versions given by the user. The corrections it proposes, one question, the save.
- **Out of scope:**
  - reading what the user sent from a mail or chat app (a connector, a hook): see Design, the alternatives;
  - learning from a draft byhand no longer has and the user can't give;
  - changing a style's body or excerpts from an edit: an edit is a correction, nothing more.

## Design

Two skill changes, no new skill, agent, command, file or key in a style.

### `write`, step 9

Step 9 already turns feedback on a draft into "Save this as a rule for <style>?". It gains one case: the user answers
a draft that used a style with their own version of it ("this is what I sent", a pasted text, a file they changed).
Then `write` asks one line, "Learn from your changes for <style>?", and on a yes hands over to `learn`. The user's
version is no request for a new draft: `write` doesn't rewrite it.

### `learn`, a new request: learn from an edit

1. **The two versions:** byhand's draft, from the conversation, and the user's; or both from the user. No draft to
   compare with: say so, and offer to learn a style from samples instead.
2. **The style:** the one the draft used; else the one the user names; else ask. The style's file is where `write`
   read it. No style at all: steps 3 and 4 still run, and the question offers to learn a style from samples to keep
   the rules in (an eval's session has no styles, so this is also the case the eval sees).
3. **The changes that are habits:** compare the two line by line, and keep a change only when it would hold for the
   next text of this kind: a greeting or sign-off swapped, a word or phrase cut or replaced, sentences shortened or
   joined, the register moved, formatting removed (bold, bullets, headings). A change to a fact of this text (a date,
   a name, a number, a point added or cut) is no correction. A change the style's rules or corrections already hold
   is no new one.
4. **Show them with one question:** each as a short rule with its before and after, numbered, and which to keep
   (all, some by number, or none). Nothing is saved on silence.
5. **Save on a yes,** with Edit, under `## Corrections`, in the format that section has: dated, the kind of text it
   came from, and the rule. A rule that repeats an older correction replaces it, with the new date. A style that
   would pass 4 KB: say so, and ask which old corrections to drop or fold into the rules.

Only the changes reach the style, as rules in the skill's own words. The user's version is never an excerpt or a
sample: the lines they left as byhand wrote them are byhand's text, and learn never takes a style from AI text.

### Alternatives

| Alternative | Why not |
|---|---|
| A hook or a connector that reads the sent mail or message | A plugin skill runs no command, and a connector is the user's to add; it would read the user's mailbox for every draft, at a cost in every session |
| byhand keeps each draft on disk to compare later | `write` would need Write, which no plugin skill pre-approves, and every draft would leave the user's text in a new folder |
| A new skill for it | The format, the index and the corrections already live in `learn`; a new skill is one more description in every session's context |
| Learn every change, no question | A style changes only on the user's yes (the bootstrap plan, Styles) |

### Cost

- **A session with no edit:** `write`'s step 9 grows by about 250 bytes, read with each draft; `learn`'s description
  by a few words, in every session's skill list. Nothing else.
- **An edit:** `learn`'s SKILL.md, already read for "remember", grows by about 1 KB, and the style file is read once.

## Compatibility

The style's format is a one-way door, and this keeps it as it is: corrections already go under `## Corrections`,
dated, with the kind of text they came from (`plugin/skills/learn/SKILL.md`, The format). No skill is renamed; no
sign, schema or kind changes. A style a project holds (#103, if it merges first) takes its corrections in its own
file, as "remember" does.

## Steps

1. **`learn`:** the new request and its description, with the eval `plugin/evals/learn-from-an-edit/`: one prompt
   that gives an invented draft and the user's version, with a sign-off swapped, bold cut and a date changed, and asks
   to learn from the changes. Graders: `learn` started; an `llm` grader that the sign-off and the bold are proposed
   and the date is not; no Write or Edit, since no one said yes. The PR names the skill's size before and after.
2. **`write`:** step 9's new case. An eval is one prompt, and this case needs a draft from an earlier turn, so it is
   tried by hand (Tests). The PR names the skill's size before and after.
3. **The release:** a minor, `plugin.json` and its `CHANGELOG.md` section (`docs/releasing.md`); `README.md`'s Use it
   and Next; `plugin/README.md`.

## Tests

- **Unit (CI):** the gate's plugin and skill checks over both skills. No test holds a skill's size; the PR names
  both skills' sizes before and after.
- **By hand, in a real session** (`claude --plugin-dir plugin`), with invented styles in a temporary home, never the
  maintainer's `~/.byhand/`: on Claude Opus 5.5 and Sonnet 5.5, in English and Hungarian:
  - a mail drafted, then the user's version with a sign-off swapped, bold cut and a date changed: the sign-off and
    the bold proposed, the date not;
  - the same with a change the style's corrections already hold: not proposed again;
  - a yes to one of two: one dated line under `## Corrections`, nothing else in the file changed;
  - silence or "no": the file unchanged;
  - a style near 4 KB: the question about old corrections;
  - the user's version given with no draft in context: the offer to learn from samples.
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
| A long document compared line by line costs many tokens | Accepted: it happens only on the user's yes, once |
| `write` offers on text that isn't an edit of its draft (a new mail pasted to reply to) | Accepted: the offer is one line, and a no costs nothing |

## Plan review

None yet.
