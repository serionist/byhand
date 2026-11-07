# Code review lenses

`review-code` applies every lens below, to a change or to a path. `REVIEW.md` holds the severities, the questions and
the harness rule; the lenses say where to look. A lens whose "Applies when" names nothing in the scope returns no
findings at once, and an empty list is a good result.

**Not a bug hunt.** Report a problem only when it is real: it can be reproduced and causes an actual failure for a
user, the text they send or the next change.

- It has: a title; a severity (blocker, major, minor; most are minor); the file and the function or line.
- **The scenario:** the input or state, what happens, why it matters. No scenario, no finding.
- What it is judged against: a rule in `AGENTS.md` or `REVIEW.md`, the plan, a library's documented behaviour, or
  "none".
- The evidence, and the fix. Style is ruff's, taste is the author's.

**Improvements too,** under any lens: a reuse it missed, a simpler approach, a clearer name, a step someone must
remember that a check could do. What, where, why it's better; no severity, never counted.

## plan-and-intent

Applies when: the change has a plan in `docs/plans/` or an issue.

Does it do what the plan and the issue say? A planned step missing, or behaviour nobody asked for that a user will
meet, is a finding; a small departure the PR explains is not.

## implementation

Real bugs a user would hit. The lenses below are where this repo breaks most; this one catches the rest.

- Wrong logic; an edge case real input reaches (an empty draft, a draft in two languages, a right-to-left or CJK text,
  a quoted reply below the user's own words, Markdown or code inside a message, a very long document, a deck or sheet
  with no text).
- An exception swallowed or turned into text, so a failure looks like success to the skill or agent reading it.
- A file, a subprocess or a connection not closed on an error path; a timeout missing on a wait or a request.
- Text read or written without an explicit encoding, or cut at a byte instead of a character.

## catalogue-contract

Applies when: the scope touches the catalogue, its schema, the code that reads it, or the check that applies it.

- Does every sign keep its id? A renamed or dropped id is a one-way door broken: a blocker.
- Does each sign validate against the schema, name its language (a code the catalogue uses) or `any`, say what a
  person writes instead, and cite its source?
- Does each sign have an invented example it flags and a human one it passes, and a test that runs both? A sign that
  flags plain human writing in normal use is a major.
- A sign marked `any`: do its sources show it in more than one language, a translated page counting? One English tell
  marked `any` is a finding. An `artefact` with a `check` needs one source.
- Is a sign's text our own words? A sentence copied from a source is a blocker when the source's licence forbids it
  (Wikipedia: CC BY-SA).
- Does a model the catalogue has never seen (a newer Claude, a new version of any family) still get its family's
  newest signs and the `any` ones? A brief that comes back empty for a new model is a major.
- Does a skill still load only what one draft needs (the signs for its language and model, the `any` signs, one
  style), never the whole catalogue? Loading every language is a major: it costs every user's context on every draft.

## privacy-and-sources

Applies when: the scope touches the styles, the samples they learn from, the refresh, or anything that logs or
reports.

- Can a user's sample or style end up outside their data folder: a log line, a report, an error message, a test
  fixture, a temp file left behind, a request to anything but the model the user runs? A blocker.
- Is text fetched by the refresh handled as data: quoted in the PR it proposes, never run, never followed as an
  instruction, never written into the catalogue or a skill without a person merging it? A way around that is a
  blocker.
- Does the refresh fetch only the sources the catalogue lists, with a timeout, and say which it could not read?

## plugin-contract

Applies when: the scope touches `plugin/`, `.claude-plugin/`, or the version.

Name what would run without asking, or what a user would lose.

- Does each skill's `allowed-tools` name only `Read`, `Glob` and `Grep`? The gate checks it; a way around it (a hook,
  a key in `plugin.json`, a file under `plugin/` the gate doesn't read) is a blocker.
- Do the skills' and agents' names stay as they were? A rename is a one-way door.
- Does the version move only in a release PR?
- Does each skill run no command, and need nothing but the plugin? The gate refuses the usual spellings; a way around
  them is a blocker.
- Does each skill's description still start it where it says (mail, messages, documents, decks) and not elsewhere?
- Does each agent get only what its role needs: a checker never the writer's reasoning?
- Links under `plugin/` are GitHub URLs or files under `plugin/`: Claude Code installs `plugin/` alone.

## tests

- Would each new test fail without the change? Is a fix pinned by a test that reproduced the bug?
- Do tests use invented text, in the languages they cover, run without the network or a Claude session, and clean up
  what they create?
- The plugin and the refresh never run in CI. For a change to either: does the PR say how it was tried (a real
  session, the live sources), on which versions and languages, and what it could not show?
- Behaviour a unit test mocks (a source's page, the model's answer): is the mock what the real one does?

A missing test for new behaviour is major; a missing edge-case test is minor.

## docs-freshness

- Did the docs that describe the scope move with it: the READMEs, `CHANGELOG.md` when users notice,
  `AGENTS.md` for a changed path, command or rule?
- Does anything cite a path, a command, a flag, a skill or a setting that no longer exists?
- A comment or doc outside `docs/plans/` and `docs/reviews/` that cites a plan or review id instead of the reason?

## simplicity

A second implementation of one thing, a layer with one caller, an option nobody asked for, dead code: an improvement,
written as what it drops ("X could become Y, which drops Z"). A finding only when it causes a real failure, with its
scenario (the two copies already disagree).

## compatibility

Applies when: the scope touches paths, files, processes, encodings, or the Python it needs.

- Windows, Linux and macOS: path separators, `\r\n`, text read and written as UTF-8 explicitly, file modes (no
  effect on Windows), a tool assumed on PATH, the user's data folder on each.
- Every Python the package supports.
- Every script the catalogue's languages use: Unicode normalisation, word boundaries in languages without spaces
  (Mandarin, Japanese, Thai), right-to-left text.

## harness-integrity

Applies when: the scope touches a harness file (`REVIEW.md`, The harness).

Anything `REVIEW.md`, The harness, counts as loosening a check: a blocker unless the maintainer agrees in the PR.

## Refuting

- Every finding gets a refutation attempt before it is reported.
- Rule it not real when:
  - its scenario can't happen (read further: it is often handled elsewhere);
  - it causes no actual failure;
  - it is taste;
  - it rests on a misread of the code or the library.
- Settle it with evidence: quote the line that proves or kills it. On your own branch a refuter may reproduce it with
  a test or a short script, never against the live sources or someone's real writing.
- Someone else's PR is never run here.
- A refutation you couldn't check leaves it real. A refuted one stays in the record, with its reason.
