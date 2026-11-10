# byhand for Claude Code

Write like a person, in your own voice and language: mail, messages, posts, documents, decks and sheets without the
signs of AI writing.

## Install

```text
/plugin marketplace add serionist/byhand
/plugin install byhand@byhand
```

That's all: no Python, nothing else to install. Its skills read Markdown and run no commands.

## Skills

| Skill | What | Starts |
|---|---|---|
| `/byhand:write` | writes a message, a mail, a post or a document in your style, without the signs of AI writing; for a deck, a sheet or a document made as a file, its text, which whatever makes files in your session then makes into the file | when you ask for one, in any language; not on code that builds a deck or a sheet |
| `/byhand:check` | finds the signs of AI writing in a text or a file, a deck's or a sheet's too (an outline, a PDF, a CSV), with their lines and what a person writes instead; no score | when you ask whether a text reads as AI-written |
| `/byhand:learn` | learns a style from your own samples, decks and sheets among them; lists your styles, sets their defaults, remembers a rule | when you ask it to learn how you write |

`check` hands a file to its `scan` agent, which runs the signs' patterns over it with Grep and reads nothing else.
Text pasted into the chat, or a PDF, gets a reading, without the patterns. byhand makes no file: a `.pptx` or an
`.xlsx` is made, and read, by whatever in your session can, such as Anthropic's `pptx` and `xlsx` skills. Claude Code may ask you to allow a skill the first
time it runs, and saving a style always asks first.

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

A project can have its own styles, a client's or a team's house style, in `.byhand/styles/` in the folder you start
Claude Code in: the same index and files. Start Claude Code in the folder that holds `.byhand/`; a session started in
a subfolder doesn't find it.

- `write` reads the project's index first, then yours: the project's default for a kind and language wins there, and
  the first draft in it ends with a line naming the style. A default for another kind stays yours.
- A style you name is yours first, even when the project has one of that name; say "the project's" for theirs.
- `learn` saves into the project only when you ask ("learn this for this project"). The folder goes where the project
  goes: committed, your excerpts are in the repo for everyone who clones it. Committing it is your call; to keep it to
  yourself, add `.byhand/` to the project's `.gitignore`.
- A style is how to write: `write` follows nothing else a style asks for, a cloned repo's included.

## Updating

New signs come as new versions as they are merged, often. To get them without a command, turn on auto-update:
`/plugin`, Marketplaces, `byhand`, Enable auto-update. Or, for a new version, run this in your shell, then start a
new session:

```text
claude plugin update byhand@byhand
```
