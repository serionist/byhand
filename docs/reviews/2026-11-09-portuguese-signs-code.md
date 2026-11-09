---
subject: "Seed the Portuguese signs (PR #55)"
base: main (daa41b0)
head: 5562141
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: needs-fixes
---

# Seed the Portuguese signs: code review

The reviewer ran the office test, `gate.py quick`, and Python against ripgrep 14.1.1 on 94 probe lines (they agree). It
wrote 48 person's lines and 46 model lines against the five strong and usual Portuguese branches, 20 paragraphs of
plain documents against the weak cluster, and scanned `pt.toml` and the office test for 5-word runs shared with the
three text sources (only fixed phrases).

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `pt.toml`, `pt-ai-vocabulary` and `pt-inflated-stakes` | Plain papers, inspection reports and quarterly results made weak clusters: 7 of 10 such paragraphs reached 3, on robusto, abrangente, crucial, mais do que nunca and no cenário atual beside one hinge. Those are English's list translated, or phrases a source says people use, and no source measures models writing them more | fixed in e63cd10: the five terms are cut; three such reports are in `REPORTS`, and `LEFT_ALONE` holds their words |
| F2 | minor | `pt.toml`, the header and four signs | "A list item of either is used only beside a second source" did not hold item by item, and some items were in no source (importa referir, vale salientar, O resultado?, A diferença?, não é simplesmente, não se trata de… trata-se de) | fixed in e63cd10: every item is named by a source; the header says a sign from either skill rests on both, or on another source beside it |
| F3 | minor | `pt.toml`, `pt-ai-vocabulary`'s citation | wikipedia-pt's vocabulary section lists English words with glosses and says English results don't carry over | fixed in e63cd10: dropped from the sign |
| F4 | minor | `any.toml`, `any-knowledge-cutoff`, Portuguese branch | A person's continuing-education course, safety training or workout fired the strong sign ("até à minha última atualização de conhecimentos em suporte básico de vida") | fixed in e63cd10: the noun must end the phrase or come before its date; three such lines in `REPLIES`, two more model lines in `MACHINE` |
| F5 | minor | `any.toml`, `any-assistant-closing-offer` | "Há mais alguma coisa em que possa ajudar?" is the stock human service close, and fired in a support script | fixed in e63cd10: the branch is dropped; the script is in `REPORTS` |
| F6 | minor | `any.toml`, `any-ai-self-reference`, Portuguese branch | It missed não tenho a capacidade (which Spanish has) and não posso acrescentar (wikipedia-pt's own verb) | fixed in e63cd10: both in the branch, each with a `MACHINE` line |
| F7 | minor | `any.toml`, `any-assistant-preamble`, Portuguese branch | It missed Segue, Abaixo está, aprimorada, mais amigável and two joined adjectives | fixed in e63cd10: each in the branch, with `MACHINE` lines |
| F8 | minor | `tests/test_office_pt.py`, `REPLIES` | "Como modelo de linguagem, não tenho preferência" passed only on the singular; the plural fires, the trade-off #53's round 5 accepted | fixed in e63cd10: the line is cut |
| F9 | minor | `pt.toml`, `pt-dash-pivots` | A reply of two sentences with its speech tag after the second fired ("— Já vou. Espera só um bocadinho — disse a Marta.") | fixed in e63cd10: a line with a dash before the sentence is skipped; the line is in `LEFT_ALONE` |
| F10 | minor | `pt.toml` flags, `FORMS` | `pt-stacked-connectors`' flags kept humanizer-pt-br's example shape and connector order; the inflated-stakes flags and a form followed its opener-and-local-shop shape | fixed in e63cd10: rewritten on other subjects and shapes |

## Refuted

- Self-reference on a person's verdict about a model ("Como modelo de linguagem, não posso garantir que seja melhor
  que o Gemini"): the trade-off #53's rounds 4 and 5 accepted; the other lines found were contrived or a quoted bot.
- The preamble on a colleague returning a document ("Claro! Aqui está o seu texto revisto:"): the French (#24) and
  Spanish rule accepts this cost.
- "Queres que eu resuma isto…" in a document: the sign reads documents only, as in Spanish.
- Placeholders on brackets: "[a confirmar]" and "[pendente]" pass; a slot left in a person's template fires on purpose.
- A cluster in mail through the dash: only a contrived mail reached 2.
- The citations' numbers and section names, the alphabetical order, copying: as claimed.
- CONTRIBUTING.md's native-read line: the plan's line for the whole language set, added with Spanish.

## Improvements

| Improvement | Answer |
|---|---|
| `test_no_portuguese_check_counts_alone` follows from `test_every_portuguese_sign_is_weak_until_a_native_review` | left: the Spanish test keeps the same pair, and the first names the rule the plan sets |
| Technical and academic paragraphs in `REPORTS` | taken, with F1 |

## Not covered

Whether a native speaker finds the signs right; the plugin sessions, which the main session ran.

## Round 2

A fresh reviewer, on 38d8cf0 (the fixes since 5562141, in e63cd10). Verdict: needs-fixes. F1 to F10 hold: it ran every
list of the office test against the 5562141 catalogue, and each line the fixes added fails there and passes now.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F11 | major | `pt.toml`, `pt-filler-hinges` | Each hinge was a term of its own, so a plain paper or report with two different hinges and Em suma or Em conclusão made a cluster: 4 of 9 such paragraphs reached 3 ("Em suma, a horta… Vale destacar que… É importante ressaltar que…"). Andrade et al.'s own paper writes two | fixed in 8367e81: the hinges are one check, which counts once; two such paragraphs in `REPORTS`, and `test_two_different_hinges_count_once` |
| F12 | minor | `any.toml`, `any-knowledge-cutoff` | F4's ending lost model forms: "em 2023,", "(outubro de 2023)", "— em abril de 2024 —", "no início de 2024" | fixed in 8367e81: the reviewer's tested ending; two more `MACHINE` lines, and F4's person's lines still pass |
| F13 | minor | `any.toml`, `any-assistant-preamble` and `any-ai-self-reference` | F7's segue, abaixo está, aprimorada, amigável and F6's capacidade are in no cited Portuguese source, and segue fired on a Brazilian returning a friend's text ("Claro! Segue seu currículo revisado:") | fixed in 8367e81: those words are out; the joined second adjective and acrescentar, which a source shows, stay; the friend's line is in `REPLIES` |
| F14 | minor | `pt.toml`, `pt-dash-pivots` | F9's fix hid a pivot after an aside pair or a dialogue tag on the same line, and an aside closing after a ? or an abbreviation still fired | fixed in 8367e81: the reviewer's tested check; two `FORMS` lines and two `LEFT_ALONE` lines. Still fires, accepted for a weak sign: an aside that ends on an abbreviation and its dash at the line's end |
| F15 | minor | `pt.toml`, `pt-ai-vocabulary`'s citation | It still named `adjetivo-robusto.yaml` after robusto was cut | fixed in 8367e81 |

Refuted: the self-reference on a person's "Como modelo de linguagem, não tenho…" (the trade-off #53 accepted); the
joined adjective on a person's document (the noun must be the reader's text); the knowledge cutoff on a person's
course followed by a comma (the model's own words, as in Spanish); a cluster in mail (2 at most); Python against
ripgrep (they agree on all 58 probe lines).

| Improvement | Answer |
|---|---|
| A test that two different hinges count once | taken, with F11 |
