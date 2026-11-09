---
title: Release a new version with each change to the plugin, signs included
issue: "#31"
status: approved
approved_by: serionist
approved_at: 2026-11-09
---

# Release a new version with each change to the plugin, signs included

## Goal

A PR that changes what the plugin does (its skills, its agents or its sign files) is a release: it moves
`plugin.json`'s version and dates its own section in `CHANGELOG.md`, and once it merges a workflow tags the merge commit
and creates the GitHub release. Existing users then get merged signs on `claude plugin update byhand@byhand`, or by
themselves with auto-update on, with no release PR by hand (#31).

Why: users install from the marketplace, which serves `main`'s head, but Claude Code updates an installed plugin only
when its computed version changes, and `plugin.json`'s `version` comes first ("Versions and updates" in Claude Code's
plugin loading reference: "a manifest that pins `"version": "1.0.0"` keeps every user on the cached copy until its
author changes the string, however many commits they push"). Today a merged sign reaches new installs at once and
existing users only at the next release PR. The refresh agent (#30) will open a sign PR every two weeks; a release PR
by hand after each would be the slow part.

In scope: the rule, a release workflow, the refresh agent's publish job moving the version, the docs. Out of scope:
turning on auto-update for users (no `marketplace.json` field does; a user turns it on under `/plugin`); a gate check
that any plugin change moved the version (Alternatives).

## Design

### The rule

One rule for every PR, by hand or from the refresh agent:

| Of what a user's session reads (`plugin/`, but `plugin/evals/` and `plugin/README.md`), the PR changes | Version | `CHANGELOG.md` |
|---|---|---|
| sign files only, or fixes a skill or an agent | patch, `0.2.0` to `0.2.1` | a new `## <version> (<date>)` section above the newest, with its lines |
| anything else: what a skill or agent does, `plugin.json` but its version, or a one-way door (a minor may break one in `0.x`) | minor, by hand | the same |
| nothing (the package, tests, docs, the catalogue's sources alone) | none | none |

`## Unreleased` goes: every line users would read lands in the section of the version that ships it. With an
Unreleased section kept beside sign patches, a sign PR would ship whatever skill change waited there to existing users
under a patch number, and the changelog would still call it unreleased. The marketplace already ships `main`'s head to
new installs at the merge, so "the merge is the release" (`docs/releasing.md`) holds for every user now.

The date is the day the PR sets it; a PR that waits keeps it, as the release PRs did.

### `tools/gate.py`

`release_problems` stays as it is: it holds `plugin.json`'s version to the newest dated section, which is what each
such PR writes. Its docstring loses the Unreleased sentence; the no-dated-section case still passes, for a repo before
its first release.

`check_version` gains one guard (Fit I1): a released section is frozen. For each range it reads `CHANGELOG.md` where
the range's fork point meets `origin/main` (`git merge-base <fork point> origin/main`), as `check_sign_ids` reads its
ids, through one helper the two share (Round 1, I6), not at the fork point itself as `check_coverage_floor` does: pre-push's range starts at the branch's last push,
whose newest section is the PR's own, not yet released (Round 1, P1). It takes that commit's newest dated section; if
the working tree still has a section for that version and its text differs, it fails: "0.2.0 is released: its lines go in
a new version's section, with plugin.json moved". So a line added to a released section, by habit or by a conflict
resolved the wrong way (below), fails CI instead of merging under a version users already have. The refresh agent's
model never edits `CHANGELOG.md`, and the publish job only adds a section above, so neither trips it.

### Two PRs open at once

Both set `0.2.1` and both put a section at the same place, above `## 0.2.0`. Once one merges, the other conflicts in
`CHANGELOG.md` (two different insertions at one spot; the fit tried it in a scratch clone), and GitHub won't merge it
until it is rebased. Main's ruleset doesn't require a branch to be up to date, so the conflict is what stops it.
`plugin.json`'s identical one-line change doesn't conflict, so the rebase must move it by hand: its author takes the
next patch, `0.2.2`, in both files. A rebase that keeps both PRs' lines under `0.2.1` fails the frozen-section guard;
one that dates `0.2.2` and leaves `plugin.json` at `0.2.1` fails `release_problems`. The refresh agent opens at most one
PR at a time (its draft job stops while one is open), so the clash is a hand PR against the refresh's; the maintainer
rebases the refresh PR's branch the same way. Two byte-identical sections would merge without a conflict; with a
date and the languages in each line, that is not a case worth a check.

### `release.yml`

`.github/workflows/release.yml`, about 40 lines, no model, no action but `actions/checkout` pinned as `ci.yml` pins it:

- **On** every `push` to `main`, no `paths` filter, and nothing else (Fit I3).
- **Permissions:** `contents: write` in its one job, nothing at the top; `concurrency: release`, never cancelled.
- **Steps:** check out the pushed commit (`persist-credentials: false`); with `GH_TOKEN: ${{ github.token }}` in
  the step's env (Round 1, I5), read the version from `plugin.json`; if `gh release view "v$version"` finds one, say so in the summary and stop; otherwise take the lines below
  `## <version> (` up to the next `## ` heading into a notes file, fail if there is no such section, and
  `gh release create "v$version" --target "$GITHUB_SHA" --title "byhand $version" --notes-file <notes>`, the command
  `docs/releasing.md` has the maintainer run today.

A push by the maintainer's squash merge starts it. A push that doesn't move the version finds its release and stops
in a few seconds. A run that failed (GitHub down) is re-run from its page ("Re-run failed jobs" keeps its
`GITHUB_SHA`, so the tag lands on the commit that set the version); left alone, the next push that keeps the version
tags its own head, the same files users get, and one that moves it leaves the failed version untagged (Round 1, P2). A push made with the workflow's token, as Dependabot's merges
are, starts no run; the next maintainer merge does.

### The refresh agent

The model can't edit `plugin.json` or `CHANGELOG.md` and shouldn't: a manifest edit could add a hook or an MCP server.
The publish job, which runs no model, moves the version after its checks pass and before its commit:

- **The draft job and the model's prompt** don't change: no model text reaches a file users read (Fit I2).
- **Publish job, "Check what was handed on",** after its checks pass and only when the staged diff touches
  `plugin/signs/`: the patch moved in `plugin.json` (the one `"version": "<old>"` string replaced, so the file's
  layout stays), and above the first `## ` heading of `CHANGELOG.md`, `## <new> (<today>)`, `### Changed` and one line
  the job writes from the paths: the `plugin/signs/<code>/` folders the diff touches, named from
  `git show HEAD:src/byhand/catalogue/languages.toml` (the base's, not the model's tree: its `[[language]]`,
  `[[extra]]` and `[[variant]]` tables, a name "X, Y" written "Y X", so `zh-Hant` reads "Traditional Chinese"), in
  alphabetical order, with `any` last as "the ones every language shares" (Round 1, I4): `- Signs for French and
  German, and the ones every language shares, from the refresh of 2026-11-15.`; with `any` alone, `- The signs
  every language shares, from the refresh of 2026-11-15.` (Round 2, I7). A folder whose code the base doesn't
  name fails the job, and nothing is published (Round 1, P3). Both files are staged
  with the rest; the commit and the PR go on as today. The PR body already lists each sign for the maintainer.

A run that moved only `read_at` touches nothing under `plugin/`, and releases nothing.

### Alternatives

- **The release PR by hand, as today:** a PR per sign PR; the slow part the issue names.
- **A workflow that bumps after the merge:** `main` takes PRs only, so it would open a PR of its own and merge it, as
  Dependabot's do; a push made with the workflow's token starts no CI, and the bump lands as a second commit. Moving
  the version in the PR itself is one commit, checked by CI before it lands.
- **No `version` in `plugin.json`:** Claude Code would then track commits ("the commit SHA of the installed
  directory", for a relative-path plugin in a git-hosted marketplace), and users would update on commits, perhaps
  docs-only ones too; the docs don't say. It drops the tag-and-version release the bootstrap plan chose on
  2026-11-07, and the gate's manifest check requires a version.
- **Sign patches beside an `## Unreleased` for skill changes:** above; a sign patch ships the waiting skill changes
  under a patch number.
- **A gate check that any change under `plugin/` moved the version against the base:** a forgotten bump delays
  existing users until the next one and nothing worse, and the refresh agent's model runs the gate before the publish
  job moves the version, so the check would fail every run's own gate. The narrower frozen-section guard catches the
  usual slip, a line added under the released version; the rest lives in `finish-work`, `propose-signs` and
  `docs/releasing.md`.
- **Model-written changelog lines from the refresh agent:** better words, but model text from a run that read fetched
  pages would reach a file users read, behind a new set of checks; the line from the paths needs none (Fit I2).
- **A `paths` filter and a dispatch on `release.yml`:** a failed run would wait for someone to remember the dispatch
  (Fit I3).

## Compatibility

No one-way door. For users: more versions, each smaller; `claude plugin update byhand@byhand` works as before. For the
repo: `## Unreleased` goes from `CHANGELOG.md`, and a PR that changes the plugin moves the version itself; a new
workflow that may create tags and releases.

## Steps

1. **`release.yml`.** Test: it runs only on `main` (Step 7); before the merge, its notes extract, run by hand on this
   repo's `CHANGELOG.md` for `0.2.0`, gives that section's lines.
2. **The refresh agent's publish job:** the bump and the line from the paths. Test: the step's Python run by hand on a
   scratch branch with a staged change, once to `plugin/signs/de/`, `plugin/signs/zh-Hant/` and `plugin/signs/any/`
   (the version moves, the line reads "Signs for German and Traditional Chinese, and the ones every language shares",
   `uv run tools/gate.py quick` passes the version check), once to `plugin/signs/any/` alone (the line for `any`
   alone), once to a folder `plugin/signs/xx/` (the job fails), and
   once to `sources.toml` alone (nothing moves).
3. **`tools/gate.py`:** the frozen-section guard in `check_version`, and `release_problems`' docstring. Test:
   `tests/test_gate.py`, a parametrised test of the guard's pure part (base and head changelogs: unchanged, a new
   section above, a line added under the released one, the released one gone), and `check_version` over a scratch
   git repo with an `origin/main`: a branch whose last push holds its own new section, reworded since, passes (the
   pre-push range); a line added under `origin/main`'s newest section fails.
4. **`CHANGELOG.md`:** `## Unreleased` removed.
5. **The docs** (below).
6. **finish-work:** `uv run tools/gate.py full`, `review-code` until clean, the PR.
7. **After the merge:** the merge's own push runs `release.yml`, which finds `v0.2.0` and stops; its run says so. The
   first sign PR, by hand or from the refresh agent, runs the whole path: its merge tags `v0.2.1`, and
   `/plugin marketplace update byhand` then `claude plugin update byhand@byhand` moves an installed copy to it.

## Tests

- Unit (CI): the guard and `check_version`, Step 3; the gate's other version tests as they are. The workflows have no
  unit test: the repo tests no workflow text.
- By hand: the notes extract and the publish step's Python, as Steps 1 and 2 say, recorded in the PR.
- After the merge: Step 7.
- What none can show before the merge: a workflow that runs only on `main`; and that `claude plugin update` picks up
  `0.2.1`, which the first sign release shows.

## Docs

- `docs/releasing.md`: rewritten for the rule: the PR moves the version and dates its section, `release.yml` tags
  it, a minor is still tried in an empty session; two PRs at once, and the rebase.
- `AGENTS.md`: the `.github/` row gains `release.yml`; the `CHANGELOG.md` row says a dated section per version; within
  its 150 lines.
- `.claude/skills/finish-work/SKILL.md`: step 1 and Never, for the rule.
- `.claude/skills/propose-signs/SKILL.md`: step 8, the patch and its section, "from the refresh agent, its publish
  job does this", since the agent's model reads this skill and may not edit either file (Round 1, P5).
- `.claude/skills/review-code/lenses.md`: "Does the version move only in a release PR?" becomes "Does a change to the
  plugin move the version, with its own dated section? (A refresh agent's draft: its publish job moves it after the
  review.)", so the agent's own review doesn't flag a bump it may not make (Round 2, P6).
- `.github/workflows/refresh-agent.yml`: its header comment names the bump.
- `CONTRIBUTING.md`: step 2's changelog line.
- `README.md` and `plugin/README.md`, Update: signs come as new versions often; auto-update under `/plugin`,
  Marketplaces, `byhand`, brings them without the command.
- `CHANGELOG.md`: no line; this changes nothing a user's session reads.

## Risks

| Risk | Answer |
|---|---|
| Two PRs take the same version | the second conflicts in `CHANGELOG.md` and is rebased to the next patch; a wrong rebase fails the gate. Resolved |
| A plugin PR forgets the bump | existing users wait for the next version, as they do today; a line added under the released version fails the gate. Accepted |
| `release.yml` fails (GitHub down) | the version is on `main` and users update anyway; GitHub mails the maintainer, who re-runs the failed run. Accepted |
| A PR's date is its opening day, not its merge's | the same as the release PRs; the maintainer may change it. Accepted |

## Plan review

### Fit

The plan at `72999d8`, by a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, which read the plugin
docs on versions and updates and on hosting a marketplace, main's ruleset, and prior art (release-please, changesets,
chart-testing's version-increment check, chart-releaser-action), and tried two PRs taking one version in a scratch
clone. The change's own question, the maintainer's "don't overcomplicate": the rule, dropping Unreleased, the
release workflow (because a release is a tag, the bootstrap plan's call) and the publish job's bump earn their keep;
the model-written changelog lines don't. Answers by the author on the maintainer's standing word ("take recommended
improvements"), 2026-11-09.

| # | Improvement | Answer |
|---|---|---|
| I1 | A frozen-section guard in `check_version`: the base's newest dated section unchanged on the head, so a line added under a released version, or a conflict resolved by keeping both PRs' lines under one, fails CI; the model never edits `CHANGELOG.md`, so it doesn't trip the refresh agent's gate | taken |
| I2 | No model-written changelog lines: the publish job writes the line from the `plugin/signs/<code>/` paths and the base's `languages.toml`; no model text in a file users read, no new checks | taken |
| I3 | `release.yml` on every push to `main`, no `paths` filter and no dispatch: a failed run heals on the next push | taken |

Noticed on the way, for Round 1: GitHub's conflict editor wouldn't move `plugin.json`, which doesn't conflict, so
"two lines in the editor" was wrong (Two PRs open at once); identical sections merge without a conflict (Two PRs open
at once); `review-code`'s lens "Does the version move only in a release PR?" contradicts the rule and wasn't in Docs;
the rule's table placed no row for `plugin/README.md`; "a 12-character sha" and "a docs commit included" overstate
the docs for a relative-path plugin (Alternatives).

### Round 1

**How:** a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, read only, on the plan at `14c86bd`; it
read CI's logs for how `base.sha` moves after a rebase, `gh release list`, and tried the guard's ranges in a scratch
repo. P1 went to a fresh refuter on the same model, which reproduced it with the real pre-push stdin line and
`hooks.push_ranges`, kept it major, and checked the fix in every place the gate runs. **Verdict:** needs-fixes.
**Now:** every finding below fixed in the plan; Round 2 reads the edits.

| # | Sev | Finding | Status |
|---|---|---|---|
| P1 | major | The frozen-section guard, read at the range's fork point as the coverage floor is, refuses a PR's second push after its own changelog line is reworded: pre-push's range starts at the last push, whose newest section is the PR's own; the way past is `--no-verify`, and every plugin PR now dates a section | fixed: the guard reads `merge-base(<fork point>, origin/main)`, as `check_sign_ids` does; Step 3's test has a pre-push-shaped range |
| P2 | minor | A failed `release.yml` run doesn't heal on the next push when that push moves the version: the failed one stays untagged | fixed: "Re-run failed jobs", which keeps the run's `GITHUB_SHA`; the Risks row says so |
| P3 | minor | The publish job's line misses `zh-Hant`, a `[[variant]]` named "Chinese, Traditional", and says nothing of a folder code the base doesn't know | fixed: `[[language]]`, `[[extra]]` and `[[variant]]` read, "X, Y" written "Y X", an unknown code fails the job; Step 2 tests both |
| P4 | minor | The rule's rows don't fit a normal sign PR, which touches the catalogue and tests too, and give an agent fix or a `plugin.json` change no row | fixed: the column reads "of what a user's session reads, the PR changes"; rows for signs or a fix, anything else, nothing |
| P5 | minor | `propose-signs` step 8 would tell the refresh agent's model to bump a version it may not edit | fixed: the step says the publish job does it for the refresh agent |

Refuted: a stale `base.sha` in CI (it is the head's merge base, and moves with a rebase, from this repo's runs); the
guard in the draft job's shallow checkout (`origin/main` is its `GITHUB_SHA`, as `check_sign_ids` already reads it);
the guard on CI's push to `main`; the publish job's bump (`git apply --index` leaves `HEAD` the base, and the path
check refuses a model change to `plugin.json`); this PR's own merge releasing `v0.2.0` again (it exists); a release
created twice (one release per tag, `concurrency: release`); Dependabot's merges starting a run; `claude plugin update`
missing a new version; a check that every plugin change moves the version (in Alternatives, with its reason). The
Fit's "Noticed on the way": each real, each fixed by the Fit's edits or accepted with its reason (identical sections).

Owner calls: none.

| # | Improvement | Answer |
|---|---|---|
| I4 | The `any` folder as "the ones every language shares", as `CHANGELOG.md` words it, not "every language" | taken |
| I5 | `GH_TOKEN` in `release.yml`'s step env, named, since `persist-credentials: false` leaves `gh` none and the slip would show only after the merge | taken |
| I6 | One helper for main's base per range, shared by `check_sign_ids` and the guard (the refuter's) | taken |

### Round 2

**How:** a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, read only, on the plan at `a5ef7ce`: the
edits since Round 1 and whether each fix closes its finding; it tried P1's ranges again in a scratch repo, a reworded
second push and a force push after a rebase. **Verdict:** approved. **Now:** P6, I7 and I8 edited in; the plan
approved on the maintainer's standing word ("approve once a round has no blocker or major"), 2026-11-09.

P1 to P5: closed, each checked against the code it rests on.

| # | Sev | Finding | Status |
|---|---|---|---|
| P6 | minor | The refresh agent runs `review-code`, whose rewritten lens asks whether a plugin change moved the version; its draft never does, since the publish job moves it after the review, so every run's review would flag a bump the model may not make | fixed: the lens's question says a refresh agent's draft is bumped by its publish job |

Refuted: a waiting `release.yml` run cancelled by a newer one (three merges inside one run of seconds, the middle one
moving the version; it costs a release page, not an update); the guard with no `origin/main` (it falls back to the
fork point, as `check_sign_ids` and the default `--base` do); I6's helper missing from Step 3 (the design names it,
and `check_sign_ids`' tests cover the move); the no-`paths` reason after P2 (a push that keeps the version still heals
a failed run).

Owner calls: none.

| # | Improvement | Answer |
|---|---|---|
| I7 | A form of the refresh's line for `any` alone, which the template had none for, and its case in Step 2's test | taken |
| I8 | "`plugin.json` but its version" in the minor row, so a sign PR's own bump doesn't read as a minor | taken |
