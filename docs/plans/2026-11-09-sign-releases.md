---
title: Release a new version with each change to the plugin, signs included
issue: "#31"
status: draft
approved_by:
approved_at:
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
that a plugin change moved the version (Alternatives).

## Design

### The rule

One rule for every PR, by hand or from the refresh agent:

| The PR changes | Version | `CHANGELOG.md` |
|---|---|---|
| `plugin/signs/` only, or fixes a skill | patch, `0.2.0` to `0.2.1` | a new `## <version> (<date>)` section above the newest, with its lines |
| what a skill or agent does, or a one-way door (a minor may break one in `0.x`) | minor, by hand | the same |
| nothing under `plugin/` users meet (`src/` alone, tests, docs, `plugin/evals/`) | none | none |

`## Unreleased` goes: every line users would read lands in the section of the version that ships it. With an
Unreleased section kept beside sign patches, a sign PR would ship whatever skill change waited there to existing users
under a patch number, and the changelog would still call it unreleased. The marketplace already ships `main`'s head to
new installs at the merge, so "the merge is the release" (`docs/releasing.md`) holds for every user now.

The date is the day the PR sets it; a PR that waits keeps it, as the release PRs did.

### `tools/gate.py`

No change to the check. `release_problems` holds `plugin.json`'s version to the newest dated section, which is what
each such PR writes; the version a PR moves to and the section it dates move together. Its docstring loses the
Unreleased sentence; the no-dated-section case still passes, for a repo before its first release. Its tests' fixtures
keep their Unreleased lines, which the check ignores.

### Two PRs open at once

Both set `0.2.1` and both put a section at the same place, above `## 0.2.0`. Once one merges, the other conflicts in
`CHANGELOG.md` (two different insertions at one spot), and GitHub won't merge it until it is rebased; its author takes
the next patch, `0.2.2`, in the rebase. `plugin.json`'s identical one-line change doesn't conflict, so the changelog is
the guard. The refresh agent opens at most one PR at a time (its draft job stops while one is open), so the clash is a
hand PR against the refresh's; the maintainer resolves the refresh PR's in GitHub's conflict editor, two lines.

### `release.yml`

`.github/workflows/release.yml`, about 40 lines, no model, no action but `actions/checkout` pinned as `ci.yml` pins it:

- **On** `push` to `main` with `paths: [plugin/.claude-plugin/plugin.json]`, and `workflow_dispatch`.
- **Permissions:** `contents: write` in its one job, nothing at the top; `concurrency: release`, never cancelled.
- **Steps:** check out the pushed commit (`persist-credentials: false`); read the version from `plugin.json`; if
  `gh release view "v$version"` finds one, say so in the summary and stop; otherwise take the lines below
  `## <version> (` up to the next `## ` heading into a notes file, fail if there is no such section, and
  `gh release create "v$version" --target "$GITHUB_SHA" --title "byhand $version" --notes-file <notes>`, the command
  `docs/releasing.md` has the maintainer run today.

A push by the maintainer's squash merge starts it. The tag points at the commit that set the version, so a later push
that doesn't move it changes nothing, and a dispatch after a failed run tags `main`'s head only when the version on it
still has no release.

### The refresh agent

The model can't edit `plugin.json` or `CHANGELOG.md` and shouldn't: a manifest edit could add a hook or an MCP server.
The publish job, which runs no model, moves the version after its checks pass and before its commit:

- **Draft job, the model's prompt** (`.github/refresh-agent.md`): when the change renders a sign file anew, write
  `.local/pr/changelog.md`, a line or two for users, each starting `- `, as `CHANGELOG.md` words them. "What it hands
  on" copies it into the hand-off when it exists.
