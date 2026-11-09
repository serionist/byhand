---
title: Write the text of decks and sheets for whatever makes the file
issue: "#66"
status: approved
approved_by: serionist
approved_at: 2026-11-09
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
| Drafts (step 6) | prose | for a deck, a `## <n>. <title>` heading per slide as it shows, its text, `Notes:` for speaker notes, and in square brackets what goes there that isn't text, a chart with the user's numbers (`[bar chart, tickets closed: Jan 180, Feb 210]`) or none (`[bar chart, tickets closed per month: your numbers]`); for a sheet, a heading per tab and a Markdown table, each row starting `\|`, of its headers and labels with the user's numbers or empty cells, never invented ones, and its notes. A single slide's text for the user is its title on a line and its text, with no heading marks |
| Answers (step 8) | the draft and nothing else | for a file, the session goes on to make it as it would without byhand (another skill, a tool the user named, a script of its own) with this text: it keeps the words, the order and what goes on each slide, and adds no slide, title, label or number the text doesn't give, and no picture, icon or chart the square brackets don't name; how the file looks (fonts, colours, where things sit) is its call. When the session can't make the file, the draft and nothing else, as now |

The outline form is the one place a deck's text is plain text: `check` and `scan` read it as a Markdown file, and
`learn` takes it as a sample. A document made as a file needs no form: its text is prose.

The description gains one clause and stays under the 1,536 characters Claude Code shows of a skill's description
(code.claude.com/docs/en/skills, frontmatter reference). The skills docs give no order between two skills that
match one request, so the description says to start before the skill that makes the file, and Step 4 tries it beside Anthropic's
`document-skills` plugin by hand: its `pptx` skill's description starts on any mention of a deck, slides or a
presentation.

### Which files a deck reads

Today `render.draft_files` gives a deck the layout files alone, so a Hungarian deck misses
`hu-title-case-headings` (kinds `document`, `deck`, `post`, in the long file) and every `any` sign. After:

- a sign renders into each file a reader of its kinds reads: the short file when its kinds hold `any`, `message` or
  `email`; else the long file when they hold `post` or `document`, and the layout file when they hold `deck` or
  `sheet`, both when both (`part` becomes `parts`; a sign in two families already renders twice). A short-file sign
  stays in the short file alone, `deck` in its kinds or not, as a deck reads that file;
- a deck or a sheet reads the short files and the layout files: every sign whose kinds hold it, and none of the 82
  post-and-document signs it would skip by kind;
- every sign whose kinds name `document` and not `deck`, 81 (76 in the long files, 5 in the short), is a sign slide text read
  as a `document` until now, and a deck drops it by kind. Step 3 goes through them and adds `deck` to those a slide's
  text shows, as `hu-title-case-headings` has it already: in the short files `any-assistant-preamble` (strong),
  `any-emoji-markers` (usual), `hu-parenthetical-gloss` and `hu-explicit-subject-repeat`; in the long files
  `any-assistant-closing-offer`, `zh-leaked-request`, `fr-english-headings`, `ja-structure-announcements` and the
  others like them. `any-raw-markdown` stays off: its pattern finds `## `, which the outline form is built of.
  `any-emoji-markers`' pattern takes an emoji after a heading's marks only, so it gains an optional slide number
  (`## 1. 🚀 …`) and a `flags` outline with one. They are in `check.md` already, so a check pays nothing more, and
  the long files are 5,169 bytes at most (`fr`).

A check reads every family's signs with their patterns. `any/check.md` and a language's `check.md` come to 31,027 bytes
for `zh-Hant` and 32,274 for `ja` today, against a budget of 32,768, so the layout-only signs go to `check.layout.md`,
one per scope, which a check reads only for a deck or a sheet. The `layout` budget, 16 KB, holds a draft's layout
files together and a check's together: one constant, two sums.

### The layout signs

From sources, as every sign is; the research found few (`docs/research/2026-11-06-sources.md`, Summary 8):

| Source | What it shows | Use |
|---|---|---|
| `analystacademy/flight-check` (B23), MIT | six deck checks: topic-label headlines, vague claims, numbers that disagree across slides, a leftover `[TBD]`, 3D charts, AI prose | a source, read through its repo |
| plusai, uxdesign.cc, presentations.ai (E6), all rights reserved | identical card grids, a coloured bar by every text box, text overload, topic-label headlines; opinion, not measured | facts only, with a citation, `by-hand`, for what the text shows (identical cards, text overload); topic-label headlines are a style's to say and a coloured bar is look, so neither gives a sign |
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
- no source for sheets: recorded here as having none, as Hindi was. A sheet still reads the layout files, as Step 1
  gives it, but only the short files' signs apply to it until a sign names `sheet`.

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
| the short files, as a mail does | 6,533 to 12,834 bytes (`vi`, `zh-Hant`) | 14 KB (`mail`) |
| its layout files | none yet: Step 3's seed | 16 KB (`layout`), lowered in Step 3 to the seed's largest read plus 4 KB |
| a style | under 4 KB | `learn` holds it |
| a check: `check.md` files, then `check.layout.md` ones | 20,991 bytes (a language with no signs of its own) to 32,274 (`ja`) | 32 KB (`check`), and `layout` |

