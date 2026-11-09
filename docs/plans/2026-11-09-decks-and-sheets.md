---
title: Write the text of decks and sheets for whatever makes the file
issue: "#66"
status: draft
approved_by:
approved_at:
---

# Write the text of decks and sheets for whatever makes the file

## Goal

A user asks Claude Code to make a deck, a sheet or a document as a file ("make me a deck about the office move"), and
`write` starts by itself, as it does for a mail. It writes the text that goes into the file, slide by slide or tab by
tab, by the signs for that kind, the layout signs among them, and the user's style, and hands it to whatever makes the
file in that session: another skill (Anthropic's `pptx`, `xlsx` or `docx`), a script, a tool, or the user. byhand
makes no file (the maintainer, on #66, 2026-11-09). `check` reads a deck's or a sheet's text, and `learn` learns a
style from the user's own decks and sheets. A deck then reads as one the user made at their own level: their words,
as much text per slide as they put, the slides a person makes, not a generator's defaults.

In scope:

- `write`, `check`, `learn` and `scan` for the kinds `deck` and `sheet`, and `write`'s hand-off for a file;
- the layout signs, from the sources a `find-sources` run finds, drafted with `propose-signs`;
- `render`: which files a deck or a sheet reads, and the layout signs in a check file of their own;
- the evals: `write` starts on deck and sheet requests, not on code that builds a deck or a sheet.

Out of scope:

- making, reading or editing a `.pptx`, `.xlsx` or `.docx`: whatever makes the file does that, and no skill
  pre-approves more than it does today (`Read` only; the gate allows `Read`, `Glob` and `Grep`);
- signs of a deck's look that no text shows (colours, fonts, images): a sign can say what a slide holds ("a photo
  under every title"), not how a renderer draws it;
- byhand's own measurements of generators' decks and sheets (the research's open question 6): a method and a human
  sample check of their own, an issue if Step 2 finds nothing to seed from;
- learning from edits (`0.5.0`).

## Design

### What `write` does for a file

The maintainer's answer on #66 is options 1 and 2 together: `write` starts when the user has a file made, and works
on its text. Whatever makes the file in the session makes it.

| | Now | After |
|---|---|---|
| Starts on | a message, a mail, a post or a document | the same, and the text of a deck or a sheet, or of a document made as a file; before the skill or tool that makes it |
| Not on | code-adjacent writing | the same, and code that builds a deck or a sheet (a `python-pptx` script, an `openpyxl` builder) |
| Kinds (step 1) | `message`, `email`, `post`, `document` ("the text of a slide" is a document) | adds `deck` (slides, a presentation, the text of a slide) and `sheet` (a spreadsheet's tabs, headers, labels, notes) |
| Reads (step 5) | short files; a post or a document the long ones too | a deck or a sheet: the short files and the `.layout.md` ones |
| Drafts (step 6) | prose | for a deck, a `## <n>. <title>` heading per slide as it shows, its text, `Notes:` for speaker notes, and in square brackets what goes there that isn't text (`[bar chart: tickets closed per month]`); for a sheet, a heading per tab, a Markdown table of its headers and labels with the user's numbers or empty cells, never invented ones, and its notes |
| Answers (step 8) | the draft and nothing else | the same when nothing in the session makes the file. When something does (another skill, a script, a tool the user named), go on to it with this text: it keeps the words, the order and what goes on each slide, and adds no slide, title or label of its own, and no picture, icon or chart the square brackets don't name; how the file looks (fonts, colours, where things sit) is its call |

The outline form is the one place a deck's text is plain text: `check` and `scan` read it as a Markdown file, and
`learn` takes it as a sample. A document made as a file needs no form: its text is prose.

The description gains one clause and stays under the 1,536 characters Claude Code shows of a skill's description
(code.claude.com/docs/en/skills, frontmatter reference). Claude Code documents no order between two skills that
match one request ("Any ordering you rely on would be prompt wording": none of the skills docs covers it), so the
description says to start before the skill that makes the file, and Step 4 tries it beside Anthropic's
`document-skills` plugin by hand: its `pptx` skill's description starts on any mention of a deck, slides or a
presentation.

### Which files a deck reads

Today `render.draft_files` gives a deck the layout files alone, so a Hungarian deck misses
`hu-title-case-headings` (kinds `document`, `deck`, `post`, in the long file) and every `any` sign. After:

- a sign renders into each file a reader of its kinds reads: the short file when its kinds hold `any`, `message` or
  `email`; else the long file when they hold `post` or `document`, and the layout file when they hold `deck` or
  `sheet`, both when both (`part` becomes `parts`; a sign in two families already renders twice);
- a deck or a sheet reads the short files and the layout files: every sign whose kinds hold it, and none of the 67
  post-and-document signs it would skip by kind;
- the post-and-document signs a slide's text shows too (headings, promotional words, a structure announced:
  `fr-english-headings`, `ja-structure-announcements`) gain `deck` in Step 3, as `hu-title-case-headings` has it
  already: slide text read them as a `document` until now. They are in `check.md` already, so a check pays nothing
  more, and the long files are 5.2 KB at most (`fr`).

A check reads every family's signs with their patterns. `any/check.md` and a language's `check.md` come to 31.0 KB
for `zh-Hant` and 32.3 KB for `ja` today, against a 32 KB budget, so the layout-only signs go to `check.layout.md`,
one per scope, which a check reads only for a deck or a sheet. The `layout` budget, 16 KB, holds a draft's layout
files together and a check's together: one constant, two sums.

### The layout signs

From sources, as every sign is; the research found few (`docs/research/2026-11-06-sources.md`, Summary 8):

| Source | What it shows | Use |
|---|---|---|
| `analystacademy/flight-check` (B23), MIT | six deck checks: topic-label headlines, vague claims, numbers that disagree across slides, a leftover `[TBD]`, 3D charts, AI prose | a source, read through its repo |
| plusai, uxdesign.cc, presentations.ai (E6), all rights reserved | identical card grids, a coloured bar by every text box, text overload, topic-label headlines; opinion, not measured | facts only, with a citation, `by-hand` |
| SlideAudit (arXiv 2508.03630) | design flaws in 2,400 slides, not AI origin | dropped: it says nothing of who made a slide |
| spreadsheets | none found | Step 2 searches again |

Step 2 runs `find-sources` for decks and sheets, in English and in the seed languages' own words ("KI-Folien",
"AI PPT 特征", "AIっぽいスライド"), as the research did for prose. Then `propose-signs` drafts them (Step 3) under
the catalogue's rules, unchanged:

- a layout sign is `any` only when its sources show it in two languages (`AGENTS.md`, Traps); one seen only in
  English is `en`'s, and a German deck reads the `any` signs alone until a German source shows it;
- its `flags` and `passes` are invented outlines in the form above, and a `check` runs on them where it has one
  (an emoji opening every slide title); the rest are for the model's own read;
- a deck source gives a sign only where it ties the habit to AI or to a generator, such as flight-check's AI
  authorship check. Its checks of a deck's quality give none (action titles, a cited source, 3D charts, a leftover
  `[TBD]`): many people's own decks have topic titles, and a sign would push `write` above the user's level. Those
  are a style's to say;
- no source for sheets: recorded here as having none, as Hindi was, and a sheet reads the short files only.

### `check` and `learn`

`check` reads a deck's or a sheet's text from what Read can read:

- the outline, pasted or as a Markdown file: as any text, a file through `scan`;
- a deck or a sheet as a PDF, which PowerPoint, Keynote, Google Slides and Excel all save: Read shows each page's
  text and image, at most 20 pages a call, so layout signs are read from the pages. Grep can't read a PDF, so it gets
  no scan and is read for every sign, as pasted text is;
- a sheet's tab as CSV: as a file, through `scan`;
- a `.pptx`, `.xlsx` or `.docx`: Read can't read it, so the text comes from whatever reads the file in the session
  (Anthropic's `pptx` reads a deck's text and its notes), as `write` hands a file on; with nothing that can, no "no
  signs": ask for a PDF, a CSV or the text, as `check` step 1 does today for a `.docx`.

For a deck or a sheet it also reads `any/check.layout.md` and the language's, and its answer names the kind. `scan`
takes the two kinds. `learn` takes decks and sheets as samples in the same forms, screened by `check`'s steps, and a
style can be the default for `deck` or `sheet`: the index's `Default for` column already holds any kind
(bootstrap plan, Styles). A deck style says what the user's slides hold: titles as topics or as sentences, how much
text, bullets or sentences, notes or none; a sheet style, their headers, units and notes. Its excerpts are slides'
or tabs' text, word for word. `write`'s choice of a style is unchanged: a deck with no deck style of its own uses
the one style in its language that is the default for no kind, or none.

### What a draft costs

Bytes, as the Step 7 record counted them (no API key counts tokens); 16 KB is about 4,000 tokens in English.

| A deck or a sheet reads | Today | Budget |
|---|---|---|
| the short files, as a mail does | 6.5 to 12.8 KB (`vi`, `zh-Hant`) | 14 KB (`mail`) |
| its layout files | none yet: Step 3's seed | 16 KB (`layout`), lowered in Step 3 to the seed's largest read plus 4 KB |
| a style | under 4 KB | `learn` holds it |
| a check: `check.md` files, then `check.layout.md` ones | 22.1 to 32.3 KB | 32 KB (`check`), and `layout` |

So a deck's draft reads what a mail reads plus its layout files: 12.8 KB at most today, about 3,200 tokens, plus
the seed's layout files, and under 30 KB (some 7,500 tokens) at the caps. Step 4's record gives the bytes per seed
language, as Step 7's did. A deck's PDF read by `check` or `learn` costs
its pages' images too: the user chose that deck, and 20 pages is one read.

### Alternatives

- **byhand makes the file** (#66's option 3): it would need a tool that runs a command, which the plugin pre-approves
  for none; the maintainer chose not to.
- **A deck reads the long files too:** one line in `draft_files`, but up to 6 KB more a deck (`fr`, `ja`) for 67
  signs it skips by kind, to reach one sign.
- **Layout signs in `check.md`:** every mail's check would pay for them, and `ja` is at its budget already.
- **A stub file-making skill in the eval suite,** to grade the order with `tool_order`: the suite loads only the
  plugin under test (code.claude.com/docs/en/plugin-evals), and a case's `plugins:` field is documented only as
  "plugin directories under test"; the try by hand with the real `document-skills` shows more.
- **A deck falls back to the user's document style:** a style is learned from one kind of writing; the existing rules
  hold, and `learn` makes a deck style from the user's decks.

## Compatibility

No one-way door changes: the kinds `deck` and `sheet` and the `layout` category are in the schema since `0.1.0`, the
skills keep their names, and a style's format and folders are as they are; `Default for` takes kinds it always could.

What users notice: a request for "the text of a slide" is a `deck` now, not a `document`, so it reads the short and
layout files instead of the short and long ones. A new file, `check.layout.md`, under `plugin/signs/`. `write` starts
on deck and sheet requests it may have missed. CHANGELOG says so under Unreleased.

## Steps

1. **Render.** `parts` for a sign; a deck's and a sheet's `draft_files` are the short and layout files;
   `check.layout.md` per scope with the layout-only signs and their patterns, and `check_files` takes a kind; the
   `layout` budget over both sums. Proven by `tests/test_render.py`: a `document`-and-`deck` sign in the long and the
   layout file; a `deck`-only sign in the layout file and `check.layout.md`, never `check.md`; `draft_files` for
   `deck` and `sheet`; a check of a deck over its layout budget fails; the files `render` writes from the catalogue
   are unchanged but `hu/any.layout.md` (from `hu-title-case-headings`).
2. **Sources.** One `find-sources` run for decks and sheets: B23 and E6 as entries, the search in the seed languages'
   own words, a research record. Proven by `byhand validate`.
3. **Signs.** `propose-signs` on Step 2's sources, and `deck` added to the post-and-document signs a slide's text
   shows, a PR per language, or one for `any` and `en` when the sources are
   few, as `docs/plans/2026-11-09-more-languages.md` allows; `layout` lowered to the largest read plus 4 KB. Sheets
   with no source: a progress-log line. Proven by `byhand validate` (each sign's `flags` and `passes`) and the render
   budgets.
4. **The skills.** `write` (description, kinds, the files, the outline, the hand-off), `check` (the forms, the layout
   check files, a file read through what the session has), `scan` (the kinds), `learn` (the kinds, the samples); the evals; the docs. Proven by the gate's
   plugin and skills checks, the eval suite and the tries by hand under Tests, recorded in
   `docs/reviews/<date>-decks-real-sessions.md`.

Each step ends with `finish-work`: the gate, `review-code` until clean, a PR.

## Tests

- **Unit (CI):** Step 1's render tests; `byhand validate` on every layout sign's `flags` and `passes`; the budgets.
- **The eval suite** (`claude plugin eval --ablation none --threshold 1.0`, three runs a case, every text invented):
  - 6 deck and sheet requests, each graded `tool_used: Skill` on `write` and never `check`: a deck in en, hu, de and
    ja ("make me a deck about…", "készíts egy prezentációt…"), a sheet in en and fr; the en ones also graded
    `tool_used: Read` on `signs[\\/](any|en)[\\/]any\.layout\.md` once Step 3 seeds them. A run loads only the
    plugin and allows only `Read` and `Skill`, so nothing makes a file: each deck case is also graded by a `regex` on
    `last_message`, `^## 1\.` with `flags: m`, and each sheet case by `^\|`, the outline answered.
    `write-en-slide-text` stays. Bar: 6 of 6.
  - 4 code cases graded `write` never started: a `python-pptx` script from a CSV, an `openpyxl` builder, a bug in a
    deck-building function, a CSV parser. Bar: at most 1 of 4, in one run.
  - 1 case of a pasted outline asked "does this deck read as AI-written?", graded on `check`.
- **By hand** (Claude Code of the day, `claude --plugin-dir plugin`, Windows at least), with Anthropic's
  `document-skills` installed: 3 deck requests and 2 sheet requests. Bar: `write` starts on all 5, before the skill
  that makes the file on 4, and each file's slide titles and headers are `write`'s. Also: `check` on a deck's PDF and
  on a sheet's CSV and on a `.pptx` read through `pptx`, `learn` from an invented deck PDF, and slides holding an
  element the outline doesn't name, counted.
- **The maintainer,** in their own session: a deck style learned from their own decks, and two decks, in English and
  Hungarian, read as theirs. The record holds counts and verdicts, never a deck or a style.
- **What none can show:** whether a reader takes a deck as the user's beyond the maintainer's two; and whether a
  maker keeps the words in sessions other than the ones tried.

## Docs

`README.md` (what byhand writes, and that it makes no file), `plugin/README.md` (the skills table: decks and sheets,
the hand-off), `docs/USAGE.md` (the files table: `check.layout.md`; what a deck reads; the budgets),
`AGENTS.md` (Where the work stands), `CHANGELOG.md` under Unreleased, this plan's progress log.

## Risks

| Risk | Answer |
|---|---|
| The maker starts first and writes its own text, so `write` never starts or its text is dropped | The description says to start first, and the hand-off says to keep the words; the try by hand measures it on the real `document-skills`; accepted, the description tuned if it misses |
| The maker adds text of its own (a "Key takeaways" slide, a chart title) | The hand-off says to add none; accepted: what a later skill does is outside byhand |
| Few or no sources for layout signs, none for sheets | No sign without one; a sheet reads the short files; recorded, as Hindi was; accepted |
| A layout sign flags a plain human deck (three bullets, a title slide) | Each has a `passes` outline, and a weak one counts only in a cluster, as for prose |
| A deck PDF costs many tokens to read | Only for a check or a sample the user gives; 20 pages a read; accepted |
| `write` starts on code that builds a deck | The description names it; 4 eval cases |

## Progress log

| Step | What | PR | State |
|---|---|---|---|

## Plan review

### Fit

The plan at `43fd541`, by a fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, read cold, with prior
art from Claude Code's skills and plugin-evals docs, Anthropic's `pptx`, `xlsx` and `docx` skills and
`analystacademy/flight-check`; not Context7. The change's own question: does the plan keep to the maintainer's answer
on #66 with no change to what the plugin pre-approves, as simply as it can, and stay open to decks at a human skill
level and to `0.5.0`? Its answer: yes, but for I2 and I3. Answers by the author on the maintainer's standing word
("take recommended improvements"), 2026-11-09.

| # | Improvement | Answer |
|---|---|---|
| I1 | Step 3 adds `deck` to the post-and-document signs a slide's text shows (`fr-english-headings`, `ja-structure-announcements`), as `hu-title-case-headings` has it: slide text read them as a `document` until now | taken |
| I2 | A deck source gives a sign only where it ties the habit to AI; flight-check's quality checks (action titles, 3D charts, `[TBD]`) give none, or `write` would push a deck above the user's level | taken |
| I3 | The hand-off: the maker adds no picture, icon or chart the outline doesn't name (`pptx` puts a visual on every slide); the try by hand counts them | taken |
| I4 | `check` and `learn` take a `.pptx`'s text from whatever reads it in the session, and ask for a PDF or a CSV only when nothing can | taken |
| I5 | A `regex` grader on each deck and sheet case proves the outline is answered with no maker; the try of it by hand cut | taken |

Noticed on the way, for Round 1: the check's cost mixes decimal and binary KB (`ja` reads 32,274 bytes of 32,768;
Which files a deck reads); a quote on skill ordering with no source in the skills docs (What `write` does for a file);
the E6 row lists look-only tells that Out of scope excludes (The layout signs); a `[TBD]` check would match the
outline's own square brackets (The layout signs); `scan` takes "one to three paths of `check.md` files", and a deck's
check passes up to six (Step 4).
