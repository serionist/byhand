---
subject: "Bootstrap step 4, the German signs (PR #23)"
base: main (3263b22)
head: a5897ad
date: 2026-11-08
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens; fixes verified by the main session, with mutants)
verdict: needs-fixes
---

# Review: Bootstrap step 4, the German signs (PR #23)

Round 1 by a fresh reviewer, who wrote their own plain German work texts (mail in Sie and du, Teams, minutes, audit and
inventory reports, invoices with Swiss and German prices) and chatbot closers, ran every pattern under Python and
ripgrep, and copycheck over wikipedia-de, avoid-ai-writing-multilingual and the Ströer post. No licence blocker.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | de-summary-formulas, de-emphasis-phrases, de-sowohl-triad, de-list-announcers, any-closing-summary | 5 of 10 plain report paragraphs reached 3 weak hits: "Alles in allem lässt sich sagen", "Es sei darauf hingewiesen", "Abschließend sei noch erwähnt", "Es ist wichtig zu bedenken", "eine große Palette von" | fixed, the maintainer's call: the official and instruction phrases go. de-summary-formulas is cut, every term being report German; de-emphasis-phrases keeps only the calques of "it's important to note" (wichtig zu bemerken or betonen); de-list-announcers keeps "breite Palette" and "Vielzahl an". Seven report paragraphs, three of them the reviewer's in our own words, are held under 3 |
| F2 | major | any-assistant-preamble, German branch | Fired strong on a person's reworked text that names no one's: "Gerne! Hier ist eine überarbeitete Version mit deinen Anmerkungen:" | fixed, the maintainer's call (the Chinese and Russian rule): it fires only when the line names the reader's text ("Version Ihres Textes", "Fassung deiner E-Mail"). Selbstverständlich!, Sehr gerne! and "Gerne, hier ist" added. Both lines join `OFFICE`; `tests/test_office.py`'s "Natürlich! Hier ist eine kürzere Fassung:" names a text now ("… Ihrer Notiz:") |
| F3 | major | any-assistant-closing-offer, German branch | The PR's narrowing dropped wikipedia-de's own closer, and the new branch missed most chatbot closers | fixed, the maintainer's call: no to the narrowing, widen instead. "Gibt es noch etwas, bei dem/womit ich (Ihnen/dir) helfen/behilflich sein kann" is back; objects (den Text, den Entwurf, es, daraus) and verbs (formuliere, umschreibe, ergänze, erstelle, mache, kürzer fasse) widened; soll-ich and lass-mich-wissen branches added. The sign reads documents only, so the office test now checks each text against the signs its kind reads, and a test holds that a service desk's line meets only a document sign. `tests/test_office.py`'s German line is main's again. Twelve closers in `MACHINE` |
| F4 | major | any-ai-self-reference, German branch | Missed "Als KI habe ich keine …", "Als Sprachmodell …", "Als KI-Modell …", "verfüge ich nicht über" | fixed: the nouns and the verb added, the noun list and the negation kept; "Als Projektleiterin habe ich keine Zeit" and "Als KI-Beauftragte habe ich keine Admin-Rechte" pass. The suggested "Als Sprachmodell kann ich nicht GPT-4 nehmen" now fires, as Sprachmodell is a noun of the list; the mutant it was to kill is the design now, and "Als Sprachmodell habe ich Llama genommen" kills the one without the negation |
| F5 | minor | de-sowohl-triad | Its check fired on a plain audit report listing three kinds of receipt | fixed, the maintainer's call: no check, for the model's read; a test holds it |
| F6 | minor | de-em-dash | Fired on prices: "CHF 20.—", "1.250,— €" | fixed, the maintainer's call: no hit on a dash after a comma or a full stop; both prices in `OFFICE` |
| F7 | minor | several | Forms missed: verb-final "Obwohl spezifische Details rar sind"; "bleibenden Erbes", "reichen Traditionen"; "Tolle Frage!" | fixed, each with a line; "Es ist jedoch wichtig …" and "Dabei ist es wichtig …" follow the one emphasis phrase that survived F1 |
| F8 | minor | citations | any-ai-self-reference cited wikipedia-de's "Eindeutige Anzeichen", which doesn't name it; de-em-dash cited a section about the short dash | fixed: the introduction's "Eindeutige Indikatoren", which names a note that an AI wrote the text; de-em-dash cites SKILL-DE's pattern 18 alone, which names the long dash |
| F9 | minor | any-unfilled-placeholder | The new "[… einfügen]" branch brought a bracket ending of its own, and the German words fire on Markdown link text | fixed: the German words stay in the shared branch, the extra branch is gone; the ending is #22's, for every language. A person's own template keeps firing: the maintainer's call |
| F10 | minor | `tests/test_office_de.py` | `_weak_hits` counted one hit per term, though a term's alternatives are different phrases | fixed: each top-level alternative counts as a phrase, with word edges as `validate` gives; de-participle-asides lists its participles as alternatives; a test holds two participles as 2 |

