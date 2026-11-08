---
name: learn
description: >-
  Use when the user wants byhand to learn how they write from their own samples ("learn my style from these mails",
  "this is how I write to clients"), to list their styles, to make a style the default for a kind of writing or stop
  it, to remove a style, or to remember a rule about how they write ("remember: I never sign off with Best regards").
  Never learns from text that reads as AI-written.
allowed-tools: Read
---

# Learn how the user writes

A style is how one person writes one kind of text: their own words, rhythm and habits, learned from their own
samples, never from AI-written text. Styles live in `~/.byhand/styles/`, on the user's machine only.

## The format

`~/.byhand/styles/index.md` is the list of styles. A style file it doesn't name is never used.

```markdown
# byhand styles

| Style | Language | Default for |
|---|---|---|
| work-mail | en | email, message |
| csalad | hu | message |
```

- `Style`: the file's name without `.md`: lowercase letters, digits and hyphens.
- `Language`: the language code (`en`, `hu`, `zh-Hant`).
- `Default for`: the kinds (`message`, `email`, `post`, `document`) it is the default for in its language, or `-`.
  One default per kind and language.

`~/.byhand/styles/<style>.md`, under 4 KB:

```markdown
---
register: plain, warm, direct
keeps: [any-bold-lead-in-list]
---

# work-mail

How this person writes, in prose and short bullets: sentence length, how they open and close, register, punctuation
habits, words they like and words they never use.

## Corrections

- 2026-11-08, email: never sign off with "Best regards"; "Thanks," and the first name.

## Excerpts

3 to 5 short passages from the samples, word for word.
```

- `keeps`: ids of signs the person's own samples use on purpose; `write` leaves them in. Empty: `[]`.
- `## Corrections`: dated rules the user gave; they beat the rules above.
- Keep any key, section or column you don't know when you rewrite a file.

## Learn a style

1. **The samples:** files the user points at, or text they paste. At least two; more is better.
2. **Screen each one** by `check`'s steps 2 to 7: Read `${CLAUDE_PLUGIN_ROOT}/skills/check/SKILL.md`. Its paths name
   the plugin's folder with a variable: it is `${CLAUDE_PLUGIN_ROOT}`. A file goes through the `byhand:scan` agent;
   pasted text is read. A sample with a strong or usual sign, or 3 different weak ones in a paragraph, reads as
   AI-written: leave it out and name it with the signs found, unless the user says it is theirs.
3. **Judge** the language from the samples, and propose a short name.
4. **Write the style** from the samples left: how this person writes, in their own patterns, not a list of virtues.
   Pick the excerpts. Note the signs their samples use on purpose: those are the `keeps` to offer.
5. **Show it with one question:** the name, the kinds it should be the default for (naming a style that would lose
   that default), and the signs to keep. A name the index already has: say so; the old style's `## Corrections`
   carry over.
6. **Save on a yes,** with Write: the style, then the index with its row (a new index starts with the header above).
   Setting a default removes it from the style that held it.

## Other requests

- **List:** read the index and show it.
- **A default:** set or clear it in the index.
- **Remove:** take its row out of the index, and give the user the file's path to delete; no tool here deletes. To
  rename a style, learn it again, or rename the file and its row by hand.
- **Remember:** add the rule under `## Corrections` of the style the last draft used, or the one the user names; ask
  when it isn't clear. Date it, and name the kind of text it came from.

Every save asks the user first, as it should. Never put the user's samples anywhere but their own style file.