So a deck's draft reads what a mail reads plus its layout files: 12,834 bytes at most today, about 3,200 tokens, plus
the seed's layout files, and under 30 KB (some 7,500 tokens) at the caps. Step 4's record gives the bytes per seed
language, as Step 7's did. A deck's PDF read by `check` or `learn` costs
its pages' images too: the user chose that deck, and 20 pages is one read.

### Alternatives

- **byhand makes the file** (#66's option 3): it would need a tool that runs a command, which the plugin pre-approves
  for none; the maintainer chose not to.
- **A deck reads the long files too:** one line in `draft_files`, but up to 6 KB more a deck (`fr`, `ja`) for 82
  signs it would mostly skip by kind.
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
layout files instead of the short and long ones, with the `document` signs a slide shows kept by Step 3, and no longer uses the user's `document` default style: `learn`
makes a style the default for `deck`, as CHANGELOG says. A new file, `check.layout.md`, under `plugin/signs/`. `write` starts
on deck and sheet requests it may have missed. CHANGELOG says so under Unreleased.

## Steps

1. **Render.** `parts` for a sign; a deck's and a sheet's `draft_files` are the short and layout files;
   `check.layout.md` per scope with the layout-only signs and their patterns, and `check_files` takes a kind; the
   `layout` budget over both sums. Proven by `tests/test_render.py`: a `document`-and-`deck` sign in the long and the
   layout file; an `email`-and-`deck` sign in the short file alone; a `deck`-only sign in the layout file and `check.layout.md`, never `check.md`; `draft_files` for
   `deck` and `sheet`; a check of a deck over its layout budget fails; the files `render` writes from the catalogue
   are unchanged but `hu/any.layout.md` (from `hu-title-case-headings`).
2. **Sources.** One `find-sources` run for decks and sheets: B23 and E6 as entries, the search in the seed languages'
   own words, a research record. Proven by `byhand validate`.
3. **Signs.** `propose-signs` on Step 2's sources, and `deck` added to the signs naming `document` that a slide's
   text shows, the four short-file ones above among them, a PR per language, or one for `any` and `en` when the sources are
   few, as one English reader reviews both; `layout` lowered to the largest read plus 4 KB. Sheets
   with no source: a progress-log line. Proven by `byhand validate` (each sign's `flags` and `passes`), the render
   budgets, and a render test that in the files a deck reads the lines of `any-assistant-preamble` and
   `any-emoji-markers` name `deck` and that of `any-raw-markdown` doesn't.
4. **The skills.** `write` (description, kinds, the files, the outline, the hand-off), `check` (the forms, the layout
   check files, a file read through what the session has), `scan` (the kinds, and up to six check files, `check.layout.md` among them), `learn` (the kinds, the samples); the evals; the docs. Proven by the gate's
   plugin and skills checks, the eval suite and the tries by hand under Tests, recorded in
   `docs/reviews/<date>-decks-real-sessions.md`.

Each step ends with `finish-work`: the gate, `review-code` until clean, a PR.

## Tests

- **Unit (CI):** Step 1's render tests; `byhand validate` on every layout sign's `flags` and `passes`; the budgets;
  an invented plain deck outline in `tests/test_office.py`'s office texts, so no strong or usual pattern, the layout
  ones and those Step 3 gives `deck` among them, counts alone on it.
- **The eval suite** (`claude plugin eval --ablation none --threshold 1.0`, three runs a case, every text invented):
  - 6 deck and sheet requests, each graded `tool_used: Skill` on `write` and never `check`: a deck in en, hu, de and
    ja ("make me a deck about…", "készíts egy prezentációt…"), a sheet in en and fr; the en ones also graded
    `tool_used: Read` on `'signs(?:/|\\\\)(?:any|en)(?:/|\\\\)any\.layout\.md'` (single-quoted YAML: the
    input is matched as JSON, where a backslash is doubled) once Step 3 seeds them. A run loads only the
    plugin and allows only `Read` and `Skill`, so nothing makes a file: each deck case is also graded by a `regex` on
    `last_message`, `^## 1\.` with `flags: m`, and each sheet case by `^\|` with `flags: m`, the outline answered.
    `write-en-slide-text` stays. Bar: 6 of 6.
  - 4 code cases graded `write` never started: a `python-pptx` script from a CSV, an `openpyxl` builder, a bug in a
    deck-building function, a CSV parser. Bar: at most 1 of 4, in one run.
  - 1 case of a pasted outline asked "does this deck read as AI-written?", graded on `check`.
- **By hand** (Claude Code of the day, `claude --plugin-dir plugin`, Windows at least), with Anthropic's
  `document-skills` installed: 3 deck requests and 2 sheet requests. Bar: `write` starts on all 5, before the skill
  that makes the file on 4, and each file's slide titles and headers are `write`'s. Also: `check` on a deck's PDF and
  on a sheet's CSV and on a `.pptx` read through `pptx`, `learn` from an invented deck PDF, and slides holding an
  element the outline doesn't name, counted. Then 2 deck requests in a session with no maker installed: what the
  session does with the text (a script of its own, or the outline answered), and whether the file's words are
  `write`'s.
- **The maintainer,** in their own session: a deck style learned from their own decks, and two decks, in English and
  Hungarian, read as theirs. Its makers (claude.ai's synced `pptx`, `xlsx` and `docx`, and any tool its system
  prompt puts first for a deck) are counted apart: whether `write` started, and whether it started first. The record holds counts and verdicts, never a deck or a style.
- **What none can show:** whether a reader takes a deck as the user's beyond the maintainer's two; and whether a
  maker keeps the words in sessions other than the ones tried.

## Docs

`README.md` (what byhand writes, and that it makes no file), `plugin/README.md` (the skills table: decks and sheets,
the hand-off), `docs/USAGE.md` (the files table: `check.layout.md`; what a deck reads; the budgets),
`AGENTS.md` (Where the work stands), `CHANGELOG.md` under Unreleased, this plan's progress log.

## Risks

| Risk | Answer |
|---|---|
| The maker starts first and writes its own text, so `write` never starts or its text is dropped | The description says to start first, and the hand-off says to keep the words; the tries by hand measure it on the real `document-skills` and in the maintainer's session; accepted, the description tuned if it misses |
| The maker adds text of its own (a "Key takeaways" slide, a chart title) | The hand-off says to add none; accepted: what a later skill does is outside byhand |
| Few or no sources for layout signs, none for sheets | No sign without one; a sheet reads the short files; recorded, as Hindi was; accepted |
| A layout sign flags a plain human deck (three bullets, a title slide) | Each has a `passes` outline, a weak one counts only in a cluster, as for prose, and the office tests' plain deck outline holds that no strong or usual pattern counts alone on it |
| A deck PDF costs many tokens to read | Only for a check or a sample the user gives; 20 pages a read; accepted |
| `write` starts on code that builds a deck | The description names it; 4 eval cases |

## Progress log

| Step | What | PR | State |
|---|---|---|---|
| 1 | the render: `parts`; a deck and a sheet read the short and the layout files; `check.layout.md` per scope, and `check_files` and `scan_files` take a kind. Departures, after #86 moved the patterns out of `check.md`: the layout-only signs' patterns go to a `scan.layout.md` per scope, beside `scan.md`, and `layout` holds three sums, a draft's layout files, a check's `check.layout.md` files and a scan's `scan.layout.md` files, while `check` (16 KB) and `scan` (9 KB) hold the rest of a deck's check. The render adds `hu/any.layout.md` and `fi/any.layout.md` (`fi-title-case-headings`, seeded in #79 after this plan), every other file byte-identical, and no `check.layout.md` or `scan.layout.md` until a layout-only sign; `byhand render --check` and the diff show it, not a test pinning the catalogue's files, which every new sign would break | — | open |
| 2 | sources for decks and sheets: 12 for decks (en, ja, zh, zh-Hant, ko), 5 for sheets (en, fr, pt); no sheet source in the other languages; `docs/research/2026-11-09-sources-decks-sheets.md` | #83 | open |

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

### Round 1

A fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, on `6da748a`, which computed the sizes against
`byhand.render` and ran the `any` patterns over an invented outline; P1 confirmed by a fresh refuter on the same
model, which corrected its list of signs. Verdict: needs-fixes; fixed in place by the author.

| # | Sev | Finding | Status |
|---|---|---|---|
| P1 | major | Slide text as a `deck` drops every sign naming `document` and not `deck`, the short-file ones too: a deck with an emoji before each title, or an "Absolutely! Here's…" preamble, passes clean of `any-emoji-markers` and `any-assistant-preamble` | fixed: Which files a deck reads names the 76 signs Step 3 goes through and the four short-file ones; `any-raw-markdown` stays off; a render test |
| P2 | minor | A user's `document` default style no longer reaches slide text, and Compatibility didn't say | fixed: Compatibility and CHANGELOG say to make a style the default for `deck` |
| P3 | minor | No try of a session with no maker, where Claude may write its own script | fixed: 2 deck requests by hand with no maker installed; Q1 |
| P4 | minor | The makers tried were not the maintainer's (claude.ai's synced skills, a tool the system prompt puts first) | fixed: counted apart in the maintainer's session |
| P5 | minor | A chart bracket with no numbers invites the maker to invent them | fixed: a chart carries the user's numbers or says they are the user's to add; the hand-off adds no number |
| P6 | minor | One slide's text for the user would carry `## 1.` scaffolding to paste | fixed: a single slide is its title on a line and its text |
| P7 | minor | Sizes mixed decimal and binary KB; 67 post-and-document signs were 82 | fixed: bytes; 82 |
| P8 | minor | A quotation no doc holds | fixed: a plain statement |
| P9 | minor | The E6 row listed a look-only tell and topic-label headlines, which I2 rules out | fixed: the row says neither gives a sign |
| P10 | minor | `scan` takes one to three check files; a deck's check passes up to six | fixed: Step 4 |
| P11 | minor | The Read grader's pattern took no doubled backslash, as JSON gives a Windows path | fixed: a slash or two backslashes, in single-quoted YAML |
| P12 | minor | `any` and `en` sharing a PR was cited to a plan that allows no such thing | fixed: its own reason |

Refuted: a `[TBD]` check matching the outline's brackets (the plan gives no `[TBD]` sign, and no `any` pattern hits
the outline); `check` running a command through another skill (the command is that skill's, under the user's
permissions; `check` pre-approves `Read` alone); the sandbox loading other skills (it loads only the plugin); a
`regex` grader without `flags` (an existing case uses `flags: im`); the 1,536-character figure; `tool_order` with a
stub maker (the `plugins:` field is documented only as under test); `check.layout.md` breaking the test of sign files
a skill names (it ends in `.layout.md`).

