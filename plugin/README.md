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
| `/byhand:check` | finds the signs of AI writing in a text or a file, with their lines and what a person writes instead; no score | when you ask whether a text reads as AI-written |

`check` hands a file to its `scan` agent, which runs the signs' patterns over it with Grep and reads nothing else.
Text pasted into the chat gets a reading, without the patterns.

## Updating

`/plugin marketplace update byhand`.
