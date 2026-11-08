# byhand for Claude Code

Write like a person, in your own voice and language: mail, messages, documents and decks without the signs of AI
writing.

Not released yet. The skills come with the first version, `0.1.0`; the
[bootstrap plan](https://github.com/serionist/byhand/blob/main/docs/plans/2026-11-06-bootstrap.md) designs them.

## Install

```text
/plugin marketplace add serionist/byhand
/plugin install byhand@byhand
```

That's all: no Python, nothing else to install. Its skills read Markdown and run no commands.

## Skills

| Skill | What | Starts |
|---|---|---|
| `/byhand:write` | writes a message, a mail, a post or a document in your style, without the signs of AI writing | when you ask for one, in any language |
| `/byhand:check` | finds the signs of AI writing in a text or a file, with their lines and what a person writes instead; no score | when you ask whether a text reads as AI-written |
| `/byhand:learn` | learns a style from your own samples; lists your styles, sets their defaults, remembers a rule | when you ask it to learn how you write |

`check` hands a file to its `scan` agent, which runs the signs' patterns over it with Grep and reads nothing else.
Text pasted into the chat gets a reading, without the patterns. The first time a skill runs in a session, Claude Code
asks you to allow it.

## Your styles

Say "learn my style from these" with two or more of your own mails, messages or posts, as files or pasted. `learn`
leaves out any sample that reads as AI-written, shows you the style, and saves it only when you say yes, to
`~/.byhand/styles/`. Your styles stay on your machine.

- `~/.byhand/styles/index.md` is the list: a style, its language, and the kinds of writing it is the default for. A
  style file it doesn't name is never used.
- A style is a short Markdown file you can edit: how you write, the signs you keep on purpose, `## Corrections` (say
  "remember: …" to add one) and a few excerpts.
- `write` uses the default for the kind and language, a style you name, or none; with no style it writes by the signs
  alone.

## Updating

`/plugin marketplace update byhand`.
