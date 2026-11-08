---
subject: "The English preamble sign narrowed to the reader's text (PR #35)"
base: main (5a1905b)
head: 5158751
date: 2026-11-08
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens; fixes verified by the main session, with mutants)
verdict: needs-fixes
---

# Review: The English preamble sign narrowed to the reader's text (PR #35)

Round 1 by a fresh reviewer, who wrote 50 lines people send with their own file (decks, contracts, HR letters, tutors,
editors, lawyers, assistants drafting for a boss) and 58 chatbot preambles, and ran the check under Python. No `rg` on
its PATH: Grep safety rests on the schema's check and on the constructs the branch uses; the main session ran the
changed check under Claude Code's Grep tool.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | any-assistant-preamble, English branch | A text word that describes another noun counted as the reader's text, as any word could follow it: "Of course! Here's your revised email signature:", "a revised version of your email policy:", "of your incident response plan:", "of your email list:", "of your intro deck:" fired strong | fixed: the text is the head noun, followed only by a comma or a linking word (about, for, from, in, on, so, that, to, which, with) before the colon. Six of these lines join `OFFICE`; "of your email so it sounds warmer:" still fires, in `MACHINE` |
| F2 | minor | the same branch, a register word after more or less | Fired on register words about things other than text: "a more neutral version of the logo:", "a less formal version of the dress code:", "a more professional version of the deck:", while "a more polished version of the deck" passed | fixed: the register branch fires bare, before for, that, which or with, or of a text ("of the email", "of your message"); the three lines join `OFFICE`, "a more formal version of the email:" and "for your manager:" join `MACHINE` |
| F3 | minor | the same branch | Missed within the rule: "an edited version of your email", corrected, proofread, rephrased, reworked, streamlined, enhanced; a register word without more or less ("a professional version of your email"); "your article", "your caption", "your personal statement"; "a revised version of the text you provided" | fixed: the words added to the version-of-your-text slot, alphabetically, with the register words; enhanced, rephrased, reworked and streamlined in the your-text slot too, but not corrected, edited or proofread, a tutor's "your corrected essay"; article, caption and personal statement added; "of the <text> you provided, shared or wrote". Report, proposal and summary stay out ("your revised valuation report" joins `OFFICE`). Six `MACHINE` lines |

## Refuted

- An editor, tutor or organiser returning the reader's own essay, bio or speech fires ("Sure! Here's a revised version
  of your essay:"): the maintainer's rule, as in the Russian, German and French branches.
- The text-to-send branch fires on a colleague's "Sure! Here's a polite email you can send to the supplier:": a branch
  from before, narrowed here to need a register word, and the PR says so; "an email you can send to the landlord"
  passes.
- A third person's text: "your mum's speech", "your team's announcement" and "Anna's email" pass, as `[\w-]+` takes no
  apostrophe.
- List order: every word list in the changed branch is alphabetical; `['’]s| is` and the order of the branches are
  structure, which no rule covers.
- Grep safety: no look-around or backreference in the English branch.
- The new tests fail without the change: 16 new `OFFICE` lines fire on the old check, 6 new `MACHINE` lines were missed.
- Plurals and odd spacing ("your emails", "Sure!Here's") miss: rare.

## Improvements

| Improvement | Answer |
|---|---|
| Openers the English branch never reads: "Sure - here's", "Sure thing!", "Certainly! Below is", "**Sure!**", from before this PR | later: an issue to file; this session had no permission to open one |
| F1's lines in `OFFICE`, so the head-noun rule is pinned by a test | taken |

Not covered: privacy-and-sources, plugin-contract and harness-integrity had nothing in scope.

## Checks

- Python (`re`) and Claude Code's Grep tool, case-insensitive, on the 30 English `MACHINE` preamble lines and the 51
  English "here" lines in `OFFICE`: 30 found and none, in both.
- 6 mutants of the fixes, one at a time: any word after the reader's text, a register version of any object, no "text
  you provided", no register word in a version of your text, no edited or proofread, no article or personal statement.
  `tests/test_office.py` fails on each, as it did on the 11 mutants of the first commit.

## Round 2

**Where:** PR #35, `5158751..1818cb8`, a fresh reviewer who read the fixes and probed them with 67 invented person
lines and 30 chatbot lines under Python. **Verdict:** needs-fixes, on F4. F1 to F3 hold: F1 by `OFFICE`'s email
signature, email policy, response plan, email list, intro deck and message template lines; F2 by the logo, dress code
and deck lines; F3 by `MACHINE`'s edited, proofread, streamlined, professional-version, text-you-provided and reworked
caption lines.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F4 | major | any-assistant-preamble, English branch, the tails after the text and after a register version | Round 1's fix stopped finding common preambles the first commit found: "a revised version of your email incorporating your feedback:", "based on your feedback", "tailored to the role", "without the jargon", "of your email - more concise and direct", "(shorter and warmer)", "of your essay below", "a more professional version you can send:", "a more formal version, keeping your main points:", "suitable for a client", "of it:", "of the paragraph above:" | fixed: after the text, a dash or a bracket, above, below or that, or a linking word (about, addressing, based, for, from, in, incorporating, on, so, tailored, to, using, which, with, without); after a register version, a comma, for, in, suitable, that, which, with, you can, or "of it", "of that", "of this". 15 lines join `MACHINE`, the em dash one as an escape |
| F5 | minor | the register branch | A register word about a non-text object still fires after for, with or that: "a more professional version for the client deck:", "a less formal version with the team photos:", "a more neutral version that uses the grey palette:" | wontfix: the rule's letter, a register word after more or less, fires on them, and they fired before this PR; narrowing for to text objects would lose "a more formal version for your manager" |
| F6 | minor | the head-noun rule | "a revised version of your email to-do list:" fired, as `to\b` matched before the hyphen; "of your email, chat and file-sharing policy:" fires through the comma | fixed for the first: a linking word needs a space after it (that and above or below keep a word edge, for "that's more concise" and "below:"), and the line joins `OFFICE`. wontfix for the second: a list of nouns after the reader's text is rare, and a comma is how "of your email, with a warmer close" goes on |

Refuted: "a more recent version of your email" fires, by the rule: it names the reader's text. F3's added words bring
no false positive among the reviewer's 67 lines.

Improvement: no test pinned "shared" or "wrote", nor rephrased, enhanced, corrected or conversational. Taken:
`MACHINE` lines for wrote, rephrased, enhanced, corrected and conversational. Left: shared, one of three verbs
after "the text you", the other two pinned.

Checks: Python and Claude Code's Grep tool on the 44 ASCII English `MACHINE` preamble lines and the 53 English "here"
lines in `OFFICE`: 44 found and none in both. 10 mutants of the round's changes, one at a time (no dash or bracket, no
above or below, that needing a space, a linking word without a space after it, no incorporating, tailored or without,
no you can, no suitable or in, no comma, not of it, no shared or wrote): `tests/test_office.py` fails on each.
