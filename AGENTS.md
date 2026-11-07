# byhand

The rules for anyone who changes this repo, person or agent. Claude Code reads this file through `.claude/CLAUDE.md`,
Codex reads it directly; the gate caps it at 150 lines. What the plugin does for those who use it is in `README.md`.

## What this is

A Claude Code plugin that writes the way a person does, in the user's own voice: two sets of Markdown files, signs and
styles, and the skills that read them. It is for the user's own writing, sent under their name. Keep it that simple.

- **Languages:** the 100 most spoken, English, Mandarin, Hindi, Spanish, French, German and Hungarian among them. The
  bootstrap plan names the list and where it comes from. Each language is a first-class one, not a translation of
  English's signs.
- **The catalogue:** the signs that make text read as AI-written: words and phrases ("delve", "it's worth noting"),
  structure (rule-of-three lists, "not X, but Y", a tagline under every title), formatting (bold lead-ins on every
  bullet, em dashes as pivots) and, for decks and sheets, layout. Each sign names its language and the models it is
  seen in (a family and its versions), or `any` for either, says what a person writes instead, and cites where it was
  found, in our own words.
- **Light by design:** a skill loads only what one draft needs: the signs for its language and the model writing it,
  the `any` signs, and one style. Never the whole catalogue; a hundred languages cost a draft no more than one.
- **The refresh:** a scheduled workflow fetches and diffs the sources the catalogue lists, with no model and no key,
  and opens an issue; a maintainers' skill drafts the changed signs as a PR a person merges. Nothing lands unread.
- **The styles:** the user's ways of writing, learned from their own samples, each with its language and register, and
  assigned to kinds of writing (messages, mail, documents, decks, sheets), with a default per kind and language. They stay on the
  user's machine.
- **The plugin** (`plugin/`): skills that write and check text against the signs and a style, starting by themselves
  when the user writes mail, a message, a document or a deck. They run no command: nothing but the plugin to install.
