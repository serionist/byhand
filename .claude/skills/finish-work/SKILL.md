---
name: finish-work
description: >-
  Use when a change is ready ("finish", "wrap up", "we're done", "open the PR"). Checks the docs moved with the
  change, runs the full gate, runs the refresh against the live sources when it changed, tries the plugin
  in a real session for what no test reaches, commits, opens a draft PR, reviews it with review-code until it is clean, and asks
  the maintainer to mark it ready or merge it; the maintainer squash-merges.
---

# Finish a change

Done means `uv run tools/gate.py full` passed, `REVIEW.md` is answered and `review-code` is clean, not that the work
feels complete. `main` takes PRs only, and the maintainer squash-merges them (`AGENTS.md`, How a change lands).

## Steps

1. **Docs in the same change.** Check each thing that describes the change moved with it: `README.md` and
   `plugin/README.md` for what users see, `CHANGELOG.md` under Unreleased when users notice it, `AGENTS.md` for a
   changed path, command or rule, and the plan when the work departed from it (where and why). A plan with a progress
   log gets the step's row. Write them the way `AGENTS.md` asks.
2. **The gate:** `uv run tools/gate.py full`. Fix every failure; never weaken a test, a check or an ignore to pass.
3. **The live sources,** for a change to the refresh: run it by hand against the sources the catalogue lists, into a
   folder git ignores, never a PR. Note which sources it read and which it could not, in which languages, and what it
   proposed. The PR says whether it ran.
4. **Try it in a real session,** for a change under `plugin/` or to a command a skill runs, which no test reaches:
   with the installed copy turned off (`claude plugin disable byhand@byhand`), start `claude --plugin-dir plugin` in
   an empty folder and ask for the writing the change touches (a short mail, a Slack message, a deck outline), in at
   least one language other than English when the change is about languages. Check that the skill started by itself,
   which signs and style it loaded, and the text it wrote. Note the Claude Code version and the model, what worked, and
   what you could not show. Turn the installed copy back on.
5. **Commit:** a plain imperative subject that says what changed, a body that says why, `Refs #<n>`. No tool
   attribution: `commit-msg` refuses it.
6. **Open a draft PR.** Write the body to `.local/pr-body.md` from `.github/pull_request_template.md`. Push with
   `git push -u origin HEAD` (`pre-push` runs gate quick), then `gh pr create --draft --title "<plain imperative
   sentence>" --body-file .local/pr-body.md`. The title becomes the commit subject on `main`. Say it's open and how
   to see it all: the PR's Files tab, or `git diff origin/main...HEAD`.
7. **Review** with `review-code` until it is `clean`. Commit each round's fixes with gate quick passing, and the
   record in `docs/reviews/`. Put the verdict and the record's path in the body's Review section:
   `gh pr edit <n> --body-file .local/pr-body.md`.
8. **CI** on the head commit: `gh pr checks <n> --watch`. A red check is fixed, never skipped.
9. **Ask the maintainer,** as one question with a recommendation: mark it ready (`gh pr ready <n>`), merge it, or
   leave it a draft.
   - If `main` moved: `git fetch origin`, `git rebase origin/main`, `git push --force-with-lease`. A rebase that
     changes code needs the gate again.
   - Merge only on the maintainer's word: `gh pr merge <n> --squash --delete-branch --subject "<title> (#<n>)"
     --body-file .local/squash.md`, a body that says what and why and ends `Refs #<issue>` or `Closes #<issue>`. No
     HTML comments, no tool attribution.
10. **Clean up** after the merge: `git switch main` and `git pull`; a worktree goes with `git worktree remove <path>`
    from the main checkout. Work that turned up on the way becomes an issue (`gh issue create`).

## Done means

- `gate full` passed on the head commit, `review-code` is clean for exactly this code, and the PR says whether the
  live tests ran and how the plugin was tried.
- The PR is ready for the maintainer, merged on their word, or left a draft by their choice.

## Never

- Open, mark ready or merge a PR with a failing gate or CI, or with a review of different code.
- Mark a `REVIEW.md` question yes without its evidence.
- Add AI co-author trailers, "Generated with" lines or session links: commits, PR titles, PR bodies.
- Push to `main`, merge without the maintainer's word, or push to someone else's branch.
- Bump the version outside a release PR: `pyproject.toml`, `plugin.json` and every `byhand==` pin move
  together, in the PR that dates the release in `CHANGELOG.md`.
