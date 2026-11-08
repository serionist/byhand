# Releasing

A release is a version in `plugin/.claude-plugin/plugin.json`, its dated section in `CHANGELOG.md`, and a tag. Nothing
goes to PyPI: users install the plugin from this repo's marketplace (the bootstrap plan's decision of 2026-11-07).

1. **The release PR,** on a branch `<issue>-release-<version>`:
   - `plugin.json`'s `version` set to the new one;
   - `CHANGELOG.md`'s `## Unreleased` items moved under `## <version> (YYYY-MM-DD)`, with an empty `## Unreleased`
     above it;
   - the gate passes; its `version` check refuses a `plugin.json` version that isn't the newest dated section.
   - `uv run tools/gate.py full`, said in the PR.
2. **After the merge,** the merge is the release: new installs take `main`'s head at once. Tag that commit, with the
   section's lines, below its heading, in `.local/notes.md`:

   ```text
   gh release create v<version> --target <full SHA of git rev-parse origin/main> --title "byhand <version>" --notes-file .local/notes.md
   ```

   Until the next version, what merges to `main` reaches new installs under the same version, and existing users
   keep their copy; so a fix users need is a patch release.
3. **Try it** in an empty session: `/plugin marketplace add serionist/byhand`, `/plugin install byhand@byhand`, then
   a mail request and a check, in the default permission mode: count the prompts. Say in the release PR what ran.

Users update with `claude plugin update byhand@byhand` and a new session. In `0.x` a minor may break a one-way door (AGENTS.md), under
the changelog's Breaking.
