# Using byhand

Not released yet. The skills come with `0.1.0`; this page grows with them.

byhand is two sets of Markdown files, signs and styles, and the skills that read them.

## For contributors: the commands

Users never run these. They build and check the catalogue in this repo.

| Command | What |
|---|---|
| `byhand validate` | check the catalogue: its schema, every sign's examples, its sources; each problem, then a count; exit 1 on any |
| `byhand render` | write the catalogue as the plugin's sign files |
| `byhand render --check` | write nothing; exit 1 when the files differ from the catalogue |

## What a skill reads

`byhand render` writes two sets under `plugin/signs/<language>/`, where `<language>` or `<family>` is `any` for the
signs of every language or model, and only languages that have signs get a folder:

| File | Holds | Read by |
|---|---|---|
| `<family>.short.md` | the signs a mail or a message reads: every kind's, and those naming `email` or `message` | `write`, every draft |
| `<family>.long.md` | the signs only a post or a document reads | `write`, a post or a document |
| `<family>.layout.md` | the signs only a deck or a sheet reads | decks and sheets, `0.4.0` |
| `check.md` | every prose sign of every family, with the pattern Grep runs where it has one | `check`, and its `scan` agent |

`write`'s files hold no regex: each term prints as plain words, one per alternative, the shortest text it matches,
with "…" for a run of letters the word needs (`…ként szolgál`). A draft reads at most four short files, six for a
script variant such as `zh-Hant`, and a post or a document as many long ones again.

The budgets, `Budgets` in `src/byhand/render.py`, set from the catalogue of 8 Nov 2026 with a margin and only ever
lowered; over any of them the render fails:

| What | Budget |
|---|---|
| the short files a mail or a message reads, together (`mail`) | 14 KB |
| the short and long files a post or a document reads, together (`document`) | 16 KB |
| the layout files a deck or a sheet adds, together (`layout`) | 16 KB |
| the check files one check reads: `any`, a variant's base language and the language (`check`) | 32 KB |
| any one file (`MAX_LINES`) | under 2,000 lines, Claude Code's `Read` default |