| # | Question | Recommendation | Answer |
|---|---|---|---|
| Q1 | With nothing in the session that makes files, does `write` answer the outline and stop, or does the session go on as it would without byhand (a script of its own), under the hand-off's rules? | go on as the session would: "whatever makes the file in that session makes it" | the recommendation, on the maintainer's standing word: the Answers row says so |

| # | Improvement | Answer |
|---|---|---|
| I6 | Say a sheet reads the layout files but only the short files' signs apply until a sign names `sheet`, as Step 1's code gives it | taken |
| I7 | An invented plain deck outline in the office tests, so no layout check counts alone on a human deck | taken |
| I8 | The sheet form's table rows start with `\|`, so the sheet grader's `^\|` holds | taken |

Round 2 reads the fixes.

### Round 2

A fresh Claude Code agent on Opus 5.5 (claude-opus-5-5), 2026-11-09, on `0410a65`, reading the round 1 edits; it
checked each sign's kinds, the counts and sizes against `byhand.render`, the grader facts against the plugin-evals
docs, and ran every pattern over invented outlines. Verdict: approved; its minors fixed in place by the author.

| # | Sev | Finding | Status |
|---|---|---|---|
| P13 | minor | Step 3's render test would fail on `any-raw-markdown`, which a deck's short file holds, and pass without Step 3 for the other two; and `parts` left open whether a short-file sign gaining `deck` is copied into the layout file | fixed: the test checks the kinds on each line; a short-file sign stays in the short file alone, with a Step 1 test |
| P14 | minor | `any-emoji-markers` misses an emoji after a slide number, the outline's own title form, so a scanned outline file passes clean | fixed: an optional slide number and a `flags` outline with one |
| P15 | minor | 76 signs named `document` and not `deck` are 81, 5 of them short | fixed: 81; the long files in bytes |

Refuted: the deck eval's regex failing on a script the session prints (with `Read` and `Skill` only, nothing makes
a file, so the outline is answered); P2's fix leaving a single-style user without a deck style (decided and said);
the short files' least, 5,925 bytes for a language with no signs (no budget rests on it); I6's wording (nothing names
`sheet`); the plain outline flagging plain text (no counted pattern fires); every other round 1 fix.

| # | Improvement | Answer |
|---|---|---|
| I9 | `flags: m` for the sheet grader too, as a sheet's answer opens with a tab heading | taken |
| I10 | The plain deck outline in `tests/test_office.py` whatever the layout signs, as Step 3 makes strong and usual signs apply to decks | taken |

### Approval

Approved on the maintainer's standing word (take the recommended improvements, answer owner calls with the
recommended option): Round 2 found no blocker or major, Q1 has its answer, and the plan names its tests and docs and
ends each step with `review-code` through `finish-work`.
