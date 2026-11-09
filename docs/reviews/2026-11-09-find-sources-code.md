---
subject: "Add find-sources, and the first Spanish sources it found (PR #48)"
base: main (ae5f9ad)
head: 5bcfd21
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, every lens with something in scope; its findings checked against GitHub by the main session)
verdict: clean
---

# Review: Add find-sources, and the first Spanish sources it found (PR #48)

One fresh reviewer read the pack (`files.txt`, `scope.diff`, issue #32), the ground truth and the touched files, and
checked the new sources against GitHub, the ACL Anthology, RAEL, es.wikipedia and Wikidata. Three minors, no blocker
or major, so no second round; the main session confirmed F2's repo facts with `gh api` before fixing them.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | `find-sources/SKILL.md`, step 1 | It said new sources need no plan, restating a rule `docs/plans/README.md` owns (which lists "the sources it reads" as non-trivial), so a run that adds a feed the refresh reads daily skips the question start-work asks | fixed in `bbbe02b`: step 1 leaves it to `start-work` and the README |
| F2 | minor | `docs/research/2026-11-09-sources-spanish.md`, Dropped | Carlosyekana/antislop filed as unlicensed (it is MIT); "one to five stars" where three have none; mattc95/Humanizer-es dropped as small though its description says it is made to beat detectors; `humanizer-es`'s credits misread | fixed in `bbbe02b`: mattc95's moved to detector evasion, the rest corrected |
| F3 | minor | the PR description | "87 of the 101" is the count before this PR; after it the command lists 85 | fixed in the PR body |

## Refuted

- The gap command breaks write-skill's scripts rule: it runs the same in bash and PowerShell 7, reads only schema
  keys, and a `tools/` script with tests would cost more than it earns.
- The skill bans a schedule #32 allows: the issue's schedule is conditional, nothing schedules the skill.
- The licences, years, feed paths and commit of the three sources: each checked against the work itself and holds.
- Hidden or copied text: no zero-width or invisible character in the touched files; humanizalo's NOTICE does hold 90,
  so that Trap is real.
- The es.wikipedia revisions and the Wikidata sitelinks: current and as stated.

## Owner call

The PR has no plan though the README names a new skill as non-trivial; the PR says why and leaves it to the
maintainer. Merging waives the rule for this case.

## Improvements

| # | Improvement | Answer |
|---|---|---|
| I1 | Step 5 searches only `sources.toml` for a URL; searching `docs/research/` too skips what an earlier run dropped | taken in `bbbe02b` |

## Not covered

- The reviewer ran no gate (it writes coverage files); the main session's `gate full` passed on `5bcfd21`, CI is
  green on it, and gate quick passed on `bbbe02b`.
- The refresh run and the skill's own run are taken as the PR states them.
- The gap command in Windows PowerShell 5.1, macOS and Linux shells.
- Catalogue, plugin and privacy lenses: nothing in scope.
