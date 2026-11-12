# byhand

A Claude Code plugin that writes your mail, messages, posts, documents, decks and sheets the way you do, without the
words, structure, formatting and layout that make text read as AI-written.

## Install

Run these in Claude Code:

```text
/plugin marketplace add serionist/byhand
/plugin install byhand@byhand
```

There is nothing else to install or run. Claude Code may ask you to allow a byhand skill the first time it runs.

## Update

New signs are released often, each as a new version of the plugin. To get them automatically, turn on auto-update in
`/plugin` (Marketplaces, `byhand`, Enable auto-update). To update by hand, run this in your shell and start a new
session:

```text
claude plugin update byhand@byhand
```

## Use it

Teaching it your style is optional. byhand works right after the install, and without a style it still leaves out
the signs of AI writing. To get text in your own voice as well, teach it first with one large request (see
[Teach it](#teach-it-optional)).

Ask Claude Code as you always do, in any language. The skills start by themselves.

- Ask for a mail, a Slack message, a post or a document. `/byhand:write` writes it in your style and reads its own
  draft before showing it.
- Ask for a deck or a sheet. `/byhand:write` writes its text, and the file is made by whatever makes files in your
  session (such as the `pptx` skill or a script). If nothing there can make the file, you get the outline.
- Ask "does this read as AI-written?" `/byhand:check` lists the signs it finds, with their lines and what a person
  writes instead. It gives no score.

`/byhand:write` isn't meant for text that lives with code, such as commit messages, READMEs and docstrings.

## Teach it (optional)

Start with one large request that covers everything you write, such as:

```text
Learn my styles from my sent mail and my Slack and Discord messages of the last six months.
Group them by language and by who I write to, and show me each style before you save it.
```

Claude Code reads the messages with the tools your session has, such as an MCP server for your mail or the browser.
byhand brings no such tool of its own. `/byhand:learn` then writes a style from each group, from your own lines only,
and saves it only when you say yes.

The result is a list of styles, such as:

| Style | Language | Default for |
|---|---|---|
| work-mail | en | email |
| team-chat | en | message |
| friends | en | - |
| familie | de | message |
| arbeit | de | email |

`/byhand:write` uses the default for the kind of writing and its language, or the style you name. To see your list or
change a default, ask for it.

You can also say "learn my style from these" with two or more of your own mails, messages, decks or sheets, as files
or pasted text. `/byhand:learn` leaves out any sample that reads as AI-written.

To fine-tune a style later:

- Say what is wrong with a draft. If it is a habit, byhand offers to keep it as a rule in that style.
- Say a rule, such as "remember: I never sign off with Best regards".
- Give it the version you sent instead of its draft. `/byhand:learn` names the habits behind your changes and keeps
  the ones you pick.
- Edit the file. Your styles are short Markdown files in `~/.byhand/styles/` (`%USERPROFILE%\.byhand\styles\` on
  Windows), and they stay on your machine.

A project can have its own styles in its `.byhand/styles/` folder. See [plugin/README.md](plugin/README.md) for the
detail on each skill and on styles.

## How it works

byhand is two sets of Markdown files and the skills that read them:

- The signs say what makes text read as AI-written and what a person writes instead, for each language and for each
  model family and version.
- The styles say how you write. They are learned from your own samples.

A draft loads only the signs for its language, its kind of writing and the model writing it, plus one style. This is
a few thousand tokens, and never the whole catalogue. A model that is newer than the catalogue gets the current signs
of its family.

The following languages have their own signs: English, Chinese (Simplified and Traditional), Japanese, Korean,
Russian, German, French, Hungarian, Spanish, Portuguese, Arabic, Italian, Vietnamese, Turkish and Finnish. Every
language also gets the signs that all languages share. More languages will be added, each from sources written in
that language.

A daily job checks the sources that the catalogue cites and opens an issue when one changes. The new signs are added
in a pull request that a person reads before it is merged.

## Contributing

The most useful contribution is a sign for your language, and you don't need to write code for it. See
[CONTRIBUTING.md](CONTRIBUTING.md). The rules for changing the repo are in [AGENTS.md](AGENTS.md).

## Licence

MIT. See [LICENSE](LICENSE).
