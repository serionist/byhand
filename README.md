# byhand

A Claude Code plugin that writes the way you do: your mail, messages, documents and decks, in your language and your
own style, without the words, structure and layout that make text read as AI-written.

Not released yet: this is the repo's harness, and [the bootstrap plan](https://github.com/serionist/byhand/blob/main/docs/plans/2026-11-06-bootstrap.md) designs the
first version.

## How it works

byhand is two sets of Markdown files and the skills that read them:

- **Signs:** what makes text read as AI-written, in each language. They ship with the plugin.
- **Styles:** how you write, learned from your own samples. They stay on your machine.

`/byhand:learn` makes a style. After that you ask Claude Code for a mail as you always do, and byhand writes it in your
style, without the signs. There is nothing else to install or run.

## What it will do

- **Know the signs.** A catalogue of what gives AI writing away ("delve", "it's worth noting", rule-of-three lists, a
  tagline under every title, bold lead-ins on every bullet), for the 100 most spoken languages and for the models
  that write them. Each sign says what a person writes instead.
- **Stay current.** A scheduled job reads the sources the catalogue lists and opens an issue when one changes; the
  new signs come as a pull request, which a person reads before it lands.
- **Load little.** For each draft, only the signs for its language and the model writing it, plus one style. Not the
  whole catalogue.
- **Write in your style.** It learns your styles from your own samples, several if you write differently for
  different people, and uses the one you set for each kind of writing, or asks. Your samples stay on your machine.
- **Start by itself** when you ask Claude Code for a mail, a message, a document or a deck.

## Install

```text
/plugin marketplace add serionist/byhand
/plugin install byhand@byhand
```

## Contributing

A sign for your language helps the most, and needs no code: see [CONTRIBUTING.md](CONTRIBUTING.md). The rules for
changing the repo, for people and agents, are in [AGENTS.md](AGENTS.md).

## Licence

MIT. See [LICENSE](LICENSE).
