# Using byhand

byhand is two sets of Markdown files, signs and styles, and the skills that read them.

## For contributors: the commands

Users never run these. They build and check the catalogue in this repo.

| Command | What |
|---|---|
| `byhand validate` | check the catalogue: its schema, every sign's examples, its sources; each problem, then a count; exit 1 on any |
| `byhand render` | write the catalogue as the plugin's sign files |
| `byhand render --check` | write nothing; exit 1 when the files differ from the catalogue |
| `byhand refresh --out <dir>` | read each source whose `due` has come round since `read_at` (a day, a week, 30 or 90 days); write `<dir>/<id>.md`, an issue body of ids and links, for each changed one; exit 1 if any source couldn't be read. It reads `GITHUB_TOKEN`, if set, and sends it to api.github.com only: without one, GitHub allows 60 calls an hour. `refresh.yml` runs it daily and opens the issues |

## What a skill reads

`byhand render` writes these files under `plugin/signs/<language>/`, where `<language>` or `<family>` is `any` for the
signs of every language or model, and only languages that have signs, or forms of the shared ones, get a folder; one
with forms alone (`id`) has a `scan.md` and no `check.md`:

| File | Holds | Read by |
|---|---|---|
| `<family>.short.md` | the signs a mail or a message reads: every kind's, and those naming `email` or `message` | `write`, every draft |
| `<family>.long.md` | the signs only a post or a document reads | `write`, a post or a document |
| `<family>.layout.md` | the signs only a deck or a sheet reads | decks and sheets, `0.4.0` |
| `check.md` | every prose sign of every family, with no pattern | `check` |
| `scan.md` | the pattern Grep runs for each sign that has one in this language: a language's own signs, and the shared signs' forms under its code (`any/scan.md`: those every language runs) | `check`'s `scan` agent |

`write`'s files hold no regex: each term prints as plain words, one per alternative, the shortest text it matches,
with "…" for a run of letters the word needs (`…ként szolgál`). A draft reads at most four short files, six for a
script variant such as `zh-Hant`, and a post or a document as many long ones again.

The budgets, `Budgets` in `src/byhand/render.py`, set from the catalogue of 8 Nov 2026 with a margin and only ever
lowered (`check` and `scan` on 9 Nov, the largest read plus at least 512 bytes, rounded up to a whole KB); over any
of them the render fails:

| What | Budget |
|---|---|
| the short files a mail or a message reads, together (`mail`) | 14 KB |
| the short and long files a post or a document reads, together (`document`) | 16 KB |
| the layout files a deck or a sheet adds, together (`layout`) | 16 KB |
| the check files one check reads: `any`, a variant's base language and the language (`check`) | 16 KB |
| the scan files `scan` reads for one check, from the same languages (`scan`) | 9 KB |
| any one file (`MAX_LINES`) | under 2,000 lines, Claude Code's `Read` default |
