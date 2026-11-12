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
| `/byhand:learn` | learns a style from your own samples, decks and sheets among them; lists your styles, sets their defaults, remembers a rule, learns rules from your edits of a draft | when you ask it to learn how you write, or say yes to `write`'s offer |

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
- Changed a draft before you sent it? Give `write` your version, pasted or as the file you changed. It offers to learn
  from the changes; `learn` lists the habits behind them as numbered rules, before and after, and adds the ones you
  pick under `## Corrections` of the style the draft used. A date or a name you changed is no habit, and your version
  never becomes an excerpt. A correction that repeats an older one replaces it; past 4 KB, `learn` asks which to drop.
- `write` uses the style you name. With none named, it takes the first style in the text's language that is the
  default for no kind and whose name plainly is who the text is for or its occasion (`vendor` for a mail to a
  supplier, `friends` for one to a friend), else the default for the kind and language. It never stretches a name:
  with no plain fit the default holds. The first draft in a style picked by its name ends with a line naming it.
- With no default for the kind either, `write` uses your one style in that language that is the default for nothing,
  whatever its name, and asks which when there are several. With no style it writes by the signs alone.
- Name a style after its reader or its occasion (`clients`, `friends`): `write` picks by the name, and `learn`
  proposes one. A style that is the default for a kind stays with that kind, whatever its name.

A project can have its own styles, a client's or a team's house style, in `.byhand/styles/` in the folder you start
Claude Code in: the same index and files. Start Claude Code in the folder that holds `.byhand/`; a session started in
a subfolder doesn't find it.

- `write` reads the project's index first, then yours: a style of the project's picked by its name, then the project's
  default for the kind and language, then your own. The project's default wins over your own styles there, one whose
  name fits included, and the first draft in a project's style ends with a line naming it. A default for another kind
  stays yours.
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
