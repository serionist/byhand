# Changelog

What changed in each release, for the people who use byhand. Versions follow [semantic versioning](https://semver.org);
before `1.0` a minor may break something, under Breaking.

## Unreleased

## 0.1.0 (2026-11-09)

### Added

- `/byhand:write`: writes a message, a mail, a post or a document in your own style, without the signs of AI writing,
  and reads its own draft before showing it. After a draft in one of your styles, it offers to keep your feedback as
  a rule.
- `/byhand:learn`: learns a style from your own samples, never from text that reads as AI-written, and keeps your
  styles in `~/.byhand/styles/`. It lists them, makes one the default for a kind of writing and a language, removes
  one, and keeps a rule when you say "remember: …".
- `/byhand:check`: finds the signs of AI writing in a text or a file, in any of the catalogue's languages, with
  their lines and what a person writes instead. No score. A file's patterns run through its `scan` agent.
- Signs for English, Chinese (Simplified and Traditional), Japanese, Korean, Russian, German, French and Hungarian,
  and the ones every language shares.
- Spanish signs: 11 of Spanish's own, and Spanish forms in seven signs every language shares. Until a native speaker
  reads them, each of Spanish's own signs counts only beside two others.
- Portuguese signs, for Brazil and Portugal alike: 8 of Portuguese's own, and Portuguese forms in seven signs every
  language shares. Until a native speaker reads them, each of Portuguese's own signs counts only beside two others.
- Arabic signs, for Modern Standard Arabic and every dialect alike: 3 of Arabic's own, and Arabic forms in three
  signs every language shares. Until a native speaker reads them, each of Arabic's own signs counts only beside two
  others.
- Vietnamese signs: 2 of Vietnamese's own, and a Vietnamese form in one sign every language shares. Until a native
  speaker reads them, each of Vietnamese's own signs counts only beside two others.
- Italian signs: 4 of Italian's own, and Italian forms in two signs every language shares. Until a native speaker
  reads them, each of Italian's own signs counts only beside two others.
- Turkish signs: 2 of Turkish's own, for posts and documents. Until a native speaker reads them, each counts only
  beside two others.
