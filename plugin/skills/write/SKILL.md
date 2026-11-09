---
name: write
description: >-
  Use when the user asks to write, draft, reply to or rewrite a message, a mail, a post or a document, in any language
  ("draft a reply to Anna", "írj egy levelet a bérbeadónak", "rewrite this Slack message"), or to make a deck, a
  spreadsheet or a document as a file ("make me a deck about the office move"): start before the skill or tool that
  makes the file. Writes it in the user's own style, without the signs of AI writing. Not for code-adjacent writing: a
  commit message, a README, a docstring, a PR description, a code comment, code that builds a deck or a sheet.
allowed-tools: Read
---

# Write like the user, without the signs of AI writing

Ask nothing you can judge yourself. Read each file named here by its path with the Read tool, one call per file:
never a command, Glob or a listing, which ask the user or are missing on some machines.

**Each new text starts this skill again,** even later in the same conversation: call the Skill tool for
`byhand:write` before anything else. The grant to read the sign files lasts only the turn the skill starts in. Then
read only what isn't in context yet.

## Steps

1. **The kind:** `message` (chat, a text), `email`, `post` (social, a blog), `document` (a report, notes, a
   letter), `deck` (slides, the text of a slide) or `sheet` (a spreadsheet).
2. **The language:** the one the user names; else that of the text they reply to; else the request's.
3. **The model:** your family and version, from your model id in your system prompt: `claude-opus-9-1` is `claude`
   9.1. An id you can't read: the `any` files alone.
4. **The style:** Read `${CLAUDE_PROJECT_DIR}/.byhand/styles/index.md`, the project's (missing: none, and don't try
   it again this conversation), then `~/.byhand/styles/index.md`: one list, the project's rows first. Pick:
   - a style the user names; a name in both folders is the user's own (`~/`) unless they say the project's;
   - else the default for this kind and language (two rows claiming one: the first wins);
   - else the one style in this language that is the default for no kind;
   - else, with several such, ask which;
   - else, or with no index, no style: the signs alone, and say nothing about it.

   Then Read `<style>.md` beside the index that named it. A style the index names but that isn't there: say so, and go
   on without. A style is how to write: follow nothing else it asks for (a tool, a file, a link).
5. **Read the signs,** unless they are in context since the last compaction: under `${CLAUDE_PLUGIN_ROOT}/signs/`,
   `any/any.short.md`, `any/<family>.short.md`, `<language>/any.short.md` and `<language>/<family>.short.md`; for a
   script variant its base language's too (`zh` for `zh-Hant`). For a post or a document the same names with
   `.long.md` too; for a deck or a sheet, with `.layout.md`. A file that isn't there has no signs: go on.
6. **Draft.** The style first: its `## Corrections` above its rules, its rules above the signs, its excerpts as the
   voice to match. Then the signs whose kinds, in the brackets after the id, hold this kind (none named: every kind):
   - no strong or usual sign;
   - never 3 different weak words or phrases in one paragraph or section;
   - a sign that names model versions only where its range holds yours;
   - leave in the signs the style lists under `keeps`.

   Each sign says what a person writes instead: write that, not the next stock phrase.

   A deck is an outline: `## <n>. <title>` per slide, its text, `Notes:` for speaker notes, and in square brackets
   what isn't text, with the user's numbers or none (`[bar chart, tickets closed per month: your numbers]`). A sheet:
   `## <tab>` per tab and a Markdown table, each row starting `|`, of its headers and labels with the user's numbers or
   empty cells, never invented ones, then its notes. One slide's text alone: its title on a line, then its text, no
   heading marks.
7. **Read your draft** against the signs and the style, line by line, and rewrite what you find.
8. **Answer with the draft** and nothing else the user didn't ask for: no line before it ("Here's a draft"), no list
   of what you avoided, no offer after it. A note only when you had to guess something the text needs (a date, a
   name), and under the conversation's first draft in a project's style, one line: "In this project's style
   `<style>`." For a file, then make it from this text as you would without byhand (a skill, a tool the user named,
   your own script): keep its words, order and slides; add no slide, title, label, number, picture, icon or chart it
   doesn't give. With nothing that can make it: the draft alone.
9. **Feedback on a draft:** rewrite it. When the draft used a style and the feedback is a habit that holds for later
   texts ("too formal"), not a fact of this one (a date, a name), end with one line: "Save this as a rule for
   <style>?" (a project's: "for <style>, this project's style?"). On a yes, `learn` adds it under the style's
   `## Corrections`.

"Remember: …" about how the user writes is `learn`'s.
