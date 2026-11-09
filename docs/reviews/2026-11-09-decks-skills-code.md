---
subject: "Decks and sheets step 4, the skills, evals and docs (PR #91)"
base: main (f3ba1b4)
head: 6fcca30
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, Opus 5.5, every lens; its finding checked against the skills by the author)
verdict: clean
---

# Decks and sheets step 4: the skills

The reviewer recomputed the record's sizes and the scan file counts with `byhand.render`, and read every new grader
against the existing cases. No blocker or major.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `plugin/skills/learn/SKILL.md`, Learn a style, step 2 | "A file goes through the `byhand:scan` agent" sends a deck's PDF to Grep, against `check` step 5 ("a PDF get[s] no scan"); a scan of a PDF's compressed text with a `ran` line would make step 6 treat the patterned signs as absent, and an AI-written deck could be kept as a sample. The try by hand followed `check`'s rule | fixed: the sentence is cut; `learn` reads `check`'s steps 5 and 6, which say it |

## Refuted

- A sign file a skill names that `render` doesn't write: `write`'s "the same names with `.layout.md`" gives the
  family files too (`ko/gemini.layout.md`), and a missing file is skipped by each skill.
- `scan`'s "one to six" files: `render.scan_files` gives six for a `zh-Hant` deck.
- The graders: the `Read` pattern's four backslashes in single-quoted YAML match a JSON-doubled Windows separator;
  `flags: m` is a key an existing case uses.
- The CHANGELOG's "no longer uses your `document` default style": `write` step 4 falls back only to a style that is
  the default for no kind.
- A PDF over 10 pages needing Read's `pages`: "20 pages a call" points there, and Read's error corrects it.

## Not covered

- Whether starting `pptx` inside `check`, before step 4's reads, ends `check`'s `Read` grant in an interactive
  session: the tries ran headless. Added to the tries' record under Not tried.
- macOS and Linux: nothing run there.

## Improvements

| Improvement | Answer |
|---|---|
| `check` step 4: say "a language with no file" before the `check.layout.md` sentence, so a missing `en/check.layout.md` doesn't read as English having no signs | taken |
| `write` step 8: cut "Its look is the maker's call." | taken |
| README: "mails, messages or decks" leaves out sheets | taken |
| `check-en-deck`: put each label on a line of its own, and add a `Read` grader on `check.layout.md` | left: the case passed every run, and the PDF and `.pptx` tries showed the labels as extracted text does; a new paid run for the wording |
| `write-en-deck` repeats the description's example | left: the tries by hand used other words ("slides for", "prezentáció", "Excel-Datei") and `write` started on each |
| CHANGELOG: "asked to add no slide" | left: the line says what the hand-off does, as the plan words it |