The maintainer also cut `de-english-constructions`: with no check and no example in its source, a model would read
"macht Sinn" in a person's text as a sign. 14 German signs remain.

## Round 2

**Where:** `a5897ad..851e3b8`, a fresh reviewer. **Verdict:** approved, with four minors fixed at once; no third round.
F1 to F10 held.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| m1 | minor | any-assistant-preamble, German branch | Case-insensitive, `ihre[sr]` took a third person's text: "Gerne! Hier ist die überarbeitete Fassung ihrer Rede, Frau Klein hat sie heute Morgen geschickt:" fired strong | fixed: the polite form is case-sensitive, `(?-i:Ihre[sr])`, which ripgrep honours under `-i`; the line, and one with "ihr überarbeiteter Entwurf", join `OFFICE` |
| m2 | minor | the same branch | Missed "Natürlich! Hier ist Ihr umformulierter Text:", which round 1 swapped out of `MACHINE`, and comparatives ("eine professionellere Version Ihrer E-Mail") | fixed: a second branch takes the possessive before the adjective (case-sensitive Ihr, or dein, euer), and any `-ere` comparative; the line is back; "Ihre überarbeitete Präsentation" still passes |
| m3 | minor | any-ai-self-reference, German branch | Missed a word between ich and the negation: "kann ich leider keine", "habe ich leider keinen Zugang", "kann ich das nicht" | fixed: up to two words, and keinen, keiner, keines; three lines in `MACHINE` |
| m4 | minor | any-assistant-closing-offer, soll-ich branch | Fired on first-person FAQ headings in a document: "Soll ich ihn selbst erstellen …?", "Soll ich es notariell machen lassen?" | fixed: erstellen and machen only after daraus; three FAQ lines join `OFFICE` |
| m5 | minor | any-unfilled-placeholder | "[Datum einfügen]" no longer fired once round 1 dropped its branch | fixed: a branch for a bracketed slot ending in einfügen, eintragen or ergänzen, beside the shared bracket, whose ending stays #22's; two lines in `MACHINE` |

The maintainer accepted the three trade-offs the reviewer raised: a person's "Soll ich den Text noch kürzen?" at the foot
of a draft document they share fires the closing offer; "Als Sprachmodell darf ich keine US-Cloud nutzen" fires the
self-reference; a press release's register can reach 3 weak hits.

Checked: 9 mutants of the changed checks, one at a time, each failing a test; the changed checks under ripgrep;
copycheck at 6 and 5 words; `validate`, `render` and `gate.py full --base origin/main`.

## Closed

Round 2's minors are fixed in the commit after `851e3b8` that carries this section, verified by their mutants in the
main session. The maintainer approved without a third round.

## Checks

- 25 mutants, one at a time, of every check this round changed and of `_weak_hits`: each fails a test.
- The changed checks under ripgrep (Claude Code's Grep) on 14 lines: the same hits as Python.
- copycheck over the downloads: 0 runs of 6 words; at 5, one hit, ordinary English in `zh-Hant-mainland-terms`.
- `uv run byhand validate`, `uv run byhand render`, `uv run tools/gate.py full --base origin/main`.
