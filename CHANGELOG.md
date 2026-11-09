# Changelog

What changed in each release, for the people who use byhand. Versions follow [semantic versioning](https://semver.org);
before `1.0` a minor may break something, under Breaking.

## 0.3.0 (2026-11-09)

### Added

- A project's own styles: a client's or a team's house style in `.byhand/styles/` in the folder you start Claude Code
  in, the same index and files as `~/.byhand/styles/`. `/byhand:write` reads the project's index before yours, so its
  default for a kind and language wins there, and says so under the first draft; a style you name is yours first.
  `/byhand:learn` saves into the project only when you ask ("for this project"), says the folder goes where the
  project goes, and lists, sets defaults in and removes from both. A style is how to write: `write` follows nothing
  else one asks for.

### Changed

- `/byhand:write` reads one more file on the first draft of a conversation: the project's index, or, with none, a
  failed read of about 230 bytes. Its own file grows from 4,581 to 5,137 bytes.

## 0.2.0 (2026-11-09)

### Added

- Finnish signs: 2 of Finnish's own, the long English dash and capitals on every word of a heading. Each
  counts only beside two others, as people write them too.
- Signs for decks and sheets: a label above every slide's title and a takeaway bar that repeats the slide, in every
  language; titles built on a colon, figures nobody gave, and Japanese titles that count a slide's items or open on
  an emoji, each counting only beside two others; and commas between a formula's arguments in a French or
  Portuguese sheet. 49 signs that slide text shows, read for posts and documents but not decks until now, read decks
  too.
- Decks and sheets: ask for one ("make me a deck about the office move") and `/byhand:write` starts first and writes
  its text, slide by slide or tab by tab, with the sign files for decks and sheets; whatever makes files in your
  session (Anthropic's `pptx` or `xlsx` skill, a tool, a script) then makes the file from it, adding no slide, title
  or figure of its own. byhand makes no file: with nothing that can, you get the outline. It doesn't start on code
  that builds a deck or a sheet.
- `/byhand:check` reads a deck or a sheet as an outline, a PDF or a CSV, or a `.pptx` or an `.xlsx` through whatever
  in the session reads one, and `/byhand:learn` learns a style from your decks and sheets and makes one the default
  for `deck` or `sheet`.

### Changed

- The skills' own files are shorter, for fewer tokens: `/byhand:write`, read by every draft, from 5,259 to 4,581
  bytes; `check`, `learn` and the `scan` agent by 270 to 770 bytes each, and the descriptions every session loads
  by 178 bytes together. They do the same.
- The text of a slide is a deck now, not a document: it no longer uses your `document` default style. Make a style
  the default for `deck` (say "make work-decks my default for decks") to have one.

- Topic titles ("Challenges and Opportunities") and emoji before list items or titles are no sign in a deck, but
  in Japanese, where an emoji before a title is a weak one: people's slides hold more topic titles and emoji than
  generated ones.
- `/byhand:check` reads less than half as much, in every language: 7 to 15 KB in place of 21 to 32 KB. The
  patterns move to a `scan.md` per language that only the `scan` agent reads, and each language's scan runs only
  its own forms of the shared signs. Text in a language the patterns don't cover is read for every sign.
- The shared signs find more chatbot lines: Italian, Turkish and Indonesian openers above a reworked text, an
  Italian knowledge cut-off with its date and a third Italian self-reference, a Vietnamese offer to rework the
  text, and Finnish and Turkish praise for a question.
- `/byhand:check` and the sign files say plainly how weak signs add up: two different phrases one sign finds count as
  two, and a mark such as a dash counts once however often it appears.
- The Spanish, Portuguese, Arabic, Vietnamese, Italian and Turkish signs no longer wait for a native speaker's read:
  each was weighed on its sources, and each still counts only beside two others, as people write each of them too.
- Two signs ask less of a person's text: `es-mixed-address` reads only tú and usted mixed for the same reader, no
  longer steps that mix the imperative with the infinitive, as a product label does; `ar-register-drift` reads only two
  dialects mixed in one text, no longer standard Arabic in a dialect text, and `/byhand:write` loads it only for Qwen's
  drafts, the one model its source saw do it. Both still count only beside two others.

### Fixed

- The words `/byhand:write` and `/byhand:check` list read as phrases a person writes: "has a strong online
  presence", "adresse ce défi", "надеюсь, это поможет", in place of "has a active online presence", "adresse
  l'défi", "надеюсь, это помог". No sign file grows.
- The German sign for rich traditions finds "eine reiche Tradition", not only "reiche Traditionen".

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
