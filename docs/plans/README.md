# Plans

A non-trivial change gets a plan here before any code: a new skill, agent or CLI command, a change to a one-way door
(`AGENTS.md`), to the catalogue's schema or its languages, to how styles are learned or kept, to the refresh or the
sources it reads, to what a skill pre-approves or where it starts by itself, work on the package and the plugin
together. A new sign, or a fix a reviewer can follow from the PR alone, needs none; its PR says `Trivial: <why>`.

- One file per plan: `YYYY-MM-DD-<slug>.md`, dated the day it was started.
- Written with `start-work` as the first commit of its branch, fitted with `fit-plan` and reviewed with `review-plan`
  until approved, then approved by the maintainer, and the approval committed in its frontmatter. Someone outside the
  maintainers puts it up as a draft PR right after that first commit, where the maintainer answers the fit and
  approves it (`start-work`).
- A plan records what was decided and why at the time. It changes while its branch is open, when the work departs from
  it, and not after the merge.
- A plan that spans several PRs is the exception: each step's PR updates it, and after its first merge only its
  progress log, the decisions taken on the way and their answers change.
- Fill every section. "None" is an answer; a blank is not.

## Template

```markdown
---
title: <a plain imperative sentence, which can become the PR title>
issue: "#<n>"
status: draft
approved_by:
approved_at:
---

# <title>

## Goal

What is true when this is done, and why it matters. In scope; out of scope.

## Design

How it works: the modules, CLI commands, skills and agents it adds or changes, in the package and in the plugin. The
alternatives considered and why this one.

## Compatibility

The one-way doors it touches (`AGENTS.md`), what breaks for users (the skills' names and arguments, a sign's id, the
catalogue's schema, their styles) and how they move over. Or "none".

## Steps

Ordered, each one buildable and testable on its own, each naming the test that proves it.

## Tests

The new and changed tests, and what proves it: unit (CI), the refresh against the live sources (by hand), a try in a
real session (`claude --plugin-dir plugin`) in the languages and on the models it is for, and what none of them can
show.

## Docs

The docs that change with it: the READMEs, `CHANGELOG.md`, `AGENTS.md`.

## Risks

What could go wrong, and whether each risk is resolved or accepted.

## Plan review

"None yet." until `fit-plan` writes `### Fit` here: the plan's commit, the agent, and its improvements (`I1`, ...),
each answered `taken`, `left: <why>` or `later: #<n>` before the first round. Then `review-plan` writes each
`### Round <n>` below it: its reviewer, date and verdict, the findings with their status, the owner calls with their
answers, and the improvements with theirs, their ids numbered on from the Fit's.
```

`issue` is quoted: a bare `#` starts a YAML comment.
