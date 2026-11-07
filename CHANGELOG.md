# Changelog

What changed in each release, for the people who use byhand. Versions follow [semantic versioning](https://semver.org);
before `1.0` a minor may break something, under Breaking.

## Unreleased

### Added

- The repository's harness: the gate, the hooks, CI, and the skills that plan, fit, review and finish a change.
- The catalogue's schema: the 100 most spoken languages, the model families, and `byhand validate` and
  `byhand models <id>`, which reads a model's family and version from its id, for models newer than the catalogue too.
- `byhand render`: the catalogue as small Markdown files in the plugin, one per language and model family, so a draft
  loads only what it needs, within a budget the build holds.
