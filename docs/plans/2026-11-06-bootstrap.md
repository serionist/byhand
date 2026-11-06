---
title: Bootstrap byhand, a plugin that writes in the user's own voice without the signs of AI writing
issue: "#1"
status: draft
approved_by:
approved_at:
---

# Bootstrap byhand, a plugin that writes in the user's own voice without the signs of AI writing

## Goal

A user asks Claude Code for a mail in Hungarian, a Slack reply in English or a deck outline in German, and byhand's
`write` skill starts without being asked. It loads only what that draft needs: the signs for its language and for the
model writing it, the signs that hold in every language, and the user's style for that kind of writing. The draft
reads as the user wrote it. `/byhand:learn` learns a style from material the user points at; `/byhand:check` finds
the signs in a text the user already has.

Why: the signs of AI writing cost the user's credibility with the people they write to, and a list of banned words
alone makes the text worse (AGENTS.md, Traps). byhand leans on structure and on the user's own voice.

This plan spans the first release and the milestones after it. In scope here, release `0.1.0`: the catalogue and its
seed, the `write`, `check`, `learn` and `styles` skills, the package's CLI, the maintainers' `propose-signs` skill,
publishing to PyPI. Out of scope here, each a milestone and a plan of its own: the scheduled refresh (`0.2.0`), more
languages (`0.3.0`), decks and sheets at a human skill level (`0.4.0`), learning from the user's edits (`0.5.0`).

## Design

### The maintainer's calls, 2026-11-06

Taken in this session before the plan was written; each holds unless the maintainer changes it.

- The name `byhand`; a public repo; the house harness (`AGENTS.md`).
- Mostly structural signs, not word lists. Each sign is scoped by language and by model (a family and a version
  range), or `any`.
- The 100 most spoken languages in the schema. The seed has signs of its own for en, zh, de, fr, hu, ko, ja and ru;
  every language gets the `any` signs.
- Light: a draft loads its language's and its model's signs, the `any` ones and one style, never the catalogue.
- A model released after the catalogue works out of the box: its family's newest signs and the `any` ones.
- Styles: learned from the user's material, under a name, for kinds of writing (message, email, document, deck,
  sheet), with a default per kind. Per user, and a project can override. Editable Markdown. 3 to 5 short excerpts of
  the user's own text, kept locally, saved only after learn asks. Learning from edits is a later milestone.
- Learn never learns from AI-written text: it asks for each sample whether the user wrote it and wants to sound like
  it; it runs each through the catalogue first; a learned rule that matches a sign is kept only on the user's yes.
- The refresh: CI fetches and diffs the sources and opens issues, with no model and no key; a maintainers' skill
  drafts the sign changes as a PR a person merges.
- `0.1.0` holds the catalogue, write and learn; the refresh is `0.2.0`.
- MIT for everything; a sign is our own words and a citation, never a source's text.

### The catalogue

TOML in the package, `src/byhand/catalogue/`, read with the standard library's `tomllib`:

| File | What |
|---|---|
| `languages.toml` | the 100 most spoken languages: BCP 47 code, English and native name, rank; the list's source and its date |
| `models.toml` | model families (`claude`, `gpt`, `gemini`, `grok`, `llama`, `deepseek`, `qwen`, ...), each with the id patterns that name it and how a version is read from an id (`claude-opus-5-5` is claude 5.5, `gpt-5.6-sol` is gpt 5.6) |
| `sources.toml` | every source a sign cites: id, URL, kind (wiki, repo, paper, dataset, vendor, review), languages, licence, how it is read, how often it is due (for `0.2.0`) |
| `signs/<language>.toml` | the signs of one language, `signs/any.toml` those of every language |

A sign:

