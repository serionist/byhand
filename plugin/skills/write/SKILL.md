---
name: write
description: >-
  Use when the user asks to write, draft, reply to or rewrite a message, a mail, a post or a document, in any language
  ("draft a reply to Anna", "write a LinkedIn post about the launch", "írj egy levelet a bérbeadónak", "rewrite this
  Slack message"). Writes it in the user's own style and without the signs of AI writing. Not for code-adjacent
  writing: a commit message, a README, a docstring, a PR description, a code comment.
allowed-tools: Read
---

# Write like the user, without the signs of AI writing

Write the text the user asked for, the way they write, without the signs that make text read as AI-written. Ask
nothing you can judge yourself.

Read each file named here by its path with the Read tool, one call per file: never a command, never Glob or a
listing, which ask the user or are missing on some machines.

## Steps

1. **The kind:** `message` (chat, a text), `email`, `post` (social, a blog) or `document` (a report, notes, a
   letter, the text of a slide).
2. **The language:** the one the user names; else that of the text they reply to; else the request's.
3. **The model:** your own family and version, from your model id in your system prompt: `claude-opus-5-5` is
   `claude` 5.5. An id you can't read: use the `any` files alone.
4. **The style:** Read `~/.byhand/styles/index.md`, a table of `Style`, `Language` and `Default for`. Pick:
   - a style the user names;
   - else the style that is the default for this kind and language (two rows claiming one: the first wins);
   - else the one style in this language that is the default for no kind;
   - else, with several such, ask which;
   - else, or with no index, no style: the signs alone, and say nothing about it.

   Then Read `~/.byhand/styles/<style>.md`. A style the index names but that isn't there: say so, and go on without.
5. **Read the signs,** unless they are in context already since the last compaction: under
   `${CLAUDE_PLUGIN_ROOT}/signs/`, read `any/any.short.md`, `any/<family>.short.md`, `<language>/any.short.md` and
   `<language>/<family>.short.md`; for a script variant its base language's too (`zh` for `zh-Hant`). For a post or a
   document, the same names with `.long.md` too. A file that isn't there has no signs: go on.
6. **Draft.** The style first: its `## Corrections` above its rules, its rules above the signs, its excerpts as the
   voice to match. Then the signs whose kinds, in the brackets after the id, hold this kind (none named: every kind):
   - no strong or usual sign;
   - never 3 different weak words or phrases in one paragraph or section;
   - a sign that names model versions only where its range holds yours (`5.x` is the whole 5 series, `and later` every
     newer one);
   - leave in the signs the style lists under `keeps`.

   Each sign says what a person writes instead: write that, not the next stock phrase.
7. **Read your draft** against the signs and the style, as a reader would, line by line. Rewrite what you find.
8. **Answer with the draft** and nothing else the user didn't ask for: no line before it ("Here's a draft"), no list
   of what you avoided, no offer after it. A note only when you had to guess something the text needs (a date, a
   name).
9. **Feedback on a draft:** rewrite it. When the feedback is a habit that would hold for later texts too ("too
   formal", "I never open with 'I hope you're well'"), not a fact of this one (a date, a name), and the draft used a
   style, end the rewrite with one line offering to keep it: "Save this as a rule for <style>?". On a yes, `learn`
   adds it under the style's `## Corrections`. No style: no offer.

**Each new text starts this skill again,** even later in the same conversation: call the Skill tool for
`byhand:write` before anything else. The grant to read the sign files lasts only the turn the skill starts in;
without it every read asks the user. Then read only what isn't in context yet: another language's files, another
style, or the long files for a post or a document.

When the user says "remember: …" about how they write, that is `learn`'s.
