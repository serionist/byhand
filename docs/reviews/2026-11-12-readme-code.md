---
subject: "Rewrite the README in plain sentences, with a Teach it section (PR #112)"
base: main (ba26c2f)
head: 83dde54
date: 2026-11-12
round: 1
tier: standard (one fresh reviewer on Claude Fable 5.2; findings checked against the code by the main session)
verdict: needs-fixes
---

# Review: Rewrite the README in plain sentences, with a Teach it section (PR #112)

One fresh agent read the pack (`git diff origin/main...HEAD` at `83dde54`), AGENTS.md, REVIEW.md, issue #109 and the
README sentence by sentence, each claim against the line that makes it true. The README describes how `write` picks a
style as PR #111 makes it, so those claims were read against #111's branch. One major, three minors: **needs-fixes**.
The minors are fixed in `b3662e3`. The major is half answered and waits for the maintainer.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `README.md`, Teach it, and Use it's first lines, which send the reader there | The large request ("Learn my styles from my sent mail and my Slack and Discord messages of the last six months") is stated as fact, and no line of `learn` makes it true: `learn` takes "files the user points at or text they paste", and has no step that fetches messages or sorts them into several styles. A user with a mail tool pastes the request first, as the README says, and what happens was seen by nobody | open, half answered. Tried twice with twelve invented messages in a folder (Checks): `learn` started, grouped them into three styles, showed each and saved nothing. The README now says Claude Code fetches the messages and that a folder of files works with no tool. Fetching from a mail or chat tool is still untried: the maintainer decides whether to try it on a real mailbox or to lead with the folder |
| F2 | minor | `README.md`, the order of `write`'s picks | Three gaps against #111: the list stopped before the fourth pick, so with the README's own table an English post is written in `friends` where the README predicted no style; the second pick left out the language, so a German mail to a friend looked like a case for `friends`; and the line under a draft comes under a style's first draft in a conversation, not each one | fixed: the fourth pick, "in the text's language", "under the first such draft". `b3662e3` |
| F3 | minor | `README.md`, Use it, `check` | "It is for your own writing, not a detector" was gone from both READMEs, so a reader who wants to judge someone else's text takes `check` for a detector | fixed: "it is for your own writing and is no detector". `b3662e3` |
| F4 | minor | `README.md`, the order of `write`'s picks | Those lines hold only once #111 is merged as it stands; nothing checks the order of the merges | recorded: the PR says "Merge after #111". If #111's order or its line changes before it merges, these lines are read again |

Refuted: "isn't meant for" text that lives with code promises too much (it promises nothing); the feedback offer
without a style (it sits under fine-tuning a style, "in that style"); "saves a style only when you say yes" (`learn`
saves on a yes); the language list (16 sign files match the 16 named); "a few thousand tokens" (unchanged from
`main`, within the budgets); "rewritten with byhand's own `write` skill" as tool attribution (byhand is not a tool the
gate names, and `PR text` passed); the anchor and the relative links (all resolve); "a pull request that a person
reads before it is merged" (`refresh-agent.yml` opens a draft the maintainer reads and merges); no version or
changelog section (docs move no version); "they stay on your machine" beside project styles (said of
`~/.byhand/styles/`); the example table (the index's format, real kinds, invented names); "byhand reads no mailbox"
(the plugin has no server and no hook, and its skills pre-approve `Read`); the Writing rules (no em dash, banned
word, bold or American spelling; no line over 120).

Facts dropped from the old README, each still in `plugin/README.md`: no Python; saving a style always asks first;
byhand makes no file; your version pasted or as the file you changed; what `check` reads of a deck or a sheet; the
index; how a project's styles travel. Dropped and not needed: that `write` "seldom starts on" code text; the deck
example and "slide by slide".

Not covered: implementation, catalogue-contract, plugin-contract and harness-integrity had nothing to read.

Improvements: none beyond the fixes.

## Checks

- `uv run tools/gate.py full` on `b3662e3`: 22 checks, 4,135 tests.
- The large request, with files: Claude Code 2.1.321, claude-fable-5-2, the plugin as on `main` (0.4.0),
  `claude --plugin-dir plugin -p` with `--allowedTools Read,Skill,Glob`, in a folder holding twelve invented messages
  (four English mails to two customers, four English chats to two friends, four German messages to family). The
  request: "Learn my styles from the files in the samples folder: they are mails and messages I sent. Group them by
  language and by who I write to, and show me each style before you save it." Two runs, the same in both: `learn`
  started, read every file, found no sample that reads as AI-written, proposed three styles (customer mail, friends,
  German family) with their excerpts, and saved nothing.
- Not tried: the request as the README words it, which needs a tool that reads a mailbox or a chat; a second turn in
  which a style is saved; more than twelve samples.
