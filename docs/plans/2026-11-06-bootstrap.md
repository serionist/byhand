---
title: Bootstrap byhand, a plugin that writes in the user's own voice without the signs of AI writing
issue: "#1"
status: approved
approved_by: serionist
approved_at: 2026-11-06
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
- Styles: learned from the user's material, under a name, for kinds of writing (message, email, post, document,
  deck, sheet), with a default per kind and language (Round 1, Q1 and Q2). Per user, and a project can override. Editable Markdown. 3 to 5 short excerpts of
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
| `sources.toml` | every source a sign cites: id, URL, kind (wiki, repo, paper, dataset, vendor, review), languages, licence, how often it is due (for `0.2.0`); `feed`, how a script reads it (`{ api = "mediawiki", site, title }`, `{ api = "github", repo, paths }`, `{ api = "arxiv", query }`, `{ api = "hf", dataset }`, or `{ api = "none" }` for a page a person reads); `read_at`, the revision or commit last read and its date, written by `propose-signs` for every source it reads, one that yielded no sign included |
| `signs/<language>.toml` | the signs of one language, `signs/any.toml` those of every language |

A sign:

| Key | What |
|---|---|
| `id` | `<language>-<slug>`, such as `en-delve` or `any-rule-of-three`; never reused, a retired sign keeps it |
| `category` | `word`, `phrase`, `structure`, `formatting`, `layout` or `artefact` (`oaicite`, `utm_source=chatgpt.com`) |
| `kinds` | the kinds of writing it applies to, or `any` |
| `models` | `any`, or a list of `{ family, from, to }`; `to` left out is open, so a newer version is covered |
| `what`, `instead` | what the text does, and what a person writes instead, in our own words |
| `terms` | for a `word` or `phrase` sign: a list of `{ term, instead }`, so an era list (Wikipedia's GPT-4-era words) or a computed excess-word list is one sign with one id and one model scope; its `check` is built from the terms. A term is a regular-expression fragment, a stem and its endings where the language inflects (`kulcsfontosság\w*`, `ключев\w+`), or the sign carries its own `check`; text and terms are compared in Unicode NFC |
| `strength` | `strong`, `usual` or `weak`: weak where people do it too (arXiv 2409.01754), so it is flagged only in a cluster: three weak signs or more in one paragraph, a constant `check` uses and the rendered files' header prints |
| `check` | optional: a regular expression `byhand check` runs; a structural sign without one is for the model's own read |
| `flags`, `passes` | an invented text the sign flags and a human one it passes. With a `check`, both run in CI. Without one, `validate` holds both present and different, and Step 7's suite runs `check` on a sample of them, the `passes` texts above all; CI can't prove a sign without a `check` |
| `sources` | `{ source, where, seen }`: the source id, the section, revision or commit, the date |
| `since`, `until` | dates, for a sign whose `models` is `any`: when it holds, and `until` retires it. A model-scoped sign retires by its range's `to` (em dashes in ChatGPT's text after 5.x, per the research) |

The 100 languages come from Wikipedia's "List of languages by total number of speakers" as it stood on the day step 2
writes it, cited by revision. Language codes are BCP 47's base subtag (`zh`, `hu`), with a script only where it
changes the signs (`zh-Hant`); a `zh-Hant` draft reads its own files and `zh`'s, six at most.

### Light by design: what a draft loads

The `write` skill pre-approves only `Read`, `Glob` and `Grep` (AGENTS.md, Never), so it runs no command: a command
would ask the user on every draft. It reads files instead. `byhand render` writes the catalogue as Markdown into one
folder of the plugin that `write`, `check` and `learn` all read, through `${CLAUDE_PLUGIN_ROOT}/signs/`: one file per
language and model family, signs sorted strongest first, and the layout signs of decks and sheets (category `layout`,
or `kinds` of only `deck` or `sheet`) in a file of their own:

```
plugin/signs/any/any.md             every language, every model
plugin/signs/any/claude.md          every language, Claude's own
plugin/signs/hu/any.md              Hungarian, every model
plugin/signs/hu/claude.md           Hungarian, Claude's own, when there are any
plugin/signs/any/any.layout.md      decks and sheets, every language, every model
```

