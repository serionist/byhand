---
title: Learn a style's corrections from the user's edits to a draft
issue: "#106"
status: approved
approved_by: serionist
approved_at: 2026-11-10
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
too. `write` rewrites it only when the user asks for a change to it ("make this warmer"), as for any feedback. When
the user's words ask to learn from it ("this is what I sent, learn from it"), `write` starts `learn` at once; for a
version with no request at all, it offers, in step 9's own wording, to learn from the changes for <style>, and starts
`learn` on a yes. The offer comes only when the draft used a style, as step 9's does, and it
takes the project wording #105 gives that offer if #105 merges first.

### `learn`, Remember gains the edit

Remember already picks the style the last draft used or the one the user names, asks when it isn't clear, offers to
learn a style from samples when there is none, dates each rule and names the kind of text it came from. Learning from
an edit is Remember with rules it finds itself:

1. **The two versions:** the user's, and the draft of byhand's it is an edit of, from the conversation (with several
   drafts, the one it changes; unclear: ask); or both from the user. The file the draft became this session is read
   again by its path; a deck or a sheet as `check` step 1 reads one, and compared with the outline by its words and
   their order, leaving out the outline's own marks (a deck's `## <n>.`, `Notes:` and square brackets; a sheet's
   `## <tab>` and the table's `|`). No draft to compare with: say so and ask for it; with no style either, offer to
   learn one from samples.
2. **The style:** the one that draft used; a byhand draft that used none has none (the no-style path below); both
   versions from the user: as Remember picks it. No style: say so and offer to learn one from samples, without
   comparing: the user's version can't be a sample, so the rules would have nowhere to go. The style file is in
   context from `write`'s step 4 unless the conversation was compacted; then it is read again.
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

No eval resumes a recorded session (the maintainer's call, Round 1, Q1): a Claude Code transcript holds the recording
account's email and ids, its CLAUDE.md files and its MCP setup, and it freezes the skill it loaded as it was then. So
`write`'s offer, which needs a draft from an earlier turn, is tried by hand. `learn`'s comparison needs none: both
versions in one prompt and a style seeded into the run's home, in the uncommitted suite of Tests.

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

- **A session with no edit:** one sentence more in `write`'s step 9, read with each draft, about 250 bytes (the PR
  names the real size); nothing in any description. A test holds `write`'s SKILL.md under a byte ceiling, set at the
  size this PR leaves.
- **An edit:** `learn`'s SKILL.md, already read for "remember", grows by about 800 bytes; the style and the sign files
  are in context from the draft.

## Compatibility

