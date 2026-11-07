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

## What a draft loads

`byhand render` writes `plugin/signs/<language>/<family>.signs.md`, and `<family>.layout.md` for the signs only decks and
sheets need. `<language>` or `<family>` is `any` for the signs of every language or model. A draft reads at most four
prose files, six for a script variant such as `zh-Hant`, and a deck or a sheet adds their layout files.

The budgets, in `src/byhand/render.py`; over any of them the render fails:

| What | Budget |
|---|---|
| the prose files one draft reads, together (`DRAFT_BUDGET`) | 16 KB |
| the layout files a deck or a sheet adds, together (`LAYOUT_BUDGET`) | 16 KB |
| a text of unknown author: `any` and one language, in every family, prose and layout each (`UNKNOWN_BUDGET`) | 48 KB |
| any one file (`MAX_LINES`) | under 2,000 lines, Claude Code's `Read` default |
