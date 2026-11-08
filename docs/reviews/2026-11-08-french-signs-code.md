---
subject: "Bootstrap step 4, the French signs (PR #24)"
base: main (3263b22)
head: fd5c698
date: 2026-11-08
round: 1
tier: standard (a fresh reviewer on Claude Opus 5.5, every lens; the fixes verified in the branch's session, with mutants)
verdict: needs-fixes
---

# Review: Bootstrap step 4, the French signs (PR #24)

One round by a fresh reviewer, writing their own plain French work texts (mail in vous and tu, France and Quebec,
Teams and Slack, comptes rendus, a co-op president's speech, a mayor's edito, a retirement speech) and chatbot lines,
running every French pattern under Python and ripgrep, and reading each field against slopcheck-fr, boileau and
avoid-ai-writing-multilingual, as copycheck can't see a translation. The fixes are in the commit after `fd5c698`,
"Fix the French signs from review round 1".

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | blocker | eight signs | Examples rebuilt from the sources' own: fr-stock-openers (ouverture-cliche's frame, then "doit s'adapter", and a `MACHINE` line on the same model), fr-inflated-stakes (grandiloquence's "marque un moment charnière" joined to avoid-ai-writing 29's new era), fr-connector-openers (boileau 13's Avant, its `what` naming the Avant's four connectors). Fields translated from a source: fr-false-contrast `what` and `instead` (contraste-appose), fr-english-headings `instead` (typo-fr casse-titre), fr-hashtag-block `what` (avoid-ai-writing 44). Closer than they should be: the `instead` of fr-article-scaffold, fr-engagement-lines, fr-staged-reveal and fr-slogan-mirrors, and fr-filler-notice's `what` | fixed: new examples on other subjects, each field written from what the sign does in a draft; every field reread against the three sources, which rewrote eight more (`instead` of fr-stock-openers, fr-inflated-stakes, fr-hedge-stack, fr-ai-vocabulary, fr-dash-asides, fr-hashtag-block, fr-copula-avoidance, fr-performative-candour); copycheck finds no run of 6, and at 5 none on a French field |
| F2 | major | fr-stock-openers | Counted alone, and fired on a co-op president's speech, a mayor's edito and a retirement speech; it fired anywhere in a line, though its `what` said "Starts with" | fixed: the maintainer's call, weak, for posts and documents; a check anchored at a line's start; the three speeches held under the weak cluster, a mid-sentence frame left alone; no French check counts alone now, and a test holds it |
| F3 | major | fr-filler-notice | A plain compte rendu reached a weak cluster on its three terms ("Il convient de noter que… Force est de constater que… Il ressort de cet échange que…"), and "Il est essentiel de noter les heures" (write them down) fired | fixed: "que" required after noter and souligner; "force est de constater" and "il ressort de" left to the model's read; the compte rendu is a weak case, at one hit |
| F4 | minor | citations | avoid-ai-writing 17 and 23 are false concessions, not fr-false-contrast; any-closing-summary's French branch cited no French source; any-knowledge-cutoff's "ma date limite / de coupure de connaissances" and "ma dernière mise à jour des connaissances" are in no source | fixed: 17 and 23 dropped; avoid-ai-writing Tier 3 and slopcheck-fr conclusion-rituelle cited; the cutoff keeps only "à la date de mes connaissances" (avoid-ai-writing 28) |
| F5 | minor | French forms | Missed "pour être franc", "soyons franches", "tournants décisifs", "moments charnières", "c'est là qu'entre en jeu X"; fr-calques fired on "J'ai adressé le problème à la DSI" | fixed: the forms added, each in `FORMS`; fr-calques takes adresser with enjeu and défi only, the DSI line in `LEFT_ALONE` |
| F6 | minor | tests/test_office_fr.py | The NFC test normalised inside the test, so it proved nothing of the code; `_weak_hits` compiled terms without the `\b` `validate` gives them; no form for "Pour conclure" | fixed: the NFC test cut; terms compiled with their edges; the form added |
| F7 | minor | AGENTS.md, the plan | "Where the work stands" and the plan's Step 4 row don't name `fr` | refuted: the maintainer's session adds both at merge, as other languages land beside this one |

The maintainer's calls in round 1:

- fr-stock-openers is weak (F2).
- any-assistant-preamble's French branch follows the Chinese and Russian rule: it fires only when the line names the
  reader's text, de votre or de ton e-mail, courriel, message, lettre, texte, annonce or publication. "Avec plaisir.
  Voici une version retravaillée de votre devis, avec la remise de 5 % :" and "Voici une version plus formelle de votre
  courrier :" are a person's, and both are in `OFFICE`.
- any-unfilled-placeholder keeps firing on "[Votre nom]" in a person's template, as English does on "[Your Name]". The
  French strings join the existing bracket group, and the bracket's ending stays as it is: #22 changes it for Markdown
  link text in every language.
- Trim the `what` of fr-false-contrast, fr-inflated-stakes and fr-filler-notice where any-negative-parallelism,
  any-significance-inflation, any-challenges-formula and any-didactic-aside already say it; their terms and checks
  stay. Done.

## Checks

- 20 mutants of the changed checks, one at a time on the catalogue: the preamble without the reader's text or without
  its adjectives, self-reference without ", je", the placeholder and cutoff widened, the stock openers unanchored,
  without "dans un monde", usual, or reading mail, the filler notice without "que" or with "force est de constater",
  fr-calques on "adresser le problème" or "faire sens", the candour terms back to "franche?", the stakes in the singular,
  the staged reveal without its inversion, the hedge with "éventuellement", the contrast without its minimiser,
  hashtags on issue numbers, the engagement lines reading chat. Each fails a test.
- Every French pattern and French branch under ripgrep against Python, on flags, passes, `MACHINE`, `FORMS`,
  `LEFT_ALONE` and `OFFICE`: 360 cases, no disagreement.
- copycheck over 239 files: no run of 6 words; at 5, one hit, on zh-Hant-mainland-terms, not this change.
- `uv run byhand validate`, `uv run byhand render`, `uv run tools/gate.py full --base origin/main`.
