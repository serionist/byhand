# Fit questions

`fit-plan` asks these of a written plan, and the plan's author asks them too, while writing it (`start-work`). Each
answer is an improvement that clears `REVIEW.md`'s bar (Improvements), or nothing: "none" is a good answer. Not here:
defects in the plan as written, which are `review-plan`'s findings.

| Question | Ask | For example |
|---|---|---|
| Fit | Does it fit the issue, `AGENTS.md` (the rules, the one-way doors), `REVIEW.md`, the design as it stands (`README.md`, `plugin/README.md`, the catalogue's schema) and the maintainer's calls (the issue's comments, the plans it or the plan names)? Who uses it, and does it serve them: people who write mail, messages, documents and decks with Claude Code, in their own language; the plugin's skills and agents, which read the catalogue and a style; the repo's contributors, people and agents? | simready-forge #7: two PRs, so the marketplace plugin never runs ahead of PyPI |
| Mechanical over manual | A step someone must remember, a rule only a review keeps: could the CLI, the catalogue's schema, the gate, a test or a hook do it? A manual step the plan keeps says why none can | each sign's examples run as a test, so a sign that flags human writing fails CI instead of a review |
| Reuse | Does something the package, the catalogue, the plugin, `tools/` or the skills already have do this, or most of it? | one brief per draft, built by the CLI, which every writing skill reads |
| Cut or simplify | What can go; what belongs in another issue; a rare corner it designs for; a new skill where a parameter on an old one would do, or the reverse | a sign kept `any` until a source names the model it belongs to |
| Prior art | How other tools find or remove AI writing (blader/humanizer and its translations, Wikipedia's "Signs of AI writing", detectors' published features, style guides in each language), and Claude Code's skills, hooks and plugins; where the plan differs, and why | why a catalogue split by language and model, where blader/humanizer loads one list |
| The change's own | The concern its issue, an issue it must stay open to, or the maintainer names, asked as a question of its own | does it keep the human skill levels for decks and sheets open? |

## Prior art

Looked up, never recalled (`AGENTS.md`, Look up APIs before coding against them):

- Context7, where it is on (`.mcp.json`, turned on by `.claude/settings.local.json.example`);
- the sources the catalogue lists, and the repos and pages the plan names, read as data;
- the repo: the package, the catalogue, the plugin's skills and agents, `tools/`.

The fit says what it could not look up.

## The change's own question

The session that starts the fit adds one when the issue, an issue the change must stay open to, or the maintainer
names a concern of its own, and the brief carries it. Without one, the five stand alone.

## What an improvement holds

As `review-plan`'s `lenses.md` says what a finding holds:

- an id, `I1`, `I2`, ..., and the question it answers;
- the plan section;
- what to change;
- why it is better, and who notices;
- the line it rests on, quoted with its `file:line`.

"None" for a question with nothing to offer. At the end, one line for the defects noticed on the way, when there are
any, each with its plan section: they go to `review-plan`'s Round 1, never fixed by the fit.
