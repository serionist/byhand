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

## Round 2

**Where:** `fd5c698..a099910`, read by a fresh reviewer, who compared each term list and alternation with the source
lists it could come from, and wrote plain reports and chatbot lines of their own. **Verdict:** needs-fixes. F1 to F6
held but for what F8 found.

The maintainer's call: a regular expression's alternation order counts as a list's order, so ours is our own, always.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F8 | blocker | fr-inflated-stakes, fr-stock-openers, fr-filler-notice, fr-staged-reveal; fields | (a) Alternations in slopcheck-fr's own order: the era and fast-world openers (ouverture-cliche), il convient / il est … de noter (il-convient-de-noter, minus one), fausse-revelation's first four. (b) fr-english-headings' `what` was casse-titre's message and its `instead` casse-titre's and gabarit-anglais's fixes. (c) Close: fr-filler-notice's `what` (il-convient-de-noter's message), fr-inflated-stakes' `instead` (grandiloquence's fix) | fixed: every French term list and alternation, and the French branches in `any.toml`, put in our own order after a check against each source list it could come from (slopcheck-fr, avoid-ai-writing-multilingual, boileau), which also reordered fr-performative-candour, fr-article-rituals, fr-ai-vocabulary, fr-calques, fr-engagement-lines, fr-false-contrast, fr-slogan-mirrors and fr-hedge-stack; items a person writes cut ("à l'ère du numérique" and "du digital", "la réponse est simple", "le constat est sans appel"); the fields written anew from what the sign does in a draft, and every field reread beside slopcheck-fr's message and fix lines, which rewrote fr-false-contrast's and fr-staged-reveal's `what` too; copycheck at 4 words finds only the checks' own strings and ordinary French |
| F9 | major | fr-false-contrast, fr-filler-notice, any-closing-summary | A plain report still reached 3 weak hits: "En conclusion, il ne s'agit pas de supprimer le service, mais de le regrouper…" with "Il convient de noter que…"; a CSE compte rendu with "Soyons lucides"; "l'intérêt de cette convention n'est plus à démontrer" | fixed: "il ne s'agit pas de X, mais de Y" counts only with simplement, juste or seulement; "n'est plus à démontrer" is left to the model's read; three reports of our own in `WEAK_CASES` and `OFFICE`, each at 2 |
| F10 | minor | any-assistant-preamble, French branch | Missed lines that name the reader's text: "de votre mail", "version révisée", "plus concise / courte / claire", "plus professionnelle et plus claire", "de ton post", "Voici votre e-mail reformulé :" | fixed: each added, with its line in `MACHINE`; the reader's-text anchor stays, and the eager yes is still needed |
| F11 | minor | fr-performative-candour | "Soyons honnête", in the singular, was missed | fixed, with a form |

### Checks

- 9 mutants of round 2's changes: the contrast's il ne s'agit pas without a minimiser, the filler notice with "n'est
  plus à démontrer", the staged reveal with "la réponse est simple", "soyons honnêtes" in the plural only, the stakes
  with "à l'ère du numérique", the preamble without "et plus X", without "votre e-mail reformulé", without mail and
  post, or without the reader's text. Each fails a test.
- ripgrep against Python: 383 cases, no disagreement.
- copycheck over 239 files: no run of 6; at 5, only zh-Hant-mainland-terms; at 4, the French checks' own strings in
  their `flags` and "dans la salle de".
- The largest French draft: 13,515 bytes of 16,384.

## Round 3

**Where:** `a099910..0f2f2c0`, read by a fresh reviewer against slopcheck-fr, boileau, avoid-ai-writing-multilingual
and wikipedia-fr-sources. **Verdict:** needs-fixes.

The maintainer's rule, so no one has to judge an order again: every French alternation, term list and list of examples
in a `what` or `instead` runs in alphabetical order of its plain text, accents and case ignored, unless that changes
what a regex matches (a shorter alternative that is a prefix of a longer one, with no edge after it): then the longer
comes first, with a comment. fr.toml's header states it, and a test holds it.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F12 | blocker | fr-false-contrast, fr-slogan-mirrors, fr-stock-openers, fr-performative-candour, fr-filler-notice, fr-engagement-lines, fr-inflated-stakes, fr-ai-vocabulary's `what` | Round 2's "own order" was slopcheck-fr's order reversed, alternation by alternation; a reversed list is still the source's list | fixed: every French alternation, term list and list of examples alphabetical, the French branches in `any.toml` too; `test_french_alternations_run_in_alphabetical_order` parses each French sign's simple alternations of plain words (49 groups) and `test_french_term_lists_run_in_alphabetical_order` each term list; no prefix needed the exception, as fr-calques' articles now carry their own space or apostrophe |
| F13 | blocker | fr-performative-candour's terms, fr-false-contrast's `what`, fr-article-scaffold's `what` | Still in a source's order: honnetete-performative's (la vérité, sans langue de bois, pour être), correction-deux-temps' (seulement, juste, simple), wikipedia-fr-sources' (summary up top, FAQ, sources at the end) | fixed: alphabetical, the scaffold's `what` rewritten as a list of its own |
| F14 | blocker | fr-dash-asides `flags` | "la démo — répétée dix fois — a planté" followed slopcheck em-dash's bad example: noun, dashed participle aside, verb | fixed: a dashed aside that is a full clause, then a dash before a closing comment |
| F15 | minor | fr-english-headings | "## Key Takeaways" was gabarit-anglais's first bad example, word for word | fixed: "## Wrap-Up", in `flags` and `what` |
| F16 | minor | fr-engagement-lines | The "Et vous" branch kept et-vous's shape and its {0,80} bound | fixed: "Et toi ?" or "Et vous ?" alone, or opening a question that runs to the line's end, with no bound; `FORMS` and `LEFT_ALONE` lines |
| F17 | minor | any-assistant-preamble, French branch | Missed "de votre rapport", "CV", "compte rendu" | fixed: in both forms, with `MACHINE` lines |

The last read, every French field and list beside the three sources: five more `flags` sat on a source example's frame
(slopcheck-fr's "Soyons honnêtes : …", "Il convient de noter que …", "Dans cet article, nous allons …", "Nous sommes
ravis d'annoncer … !", and correction-deux-temps' "n'est pas un simple … : c'est le [image]"), and fr-calques' on
calque-anglais's "Il faut adresser ce problème": each rewritten in another shape. fr-staged-reveal's two "entre en jeu"
terms became one.

### Checks

- 7 mutants: an alternation reversed, a term list out of order, "Et vous" only before a comma, fr-calques without l',
  the staged reveal without the words before "entre", the preamble without rapport, CV and compte rendu in either
  form. Each fails a test.
- ripgrep against Python: 394 cases, no disagreement.
- copycheck over 239 files: no run of 6; at 5, only zh-Hant-mainland-terms; at 4, the French checks' own strings in
  their `flags` and "dans la salle de".
- The largest French draft: 13,417 bytes of 16,384.

## Round 4

**Where:** `0f2f2c0..12b48e4`: the alphabetical order, the reshaped examples, and the merge of main (#22, #23), whose
four `any` checks and one feed the maintainer's session joined by hand. Approved: copycheck at 6 and 5 finds nothing,
no example sits on a source's frame, and the merge keeps every German and Russian branch byte for byte.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F15 | minor | fr-false-contrast `instead` | "a figure or an example" broke the header's alphabetical rule | fixed: "an example or a figure" |
| I1 | improvement | tests/test_office_fr.py | the order test skips groups with `?`, `[` or `\` (15 of 58) and the French branches in `any.toml`; all are in order today | later: with the rule in `propose-signs` for every language |

## Closed

The maintainer merged on round 4's approval.
