---
subject: "Learn a style's corrections from the user's edits to a draft (PR #107)"
base: main (dc0e942)
head: e78ed80
date: 2026-11-10
round: 1
tier: standard (one fresh reviewer on Claude Opus 5.5; findings checked against the code by the main session)
verdict: needs-fixes
---

# Review: Learn a style's corrections from the user's edits to a draft (PR #107)

One fresh agent read the pack (`git diff origin/main...HEAD` at `e78ed80`), AGENTS.md, REVIEW.md, issue #106, the plan
and every touched file, with every lens. Minors only, so no second round: the main session fixed them and checked the
fixes. After them, on `76d5a68`: **clean**.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `plugin/skills/learn/SKILL.md`, Learn from an edit, step 4 | A `zh-Hant` version read only `zh-Hant/any.short.md`, missing the Mandarin signs `write` reads from `zh`; and `<language>/any.short.md` isn't there for `ar`, `tr`, `vi` or `id`, with no word on what a missing file means | fixed: a script variant's base language's too; a file that isn't there has no signs. `76d5a68` |
| F2 | minor | `plugin/skills/learn/SKILL.md`, step 1 | "as `check` step 1 reads one" pointed at text not in context on this path, so a `.pptx` the user changed in PowerPoint had no instruction when Read failed | fixed: check step 1's clause inlined: the text from what reads it in the session, else a PDF, a CSV or the text |
| F3 | minor | `plugin/skills/learn/SKILL.md`, step 1 | With no draft, learn asks for it; the user's answer in the next turn reads the sign files after the grant has gone, a prompt in default mode and a skipped note in dontAsk | fixed: "their answer starts this skill again"; not run in a session |
| F4 | minor | the release, `docs/releasing.md` step 3 | A minor ships without its empty-session try and prompt count | wontfix here: the try would run in the maintainer's real home; it runs right after the merge, from the marketplace, and the PR says so |

The fixes are in `76d5a68`; `tests/test_render.py`'s ceiling moved to the new 5,488 bytes, and gate
quick and the render tests passed on it.

Refuted: picks saved into the wrong style (step 2 fixes the style, and the two-drafts try passed); an eval that passes
when wrong or fails when right (its grader fails on any rule, sample or draft, and passes either answer step 1
allows); new behaviour without a committed test (the maintainer's Round 1 Q1 in the plan); cost to a user who never
edits (no description moved, and the ceiling test holds `write`); the 4 KB rule (no read-only tool counts bytes, an old
limit); the style's format (a replaced correction stays a dated line with its kind); the plugin contract (both skills
keep `allowed-tools: Read`, paths through `${CLAUDE_PLUGIN_ROOT}`, names end `.short.md`); Remember's repeat rule
against step 3's "already held" (different inputs); Sonnet's deck misses (a defensible call on the seeded style);
`write` step 9 against #105's wording ("in the same form" carries it); a re-read after compaction (the draft is gone
too, out of scope); privacy (`.local/` is ignored and nothing under it is tracked); the release (0.4.0 is the newest
dated section, no other PR takes it); docs (all moved); the PR's text (no attribution, `Closes #106`).

Not covered: none. catalogue-contract and harness-integrity had nothing to read; F3 needs a live default-mode session.

| Improvement | Answer |
|---|---|
| `write` step 9: answer a bare version with only the offer, as "end with" implied a rewrite before it | taken |
| `learn` step 3: "leave it out" for a change the style already holds, as "propose nothing" could drop the whole edit | taken |
| The milestones "0.4.0 Decks and sheets" and "0.5.0 Learn from edits" disagree with the versions released: drop their numbers | taken: renamed on GitHub |

## Checks

- `uv run tools/gate.py full` on `e78ed80`: 22 checks, 4,135 tests, 99.16% coverage; CI green on it.
- On the fixes: `uv run pytest tests/test_render.py` (85 passed), gate quick, CI on the PR's head.
- The fixes are wording in the two skills; the evals and tries were not run again on them.
