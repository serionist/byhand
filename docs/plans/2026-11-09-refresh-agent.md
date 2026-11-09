---
title: Draft the refresh's sign changes with an agent every two weeks, as one draft PR
issue: "#30"
status: approved
approved_by: serionist
approved_at: 2026-11-09
---

# Draft the refresh's sign changes with an agent every two weeks, as one draft PR

## Goal

Every two weeks, when the refresh has opened at least one issue labelled `refresh`, an agent in CI runs
`propose-signs` on every source those issues name, reviews its own change with one round of `review-code`, and opens
one draft PR that closes them. The maintainer reads it, marks it ready and merges it; the agent does neither. Today
each refresh issue waits for the maintainer to run `propose-signs` in a session (#46 to #47); this leaves only the read
and the merge (#30).

The maintainer's decisions on #30, 2026-11-09:

| Decision | What it sets |
|---|---|
| A Claude OAuth token from `claude setup-token`, as a repo secret | counted against the subscription, not billed per token |
| Every two weeks, and only when a `refresh` issue is open | no run, no tokens, when nothing changed |
| One run takes every open refresh issue and opens one draft PR, with one review round | one PR to read, not one per source |
| The maintainer merges | the agent never marks a PR ready and never merges |

In scope: `byhand fetch`, which downloads a source's old and new text for the agent and for a person; the workflow
`refresh-agent.yml` and its prompt; the triggers that let CI run on a PR the workflow opens; the repo setting that
lets Actions open a PR; the docs. Out of scope: how sources are found (#32) and released (#31); a second review round
in CI; drafting from anything but a refresh issue.

## Design

### What the agent may do

The run treats every fetched page as data, and no one watches it, so the design keeps what a page could make the model
do small, and checks the result mechanically before anything is published. It splits into two jobs, so the model never
shares a runner with a token that can write.

| | `draft` job: the model | `publish` job: no model |
|---|---|---|
| GitHub token | `contents: read`, `issues: read`, `pull-requests: read`, and only in the steps before the model; checkout with `persist-credentials: false` | `contents: write`, `pull-requests: write` |
| Other secret | `CLAUDE_CODE_OAUTH_TOKEN`, in the model's step only | none |
| Network for the model | none: no WebFetch, no WebSearch, no MCP server (`--strict-mcp-config`); it reads what `byhand fetch` downloaded before it started | |
| Writes | files in the checkout, its own local commits, none of them published as they are | one commit of its own, a branch `refresh-agent/<date>` and a draft PR |

The model's step runs Claude Code's CLI directly, at the version `ci.yml` pins (`npm install -g
@anthropic-ai/claude-code@2.1.285`; the two move together, Fit I3):

```
claude -p "$(cat .github/refresh-agent.md) <the source ids and issue numbers>" \
  --model opus --restricted --permission-mode dontAsk --strict-mcp-config --max-budget-usd "$BUDGET" \
  --output-format json --tools "Read,Glob,Grep,Edit,Write,Bash,Agent" --settings .github/refresh-agent.json
```

`--restricted` (Round 1, I8) loads no settings but managed ones and `--settings`, confines the file tools to the
checkout, and keeps Bash only because `--tools` names it. So `.github/refresh-agent.json` holds the whole of what the
run allows, with an empty `attribution` as `.claude/settings.json` has, the read block
(`blockReadsOutsideWorkingDirectories`, so the built-in read-only shell commands can't read outside the checkout
either; Round 2, P9), and only whole commands (Round 1, P1, P2):

| Allow | Why |
|---|---|
| `Edit(src/byhand/catalogue/**)`, `Edit(docs/reviews/**)`, `Edit(docs/research/**)`, `Edit(.local/**)` | the signs and `read_at`, the records, its PR text and commit messages |
| `Bash(uv run byhand validate)`, `Bash(uv run byhand render)`, `Bash(uv run tools/copycheck.py)` | `propose-signs` step 7; copycheck's default folder is `.local/sources` |
| `Bash(uv run tools/gate.py quick)`, `Bash(uv run tools/gate.py full)` | `propose-signs` step 7, `review-code` step 2 |
| `Bash(git add -A)`, `Bash(git commit -F .local/commit.txt)` | its local commits, so `review-code` can name one; never `git add *` or `git commit *`, whose `--pathspec-from-file`, `-F` and `--template` read any file into what the model sees |

The read-only git forms `review-code` uses (`git diff`, `git log`, `git show`) run as Claude Code's built-in read-only
commands, inside the checkout only.

- **`dontAsk`:** anything not allowed is denied, not asked. Reads inside the checkout need no rule; an edit needs one
  of the four `Edit` allows, which cover Write too, so nothing outside them is written.
- **`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`:** the commands the model runs get no credential in their environment, and on
  Linux run in their own PID namespace, so they can't read the CLI's environment through `/proc`; the CLI keeps the
  token for its own calls. No GitHub token is in that step's environment at all.
- **The edits it may make** are the catalogue (signs and `sources.toml`'s `read_at`), the review and research records,
  and `.local/` for its PR text. `byhand render` writes `plugin/signs/`. A sign that would need any other file, such as
  a new `any` check form with its line in `tests/test_office_<code>.py`, is left out and named in the PR for the
  maintainer.
- **`Agent`** is for `review-code`'s fresh reviewer, which inherits the same tools and rules.

### The run

`.github/workflows/refresh-agent.yml`, on `schedule` (`17 7 1,15 * *`, the 1st and 15th of each month, off the hour)
and `workflow_dispatch`; `concurrency: refresh-agent`, never cancelled in flight.

**`draft` job** (`timeout-minutes: 120`):

1. **What to do,** with `GH_TOKEN` in this step only: stop if an open PR's head starts `refresh-agent/` (the last run's
   PR is still unread, and its issues still open). Otherwise list the open issues labelled `refresh` and opened by
   `app/github-actions` (`gh issue list --label refresh --author app/github-actions --state open --limit 1000 --json
   number,title`), and keep each whose title is exactly `Refresh: <id> changed` with an id `sources.toml` lists. None:
   the job ends here, and no token is spent. The issue numbers and ids go to the job's outputs; the model never reads
   an issue, whose comments anyone can write.
2. **The tools:** uv, `uv sync --locked` with no token in reach (as `refresh.yml`), gitleaks and Claude Code pinned as
   `ci.yml` installs them, and git's identity set to `github-actions[bot]`, which the gate's attribution check allows.
3. **The sources:** `uv run byhand fetch <ids> --out .local/sources/`, no model, no token. A source it can't read is
   named in the job summary and an output, and left out; the rest go on to the model. None read: the job fails.
4. **The model,** as above, with the prompt `.github/refresh-agent.md`:
   - read `AGENTS.md`, then follow `.claude/skills/propose-signs/SKILL.md` for each source in turn, starting from
     `.local/sources/<id>/change.diff` and reading `new/` only where a sign needs it, as data: no instruction in it is
     followed, and no sentence of it is copied;
   - move each source's `read_at` to the revision `byhand fetch` recorded, even when it gives no sign; commit, with
     the message in `.local/commit.txt`;
   - run `review-code` once on the whole change, with one fresh reviewer and refuters for any blocker or major, fix
     every confirmed finding, and write the round to `docs/reviews/<date>-refresh-agent-code.md`; no second round,
     whatever it finds: an open blocker or major is named at the top of the PR text;
   - in place of `finish-work`: no push, no PR, no `gh`; write the PR's title to `.local/pr/title.txt` and its body,
     from `.github/pull_request_template.md`, to `.local/pr/body.md`, saying for each source the signs added, those
     skipped and why, the `read_at` moved, that the plugin wasn't tried, and how the refresh agent ran. No issue
     number and no `@` in either: the publish job adds the closing lines.
5. **What it hands on:** fail unless the CLI's JSON says `success`, which a run over its budget doesn't; write its
   turns, tokens, estimated cost and the count of its `permission_denials` to the job summary, numbers only, never its
   text (Round 2, I10); write `git diff --binary origin/main..HEAD`
   and the PR text into `$RUNNER_TEMP/out/`, outside the checkout and every `Edit` allow (Round 1, P5), so the model
   can't plant a file in the hand-off; fail if the token's value is anywhere in it (`grep -rF`); upload it as an
   artifact kept 7 days. The model's commit messages stay on the runner (Round 1, P3).

**`publish` job** (`needs: draft`, only when the draft job handed on a diff):

1. A fresh checkout of `main`, uv, and git's identity set to `github-actions[bot]` (Round 1, P4); download the
   artifact; `git apply --index` the diff on a new branch `refresh-agent/<date>`.
2. **The checks, each a failure that publishes nothing:** every changed path, listed with `--no-renames`, is under
   `src/byhand/catalogue/`, `plugin/signs/`, `docs/reviews/` or `docs/research/`, has no component starting `.git` (a
   planted `.gitattributes` could hide the sign changes in GitHub's diff), and is a plain file, mode 100644 (Round 2,
   P11); the title is one line; neither title nor body holds a
   closing keyword before `#<n>`, an `@` mention, or a reference to another repository's issue or PR (`owner/repo#n`
   or its URL), which would post a backlink there from a public draft (Fit I6).
3. **The closing lines,** by a few lines of Python with `tomllib`: `Closes #<n>` for each issue whose source's
   `read_at` moved on the branch, `Refs #<n>` for any whose didn't. Then `uv run --no-sync tools/gate.py text --file -`
   over the title and the whole body, as `PR text` will run it, so a PR never opens failing it (Round 1, I7).
4. One commit, its subject the checked title and its body the closing lines; `git push origin refresh-agent/<date>`,
   then `gh pr create --draft --base main`. A PR opened with the workflow's
   token starts `ci.yml` and `pr-text.yml` in an approval-required state: the maintainer selects "Approve workflows to
   run" in the PR, reads it while the checks run, marks it ready and merges it (Fit I1).
5. **A source `byhand fetch` couldn't read** (draft step 3) fails this job's last step, after the PR is open, so GitHub
   mails the maintainer and its issue stays open (Round 1, P8).

### `byhand fetch`

`byhand fetch <id>... --out <dir>`: for each source, its text as it is now into `<dir>/<id>/new/`, a unified diff of its
text at `read_at` against now into `<dir>/<id>/change.diff` (`difflib`), and the revision now into
`<dir>/<id>/revision`, the value `read_at` moves to. The diff is where reading starts (`propose-signs` step 1): a
typical edit's diff is a few kB, where `wikipedia-en` is 181 kB a copy (Fit I5). `copycheck` reads `new/`. Standard
library, in `refresh.py` beside the feeds it reads, and the same command a person runs before `propose-signs` by hand (its step 2):

| Feed | Read at `read_at` and now |
|---|---|
| `mediawiki` | the page's wikitext at `read_at.revision` and at its latest revision (`api.php`, `prop=revisions`, `rvprop=ids\|content`, `rvslots=main`, `redirects=1`) |
| `github` | the files under `paths` at `read_at.commit` and at `HEAD` (its sha from `api.github.com/repos/{repo}/commits/HEAD`), from `codeload.github.com/{repo}/tar.gz/{sha}`, extracted with `tarfile`'s `data` filter, members outside `paths` skipped |
| `hf` | the dataset card, `README.md`, at both shas |
| `none` | refused: a person reads it |

The GitHub token, when set, goes to `api.github.com` only, never across a redirect; the tarballs need none. As
`byhand refresh` does, a source that can't be read (a force-pushed `read_at` commit, a missing page) or an id that isn't
in `sources.toml` is reported with its reason and doesn't stop the others; the command exits 1 at the end if any was
(Round 1, P8). A 12-character `read_at.commit` works with codeload and Hugging Face, checked live in Round 1.

### Cost

From tonight's measures: a change that gave no sign (#46 to #47) took about 95k tokens with its review; a change with a
few signs, 150k to 300k. The refresh has seen about one change in two days, and an issue stays one per source, so a run
expects two to five issues:

| Run | Tokens |
|---|---|
| one source, no sign | about 100k |
| three sources, a few signs in one | about 400k to 500k |
| five sources, signs in each | about 1M to 1.5M |

Most of it is cached reads of `AGENTS.md`, the skills and the catalogue. Two runs a month at the middle row is about
1M tokens a month on the subscription. The cap is `--max-budget-usd`, one constant in the workflow: the CLI's own
estimate of the spend, the reviewer's and refuters' subagents included, set from the try in Step 4 to the top row,
1.5M tokens (Fit I2). The job's 120 minutes stand behind it. A run that hits either fails and publishes nothing, and
GitHub mails the maintainer. The job summary records each run's turns, tokens and estimate, so the first runs tune the
constant.

### Alternatives

- **`anthropics/claude-code-action`:** it takes `claude_code_oauth_token` and `claude_args`, but always adds its
  GitHub tools and asks for `contents`, `pull-requests` and `issues: write` in the model's job; the CLI directly keeps
  every GitHub token away from the model.
- **WebFetch, limited to the sources' domains:** less code, but WebFetch returns a summary, not the page, so
  `copycheck` has nothing to read, and the model gets a network.
- **One PR per source:** more to read, and more runs of the reviewer; the maintainer chose one.
- **A run as each issue opens:** a model run a day at worst; the maintainer chose every two weeks.
- **An API key:** billed per token; the maintainer chose the subscription.
- **A personal token or an App for the PR, so CI starts on its own:** a second secret, to save the maintainer one
  "Approve workflows to run" click.
- **GitHub's agentic workflows (gh-aw):** its "safe outputs" are this split, an agent job with no write permission
  whose output a separate job publishes, and its sanitising is the checklist for the body checks (Fit I6). Not used
  itself: a framework and a compiler for one workflow, where two jobs and a few checks do.

## Compatibility

No one-way door. Harness changes, each agreed on #30 or named for the maintainer here:

- a new workflow holding a secret, whose `publish` job may push a branch and open a draft PR;
- `.github/refresh-agent.json`, the agent's allows, held by the same exact-or-swept test as `.claude/settings.json`;
- the repo setting "Allow GitHub Actions to create and approve pull requests" turns on, and `tools/setup.py settings`
  checks it with the workflow token's default kept `read`. Main's ruleset requires no approval, so an approval by
  Actions gives nothing.

## Steps

1. **`byhand fetch`,** in `refresh.py` and `cli.py`; `tests/test_refresh.py` with the network replaced: each feed's
   new text, diff and revision; a tarball member outside `paths` skipped and one with `..` or an absolute path
   refused; the token never sent off `api.github.com`; a `none` feed, an unknown id and an unreadable source failing
   with their reason.
2. **The settings check:** `tools/setup.py`'s `SETTINGS` gains the Actions PR setting and the default token's `read`;
   `settings_problems`' tests in `tests/test_gate.py` for both.
3. **The workflow, its prompt and its settings:** `.github/workflows/refresh-agent.yml`, `.github/refresh-agent.md`,
   `.github/refresh-agent.json`. `tests/test_gate.py`'s exact-or-swept allow test reads `.github/refresh-agent.json`
   too, with nothing added to the commands it sweeps; `.claude/settings.json` keeps its Bash-only assertion, and the
   agent's file may hold, beside its Bash allows, exactly `Edit(src/byhand/catalogue/**)`, `Edit(docs/reviews/**)`,
   `Edit(docs/research/**)` and `Edit(.local/**)`, and must set the read block (Fit I4; Round 1, P1; Round 2, P10).
4. **A try by hand before the merge:** the maintainer runs `claude setup-token` (Round 2, I9); on their machine, in a
   fresh clone, with `CLAUDE_CONFIG_DIR` set to an empty folder and `CLAUDE_CODE_OAUTH_TOKEN` set to that token, as CI
   has them, `byhand fetch` and the model's command line from
   the workflow on an open refresh issue, or on `wikipedia-en` with `read_at` set back to
   1384165696 on a scratch branch. Its turns, tokens and the PR text it wrote go in the PR, and the budget constant is
   set from it. It also shows whether `AGENTS.md` and the skill files load under `--restricted` (the prompt names
   them, so the model reads them either way), and that `cat ../x` and `git diff --no-index ../x /dev/null` are
   denied (Round 2, P9).
5. **The docs** (below).
6. **finish-work:** the gate, `review-code` until clean, the PR.
7. **Before the merge, by the maintainer:** the token from Step 4 as the secret `CLAUDE_CODE_OAUTH_TOKEN`, the repo
   setting, all inert until the workflow is on `main`, so a cron run between the merge and the try finds them in place
   (Round 1, P7).
8. **After the merge:** `gh workflow run refresh-agent.yml` once with no refresh issue open (it ends at step 1) and
   once with one open; approve the PR's workflow runs, read it, mark it ready. The schedule runs on the next 1st or
   15th.

## Tests

- Unit (CI): `byhand fetch` with no network; the settings check; the agent's settings swept with the repo's; the gate.
- By hand: the try in step 4, and the two dispatches in step 8, said in the PR as to come.
- What none can show: whether a page can still talk the model into a bad sign, whose guard is the maintainer's read of
  the draft PR, as for any sign today; and the scrub's Linux PID namespace, which the try on Windows doesn't have and
  only the first dispatch runs (Round 1, P6).

## Docs

`AGENTS.md`: The refresh (the agent drafts the PR every two weeks; the fetch and the detection still run with no
model), the `.github/` row (`refresh-agent.yml`, its prompt and settings), the `src/byhand/` row (`byhand fetch`), a Traps row for a
model reading fetched text unattended, within the gate's 150 lines (it is at 150 now, so lines are merged to make
room). `docs/USAGE.md`: `byhand fetch`. `.claude/skills/propose-signs/SKILL.md`: step 2
reads from `byhand fetch`. `SECURITY.md`: the refresh agent's token or permissions reached from a fetched page counts.
`CHANGELOG.md`: no line; users don't see it.

## Risks

| Risk | Answer |
|---|---|
| A page tells the model to leak the OAuth token | no network tool; the token scrubbed from its commands' environment, their `/proc` view cut off by the scrub's PID namespace, the file tools confined to the checkout by `--restricted`, and reads outside it by the built-in shell commands refused
by the read block; no allowed command takes a path; the output grepped for its value before upload; the repo is public, so the job log prints numbers only. A leaked token can only make model requests on the subscription. Resolved, with the grep as the backstop |
| A page tells the model to change code, a workflow or a skill | `Edit` rules allow four folders; the `publish` job refuses any other path. Resolved |
| A page tells the model to close or ping issues, or merge | the model has no GitHub token; the `publish` job writes the closing lines and refuses keywords and mentions in its text; nothing marks ready or merges. Resolved |
| A plausible but wrong sign | the maintainer reads the draft PR before marking it ready, as today. Accepted |
| The subscription's limits stop a run part way | the run fails and publishes nothing; the issues stay open for the next run. Accepted |
| The OAuth token expires (a year) | the run fails, GitHub mails the maintainer, who runs `claude setup-token` again. Accepted |
| A run every two weeks while the last PR waits | step 1 skips while a `refresh-agent/` PR is open. Resolved |

## Plan review

### Fit

The plan at `9ac3061`, by a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, which read the docs of
`claude-code-action`, Claude Code's CLI, permissions and environment variables, and GitHub's `GITHUB_TOKEN`. The
change's own question, the maintainer's "don't overcomplicate": the two-job split, `byhand fetch`, the settings check
and the body checks earn their keep; the `ready_for_review` trigger, the scaled turn cap, the write block and the
workflow text test don't. Answers by the author on the maintainer's standing word ("take improvements that are
recommended"), 2026-11-09.

| # | Improvement | Answer |
|---|---|---|
| I1 | No `ready_for_review` trigger: GitHub now starts CI on a PR opened with `GITHUB_TOKEN`, held for "Approve workflows to run"; the trigger would re-run CI on every PR `finish-work` marks ready | taken |
| I2 | `--max-budget-usd`, one constant that counts the reviewer's subagents, in place of a turn cap of 40 + 50 a source | taken |
| I3 | No write block: under `dontAsk` the `Edit` allows already confine writes; the CLI stays at `ci.yml`'s 2.1.285 | taken |
| I4 | The allows in `.github/refresh-agent.json`, swept by `tests/test_gate.py` as the repo's are; drop `git diff *` and the gate allows `.claude/settings.json` has, and the workflow text test | taken |
| I5 | `byhand fetch` writes `new/` and a `change.diff`, not a full old copy: the diff is where reading starts, and a page is 45k tokens a copy | taken |
| I6 | Name gh-aw's "safe outputs" as the split's prior art, and add its check on references to other repositories to the body checks | taken |

Noticed on the way, for Round 1: the hand-off folder `.local/out/` is one the model may write (The run, `draft` step
5); `git am` in the `publish` job needs a committer identity (`publish` step 1); `/proc` is kept out by the scrub's
PID namespace on Linux, not the read block (What the agent may do); the cron can fire between the merge and the first
dispatch (Steps 7); whether codeload and Hugging Face take a 12-character sha (`byhand fetch`); a try on Windows can't
show the Linux-only scrub isolation (Steps 4, Tests).

### Round 1

**How:** a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, read only, on the plan at `d98a749`; it
checked the Claude Code and GitHub docs, `gh issue list --author app/github-actions` (#46 comes back), codeload and
Hugging Face with 12-character shas, and `git add` and `git commit` options in a scratch repo. P1 went to a fresh
refuter, which reproduced it and graded it a blocker under the harness rule ("a permission widened"); it also found
`copycheck --sources <folder> --run 1` echoes text from any folder. **Verdict:** needs-fixes. **Now:** every finding
below fixed in the plan; Round 2 reads the edits.

| # | Sev | Finding | Status |
|---|---|---|---|
| P1 | blocker | `Bash(git add *)`, `Bash(git commit *)` and `Bash(uv run tools/copycheck.py *)` fail the exact-or-swept allow test, and can read any file into what the model sees: `git commit -F ../outside/secret.txt` makes it a commit message, `--pathspec-from-file` echoes it, `copycheck --sources` prints it; a page could steer it into the public PR | fixed: whole commands only, `git add -A`, `git commit -F .local/commit.txt`, `uv run tools/copycheck.py`; the test reads the file with nothing added to its sweep, and a test holds the `Edit` allows to four folders |
| P2 | minor | `.claude/settings.json`'s allows don't load in `claude -p` on an untrusted fresh checkout, so `gate.py quick` and `full` are denied and the review can't reach `clean` | fixed: under `--restricted` (I8) the agent's settings file holds every allow, the gate's two and `attribution` included |
| P3 | minor | The model's commit messages went out through `format-patch` and `git am` unchecked, so a page could put a backlink or a mention on a public branch | fixed: one `git diff --binary` handed on; the `publish` job commits once with the checked title and the closing lines |
| P4 | minor | `git am` in the `publish` job has no committer identity on a hosted runner | fixed: `publish` step 1 sets `github-actions[bot]` |
| P5 | minor | The hand-off in `.local/out/` is a folder the model may write, so a planted patch could ride in unreviewed | fixed: `$RUNNER_TEMP/out/`, outside the checkout |
| P6 | minor | `/proc` is kept from Bash by the scrub's PID namespace on Linux, not the read block; a try on Windows with the maintainer's own config is not CI's setup | fixed: the namespace named in the design and Risks; the try runs with an empty `CLAUDE_CONFIG_DIR`; Tests says only the first dispatch runs the namespace |
| P7 | minor | A cron run can fire between the merge and the setup; "the 15th" is wrong for a `1,15` cron | fixed: token, secret and setting before the merge; "the next 1st or 15th" |
| P8 | minor | One source `byhand fetch` can't read (a force-pushed commit) stopped every source, every run | fixed: as `byhand refresh`, it reports and goes on, exits 1 at the end; the run drafts the rest and fails after the PR opens |

Refuted: the 12-character shas (codeload and Hugging Face take them, checked live); `--author app/github-actions`
(works with gh 2.93); approval-required runs on a PR the workflow token opens (GitHub's docs say so, Fit I1 holds);
code planted in `src/byhand/catalogue/` (no Python package there, and pytest's `testpaths` is `tests`); the template's
bare `Closes #` line (the appended `Closes #<n>` satisfies `PR text`).

Owner calls: none.

| # | Improvement | Answer |
|---|---|---|
| I7 | Run `gate.py text` over the title and body in the `publish` job, so a body saying how the agent ran never opens failing `PR text` | taken |
| I8 | `--restricted`: only managed settings and `--settings` load, the file tools stay in the checkout, Bash only because `--tools` names it; one flag in place of the read block and the trust question | taken; the try in Step 4 shows whether `AGENTS.md` and the skills load, which the prompt names anyway |

### Round 2

**How:** a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, read only, on the edits from `d98a749`
to `2711f63` and the open findings; it checked `--restricted`, `dontAsk`, the read-only commands and the scrub in
Claude Code's docs, and `git diff --binary` with `git apply --index` on new, binary, renamed and gitlink entries in a
scratch repo. **Verdict:** approved once P9 to P11 are fixed, which they are; no blocker or major, so no third round.
**Now:** P1 to P8 confirmed fixed; P9 to P11 fixed in the plan.

| # | Sev | Finding | Status |
|---|---|---|---|
| P9 | minor | Round 1's edit dropped the read block, but `--restricted` confines only the file tools: a built-in read-only command (`cat`, `git diff --no-index`) might still read a runner file outside the checkout into a public PR; the docs don't settle it | fixed: the read block is back in `.github/refresh-agent.json`, and the try checks both commands are denied |
| P10 | minor | Step 3's test can't be built as written: the current test asserts every allow is `Bash(`, and the `Edit` folders it named were the `publish` job's, not the agent's | fixed: `.claude/settings.json` keeps its assertion; the agent's file may hold exactly its four `Edit` allows and must set the read block |
| P11 | minor | `git add -A` stages a planted `.gitattributes` in an allowed folder (`linguist-generated` would hide the sign changes in GitHub's diff), and a rename's source path hides without `--no-renames` | fixed: the path check lists with `--no-renames`, refuses any component starting `.git` and any mode but 100644 |

Refuted: drift between the two jobs' base (both check out `github.sha`); `git commit -F .local/commit.txt` reading
another file (a fixed path, no `ln`, `.git` writes denied); `git add -A` staging `.local/` or `.venv/` (ignored);
relative `Edit` patterns in a `--settings` file (no leading slash, so they resolve against the working directory);
losing `git fetch origin` with `.claude/settings.json` (the checkout already has `origin/main`); copycheck reading
`change.diff` (not among its suffixes; it reads `new/`).

Owner calls: none.

| # | Improvement | Answer |
|---|---|---|
| I9 | `claude setup-token` in Step 4, where the try needs the token, and Step 7 stores that same token | taken |
| I10 | The count of the CLI's `permission_denials` in the job summary, numbers only, so a denied gate command or an injection attempt shows | taken |

### Approval

Treated as approved on the maintainer's standing word for the night ("take improvements that are recommended",
owner calls answered with the recommended option): the Fit's six improvements and Round 1's and Round 2's four taken,
no owner call raised, and Round 2 found no blocker or major. The maintainer's own review of the plan PR stands over it.

## Built

PR for #30, 2026-11-09. Departures from the design above, each small and said here so the review reads them:

- **The fetch step holds the workflow's read-only token.** GitHub allows 60 unauthenticated calls an hour, shared by
  a hosted runner's address; `refresh.yml` passes it for the same reason. It is before the model, and `byhand fetch`
  sends it to api.github.com alone, as an unredirected header (`get_json` now does too).
- **The `draft` job runs on `main` only:** the gate the model runs compares with `origin/main`, and the PR goes to
  `main`. The hand-off is `git diff --binary "$GITHUB_SHA"..HEAD`, the same commit as `origin/main` there.
- **The `publish` checks are a little stricter:** a deleted file fails the mode check (its new mode is `000000`; the
  agent never needs to delete one), and the title and body may hold no `@` at all, not only a mention. The body gets
  one line of our own naming any source `byhand fetch` couldn't read.
- **`byhand fetch --out`** defaults to `.local/sources`, where `copycheck` reads. A failed fetch leaves nothing of an
  earlier one behind, so no old diff is read as new.
- **The permission mode:** Claude Code 2.1.285 forces it to `default` when `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` is set
  ("allowed_non_write_users hardening"), whatever `--permission-mode` says. In `-p`, with no one to ask, everything
  that would prompt is still denied, as the try showed; `--permission-mode dontAsk` stays in the command line.
- **The budget is $15, not 1.5M tokens' worth.** The try below took about 1M tokens for one source with no sign, ten
  times the Cost table's 100k, as the table left out the cached reads the CLI's estimate counts. At the try's $1.00 for
  the lightest run, the table's top row (five sources, signs in each) is about $15.

The try, 2026-11-09, on this machine (Windows 11), in a scratch clone with `wikipedia-en`'s `read_at` set back to
1384165696 and `origin/main` pointed at that commit, as CI's checkout has it: `byhand fetch` (a diff of 10.7 kB), then
the workflow's command line with Claude Code 2.1.285, `--model opus` (Opus 5.5), `.github/refresh-agent.json` and the
scrub. It used the maintainer's own login under `--restricted`, not an empty `CLAUDE_CONFIG_DIR` with the setup token,
which only the first dispatch runs.

| What | Result |
|---|---|
| The run | `success` in 195 s: 33 turns, one reviewer subagent, an estimate of $1.00; 869k tokens read from the cache, 82k written to it, 15k out |
| What it did | read `AGENTS.md`, both skills and `REVIEW.md` (it reads them because the prompt names them); found no sign in the change and said why for each hunk; moved `read_at` to 1384534594; ran validate, render, copycheck, gate quick and full; one `review-code` round, clean, recorded in `docs/reviews/`; wrote the title and the body from the template, with no issue number and no `@` |
| Denied | its two compound commands (`cd <checkout> && ...`), which it then ran one by one; in a probe, `cat ../x`, `git diff --no-index ../x /dev/null`, `Read ../x`, `env`, `curl`, a write to `tools/` and `echo > tools/x` were denied, and `git log`, `git diff origin/main...HEAD`, `uv run byhand validate` and a write to `.local/` allowed |
| The publish checks | on its hand-off: passed, and `gate text` with the closing line; on invented hand-offs: a path in `tools/` or `.github/`, a `.gitattributes`, an executable file, a symlink, a closing keyword (`fixes #12`, `Resolves: someone/thing#3`), an `@` mention, `octo/repo#3` and its URL, a two-line title and a "Generated with" line each refused; the draft job's grep refused a hand-off holding an invented token |
