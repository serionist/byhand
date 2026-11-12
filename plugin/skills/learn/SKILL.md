---
name: learn
description: >-
  Use when the user wants byhand to learn how they write from their own samples ("learn my style from these mails",
  "this is how I write to clients"), to list their styles, to set or clear a style's default for a kind of writing, to
  remove a style, or to remember a rule about how they write ("remember: I never sign off with Best regards").
allowed-tools: Read
---

# Learn how the user writes

A style is how one person writes one kind of text, learned from their own samples, never from AI-written text. The
user's own live in `~/.byhand/styles/`, on their machine; a project's in `${CLAUDE_PROJECT_DIR}/.byhand/styles/`,
which goes where the project goes. Read both indexes, `${CLAUDE_PROJECT_DIR}/.byhand/styles/index.md` (missing, or
the home folder itself: no project styles) and `~/.byhand/styles/index.md`.

Read each file named here by its path with the Read tool, one call per file: never a command, Glob or a listing, which
ask the user or are missing on some machines.

**Each new request about styles starts this skill again,** even later in the same conversation: call the Skill tool
for `byhand:learn` first. The grant to read the plugin's files lasts only the turn the skill starts in.

## The format

Each folder's `index.md` lists its styles. A style file its index doesn't name is never used.

```markdown
# byhand styles

| Style | Language | Default for |
|---|---|---|
| work-mail | en | email, message |
| csalad | hu | message |
```

- `Style`: the file's name without `.md`: lowercase letters, digits and hyphens.
- `Language`: the language code (`en`, `hu`, `zh-Hant`).
- `Default for`: the kinds (`message`, `email`, `post`, `document`, `deck`, `sheet`) it is the default for in its
  language, or `-`. One default per kind and language in each index: setting one takes it from the style in that
  index that held it. A project's default leaves the user's own in place.

`<style>.md`, beside its index, under 4 KB:

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

1. **The samples:** at least two, files the user points at or text they paste; decks and sheets in the forms
   `check` step 1 takes.
2. **Screen each one** by `check`'s steps 1 to 7: Read `${CLAUDE_PLUGIN_ROOT}/skills/check/SKILL.md`. Its paths name
   the plugin's folder with a variable: it is `${CLAUDE_PLUGIN_ROOT}`. A sample in which a sign counts reads as
   AI-written: leave it out and name it with its signs, unless the user says it is theirs.
3. **Judge** the language from the samples, and propose a short name that says who the style is for or its occasion
   (`clients`, `csalad`): `write` picks a style by it when the user names none and the style is the default for no
   kind.
4. **Write the style** from the samples left, and from the user's own lines only: never a quoted reply, a forwarded
   message or code. How this person writes, in their own patterns, not a list of virtues. A deck style says what
   their slides hold: titles as topics or sentences, how much text, bullets or sentences, notes or none; a sheet
   style, their headers, units and notes. Pick the excerpts. Note the signs their samples use on purpose: those are
   the `keeps` to offer.
5. **Show it with one question:** the name, the kinds it should be the default for (naming a style that would lose
   that default), and the signs to keep. A name the index already has: say so; the old style's `## Corrections`
   carry over. For a project, a name `~/.byhand/styles/index.md` has is taken: propose another. Into a project with
   no index yet, the question also says that the excerpts are the user's own words and the folder goes where the
   project goes if it is committed; to keep it to themselves, add `.byhand/` to the project's `.gitignore`.
6. **Save on a yes,** with Write or Edit, into `~/.byhand/styles/`, or `${CLAUDE_PROJECT_DIR}/.byhand/styles/` when
   the user asked for this project ("for this project", "in this repo"): the style, then the index with its row (a new
   index starts with the header above). Write nothing else into a project.

## Other requests

- **List:** show both, the project's marked as this project's.
- **A default:** set or clear it in the index that holds the style; a name in both: ask which.
- **Remove:** take its row out of the index that holds it (a name in both: ask which), and give the user the file's
  path to delete; no tool here deletes. To rename a style, learn it again, or rename the file and its row by hand.
- **Remember:** add the rule under `## Corrections` of the style the last draft used, in the file the draft read, or
  the one the user names; ask when it isn't clear. A project's style: say it is this project's when you save. No
  style yet: say so, and offer to learn one from their samples. Date it, and name the kind of text it came from. A
  repeat of an older correction replaces it, newly dated; past 4 KB, ask which old corrections to drop or fold into
  the rules.

## Learn from an edit

The user's version of a byhand draft is Remember with rules you find:

1. **The two versions:** theirs and the draft of yours it changes (unclear which: ask), or both from the user. The
   file the draft became: Read it again; a `.pptx`, `.xlsx` or `.docx` Read can't read: its text from what reads it
   in the session, else ask for a PDF, a CSV or the text. A deck or a sheet is compared by its words and their order,
   without the outline's marks (`## <n>.`, `Notes:`, `[...]`, `## <tab>`, `|`). No draft: say so, guess no rule and
   ask for it (their answer starts this skill again); with no style either, offer to learn one from other samples, as
   this version is none.
2. **The style:** the one that draft used, or none; both from the user: as Remember picks it. None: say so and offer
   to learn one from samples, without comparing.
3. **The habits:** keep a change only if it would hold for the next text of this kind (a sign-off, a word, sentence
   length, register, bold or bullets cut), never a fact of this text (a date, a name, a point). One the style already
   holds is no new rule: say so, and leave it out.
4. **One question:** each as a short rule with its before and after, numbered: which to keep? A rule that puts in
   what a sign names says so (the signs from the draft, else Read `any/any.short.md` and `<language>/any.short.md`
   under `${CLAUDE_PLUGIN_ROOT}/signs/`, a script variant's base language's too; a file that isn't there has no
   signs). A style they would take past 4 KB: ask in it what to drop, as in Remember. Silence saves nothing.
5. **Save the picks** as Remember does. The user's version is never a sample or an excerpt: the lines they kept are
   yours.

Never put the user's samples anywhere but their own style file.
