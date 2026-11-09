# byhand

A Claude Code plugin that writes the way you do: your mail, messages, posts and documents, in your language and your
own style, without the words, structure and formatting that make text read as AI-written.

## Install

```text
/plugin marketplace add serionist/byhand
/plugin install byhand@byhand
```

That's all: no Python, nothing else to install or run. Claude Code may ask you to allow a byhand skill the first
time it runs, and saving a style always asks first.

## Update

For a new version, run this in your shell, then start a new session:

```text
claude plugin update byhand@byhand
```

## Use it

- **Write as you always do.** Ask Claude Code for a mail, a Slack message, a post or a document, in any language.
  `/byhand:write` starts by itself, writes it in your style without the signs of AI writing, and reads its own draft
  before showing it. It isn't meant for text that lives with code, such as commit messages, READMEs and
  docstrings, and seldom starts on it.
- **Teach it your style.** "Learn my style from these" with two or more of your own mails or messages, as files or
  pasted. `/byhand:learn` leaves out any sample that reads as AI-written, shows you the style, and saves it only when
  you say yes. You can have several, and make one the default for each kind of writing and language.
- **Tell it what you don't like.** After a draft in one of your styles, say what's off. If it's a habit, it offers to
  keep it as a rule in that style; "remember: …" does the same.
- **Check a text.** "Does this read as AI-written?" `/byhand:check` lists the signs with their lines and what a person
  writes instead. No score: it is for your own writing, not a detector.

Your styles live in `~/.byhand/styles/` (`%USERPROFILE%\.byhand\styles\` on Windows), on your
machine only: an index and one short Markdown file per style, which you can edit.

## How it works

byhand is two sets of Markdown files and the skills that read them:

- **Signs:** what makes text read as AI-written, per language and per model family and version. English, Chinese
  (Simplified and Traditional), Japanese, Korean, Russian, German, French, Hungarian, Spanish, Portuguese, Arabic,
  Italian, Vietnamese and Turkish have their own; every language gets the signs all languages share. Each sign says what a person writes instead.
- **Styles:** how you write, learned from your own samples.

Each draft loads only the signs for its language, its kind of writing and the model writing it, plus one style: a few
thousand tokens, never the whole catalogue. A model newer than the catalogue gets its family's current signs.

The catalogue stays current: a daily job checks the sources it cites and opens an issue when one changes, and the new
signs come as a pull request a person reads.

## Next

- **More languages,** each from sources in its own language (`0.3.0`), **decks and sheets** (`0.4.0`), **learning
  from your edits** (`0.5.0`).

## Contributing

A sign for your language helps the most, and needs no code: see [CONTRIBUTING.md](CONTRIBUTING.md). The rules for
changing the repo, for people and agents, are in [AGENTS.md](AGENTS.md).

## Licence

MIT. See [LICENSE](LICENSE).
