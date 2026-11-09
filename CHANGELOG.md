# Changelog

What changed in each release, for the people who use byhand. Versions follow [semantic versioning](https://semver.org);
before `1.0` a minor may break something, under Breaking.

## Unreleased

### Added

- `/byhand:write`: writes a message, a mail, a post or a document in your own style, without the signs of AI writing.
- `/byhand:learn`: learns a style from your own samples, never from text that reads as AI-written, and keeps your
  styles in `~/.byhand/styles/`.
- `/byhand:check`: finds the signs of AI writing in a text or a file, in any of the catalogue's languages, with
  their lines and what a person writes instead. No score. A file's patterns run through its `scan` agent.
- Spanish signs: 11 of Spanish's own, and Spanish forms in seven signs every language shares. Until a native speaker
  reads them, each of Spanish's own signs counts only beside two others.
- Portuguese signs, for Brazil and Portugal alike: 8 of Portuguese's own, and Portuguese forms in seven signs every
  language shares. Until a native speaker reads them, each of Portuguese's own signs counts only beside two others.
