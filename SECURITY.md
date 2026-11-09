# Security

byhand reads what you write, and learns your styles from samples of your own writing. What keeps that safe is that
your samples and styles stay in a folder on your machine, that its skills pre-approve only tools that read, and that
nothing a web page says reaches the catalogue until a person has read it and merged it.

## Reporting

Report it privately through a
[GitHub security advisory](https://github.com/serionist/byhand/security/advisories/new), never in an issue, which
anyone can read. Say what you did, what happened and what you expected, the smallest steps that show it, and which
version or commit you tested, on which operating system and Claude Code version. Take any key, token or real writing
out of what you send.

You get an answer within a week. A fix goes out as a release, and the advisory is published with it, crediting you
unless you ask not to be named.

## What counts

- A sample or style of yours leaving the folder byhand keeps it in: written elsewhere, logged, put in a report or an
  error message, or sent anywhere but the model you run Claude Code with.
- Text from a page the refresh reads reaching the catalogue or a skill without a person merging it, or being followed
  as an instruction.
- A page the refresh reads reaching the refresh agent's token or permissions (`refresh-agent.yml`): its OAuth token
  leaving the job, a GitHub token in the model's reach, a file written outside the folders it may edit, or a PR it
  opens that closes, mentions or links where it shouldn't.
- A plugin skill that runs a command or writes a file without Claude Code asking you first.
- A secret written where it shouldn't be: a key or token in the catalogue, a report or a log.

What does not count:

- The model you run doing what it does with the text you give it; report its flaws to its maker.
- A sign in the catalogue that is wrong: that is a bug, so open an issue.
- Someone who already runs code as your user.

## Supported versions

| Version | Fixes |
|---|---|
| `main` | Every fix, until the first release |
| The latest release | Every fix, from the first release |
| Older releases | None before `1.0`: update to the latest |

From `0.1.0` until `1.0`, only the latest release gets fixes.