The style's format is a one-way door, and this keeps it as it is: corrections already go under `## Corrections`,
dated, with the kind of text they came from (`plugin/skills/learn/SKILL.md`, The format). No skill is renamed; no
sign, schema or kind changes. A style a project holds (#103, if it merges first) takes its corrections in its own
file, as Remember does.

## Steps

1. **`learn`:** Remember gains the edit and its two rules. The eval `plugin/evals/learn-from-an-edit/`, one prompt
   as every eval here: an invented mail "I sent instead of your draft", with "learn from my changes", and no draft
   before it. Graders: `learn` started, which tries the unchanged description; an `llm` grader that it says there is
   no draft to compare with and asks for it or offers to learn a style from samples, proposes no rule, and takes
   the mail as no sample; `write` not started.
2. **`write`:** step 9's sentence, tried by hand (Tests). The byte ceiling test for `write`'s SKILL.md in
   `tests/test_render.py`.
3. **The release:** a minor, `plugin.json` and its `CHANGELOG.md` section (`docs/releasing.md`); `README.md`'s Use it
   and Next; `plugin/README.md`.
4. **finish-work:** `uv run tools/gate.py full`, `review-code` until clean, the tries by hand, the PR.

## Tests

- **Unit (CI):** the gate's plugin and skill checks over both skills; the byte ceiling on `write`'s SKILL.md.
- **The eval,** run by hand (`claude plugin eval`), on Claude Opus 5.5 and Sonnet 5.5, with the plugin's other evals
  around `learn` and `write`, so the unchanged descriptions still start the right skill.
- **A seeded suite, never committed,** as the project-styles plan's (`docs/plans/2026-11-09-project-styles.md`,
  Evals): a copy of `plugin/` in `.local/learn-from-edits-try/` (git-ignored), its cases' seed scripts writing
  invented styles into the run's temporary `$HOME/.byhand/styles/`, run with `claude plugin eval
  .local/learn-from-edits-try --scaffold --ablation none`, three runs a case on both models. Each case gives both
  versions in one prompt with "learn from my changes":
  - a sign-off swapped, bold cut and a date changed: the sign-off and the bold proposed, the date not;
  - the same in Hungarian;
  - a change the seeded style's corrections already hold: not proposed again;
  - a version that puts back "Best regards", which a sign names: the note beside its rule;
  - a seeded style near 4 KB: the question about old corrections.
- **By hand, in a real session** (`claude --plugin-dir plugin`), with invented styles in a temporary home, never the
  maintainer's `~/.byhand/`, on both models, in English and Hungarian:
  - a mail drafted, then the user's bare version with a sign-off swapped, bold cut and a date changed: `write`
    offers to learn and writes no new draft; on a yes, `learn` proposes its rules;
  - the same version with "learn from it": `learn` starts with no offer before it;
  - the same version with "make this warmer": rewritten, no offer to learn from the changes (step 9's own offer to
    save "warmer" as a rule may come);
  - two drafts in two styles, then an edit of the first: its style, not the second's;
  - a yes to one of two: one dated line under `## Corrections`, nothing else in the file changed;
  - "no": the file unchanged;
  - a document written to a file, changed by hand, then "I changed it": the file read again, its changes proposed;
  - a deck made from an outline, a title changed in the file: that change proposed, none for the outline's marks;
  - a sheet made from an outline, a header changed in the file: the same.
- **What none can show:** whether the proposed rules are the habits the user means, over weeks of real mail. The
  maintainer's own use is that test.

## Docs

`README.md` (Use it: "Tell it what you don't like" gains the edit; Next drops learning from edits, and the version
numbers, as each PR that changes the plugin is a release of its own), `plugin/README.md`,
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
| `write`'s offer and `learn`'s comparison have no committed eval to run again after a later change or a new model | Accepted: the offer would need a recorded session (Design), and the seeded suite stays uncommitted, as the gate refuses a seed script in `plugin/evals/`; the PR says what ran, as for every plugin change |

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

### Round 1

**How:** a fresh general-purpose agent on Claude Opus 5.5 (`claude-opus-5-5`), 2026-11-10, on the plan at `1c89f25`.
**Verdict:** needs-fixes. **Now:** Q1 answered by dropping the recorded evals, which removes P1 and P2 with their
cause; P3 to P5 and I13 edited into the plan; Round 2 reads the edits.

| # | Sev | Finding | Status |
|---|---|---|---|
| P1 | major | Steps 1, Risks: a recorded session holds the recording account's email and ids, its private CLAUDE.md files, its MCP setup and its skill list; "scrubbed of paths" leaves all of that in the public repo, gitleaks finds none of it, and a recording made in the repo trips the gate's command check | fixed: no recorded session is committed (Q1) |
| P2 | major | Steps 1, 2: the transcript holds `write`'s SKILL.md as it was when recorded, so the resumed eval tests the old step 9, and a later change to it fails nothing | fixed: no recorded session (Q1); step 9 is tried by hand |
| P3 | minor | Design, `learn` step 2: "as Remember picks it" takes the last draft's style; an edit of an earlier draft in another style gets the wrong one | fixed: the draft the version is an edit of, and its style; several and unclear: ask |
| P4 | minor | Design, `write` step 9: "doesn't rewrite it" refuses "make this warmer" on the user's own version | fixed: rewritten when asked; the offer only for a version with no request |
| P5 | minor | Design, `learn` steps 1, 3: a deck or sheet file compared with its outline proposes rules for the outline's own marks | fixed: compared by words and their order, the outline's marks left out |

