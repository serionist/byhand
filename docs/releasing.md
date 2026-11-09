# Releasing

A release is a version in `plugin/.claude-plugin/plugin.json`, its dated section in `CHANGELOG.md`, and a tag. Nothing
goes to PyPI: users install the plugin from this repo's marketplace (the bootstrap plan's decision of 2026-11-07).
Claude Code updates an installed copy only when that version moves, so every PR that changes what a user's session
reads is a release of its own (`docs/plans/2026-11-09-sign-releases.md`).

1. **The PR moves the version,** by what it changes of `plugin/` (but `plugin/evals/` and `plugin/README.md`):

   | The PR changes | Version |
   |---|---|
   | sign files only, or fixes a skill or an agent | patch, `0.2.0` to `0.2.1` |
   | anything else: what a skill or agent does, `plugin.json` but its version, a one-way door (a minor may break one in `0.x`, under Breaking) | minor, `0.2.0` to `0.3.0` |
   | nothing a user's session reads: the package, tests, docs, the catalogue's sources alone | none |

   - It sets `plugin.json`'s `version`, and adds `## <version> (YYYY-MM-DD)` above the newest section in
     `CHANGELOG.md`, with its lines under `### Added`, `### Changed` or `### Fixed`. There is no Unreleased section.
   - The gate's `version` check refuses a `plugin.json` version that isn't the newest dated section, and a change to
     the newest section released on `main`: a line added there would merge under a version users already have.
   - The refresh agent's PRs do this by themselves: its publish job moves the patch and writes the line.
2. **After the merge,** `release.yml` tags the merge commit `v<version>` and creates the release, with the section as
   its notes; a push that doesn't move the version finds its release and stops. A failed run is re-run from its page,
   which keeps the commit. Users update with `claude plugin update byhand@byhand` and a new session, or by themselves
   with auto-update on.
3. **A minor is tried** in an empty session: `/plugin marketplace add serionist/byhand`, `/plugin install
   byhand@byhand`, then a mail request and a check, in the default permission mode: count the prompts. Say in the PR
   what ran.

## Two PRs that take the same version

Both add a section above the same one, so once one merges, the other conflicts in `CHANGELOG.md`. Rebase it on
`origin/main` and take the next version, in both files: `plugin.json` doesn't conflict, and has to move by hand. A
rebase that keeps both PRs' lines under the merged version fails the gate, and so does one that dates the next
version and leaves `plugin.json` behind. The refresh agent's PR is rebased the same way.