A prose draft reads at most four: `any/any.md`, `any/<family>.md`, `<language>/any.md`, `<language>/<family>.md`,
where they exist, six for a `zh-Hant` draft (its own and `zh`'s); a deck or a sheet adds their `.layout.md` files,
four more at most, six for `zh-Hant`. A skill's `allowed-tools` grant
lasts only the turn that invokes it (Claude Code's skills docs, Pre-approve tools for a skill), and the files sit
outside the user's working directory, so `write`'s SKILL.md says to invoke `write` again for each new draft, and to
read the files again after a compaction: a second mail in the same session then asks nothing either.

A version range is printed beside each model sign, and the model applies each sign whose range holds its version. A
range with no `to` holds every later version, so a model newer than the catalogue gets its family's current signs; a
closed range never applies past its `to`. The family comes from the model's own id, which Claude Code puts in its
system prompt; no id, or a family the catalogue lacks: the two `any.md` files alone.

A text the user already has (`check`, learn's screen) has no known author: with no model named, both read every family
file of the text's language and of `any`, still one language, and `byhand check` without `--model` applies every
family's signs and names the family on each finding.

The budget, one constant that `render`'s test and `docs/USAGE.md` name: the prose files any one draft reads, six for
`zh-Hant`, come to 16 KB at most together, about 4,000 tokens in English, and no file reaches 2,000 lines, Claude
Code's `Read` default. A second constant holds the read of a text of unknown author, `any` and one language in every
family: 48 KB at most, tested the same way. The gate
holds the rendered files equal to the catalogue (Step 3).

### Styles

A style is Markdown with frontmatter: `name`, `kinds`, `language`, `register`, `default_for` (kinds, a default in its
own language), `keeps` (the ids of signs the user chose to keep), `updated`; the
body holds its rules in prose and bullets, then `## Corrections`, then `## Excerpts`, 3 to 5 short ones.
`## Corrections` is a dated running list of rules the user gave, each with its date and the kind of text it came from;
`write` reads them as rules that beat the body. In `0.1.0` the user writes them by hand, or says "remember this";
`0.5.0` learns them from edits into the same section. Readers keep frontmatter keys and sections they don't know, so a
later release can add one without breaking a style. robotics-personal's
`90-reference/soma-writing-style.md` is the model and the first real test, never committed here.

- **Where:** the user's in `~/.byhand/styles/<name>.md`; a project's in `<project>/.byhand/styles/<name>.md`, which
  wins over a user style of the same name and whose default wins for its kinds. Not `${CLAUDE_PLUGIN_DATA}`: Claude
  Code deletes it when the plugin is uninstalled, and a user's styles outlive the plugin.
- **A project's styles hold real writing:** learn adds `.byhand/` to the project's `.gitignore` when it writes one
  there, and says so; this repo's gate refuses a tracked file under `.byhand/`.
- **The draft's language:** the one the user names; else that of the text being replied to; else the request's.
- **Which style a draft uses:** a style the user names; else, among the styles in the draft's language, the project's
  default for the kind, then the user's; else, with several, the skill asks; with none in that language, the
  catalogue alone, and the skill says so. A user can have a Hungarian default and an English one for `message`.
- **The style beats a sign:** a rule the user kept on learn's question, and every correction, wins over the catalogue.
  `write` and `check` skip the signs a style `keeps` for drafts in that style, so a review mail keeps the bold headings
  its user asked for.

### The plugin's skills

| Skill | What | Runs |
|---|---|---|
| `write` | starts by itself on a request to write, draft, reply to or rewrite a message, mail, post, document or slide text, in any language; never on code-adjacent writing (a docstring, a commit message, a README, a PR description, a code comment); picks the kind, language and style, reads the signs, drafts, reads its draft against them, rewrites what it finds | nothing; reads only |
| `check` | starts on a question whether a text reads as AI-written; finds the signs in a text or a file the user gives, each with its line, the sign and what a person writes instead: the mechanical ones through `byhand check`, the structural ones by reading the text against the rendered signs. A text that is a draft in one of the user's styles is checked with that style: `--style`, and its corrections honoured in the model's read, since a correction is prose, not an id. A request to rewrite such a text is `write`'s | `byhand check` |
| `learn` | learns a style from material the user points at: asks the name, kinds, default and whether each sample is theirs and liked; checks each sample as `check` does, mechanical and structural, and leaves out one that reads as AI-written unless the user says it is theirs; drafts the style, shows it, saves it on a yes | `byhand check`, `byhand styles save` |
| `styles` | lists the styles, shows one, sets or clears a default, removes one | `byhand styles` |

The commands run as `uv run --no-project --with byhand==<version> byhand ...`, one pinned version as in
simready-forge; each asks the user, as every command does. `--no-project` keeps uv out of the user's own project: in a
folder with a `pyproject.toml`, `uv run --with` creates its `.venv`, writes its `uv.lock` and installs its
dependencies (Round 1, P4, reproduced with uv 0.12.1).

**Starting by itself** rests on `write`'s description: Claude Code matches requests against it, with no documented
guarantee (Claude Code's skills docs, Troubleshooting), and when the skill listing overflows its budget Claude Code
drops the descriptions of the skills used least, a new `write` first. Step 7 measures both: in a clean eval, and in the
maintainer's own crowded session. Below the bar in either, a `SessionStart` hook that adds one line of context is the
fallback, a plan of its own that comes before the release step (Round 1, Q4): plugin hooks are a key the gate refuses
today. `plugin/README.md` says how a user keeps the description in a crowded listing (`skillListingBudgetFraction`).

### The CLI

`byhand validate` (the catalogue: schema, unique ids, each check against its `flags` and `passes`, every source and
language known, each source's `feed` and `read_at`, and an `any` sign refused when its sources together cover fewer
than two languages), `byhand render` (the plugin's sign files), `byhand check <file|-> --lang <code> [--model <id>]
[--kind <kind>] [--style <name>]` (the mechanical signs, with line, id and `instead`; exit 1 on a strong one;
`--style` drops the signs that style `keeps`), `byhand styles
list|show|default|save|remove|path`, `byhand models <id>` (the family and version the catalogue reads from an id).
Standard library only for `0.1.0`. The CLI reads and writes UTF-8 whatever the platform: standard input from
`sys.stdin.buffer`, standard output reconfigured, files opened with `encoding="utf-8"`, as `tools/gate.py` does; on
Windows a pipe is cp1252 otherwise, and Hungarian or Chinese text crashes it (Round 1, P5, reproduced).
`byhand render --check` exits 1 when the rendered files differ, and the gate runs it as a tool after its `uv sync`,
so the gate itself stays standard library only and never imports the package.

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
id, the catalogue's schema, the language and model codes, the kinds (`message`, `email`, `post`, `document`, `deck`,
`sheet`; a later kind is added, never renamed); the style's format and its folders (`~/.byhand/styles/`,
`.byhand/styles/`). AGENTS.md names them in Step 2's PR.

The harness changes, each stricter, none looser: the gate's plugin check takes the rendered files under
`plugin/signs/` and fails when they differ from `byhand render`'s; it takes `plugin/evals/`'s `.md`, `.yaml` and a
case's `.jsonl` history, never a script, and skips `plugin/evals/results/`, which `.gitignore` lists, as every eval run
writes there; it refuses a tracked file under `.byhand/`; `byhand validate` joins gate quick.

## Steps

Each step is a PR on its own branch from `main`, after this plan's PR, and ends with `finish-work`: `uv run
tools/gate.py full`, `review-code` until clean, the PR. This plan's progress log gets a row per merge.

1. **The harness and this plan.** This branch. Proven by `uv run tools/gate.py full` and CI.
2. **The catalogue's schema.** `languages.toml`, `models.toml`, an empty `sources.toml` and `signs/`, the loader,
   `byhand validate`, `byhand models`. Proven by `tests/test_catalogue.py` (a bad sign of each kind fails, a good one
   passes) and `tests/test_models.py` (`claude-opus-5-5`, `claude-opus-9-1`, `gpt-5.6-sol`, `gpt-7`, dated and
   provider-prefixed ids such as `claude-sonnet-4-5-20250929`, `us.anthropic.claude-opus-4-6-v1:0` and
   `claude-opus-4-6@20250514`, an unknown family, an empty id).
3. **Render and its gate check.** `byhand render`; the gate's plugin check extended to `plugin/signs/`,
   `plugin/evals/` and `.byhand/`. Proven by `tests/test_render.py` (files per language and family, the layout
   files apart, the budget, a newer version inside an open range, none past a closed `to`) and `tests/test_gate.py`
   (a stale render fails, a tracked `.byhand/` file fails, an eval result folder is skipped).
4. **`propose-signs` and the seed.** The skill, `sources.toml` from the research, then the signs: `any` first, then
   en, then one PR per language. Proven by `byhand validate` in the gate, each sign's `flags` and `passes`.
5. **`check`.** `byhand check` and the `check` skill. Proven by `tests/test_check.py` (findings in en, hu, zh and
   ja text, an inflected hu and ru term, an NFD Hungarian text, a GPT-scoped sign found with no `--model`, Markdown
   and code left alone, a quoted reply left alone, exit codes) and a subprocess test that pipes zh and hu text through
   `byhand check -`, run on CI's Windows leg too.
6. **Styles, `learn` and `write`.** The style format, `byhand styles`, the three skills. Proven by
   `tests/test_styles.py` (parse, a default per kind and language with a hu and an en default for `message`, the
   project over the user, a sign a style `keeps` left out, unknown keys and sections kept, a style without frontmatter
   refused, `.gitignore` written), `tests/test_check.py`'s case of `--style` leaving out a kept sign, a subprocess
   test of `byhand styles save` with Hungarian text on stdin, and the plugin check. Tried by hand: `/byhand:check` run
   from inside a Python project leaves it untouched.
   - The tries by hand, here and in Step 7, run before `byhand==0.1.0` is on PyPI: they resolve the pin from a wheel
     of the clone, `uv build`, then `UV_FIND_LINKS=<clone>/dist` in the session's environment (`--refresh-package
     byhand` after a rebuild). The pin's text stays as it is, so no pin runs another package. `docs/USAGE.md` and
     finish-work's try step (through `write-skill`) say so.
7. **Tried in real sessions.**
   - A `claude plugin eval` suite in `plugin/evals/`, run with `--ablation none` and `--threshold 1.0`, three runs a
     case: 23 writing requests (en, hu, de, zh, fr, and one each in ja, ko and ru; mail, Slack, post, document, deck),
     each graded `tool_used: Skill` on `write`; 10 others graded `min: 0, max: 0`, code-adjacent writing among them
     (a docstring, a commit message, a README); 5 `check` cases graded `tool_used: Skill` on `check`, and 2 where
     `check` and `write` meet, graded on the skill each should start; a case with
     a history file of invented turns for a second draft in another language, graded `tool_order` (`write` invoked
     again before a `Read` whose input matches the second draft's language, `signs[\\/]hu[\\/]`, either separator); `check` run on a sample of the signs without a `check`, their `passes`
     texts above all. The bar: 21 of 23 writing requests, 1 of 10 others at most, 6 of the 7 `check` and boundary
     cases; a `passes` text a sign flags is a finding, fixed before Step 8.
   - By hand, on Windows at least: a session started outside the clone, two drafts in a row and one after `/compact`,
     counting permission prompts (none is the bar); the maintainer's own crowded session, with their usual plugins,
     10 writing requests, `write` starting on 9 at least; `~/.byhand/styles/` found without a command; the CLI's streams.
   - The maintainer's own style learned from the material behind `soma-writing-style.md`, and drafts read by them in
     English and Hungarian.
   - The record in `docs/reviews/` holds the cases, counts, versions, the OS and the maintainer's verdict per draft,
     never a draft, an excerpt or the style.
8. **Release `0.1.0`.** `release.yml` and `docs/releasing.md` from simready-forge, PyPI's trusted publishing,
   CHANGELOG dated, the version moved from `0.0.0` to `0.1.0` in `pyproject.toml`, `plugin.json` and every pin (the
   maintainer's call in the review of #9: an install before the release must not already read `0.1.0`), and the
   first upload to PyPI. Proven by CI's package job and `uvx --from byhand==0.1.0 byhand validate`.

If Step 7 falls below its bar, the `SessionStart` hook's plan comes before Step 8 (Round 1, Q4).

### Progress log

| Step | Issue | PR | State |
|---|---|---|---|
| 1. The harness and this plan | #1 | #9 | plan approved 2026-11-06 |
| 2. The catalogue's schema | #2 | #12 | merged 2026-11-07 |
| 3. Render and its gate check | #3 | #14 | |
| 4. `propose-signs` and the seed | #4 | | |
| 5. `check` | #5 | | |
| 6. Styles, `learn` and `write` | #6 | | |
| 7. Tried in real sessions | #7 | | |
| 8. Release `0.1.0` | #8 | | |

Decisions on the way:

- **Simple, and no command on a user's machine (the maintainer, 2026-11-07):** byhand is two sets of Markdown files,
  signs and styles, and the skills that read them. Install is `/plugin install`, with no uv, no Python and no PyPI.
  This replaces what the plan says of the CLI for users, and changes three steps:
  - Step 5: `check` reads a text against the rendered signs, and uses `Grep` on a file for their terms and checks,
    which `render` prints. `byhand check` isn't built.
  - Step 6: a style is a Markdown file, listed with `Glob`, read with `Read`, saved with `Write`. `byhand styles` isn't
    built. `.gitignore` for a project's styles is written the same way.
  - Step 8: a release is a tag and `plugin.json`'s version; nothing goes to PyPI. Round 1's P4 and P5 no longer apply to
    a user, and the pin checks in the gate and the lenses go when the first skill lands.

  The package stays, as the repo's own tool: `byhand validate`, `byhand render`, and the refresh in `0.2.0`.
- **What that cuts (the maintainer, 2026-11-07):**
  - Three skills, `write`, `check` and `learn`. `learn` lists a user's styles and sets a default; `styles` isn't built.
  - `byhand models`, and reading a family from an id: the model reads its own id and picks the file, as a skill's prose
    says, and Step 7's evals prove it on an id the catalogue has never seen.
  - `render --out`: the folder is always `plugin/signs`, so `render` owns it, which replaces the Step 3 call below.
  - The packaging: no CI job, no metadata; `Private :: Do Not Upload` keeps it off PyPI.
  - One version, `plugin.json`'s. `pyproject.toml`'s stays fixed.
  - The gate's pin checks: a ban on a command under `plugin/` takes their place, which is stricter.
- **A check is what Grep can run (the maintainer, 2026-11-07):** no look-around and no backreference, held by
  `validate`. A term's edge is `\b`. `render` prints a sign's `check` in Step 5, for `Grep`; where it goes, the draft's
  files or a side file, is that step's call.
- **Step 3, its review (the maintainer, 2026-11-07):** a third budget, 16 KB, holds a deck's or a sheet's layout files. The gate's link scan
  skips code spans in `plugin/signs/` alone, where a term is a regular expression. A future `until` retires a sign
  today, and every reader of the signs treats it so.
- **Step 3, a retired sign (2026-11-07):** a sign with an `until` renders nowhere, whatever the date: rendering by the
  clock would turn a file stale overnight and fail the gate on no change.
- **Step 3, the rendered files hold no citation and no example:** what a draft loads is what the model acts on; the
  sources stay in the catalogue.
- **Step 2, the languages' source (2026-11-07):** the Wikipedia list The catalogue names holds only 38 languages, so it
  can't give 100, and language codes are a one-way door, not to be filled in from memory. `languages.toml` comes from
  Unicode CLDR 49 instead: each territory's population times CLDR's percentage of speakers, script variants merged into
  their base code, with CLDR's BCP 47 codes and its name of each language in itself. All eight seed languages are in
  the hundred, Hungarian at rank 90. `zh-Hant` is a variant of `zh`, outside the hundred. The list treats Chinese and
  Arabic varieties as CLDR does, each its own code (`yue`, `arz`).
- **Step 2, version ranges (the maintainer, 2026-11-07):** `to = "5"` holds the whole 5 series; `to = "5.0"` stops at
  5.0. `ModelRange.holds` comes here, not in Step 3, as `validate` needs it to compare `from` and `to`.
- **Step 2, a check's flags (the maintainer, 2026-11-07):** a `check` runs case-insensitive and line by line, so `^`
  and `$` match at each line.
- **Step 2, the schema's stricter rules, from its review:** an `any` sign has no `terms`, as a word's edge differs
  between languages; a language sign cites a source in its language; a `word` or `phrase` sign needs `terms` or a
  `check`, an `artefact` a `check`; a `layout` sign is only for `deck` and `sheet`; a sign id at a base stays in the
  tree (the gate's `sign ids`).
- **Step 2, the model families:** a family is one the research names signs for: claude, gpt, gemini, grok, llama,
  deepseek, qwen, kimi, mistral and doubao. `gpt-4o` reads as gpt 4 and `deepseek-r1` as deepseek 1, kept by the
  maintainer on 2026-11-07: a range can't split them from their base version, and few write with them now. The
  o-series names no family yet. Two ids read wrongly and are kept: `gpt-35-turbo`, Azure's name for 3.5, reads 35, and
  `grok-code-fast-1` reads 1. `lah` stays beside `pa`, as CLDR counts it, so `aeb` falls to rank 101.

GitHub milestones: `0.1.0 Write in your own voice` (Steps 2 to 8), `0.2.0 Refresh`, `0.3.0 More languages`,
`0.4.0 Decks and sheets`, `0.5.0 Learn from edits`; an issue per step, #2 to #8, opened when this plan was approved.

## Tests

- **Unit (CI):** the catalogue, models, render, check, styles, the gate; invented text in every seeded language.
- **By hand:** the `claude plugin eval` suite and the drafts read in real sessions (Step 7), on the Claude Code version and models
  of the day, recorded with what they could not show.
- **What none can show:** whether a reader takes a draft as the user's. The maintainer's read in Step 7 is the only
  evidence, for two languages; the others rest on their sources and native contributors.

## Docs

`README.md` and `plugin/README.md` (the skills, install), a new `docs/USAGE.md` (skills, the CLI, the style format,
the catalogue's schema, how to add a sign), `CONTRIBUTING.md` (adding a sign through `propose-signs` or the form),
`CHANGELOG.md`, `AGENTS.md` (the catalogue's row, the one-way doors, the commands), `docs/research/` for the research
this plan rests on, and `write-skill` (the `plugin/signs/` and `plugin/evals/` rules, and the pin written as `uv run
--no-project --with byhand==<version>`).

## Risks

| Risk | Answer |
|---|---|
| `write` doesn't start by itself often enough, or loses its description in a crowded skill listing | Measured in Step 7, in a clean eval and a crowded session; the hook is the fallback, its own plan, before Step 8. Accepted |
| A sign flags plain human writing | `strength`; `passes` tested in CI where a sign has a `check`, sampled in Step 7 where it hasn't; weak signs only in clusters. Accepted, watched through issues |
| A source's licence: Wikipedia's CC BY-SA, lieflat's CC BY-NC, vendors' all rights reserved | Our words and a citation; non-commercial and vendor sources as facts only; review lens `catalogue-contract`. Resolved by rule |
| No model id in the session, or a subagent on another model | The two `any.md` files alone; the skill names the model that writes the draft. Accepted |
| Thin sources for most languages, Hungarian included | The `any` signs carry them; native review as a source; `0.3.0` measures excess words from datasets. Accepted |
| Rendered files grow with the catalogue | Two budgets, tested: 16 KB for the prose files one draft reads, 48 KB for a text of unknown author read in every family; over either fails the build. Resolved |
| A user's real writing in a project's `.byhand/` gets committed | learn writes the `.gitignore` line and says so. Accepted: a user can still force-add it |
| The PyPI name is free today and open to a squatter until `0.1.0` (omniverse-mcp's R9) | Nothing is uploaded before Step 8, which publishes `0.1.0` itself: the maintainer's call on 2026-11-07, in place of Q3's placeholder. Accepted |

## Plan review

### Fit

The plan at `232347f`, by a fresh agent on Claude Opus 5.5 (`claude-opus-5-5`), 2026-11-06. Answers by the
maintainer, 2026-11-06. The change's own question: does the design stay open to the refresh, more languages, decks
and sheets at a human skill level and learning from edits, and is the light loading the right mechanism. Its answer:
mostly yes; I1 to I6 are where it was not open enough.

| # | Improvement | Answer |
|---|---|---|
| I1 | Light by design, Step 7: `allowed-tools` grants `Read` only for the turn that invokes the skill, and the files sit outside the working directory, so a second draft would ask; `write` invokes itself again per draft and re-reads after a compaction, and Step 7 checks a second draft | taken |
| I2 | Light by design, skills: render to one shared `plugin/signs/`, read through `${CLAUDE_PLUGIN_ROOT}` by `write`, `check` and `learn`; otherwise `check` and learn's screen see only the mechanical signs, and most are structural | taken |
| I3 | Light by design: layout signs of decks and sheets in `.layout.md` files of their own, so a message never loads them and `0.4.0` doesn't overrun `any/any.md`'s cap | taken |
| I4 | The catalogue: `sources.toml` gets a machine-readable `feed` and `read_at`, written for every source read, so `0.2.0`'s model-free diff has a baseline; `validate` checks both | taken |
| I5 | The catalogue: a `word` or `phrase` sign holds `terms`, so an era list or a computed list is one sign, not hundreds of permanent ids | taken |
| I6 | Styles: a dated `## Corrections` section that beats the body, as half of the maintainer's own style file is; readers keep unknown keys and sections | taken |
| I7 | The CLI: `validate` refuses an `any` sign whose sources cover fewer than two languages, a rule only a reviewer kept | taken |
| I8 | Step 7, Tests: `claude plugin eval` in place of a new `tools/triggers.py`: repeated runs, a no-plugin baseline, one command to measure again | taken |

Noticed on the way, for Round 1: a structural sign without `check` has nothing its `flags` and `passes` test can run
(The catalogue); "the newest range below it" contradicts a closed `to` (Light by design); the size cap has no number
(Light by design, Risks); nothing says the user's style beats a sign they said yes to (Styles); `write` starts on
"post" but `kinds` has no `post` (The plugin's skills); Claude Code drops the descriptions of the least-used skills when
the listing overflows its budget, which a clean Step 7 session can't show (Risks, Step 7).

### Round 1

**How:** a fresh agent on Claude Opus 5.5 (`claude-opus-5-5`), 2026-11-06, on the plan at `5c7f576`, every lens
applied; it reproduced P4, P5 and P13 on Windows 11 with uv 0.12.1 and Python 3.12 and 3.14. The majors were checked
in the main session, not by fresh refuters: P4 and P5 run again (a `.venv` and `uv.lock` written into a project; a
pipe in cp1252 raising `UnicodeEncodeError` on Chinese and "ő"), P6 against the skills docs ("drops descriptions
starting with the skills you invoke least") and the eval docs ("other installed plugins ... are absent"), P1 to P3
against the plan's own lines. **Verdict:** needs-fixes. **Now:** every finding below edited into the plan; the owner
calls answered by the maintainer the same day.

| # | Sev | Finding | Status |
|---|---|---|---|
| P1 | major | A rule the user kept, or a correction, is rewritten away by a sign: `write` rewrites what it finds, and nothing put the style above the catalogue, so a review mail loses the bold headings its user asked for | fixed: `keeps` in the frontmatter, "The style beats a sign" in Styles, a test |
| P2 | major | The style is picked by kind alone: a Hungarian chat default for `message` writes an English Slack reply | fixed: the draft's language first, a default per kind and language (Q1), a test |
| P3 | major | `check` and learn's screen read only the session model's family, so a pasted ChatGPT text passes and learn learns from it | fixed: a text of unknown author reads every family of its language; `check` without `--model` applies all, a test |
| P4 | major | `uv run --with` in a Python project writes its `.venv` and `uv.lock` and installs its dependencies, or errors | fixed: `--no-project`; write-skill's pin line in Docs; tried from inside a project in Step 6 |
| P5 | major | On Windows the CLI's pipe is cp1252: Chinese or Hungarian output crashes, input is mangled | fixed: UTF-8 streams as the gate's; subprocess tests on CI's Windows leg |
| P6 | major | A crowded skill listing drops a new `write`'s description, and a clean eval can't see it | fixed: Step 7's crowded session, the Risks row, `plugin/README.md`'s note; the hook before Step 8 if below the bar (Q4) |
| P7 | minor | A structural sign without a `check` never has its `flags` and `passes` run | fixed: `validate` holds them present and different; Step 7 samples them |
| P8 | minor | "The newest range below it" brings back a sign a closed `to` retired | fixed: a sign applies only inside its range; an open `to` covers newer versions |
| P9 | minor | The size cap had no number | fixed: 16 KB for a draft's four prose files, under 2,000 lines each, one constant |
| P10 | minor | `write` starts on "post", but there was no `post` kind | fixed: `post` is a kind (Q2) |
| P11 | minor | The second-draft eval case can't show a permission prompt: evals never ask, and from the clone reads never ask | fixed: the case grades `tool_order`; the no-prompt claim moves to a by-hand try outside the clone |
| P12 | minor | The gate's `plugin/evals/` rule refused the `.jsonl` history and failed on every run's `results/` | fixed: `.md`, `.yaml`, `.jsonl`; `results/` skipped and ignored; invented history; write-skill in Docs |
| P13 | minor | `uvx byhand==0.1.0 byhand validate` runs `byhand byhand` | fixed: `uvx --from byhand==0.1.0 byhand validate` |
| P14 | minor | The Steps never ended with `review-code` | fixed: each step ends with `finish-work` |
| P15 | minor | Step 7's record could hold drafts in the maintainer's learned voice | fixed: cases, counts and verdicts only |
| P16 | minor | Reserving the PyPI name at Step 2 would publish `0.1.0` for good | fixed: a `0.0.0` placeholder by hand (Q3) |
| P17 | minor | `zh-Hant` falling back to `zh` only when its file is missing skips `zh`'s signs | fixed: a `zh-Hant` draft reads both, six files at most |
| P18 | minor | "Only in a cluster" was undefined | fixed: three weak signs in one paragraph, one constant |
| P19 | minor | A term in an inflecting language misses its forms or matches inside other words | fixed: a term is a stem and its endings, or the sign carries its own `check`; a test in hu and ru |
| P20 | minor | Where `write` must not start was unnamed, and `check`'s start unmeasured | fixed: the skills table says where each starts; code-adjacent negatives and `check` cases in Step 7 |

Refuted:

- R1, re-invoking `write` doesn't restore the grant: the skills docs say "invoking the skill again re-applies it for
  that turn"; only the test was wrong (P11).
- R2, `${CLAUDE_PLUGIN_ROOT}` isn't available in a skill's Markdown: the plugins reference says it resolves anywhere in
  the body.
- R3, admitting `plugin/signs/` and `plugin/evals/` loosens the gate: the first is held equal to `render`, the second by
  file type; REVIEW.md, a check made stricter.
- R4, a `SessionStart` hook can't add context: the hooks docs, `additionalContext` "adds context for Claude".
- R5, the refresh is missing: out of scope openly, `0.2.0`.
- R6, styles in `${CLAUDE_PLUGIN_DATA}` are simpler: deleted on uninstall.

| # | Question | Recommendation | Answer |
|---|---|---|---|
| Q1 | A default per kind and language, so `message` can have a Hungarian and an English default? | yes | yes, the maintainer, 2026-11-06 |
| Q2 | Is a social post its own kind? | map it to `message` or `document` | a kind of its own, `post`: the maintainer, 2026-11-06 |
| Q3 | How is the PyPI name held before `0.1.0`? | a `0.0.0` placeholder by hand at Step 2's merge | the placeholder, the maintainer, 2026-11-06; changed on 2026-11-07: nothing until Step 8 publishes `0.1.0`, the risk accepted |
| Q4 | Below Step 7's bar in a crowded session, does the hook come before `0.1.0`? | before | before, the maintainer, 2026-11-06 |

| # | Improvement | Answer |
|---|---|---|
| I9 | The gate runs `byhand render --check` as a tool after its `uv sync`, never importing the package, so it stays standard library only for the hooks | taken |
| I10 | Trigger cases run with `--ablation none` (the baseline says nothing for them) and pass only when all three runs fire, `--threshold 1.0` | taken |
| I11 | `test_models.py` adds dated and provider-prefixed ids | taken |
| I12 | Step 7 adds a trigger case each in ja, ko and ru | taken |
| I13 | `check` compares text and terms in NFC, with a test on an NFD Hungarian text | taken |
| I14 | A model-scoped sign retires by its range's `to`; `until` only for signs whose `models` is `any` | taken |
| I15 | Step 7's by-hand try names its OS, Windows at least: plugin paths, styles found without a command, the CLI's streams | taken |

### Round 2

**How:** a fresh agent on Claude Opus 5.5 (`claude-opus-5-5`), 2026-11-06, on the edits from `5c7f576` to `c6307a3`
and round 1's open findings. **Verdict:** approved: P1 to P20 hold, no blocker or major open, every owner call
answered. **Now:** the four minors below edited into the plan.

| # | Sev | Finding | Status |
|---|---|---|---|
| P21 | minor | The budget and "at most four" left out a `zh-Hant` draft's six files and the read of a text of unknown author in every family | fixed: six for `zh-Hant` in both rules; a second budget, 48 KB, for the every-family read; the Risks row |
| P22 | minor | `byhand check` took no style, so `check` flagged a sign a style keeps | fixed: `--style`, the `check` skill passes it, corrections honoured in the model's read; a test in Step 6 |
| P23 | minor | The tries by hand in Steps 6 and 7 run the pinned command before `byhand==0.1.0` is on PyPI | fixed: a wheel of the clone through `UV_FIND_LINKS`; `docs/USAGE.md` and finish-work say so |
| P24 | minor | The crowded session, the `check` cases and the `passes` sample had no bar, so Q4's rule couldn't be applied | fixed: 9 of 10 in the crowded session, 6 of 7 `check` and boundary cases, a flagged `passes` text fixed before Step 8 |

Refuted: a leftover "no-plugin baseline" (the Fit is a dated record, I10 supersedes it); 23 against 20 (I12 added
three); `until` against `to` (consistent since I14); `keeps` against the call on learn's yes (`keeps` is filled by that
yes); `post` missing from AGENTS.md (Step 2's PR names the kinds); the token gloss for CJK (the constant is in bytes);
the `0.0.0` placeholder against the one-version rule (never committed); start-work's changed examples.

| # | Improvement | Answer |
|---|---|---|
| I16 | Step 7's history case grades `tool_order` with an `input_match` on the second draft's language path, accepting either separator (`signs[\\/]hu[\\/]`): a path the invented history never reads, and a Windows `Read` path has backslashes | taken |
