# Releasing

A release is a version in `plugin/.claude-plugin/plugin.json`, its dated section in `CHANGELOG.md`, and a tag. Nothing
goes to PyPI: users install the plugin from this repo's marketplace (the bootstrap plan's decision of 2026-11-07).

1. **The release PR,** on a branch `<issue>-release-<version>`:
   - `plugin.json`'s `version` set to the new one;
   - `CHANGELOG.md`'s `## Unreleased` items moved under `## <version> (YYYY-MM-DD)`, with an empty `## Unreleased`
     above it;
   - the gate passes; its `version` check holds `plugin.json` against the changelog.
2. **After the merge,** on `main`'s merge commit: `gh release create v<version> --target <commit> --title "byhand
   <version>" --notes-file <the changelog section>`. The tag is the release.
3. **Try it** in an empty session: `/plugin marketplace add serionist/byhand`, `/plugin install byhand@byhand`, then
   a mail request and a check. Say in the release PR what ran.

Users update with `/plugin marketplace update byhand`. In `0.x` a minor may break a one-way door (AGENTS.md), under
the changelog's Breaking.
