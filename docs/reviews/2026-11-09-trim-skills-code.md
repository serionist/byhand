---
subject: "Trim the plugin's skill files to what changes behaviour (PR #96)"
base: main (4c0a640)
head: d37590c
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer, Opus 5.5, every lens; its nits checked against the files by the author)
verdict: clean
---

# Trim the skill files: code review

The reviewer read the four files against their old versions, the plans and the review records each rule came from,
swept the rendered sign files for the rules the skills now leave to them, and ran gate quick and `tests/test_render.py`
(77 tests). No blocker, major or minor.

## Refuted

- The weak cluster rule cut from `check` step 7 and `learn` step 2: `render._rules` prints it atop every file that
  holds a weak sign, #76's mark exception included; `any/check.md` and `any/check.layout.md` are always read, and
  `learn`'s screen reads them through `check` step 4.
- The version-range note cut from `write` step 6: every file with a ranged sign prints it; no ranged sign sits in a
  file without it.
- The restart rule, read by path, the triggers and anti-triggers, the deck and sheet hand-off and outline (the
  `^## 1\.` and `^\|` graders), `allowed-tools: Read`: each kept.
- `check` step 5's paths: "the full paths of `scan.md` in step 4's folders" with the variant's base and the layout
  files; `learn` keeps its `${CLAUDE_PLUGIN_ROOT}` note.
- `check` step 3 without "as the check files name families": a family passed as "ChatGPT" leaves the ranged sign out
  of `ran`, and step 6 then reads the text for it.
- `scan`'s contract: `ran` always last, never a rejected id, a missing file skipped; the description still names
  `scan.md` (check-budget plan, P4).
- `learn`: steps 1 to 7 still numbered so; the default rule said once in the format.
- The numbers in the PR and CHANGELOG: each file's and description's bytes match.

## Not covered

The eval runs and the reruns of `passes-any-tacked-on-analysis` (out of bounds for a reviewer); they rest on the PR's
Tested by. No eval runs `check` on a file, so step 5 rests on the four runs by hand.

## Improvements

| Improvement | Answer |
|---|---|
| PR body: the cluster rule is the same rule `check.md` prints, not the same words | taken |
| PR body: the restart rule is kept, not "as it was" (in `write` it moved above Steps, its tail cut) | taken |
| `write` line 52 was 130 characters, the only line over 120 | taken: rewrapped (+3 bytes, 4,581) |
| Rebase on `origin/main` (#95) so the CHANGELOG reads in order | left: the force push it needs was refused here; the merge is clean, and the squash puts it in order |