| Key | What |
|---|---|
| `id` | `<language>-<slug>`, such as `en-delve` or `any-rule-of-three`; never reused, a retired sign keeps it |
| `category` | `word`, `phrase`, `structure`, `formatting`, `layout` or `artefact` (`oaicite`, `utm_source=chatgpt.com`) |
| `kinds` | the kinds of writing it applies to, or `any` |
| `models` | `any`, or a list of `{ family, from, to }`; `to` left out is open, so a newer version is covered |
| `what`, `instead` | what the text does, and what a person writes instead, in our own words |
| `strength` | `strong`, `usual` or `weak`: weak where people do it too (arXiv 2409.01754), so it is flagged only in a cluster |
| `check` | optional: a regular expression `byhand check` runs; a structural sign without one is for the model's own read |
| `flags`, `passes` | an invented text the sign flags and a human one it passes; both run as a test |
| `sources` | `{ source, where, seen }`: the source id, the section, revision or commit, the date |
| `since`, `until` | when the sign holds; `until` retires it (em dashes in ChatGPT's text after 2026, per the research) |

The 100 languages come from Wikipedia's "List of languages by total number of speakers" as it stood on the day step 2
writes it, cited by revision. Language codes are BCP 47's base subtag (`zh`, `hu`), with a script only where it
changes the signs (`zh-Hant`); a brief for `zh-Hant` falls back to `zh`.

### Light by design: what a draft loads

The `write` skill pre-approves only `Read`, `Glob` and `Grep` (AGENTS.md, Never), so it runs no command: a command
would ask the user on every draft. It reads files instead. `byhand render` writes the catalogue as Markdown into the
plugin, one file per language and model family, signs sorted strongest first:

```
plugin/skills/write/signs/any/any.md        every language, every model
plugin/skills/write/signs/any/claude.md     every language, Claude's own
plugin/skills/write/signs/hu/any.md         Hungarian, every model
plugin/skills/write/signs/hu/claude.md      Hungarian, Claude's own, when there are any
```

The skill reads at most four: `any/any.md`, `any/<family>.md`, `<language>/any.md`, `<language>/<family>.md`, where
they exist. A version range is printed beside each model sign; the model applies the signs of its version, or of the
newest range below it. The family comes from the model's own id, which Claude Code puts in its system prompt; no id,
or a family the catalogue lacks: the two `any.md` files alone. A test caps each file's size, and the gate holds the
rendered files equal to the catalogue (Steps 3).

### Styles

A style is Markdown with frontmatter: `name`, `kinds`, `language`, `register`, `default_for` (kinds), `updated`; the
body holds its rules in prose and bullets, then `## Excerpts`, 3 to 5 short ones. robotics-personal's
`90-reference/soma-writing-style.md` is the model and the first real test, never committed here.

- **Where:** the user's in `~/.byhand/styles/<name>.md`; a project's in `<project>/.byhand/styles/<name>.md`, which
  wins over a user style of the same name and whose default wins for its kinds. Not `${CLAUDE_PLUGIN_DATA}`: Claude
  Code deletes it when the plugin is uninstalled, and a user's styles outlive the plugin.
- **A project's styles hold real writing:** learn adds `.byhand/` to the project's `.gitignore` when it writes one
  there, and says so; this repo's gate refuses a tracked file under `.byhand/`.
- **Which one a draft uses:** a style the user names; else the project's default for the kind, else the user's; else,
  with several for the kind, the skill asks; with none, the catalogue alone.

### The plugin's skills

| Skill | What | Runs |
|---|---|---|
| `write` | starts by itself on a request to write, draft, reply to or rewrite a message, mail, document, post or slide text, in any language; picks the kind, language and style, reads the signs, drafts, reads its draft against them, rewrites what it finds | nothing; reads only |
| `check` | finds the signs in a text or a file the user gives, each with its line, the sign and what a person writes instead | `byhand check` |
| `learn` | learns a style from material the user points at: asks the name, kinds, default and whether each sample is theirs and liked; runs `byhand check` on each sample and leaves out one that reads as AI-written unless the user says it is theirs; drafts the style, shows it, saves it on a yes | `byhand check`, `byhand styles save` |
| `styles` | lists the styles, shows one, sets or clears a default, removes one | `byhand styles` |

The commands run as `uv run --with byhand==<version> byhand ...`, one pinned version as in simready-forge; each asks
the user, as every command does.

**Starting by itself** rests on `write`'s description: Claude Code matches requests against it, with no documented
guarantee (Claude Code's skills docs, Troubleshooting). Step 7 measures it. Below the bar there, a `SessionStart` hook
that adds one line of context is the fallback, a plan of its own: plugin hooks are a key the gate refuses today.

### The CLI

`byhand validate` (the catalogue: schema, unique ids, each check against its `flags` and `passes`, every source and
language known), `byhand render` (the plugin's sign files), `byhand check <file|-> --lang <code> [--model <id>]
[--kind <kind>]` (the mechanical signs, with line, id and `instead`; exit 1 on a strong one), `byhand styles
list|show|default|save|remove|path`, `byhand models <id>` (the family and version the catalogue reads from an id).
Standard library only for `0.1.0`.

### Seeding the catalogue: `propose-signs`

A maintainers' skill in `.claude/skills/propose-signs/`: given a source id from `sources.toml`, it reads the source
as data, drafts signs in our own words with their citations, `flags` and `passes`, runs `byhand validate`, and opens a
PR. The seed for `any` and the eight languages comes from it, from the sources the research ranked first
(`.local/research/sources.md`, kept with this plan's PR as `docs/research/2026-11-06-sources.md`). Hungarian has thin
sources (one short wiki essay): the maintainer's review as a native speaker is a source of kind `review`, cited by its
issue. The same skill drafts the refresh's changes in `0.2.0`.

### Alternatives considered

- **One English list, as blader/humanizer:** no languages, no models, no styles; the reason byhand exists.
- **The CLI on every draft:** a permission prompt per mail, and uv's start-up; the rendered files avoid both.
- **A model in CI for the refresh:** a key and tokens on every run, and fetched text read by a model unattended.
- **Styles in `${CLAUDE_PLUGIN_DATA}`:** gone on uninstall.
- **YAML for the catalogue:** friendlier, but a dependency; TOML is in the standard library and strict.

## Compatibility

New repo, nothing to migrate. The one-way doors it creates, from `0.1.0`: the names (`byhand` for the repo, the PyPI
distribution, the CLI, the plugin and the import); the skills' names (`write`, `check`, `learn`, `styles`); a sign's
id, the catalogue's schema, the language and model codes; the style's format and its folders (`~/.byhand/styles/`,
`.byhand/styles/`). AGENTS.md names them in Step 2's PR.

The harness changes, each stricter, none looser: the gate's plugin check takes the rendered files under
`plugin/skills/write/signs/` and fails when they differ from `byhand render`'s; it refuses a tracked file under
`.byhand/`; `byhand validate` joins gate quick.

## Steps

Each step is a PR on its own branch from `main`, after this plan's PR; this plan's progress log gets a row per merge.

1. **The harness and this plan.** This branch. Proven by `uv run tools/gate.py full` and CI.
2. **The catalogue's schema.** `languages.toml`, `models.toml`, an empty `sources.toml` and `signs/`, the loader,
   `byhand validate`, `byhand models`. Proven by `tests/test_catalogue.py` (a bad sign of each kind fails, a good one
   passes) and `tests/test_models.py` (`claude-opus-5-5`, `claude-opus-9-1`, `gpt-5.6-sol`, `gpt-7`, an unknown
   family, an empty id).
3. **Render and its gate check.** `byhand render`; the gate's plugin check extended to the rendered files and to
   `.byhand/`. Proven by `tests/test_render.py` (files per language and family, size caps, a newer version's
   fallback) and `tests/test_gate.py` (a stale render fails, a tracked `.byhand/` file fails).
4. **`propose-signs` and the seed.** The skill, `sources.toml` from the research, then the signs: `any` first, then
   en, then one PR per language. Proven by `byhand validate` in the gate, each sign's `flags` and `passes`.
5. **`check`.** `byhand check` and the `check` skill. Proven by `tests/test_check.py` (findings in en, hu, zh and
   ja text, Markdown and code left alone, a quoted reply left alone, exit codes).
6. **Styles, `learn` and `write`.** The style format, `byhand styles`, the three skills. Proven by
   `tests/test_styles.py` (parse, defaults per kind, the project over the user, a style without frontmatter refused,
   `.gitignore` written) and the plugin check.
7. **Tried in real sessions.** `tools/triggers.py` runs `claude -p` on 20 writing requests (en, hu, de, zh, fr; mail,
   Slack, document, deck) and 10 others, and reads whether `write` loaded. The bar: 18 of 20, and 1 of 10 at most.
   Then the maintainer's own style learned from the material behind `soma-writing-style.md`, and drafts read by them
   in English and Hungarian. Recorded in `docs/reviews/`.
8. **Release `0.1.0`.** `release.yml` and `docs/releasing.md` from simready-forge, PyPI's trusted publishing,
   CHANGELOG dated, the plugin's pin. Proven by CI's package job and `uvx byhand==0.1.0 byhand validate`.

GitHub milestones: `0.1.0 Write in your own voice` (Steps 2 to 8), `0.2.0 Refresh`, `0.3.0 More languages`,
`0.4.0 Decks and sheets`, `0.5.0 Learn from edits`; an issue per step, opened when this plan is approved.

## Tests

- **Unit (CI):** the catalogue, models, render, check, styles, the gate; invented text in every seeded language.
- **By hand:** `tools/triggers.py` and the drafts read in real sessions (Step 7), on the Claude Code version and models
  of the day, recorded with what they could not show.
- **What none can show:** whether a reader takes a draft as the user's. The maintainer's read in Step 7 is the only
  evidence, for two languages; the others rest on their sources and native contributors.

## Docs

`README.md` and `plugin/README.md` (the skills, install), a new `docs/USAGE.md` (skills, the CLI, the style format,
the catalogue's schema, how to add a sign), `CONTRIBUTING.md` (adding a sign through `propose-signs` or the form),
`CHANGELOG.md`, `AGENTS.md` (the catalogue's row, the one-way doors, the commands), `docs/research/` for the research
this plan rests on.

## Risks

| Risk | Answer |
|---|---|
| `write` doesn't start by itself often enough | Measured in Step 7; the hook is the fallback, its own plan. Accepted |
| A sign flags plain human writing | `strength`, `passes` tested, weak signs only in clusters. Accepted, watched through issues |
| A source's licence: Wikipedia's CC BY-SA, lieflat's CC BY-NC, vendors' all rights reserved | Our words and a citation; non-commercial and vendor sources as facts only; review lens `catalogue-contract`. Resolved by rule |
| No model id in the session, or a subagent on another model | The two `any.md` files alone; the skill names the model that writes the draft. Accepted |
| Thin sources for most languages, Hungarian included | The `any` signs carry them; native review as a source; `0.3.0` measures excess words from datasets. Accepted |
| Rendered files grow with the catalogue | Size caps tested per file; a file over its cap fails the build. Resolved |
| A user's real writing in a project's `.byhand/` gets committed | learn writes the `.gitignore` line and says so. Accepted: a user can still force-add it |
| The PyPI name is free today and open to a squatter until `0.1.0` (omniverse-mcp's R9) | Reserve it with Step 2's merge. Open |

## Plan review

None yet.
