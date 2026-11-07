# Plan review lenses

`review-plan` applies every lens below. `REVIEW.md` holds the severities, the questions and the harness rule; the
lenses say where to look in a plan. A lens that names nothing in the plan returns no findings at once, and an empty
list is a good result.

**Not a hunt.** A finding on a plan is a defect that would really hurt if the plan were followed as written: a step
that can't be built, a sign that would flag plain human writing, a user's style that would leave their machine, a
skill that pre-approves a write, a one-way door changed silently, a test that can't prove what it claims.

- It has: a title; a severity (blocker, major, minor; most are minor); the plan section.
- **The scenario:** what goes wrong when the plan is followed as written. No scenario, no finding.
- What it is judged against: a rule in `AGENTS.md` or `REVIEW.md`, the code, a library's documented behaviour.
- The evidence (quote the plan), and the proposed plan edit.

**Improvements too,** under any lens: what would make the plan, or the code it leads to, simpler, safer or cheaper
to change. No severity, never counted. Mechanical over manual: a step someone must remember, which a check could do.

## plan-and-intent

- Does the plan do what its issue asks, and nothing nobody asked for?
- Does it contradict a rule in `AGENTS.md` or `REVIEW.md`, or change a one-way door without naming it under
  Compatibility? Named openly, it is a choice for the maintainer; silent, it is a blocker.

## omissions

Read `REVIEW.md` and the code the plan changes, and list what they require that the plan leaves out and that would
really bite: the other end of a command (the module, its subcommand, the skill or agent that runs it), a doc (the
READMEs), a CHANGELOG line users need, how existing users move over (their styles, the signs they rely on).

## catalogue-contract

Applies when: the plan touches the catalogue, its schema, its languages, or the check that applies it.

Does every sign keep its id, name its language or `any`, say what a person writes instead, cite its source in our own
words, and come with an invented example it flags and a human one it passes? Does a sign marked `any` rest on sources
in more than one language, a translated page counting, or is it an artefact with a `check`? Are the language codes and the list of languages from one source the plan names? Does a
skill load only one draft's language and model, the `any` signs and one style, and does a model released after the
catalogue still get its family's signs? A renamed id or a changed schema is a one-way
door.

## privacy-and-sources

Applies when: the plan touches the styles, their samples, the refresh, or what is logged or reported.

Can a user's sample or style leave their data folder: a log, a report, a fixture, a request to anything but the model
they run? Is fetched text kept as data until a person merges it? Either one, as written, is a blocker.

## plugin-contract

Applies when: the plan touches `plugin/`, `.claude-plugin/`, or the version.

Name what a user would lose or what would run without asking. Does each skill pre-approve only `Read`, `Glob` and
`Grep`, so every write and command asks the user? Do the skills and agents keep their names, or does the plan name the
change under Compatibility? Does every skill run no command, so the plugin needs nothing else? Does each skill say where it starts by itself, and does the plan measure that it
does, and not elsewhere? Does each agent see only what its role needs? A skill that pre-approves a write or a
command is a blocker.

## compatibility

Does it work on Windows, Linux and macOS, on every Python the package supports, and on text in every script the
catalogue's languages use (CJK without spaces, right-to-left, combining marks)? An API taken from memory instead of
the pinned version (Context7) is the usual way this breaks.

## sequencing-and-tests

- Can each step be built, tested and committed on its own, in that order?
- Does each step name the test that proves it, one that fails without the change?
- Can it run in CI (no network, no Claude session)? What only a real session or the live sources can show goes to a
  try by hand: does the plan say which, in which languages, and what it still cannot show?

## simplicity

A seam with no caller, a setting nobody asked for, a second way of doing one thing, scope beyond the issue: an
improvement, written as what it drops and who would notice. A finding only when following the plan as written causes
a real failure.

## harness-integrity

Applies when: the plan touches a harness file (`REVIEW.md`, The harness).

Does it loosen a check, a hook, the gate or the agent setup? A blocker unless the plan says so and the maintainer
agrees.

## premortem

Assume the plan shipped and a user's mail still read as AI-written, a sign flagged their plain writing, the wrong
style or language was used, or a skill stopped starting by itself:
what was the likeliest cause, and what plan edit prevents it? Report it only when the plan's text makes the cause
plausible.

## Refuting

- Every finding gets a refutation attempt before it is reported.
- Rule it not real when:
  - the plan covers it elsewhere (read the whole plan: this is the usual false positive);
  - it is deferred openly, under Later or Out of scope;
  - it is taste;
  - it rests on a misread rule or code.
- Quote the plan and the rule or code; a refutation without quoted text leaves it real.
- A refuted one stays in the record, with its reason; if the edit would still make the plan simpler, list it as an
  improvement too.
