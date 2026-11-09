# Contributing

Thanks for helping. This is the short path for a first contribution; [AGENTS.md](AGENTS.md) has the full rules, for
people and agents alike, and [REVIEW.md](REVIEW.md) what a review checks.

## Before you start

- **Open an issue** for every change, a typo included, with the bug or feature form, and say there that you want to
  work on it.
- **Write a plan first** for a non-trivial change: a new skill, agent or command, a change to the catalogue's schema,
  the styles or the refresh, work on the package and the plugin together. Use the template in
  [docs/plans/README.md](docs/plans/README.md) and open it as a draft PR. The maintainer approves it before any code.
- **Leave the one-way doors alone** unless the maintainer agrees in the issue first: the names, the skills' and
  agents' names, a sign's id and the catalogue's schema, where users' styles live (AGENTS.md, One-way doors).
- **Use invented text.** Tests, examples and issues never hold anyone's real mail, messages or style, yours included,
  and never a real key or token.
- **Report security issues privately**, never in an issue: see [SECURITY.md](SECURITY.md).
- **Your contribution is MIT licensed.** Opening a pull request means you agree to license it under the repository's
  [MIT licence](LICENSE).

## Adding a sign

A sign for your language is the most useful contribution there is, and you don't need to write code for it: open a
feature request with the form's "A sign" area. Say what the text does, in which language and, if you know, which
model writes it; give a short invented example that shows it, a line a person would write instead, and where you saw
it named (a link). Write it in your own words: a sentence copied from a source can break its licence.

## Build and test

You need [uv](https://docs.astral.sh/uv/) (it brings Python), git and [gitleaks](https://github.com/gitleaks/gitleaks).

```
uv sync
uv run tools/setup.py
uv run tools/gate.py full
```

- `uv run tools/setup.py` sets up the clone once: the git hooks (`commit-msg` refuses tool attribution, `pre-push`
  runs the gate's quick lane), `git blame` past the reformat, the skill links. It is safe to run again.
- `gate full` runs the lock check, ruff, ruff format, basedpyright, import-linter's contracts, the coverage floor,
  the harness checks, the plugin check, the attribution check and gitleaks, then the tests under coverage, which must
  reach the floor. Without gitleaks it skips the secret scan with a warning; CI runs it.

After a change to a sign in a PR of your own, run `uv run byhand render`: the gate fails when `plugin/signs/` differs
from the catalogue.

### The plugin from your clone

`claude --plugin-dir plugin` starts Claude Code with the clone's plugin in place of an installed one. Turn the
installed copy off first (`claude plugin disable byhand@byhand`), and on again after. CI never runs a Claude session,
so a PR that changes a skill says how it was tried: the Claude Code version, the model, the language and what you
asked for.

## Open the pull request

1. Fork, and branch from `main` as `<issue>-<slug>`, such as `42-hungarian-signs`.
2. Make the change with its tests and docs: the READMEs; for a change to the plugin, its version and a dated section
   in [CHANGELOG.md](CHANGELOG.md) ([docs/releasing.md](docs/releasing.md));
   AGENTS.md when a path, a command or a rule changes.
3. Commit with a plain imperative subject that says what changed, and a body that says why. No AI co-author
   trailers, "Generated with" lines or session links, and you, not a tool, as author and committer: `commit-msg`
   refuses them.
4. Open the PR with [the template](.github/pull_request_template.md) filled in, ending `Closes #<issue>`, or
   `Refs #<issue>` for one step of it. Its title becomes the commit on `main`.

CI runs the gate's quick lane and the tests on Linux, Windows and macOS, CodeQL scans the code, and a check reads the
PR's title and description whenever they change: no attribution, and a line that names the issue. The maintainer
reviews a PR from outside by reading it: they never check it out, build or run it on their machine, where it would
run next to their credentials. Your PR is ready for review when CI is green. The maintainer squash-merges it.