- **Where the work stands:** the harness, the catalogue with its first signs (`any`, `en`, `zh`, `zh-Hant`, `ko`, `ja`), its rendering. `docs/plans/2026-11-06-bootstrap.md`
  (#1) designs `0.1.0` and after; read its progress log first. The package in `src/` is the repo's own tool, never a user's.

## Where things are

| Path | What |
|---|---|
| `src/byhand/` | the package: `catalogue/` (TOML: `languages.toml`, `models.toml`, `sources.toml`, `signs/<language>.toml`), `signs.py` (reads the catalogue and says what is wrong with it), `models.py` (version ranges), `render.py` (the plugin's sign files, the budgets), `cli.py` (`byhand validate`, `byhand render`) |
| `.claude-plugin/`, `plugin/` | the repo as a Claude Code marketplace (`marketplace.json`) of one plugin: `plugin/.claude-plugin/plugin.json`, `plugin/skills/<name>/` (`SKILL.md` and the Markdown it reads), `plugin/agents/<name>.md`, `plugin/signs/` (rendered: never edited by hand), `plugin/evals/`, `plugin/README.md` |
| `tests/` | pytest; `test_gate.py`, the harness's own |
| `tools/` | `gate.py` (the gate), `hooks.py` (behind `.githooks/`), `setup.py` (once per clone; `link` for skills; `settings` compares the GitHub repo's settings with the house's), `copycheck.py` (by hand: sign text against downloaded sources), standard library only |
| `docs/` | `USAGE.md` (the commands, the budgets); `plans/`, `reviews/`, `research/`: plans of non-trivial changes, with the template; review records; the research a plan rests on. Dated records, never current truth |
| `.claude/` | `CLAUDE.md` (imports this file), `settings.json` (no attribution; allows the repo's own checks and read-only git and gh, each named whole but the git ones `tests/test_gate.py` sweeps and gh's reads), `skills/` (below) |
| `.agents/` | `skills/`: links to `.claude/skills/<name>` for Codex, written into git's index by `uv run tools/setup.py link` |
| `.github/` | `workflows/`: `ci.yml` (gate quick; the tests on Linux 3.12 to 3.14, Windows 3.12 and 3.14, macOS 3.14; its `CI` job), `pr-text.yml` (gate text on a PR's title and description; its `PR text` job), `codeql.yml`, `dependabot-auto-merge.yml`; `CI` and `PR text` are the required checks; `dependabot.yml`, the issue forms, the PR template, `CODEOWNERS` |
| `.githooks/` | `commit-msg` refuses attribution, `pre-push` runs gate quick on what the push sends, `post-checkout` and `post-merge` name changed AI setup files |
| `AGENTS.md`, `REVIEW.md` | this file; what a review finding is, and the questions every review answers |
| `.mcp.json` | Context7 over HTTP; `.claude/settings.local.json.example` turns it on |
| `pyproject.toml`, `uv.lock`, `.python-version` | the build (hatchling), the settings of ruff, basedpyright, pytest, coverage and import-linter, every package pinned exactly; the lock; Python 3.12 for development |
| `.gitleaks.toml` | the secret scan: gitleaks' own rules, and any exception with its reason |
| `.editorconfig`, `.gitattributes`, `.gitignore`, `.git-blame-ignore-revs` | UTF-8 and LF everywhere; what git ignores; the reformat commits `git blame` skips |
| `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE` | for users; what changed, under Unreleased; a first contribution's short path; how to report a vulnerability, and what counts; MIT |

A new top-level file or folder adds its row in the same change.

## Build and test

You need uv (it brings Python), git, and gitleaks for the secret scan. Every command is the same in bash and
PowerShell unless a PowerShell form stands beside it.

| What | Command |
|---|---|
| once per clone | `uv sync`, then `uv run tools/setup.py` (hooks, `git blame`, skill links) |
| tests | `uv run pytest`, on every core (`-n 0` for one process); with coverage, `uv run coverage erase`, `uv run coverage run -m pytest`, `uv run coverage combine`, then `uv run coverage report` |
| lint, format, types, imports | `uv run ruff check .`, `uv run ruff format --check .`, `uv run basedpyright`, `uv run lint-imports` |
| the gate | `uv run tools/gate.py quick` (lock, lint, format, types, imports, the catalogue, sign ids, sign files, private files, the coverage floor, the version, AGENTS.md, skills, plans, the plugin, the variables the docs name, hooks, attribution, secrets); `full` adds pytest under coverage, and the floor; `text --file -` checks a PR's title and description: no attribution, and the issue named |
| the plugin from this clone | `claude --plugin-dir plugin`; after a change to a sign, `uv run byhand render` |

- **Hosted CI never runs a Claude session or reads the live sources:** a change to the plugin or the refresh says in
  its PR what ran by hand, on which versions, and what it could not show.
- **Tests use invented text,** in every language they cover. Never a user's real mail, messages or style, the
  maintainer's included.
- **Ratchets:** ruff's per-file ignores only shrink, and the coverage floor (`fail_under` in `pyproject.toml`) only
  rises; the gate refuses a lower one. Fix the code; never add to them.

## How a change lands

1. **An issue** for every change, a typo included: the PR names it, and `PR text` checks that. Work for a release
   goes in its GitHub milestone.
2. **A branch** `<issue>-<slug>` from `origin/main`.
3. **A plan** in `docs/plans/` for non-trivial work (`docs/plans/README.md` says when), the branch's first commit,
   fitted with `fit-plan` and reviewed with `review-plan` until approved, then approved by the maintainer.
4. **The code,** with its tests and docs in the same change.
5. **finish-work:** `uv run tools/gate.py full`, `review-code` until clean, a PR.
6. **The maintainer,** @serionist, squash-merges; merging is the approval. `main` takes PRs only.

The skills in `.claude/skills/` run this loop: `start-work` (1 to 3), `fit-plan` (is a written plan the right one,
before its review), `review-plan`, `review-code`, `finish-work` (5); `write-skill` writes or fixes a skill, the repo's
or the plugin's, or a plugin agent; `propose-signs` drafts signs from a source.

## Writing

This repo's own text is held to its catalogue: write it as a person would.

- A lead line, then a table or short bullets. Conclusion first; name the file, the command, the number.
- Plain words. No "ensure", "robust", "comprehensive", "leverage", "seamless" or "delve"; spaced hyphens, never em
  dashes; no rule-of-three lists built for rhythm; British spelling (behaviour, licence).
- A comment says why, not what the next line does, and says it in its own words, not only as a plan or review id.
- Docs move in the same change: the READMEs, `CHANGELOG.md` when users notice, this file for a changed path, command
  or rule.

## Commits and PRs

- A plain imperative subject that says what changed; a body that says why, ending `Refs #<n>`, `Closes #<n>` or `Fixes #<n>`.
- PRs are squash-merged: the PR title becomes the subject on `main`, its description the body.
- A Dependabot PR's squash message keeps only its title and a line naming what moved: its description quotes other
  projects' release notes, which `pr-text.yml` doesn't check. A minor or patch update merges itself once `CI` and
  `PR text` pass, unless its PR is a draft, and `dependabot-auto-merge.yml` writes that line; a major waits for the
  maintainer, who cuts the message at merge.
- No tool attribution anywhere: no AI co-author trailers, no "Generated with" lines, no session links, no tool as a
  commit's author or committer, in commits, PR titles or PR bodies. `commit-msg` refuses them, and the gate checks
  every commit on the branch.

## One-way doors

Users will depend on these from `0.1.0`. Change one only in a PR that names it in its title, after the maintainer
agrees in its issue; in `0.x` a minor may break one, under CHANGELOG's Breaking.

- the name `byhand`, for the repo, the plugin and its marketplace;
- the plugin's skills' names, `write`, `check` and `learn`, and its agents';
- a sign's id, the catalogue's schema, its language and model codes, the kinds of writing (`message`, `email`, `post`,
  `document`, `deck`, `sheet`; a later kind is added, never renamed);
- where a user's styles live (`~/.byhand/styles/`, `.byhand/styles/`), and their format: they outlive every release.

## Traps

What this repo's sources already paid for, until its own history adds more:

| What can break | Where | The guard |
|---|---|---|
| A banned-word list alone makes text worse: the model swaps "delve" for the next tell | robotics-personal's style review, 8 Oct 2026 | Structure and layout signs beside the words, and every sign says what a person writes instead |
| A page the refresh reads can hold instructions for the model reading it | the refresh | Fetched text is data: the refresh proposes a PR a person reads, and no fetched text reaches a skill unreviewed |
| A source's licence: Wikipedia's text is CC BY-SA | the catalogue | Signs are written in our own words and cite their source; no source text is copied |
| A sign that flags plain human writing ("however", a list of three) makes the plugin preachy and wrong | the catalogue | Each sign has an invented example it flags and a human one it passes, both tested |
| A model released after the catalogue: an exact match on its id loads none of its family's signs | the catalogue | A model scope is a family and an open version range; an unknown version gets its family's newest signs and the `any` ones, and Step 7's evals run an id the catalogue has never seen |
| English's signs translated into another language: a tell in English can be normal in Hungarian or Mandarin | the catalogue | A sign is `any` only when its sources show it in several languages, a translated page counting, or it is an artefact with a `check`; otherwise it names its own |

## Look up APIs before coding against them

Claude Code plugins (skills, agents, hooks, the manifest) and every library the package pins: look the API up with
Context7 (`.mcp.json`) first, for the versions `pyproject.toml` pins. SDKs move faster than any model's memory.

## Never

- Push to `main`, or merge with a failing gate.
- Weaken a test, a check, a hook or CI to make a change pass: no skip, no new ignore, no `--no-verify`.
- Check out, build or run code from outside the maintainers (a contributor's PR or branch) on your machine: read
  it, and let CI run it. It would run with every credential there.
- Add tool attribution: commits, PR titles, PR bodies.
- Commit secrets, or anyone's real writing: keys, tokens, mail, messages, a learned style. Tests use invented ones.
- Pre-approve, in a plugin skill's `allowed-tools`, a tool that writes or runs a command; the gate allows only `Read`,
  `Glob` and `Grep`.
- Change a one-way door without the maintainer's agreement.