- **Publish job, "Check what was handed on":** the changelog lines get the title's and body's checks (no closing
  keyword, no `@`, no other repository's issue or PR), and each line starts `- ` or is a continuation indented two
  spaces, so no heading can be planted. Then, only when the staged diff touches `plugin/`: the patch moved in
  `plugin.json` (the one `"version": "<old>"` string replaced, so the file's layout stays), and
  `## <new> (<today>)`, `### Changed` and the lines inserted above the first `## ` heading of `CHANGELOG.md`. No
  `changelog.md` handed on: the line `- Sign changes from the refresh of <today>.`, which the maintainer can reword in
  the PR. Both files are staged with the rest; the commit and the PR go on as today.

A run that moved only `read_at` touches nothing under `plugin/`, and releases nothing.

### Alternatives

- **The release PR by hand, as today:** a PR per sign PR; the slow part the issue names.
- **A workflow that bumps after the merge:** `main` takes PRs only, so it would open a PR of its own and merge it, as
  Dependabot's do; a push made with the workflow's token starts no CI, and the bump lands as a second commit. Moving
  the version in the PR itself is one commit, checked by CI before it lands.
- **No `version` in `plugin.json`:** Claude Code would then track commits, the version a 12-character sha, and every
  commit to `main` would update users, a docs commit included. It drops the tag-and-version release the bootstrap plan
  chose on 2026-11-07, and the gate's manifest check requires a version.
- **Sign patches beside an `## Unreleased` for skill changes:** above; a sign patch ships the waiting skill changes
  under a patch number.
- **A gate check that a change under `plugin/` moved the version against the base:** a forgotten bump delays existing
  users until the next one and nothing worse, and the refresh agent's model runs the gate before the publish job moves
  the version, so the check would fail every run's own gate. The rule lives in `finish-work`, `propose-signs` and
  `docs/releasing.md` instead.

## Compatibility

No one-way door. For users: more versions, each smaller; `claude plugin update byhand@byhand` works as before. For the
repo: `## Unreleased` goes from `CHANGELOG.md`, and a PR that changes the plugin moves the version itself; a new
workflow that may create tags and releases.

## Steps

1. **`release.yml`.** Test: it runs only on `main`, so a dispatch after the merge (Step 7); before it, its notes
   extract, run by hand on this repo's `CHANGELOG.md` for `0.2.0`, gives that section's lines.
2. **The refresh agent:** the prompt's changelog line, the hand-off copy, the publish job's checks and bump. Test: the
   publish step's Python run by hand on a scratch branch with a fake hand-off, once with a `plugin/signs/` change (the
   version moves, the section is in place, `uv run tools/gate.py quick` passes the version check) and once with only
   `sources.toml` (nothing moves).
3. **`tools/gate.py`:** the docstring. Test: `tests/test_gate.py` as it is.
4. **`CHANGELOG.md`:** `## Unreleased` removed.
5. **The docs** (below).
6. **finish-work:** `uv run tools/gate.py full`, `review-code` until clean, the PR.
7. **After the merge:** `gh workflow run release.yml` once on `main`; it finds `v0.2.0` and stops. The first sign PR,
   by hand or from the refresh agent, runs the whole path: its merge tags `v0.2.1`.

## Tests

- Unit (CI): the gate's version tests as they are; no new unit test, since both changes are workflow steps, and the
  repo tests no workflow text.
- By hand: the notes extract and the publish step's Python, as Steps 1 and 2 say, recorded in the PR.
- After the merge: the dispatch, and the first sign PR's merge.
- What none can show before the merge: a workflow that runs only on `main`; and that `claude plugin update` picks up
  `0.2.1`, which the first sign release shows (`/plugin marketplace update byhand`, then `claude plugin update
  byhand@byhand`).

## Docs

- `docs/releasing.md`: rewritten for the rule: the PR moves the version and dates its section, `release.yml` tags
  it, a minor is still tried in an empty session; two PRs at once.
- `AGENTS.md`: the `.github/` row gains `release.yml`; the `CHANGELOG.md` row says a dated section per version; within
  its 150 lines.
- `.claude/skills/finish-work/SKILL.md`: step 1 and Never, for the rule.
- `.claude/skills/propose-signs/SKILL.md`: step 8, the patch and its section.
- `CONTRIBUTING.md`: step 2's changelog line.
- `README.md` and `plugin/README.md`, Update: signs come as new versions often; auto-update under `/plugin`,
  Marketplaces, `byhand`, brings them without the command.
- `CHANGELOG.md`: no line; this changes nothing under `plugin/`.

## Risks

| Risk | Answer |
|---|---|
| Two PRs take the same version | the second conflicts in `CHANGELOG.md` and is rebased to the next patch. Resolved |
| A plugin PR forgets the bump | existing users wait for the next version, as they do today. Accepted |
| The model plants a heading or a link in the changelog lines | the publish job's checks, as for the PR text, and the maintainer reads the PR. Resolved |
| `release.yml` fails (GitHub down) | the version is on `main` and users update anyway; a dispatch tags it. Accepted |
| A PR's date is its opening day, not its merge's | the same as the release PRs; the maintainer may change it. Accepted |

## Plan review

None yet.