Refuted: the five defects the Fit noticed, each fixed by the taken improvements; the eval's home with no style (the
style was in the recorded history); a missing empty-session try (`docs/releasing.md` step 3 has it); two minors on one
version with #105 (`docs/releasing.md` covers it); a `.jsonl` refused under `plugin/evals/` (the gate allows it); the
150 bytes against the issue's "no cost" (the maintainer took "nearly zero", and the ceiling test holds it); folding
corrections into the rules against Out of scope (it is the user's pick, for both ways in); the auto memory row (the
memory docs bear it out); other scripts (the comparison is the model's reading, no code depends on a script).

| # | Question | Recommendation | Answer |
|---|---|---|---|
| Q1 | How is an eval's recorded session made: recorded and filtered to its user and assistant lines with a gate check and a pin test, written by hand, or none? | none: the fixes cost a check, a test and a re-recording on every change to `write`, for a format the docs don't say still resumes once filtered | the maintainer, 2026-11-10: none; drop the recorded evals and try those cases by hand |

| # | Improvement | Answer |
|---|---|---|
| I11 | A gate check that a `.jsonl` under `plugin/evals/` holds only user and assistant lines | left: no recorded session is committed (Q1) |
| I12 | A test pinning the recorded `write` body to the current SKILL.md | left: no recorded session is committed (Q1) |
| I13 | README's Next drops its version numbers, as each PR is a release now | taken |

### Round 2

**How:** a fresh general-purpose agent on Claude Opus 5.5 (`claude-opus-5-5`), 2026-11-10, on the edits from `1c89f25`
to `3d99691` and Round 1's findings. **Verdict:** approved. **Now:** P6 to P8 and I15 to I17 edited into the plan;
I14 taken by the maintainer, who approved the plan the same day.

P1 to P5 are fixed by the edits, P3 and P5 with the gaps P6 and P7 left. Q1 is carried through Design, Steps, Tests
and Risks.

| # | Sev | Finding | Status |
|---|---|---|---|
| P6 | minor | Design, `learn` step 2: an edit of a draft that used no style fell to Remember's pick, the last draft's style, and could save Hungarian habits in an English style | fixed: a draft with no style has none, and takes the no-style path; Remember's pick only when the user gives both versions |
| P7 | minor | Design, `learn` step 1: P5's fix named a deck outline's marks only; a sheet's `## <tab>` lost in its CSV would read as a habit | fixed: a sheet's marks named, and a sheet try added |
| P8 | minor | Design, `learn` step 1 and the eval's grader: with no draft, learn offered samples to a user who has a style and could paste the draft | fixed: it asks for the draft; samples only with no style either; the grader takes either |

Refuted: the byte ceiling test not in `tests/test_render.py` yet (Step 2 adds it); the empty-session try for a minor
(`docs/releasing.md` step 3); README's Next (the Docs edit matches `docs/releasing.md`); an eval that shows nothing
(the grader fails a mail taken as a sample); new behaviour without a test (tried by hand, the maintainer's Q1). The
Fit's I5 still reads `taken`: a dated record, and Round 1's Now line says Q1 reversed it.

| # | Improvement | Answer |
|---|---|---|
| I14 | A seeded suite, never committed, as the project-styles plan's, for `learn`'s comparison with both versions in one prompt: in place of four tries by hand, three runs a case on both models | taken |
| I15 | Risks: the row implied evals run in CI, and that the comparison needs a recorded session | taken |
| I16 | Tests: "make this warmer" expects no offer to learn from the changes, while step 9's own offer to save a rule may come | taken |
| I17 | Cost: the three-way sentence is nearer 250 bytes than 150; the PR names the real size | taken |
