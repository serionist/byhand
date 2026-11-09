---
subject: "Decks and sheets step 4, the skills tried in real sessions"
base: main (f3ba1b4)
head: 66-skills
date: 2026-11-09
round: 1
tier: by hand (Claude Code 2.1.319, Opus 5.5, Windows 11), headless sessions; the maintainer's own session still to come
verdict: clean
---

# Step 4: decks and sheets in real sessions

Cases, counts and verdicts only: no draft beyond the invented requests' slide titles, no sample and no style is
recorded here (AGENTS.md, Never). Every text is invented.

## The eval suite

`claude plugin eval plugin --ablation none --threshold 1.0 -j 6`, Claude Code 2.1.319, Opus 5.5, three runs a case,
every text invented and pasted. One run of the whole suite on this branch's skills: 63 cases, 189 runs, 711 seconds,
about $27.10. A run loads only the plugin and allows only `Read` and `Skill`, so nothing makes a file.

| Bar (decks and sheets plan, Tests) | Cases | Result |
|---|---|---|
| `write` starts on 6 of 6 deck and sheet requests, never `check`, and answers the outline (`^## 1\.`) or the tables (`^\|`); the en ones read `any/any.layout.md` | a deck in en, hu, de and ja; a sheet in en and fr | 6 of 6, every run, every grader |
| `write` starts on at most 1 of the 4 code cases, in one run | a `python-pptx` script from a CSV, an `openpyxl` builder, a bug in a deck-building function, a CSV parser | 0 of 4 |
| a pasted outline asked "does this deck read as AI-written?" starts `check`, not `write` | `check-en-deck`, also graded on naming `any-label-above-title` or `any-takeaway-bar` | passed, every run |

The 52 cases from the bootstrap's Step 7 pass every run too, `write-en-slide-text` among them, now a `deck`.

## By hand, beside Anthropic's document skills

`claude -p` with `--plugin-dir plugin`, in an empty folder, `acceptEdits` and Bash allowed, the maintainer's usual
plugins and claude.ai's synced skills loaded: `anthropic-skills:pptx`, `xlsx`, `docx` and `docs`, which are the
`document-skills` plugin's skills as claude.ai syncs them. The `document-skills` plugin itself is not installed here.

| Request | `write` | Before the maker | The maker | The file's titles or headers |
|---|---|---|---|---|
| a PowerPoint deck, en, office move | started | yes | `pptx` (pptxgenjs) | the outline's, word for word, 3 slides |
| a presentation as a file, hu, summer rota | started | yes | `pptx` (pptxgenjs) | the outline's, 4 slides |
| slides for the board, en, support figures | started | yes | `pptx` (pptxgenjs) | the outline's, 4 slides; its two charts are the two the brackets named, with the user's numbers |
| a spreadsheet, en, team offsite | started | yes | `xlsx` (openpyxl) | `write`'s, with no outline shown: the answer described the tabs; every cell but the venue's 2,400 left empty |
| an Excel file, de, holiday planning | started | no maker skill: a script of its own (openpyxl) | its own script | `write`'s, shown as tables; the Bavarian holiday dates the user asked for came from memory and the answer says to check them |

Bar: `write` starts on all 5 (5 of 5); before the skill that makes the file on 4 (4 of the 4 that used one, the fifth
used none); each file's titles and headers are `write`'s (5 of 5).

Slides holding an element the outline doesn't name, over the 11 slides made: no picture, no icon, no chart and no
text the outline didn't give. The makers added what is look: a slide number on 8 slides and plain shapes behind text
(cards, a bar) on 6. Each answer also printed the outline it built from, with a note for each guess (a year, which
quarter "up from 1,050" meant).

## By hand, `check` and `learn` on files

Same sessions, Write and Edit refused, so nothing was saved.

| Try | What ran | Result |
|---|---|---|
| `check` on a deck's PDF (3 invented generated-looking slides) | `check`; Read on the PDF; `check.md` and `check.layout.md` for `any` and `en`; no scan, as the skill says | `any-takeaway-bar` and `any-label-above-title` on every slide, two usual prose signs, the weak ones named as near misses; kind `deck` |
| `check` on a sheet's CSV | `check`; the `scan` agent with `scan.md` and `scan.layout.md` for `any` and `en` | the patterns hit nothing; read for every sign: `any-invented-figures` in a cluster of four phrases; kind `sheet` |
| `check` on a `.pptx` | `check`, then `pptx`, whose Python pulled the slides' text into a `.txt`; then the `scan` agent on that file | as for the PDF, with line numbers from the text; it also named the speaker notes repeated on every slide |
| `learn` from two invented plain deck PDFs | `learn`; `check`'s steps on each PDF, read for every sign | both kept as the user's; a deck style shown with slides' text as excerpts, `Default for` offered as `deck`, nothing written |

## By hand, with no maker

`--setting-sources project,local`, which loads no installed plugin and no synced skill: the session's skills were
byhand's and Claude Code's own, with Bash and Write. `claude plugin eval` with Bash granted was tried first and
refused on this machine (a PATH folder it could not examine for credential helpers).

| Request | `write` | What the session did | The file's words |
|---|---|---|---|
| a PowerPoint deck, en, office move | started | wrote a `python-pptx` script of its own and ran it | the outline's, 5 slides, each title and line as drafted; the outline itself ends on a "Questions?" slide |
| a presentation as a file, de, travel policy | started | the same | the outline's, 4 slides |

## What a deck reads

The largest read per seed language, across model families, in bytes, from `byhand.render` on this branch's
catalogue. A deck's draft reads the short and the layout files; its check the `check.md` and `check.layout.md` files;
its scan, run by the agent, the `scan.md` and `scan.layout.md` ones.

| Language | Draft | of which layout | Check | Scan |
|---|---|---|---|---|
| en | 13,172 | 2,067 | 14,589 | 8,566 |
| zh | 15,075 | 2,719 | 15,565 | 5,535 |
| zh-Hant | 16,050 | 2,719 | 16,530 | 5,993 |
| de | 13,281 | 5,195 | 13,777 | 6,985 |
| fr | 12,920 | 5,287 | 15,143 | 6,677 |
| hu | 13,647 | 2,783 | 13,967 | 3,722 |
| ko | 14,280 | 2,849 | 15,173 | 4,356 |
| ja | 16,816 | 6,913 | 18,245 | 6,275 |
| ru | 14,193 | 4,473 | 15,330 | 7,619 |

## Not tried

- **The maintainer's session:** a deck style learned from their own decks, two decks read in English and Hungarian,
  and their makers (claude.ai's synced skills, a tool the system prompt puts first) counted apart. Theirs to run.
- **The `document-skills` plugin as installed,** rather than its skills synced from claude.ai; and an `.xlsx` read
  through `xlsx` for `check`.
- **Interactive sessions, permission prompts, macOS, Linux and WSL.**
- **A maker that keeps the words in sessions other than these;** the plan's "What none can show".
