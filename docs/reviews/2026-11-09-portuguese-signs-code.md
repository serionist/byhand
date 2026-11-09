---
subject: "Seed the Portuguese signs (PR #55)"
base: main (daa41b0)
head: 5562141
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: clean (round 8)
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

## Round 3

A fresh reviewer, on ee3c6b3 (the fixes since 38d8cf0, in 8367e81). Verdict: needs-fixes. F12 to F15 hold, each line
the fixes added failing on the 38d8cf0 catalogue and passing now; F11 held only in the test's count.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F16 | major | `pt.toml`, `pt-filler-hinges`, as rendered | "A check is one habit" lives only in the test's counter: the rendered files tell the model to count each different word or phrase, so a paper with Em suma and two hinges was still a cluster for the plugin (both of F11's paragraphs) | fixed in ecee69b: the sign is cut, as most of German's report hinges were in #23's F1. Papers and reports write two hinges in a paragraph, Andrade et al.'s own among them; the sources show no more than that |
| F17 | major | `pt.toml`, `pt-ai-vocabulary`, holístico and sinergia | A nursing paper ("abordagem holística do paciente") or merger news ("sinergias de R$ 400 milhões") with Em suma and a hinge made a cluster; both words rest only on the two skills with no evidence of their own | fixed in ecee69b: both terms cut; the two paragraphs in `REPORTS`, the words in `LEFT_ALONE` |
| F18 | minor | `tests/conftest.py`, `_weak_hits`, with `pt-dash-pivots` | The dash's match runs from the line's start, so a phrase inside it folds the dash in, and the test can count fewer hits than the plugin's rule | wontfix here: `conftest.py` is being changed by #13's PR and this one may not touch it; with the hinges cut, no office line is hidden by it |
| F19 | minor | `pt.toml`, `pt-dash-pivots` | Missed since the seed: a pivot on a line with no closing stop ("Promoção de verão — até 50% de desconto"), and one after an aside pair in the same sentence | wontfix: accepting a line's end would fire on a person's headings and signatures ("Ata — 6 de novembro"); both misses are written in the sign's comment |
| F20 | minor | `tests/test_office_pt.py`, `MACHINE` | Two of F12's date forms (the dash, "no início de 2024") had no line, so a mutation dropping them passed | fixed in ecee69b: a line each |

Refuted: the knowledge cutoff on a person's course with a year, "(" or "—" (the class round 2 accepted); the dash
check's cost (linear: 25 ms on a 160,000-character line in Python, 47 ms on 7.5 MB in ripgrep); the hinge check's
coverage (moot with the cut); cliché speeches with three different stock phrases (what the weak rule is for); clusters
in mail (contrived only); the other strong and usual branches (nothing beyond the recorded trade-offs). Python and
ripgrep agree on all 59 probe lines.

| Improvement | Answer |
|---|---|
| Narrow `conftest.py`'s "a check is one habit" to marks, so the test counts as the rendered rule does | later: `conftest.py` is #13's to change now; the PR names it for a follow-up |

## Round 4

A fresh reviewer, on ec3b614 (the fixes since ee3c6b3, in ecee69b). Verdict: needs-fixes. F16, F17 and F20 hold, each
checked against the ee3c6b3 catalogue (F20 by two mutations, each caught); F18's and F19's reasons are sound
(`origin/13-marks` does change `conftest.py`; a line's end would fire on "Ata — 6 de novembro"). Nothing the cut left
dangles.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F21 | major | `pt.toml`, `pt-ai-vocabulary` (ecossistema de inovação) and `pt-inflated-stakes` (divisor de águas, na era digital) | With Em resumo or Em suma, any two made a cluster in a plain innovation report, telecom report or book review. Ecossistemas de inovação is a term Brazilian law defines (Decreto 9.283/2018); the other two are idioms people write; all three rest only on the two skills | fixed in 1163aca: the three are cut, the report and review in `REPORTS`, the phrases in `LEFT_ALONE`, the flags rewritten |
| F22 | minor | `pt.toml`, `pt-false-contrast` | "Não é só X, é também Y", the additive form the sign's comment calls ordinary, fired (5 of 5 lines) | fixed in 1163aca: the second é or são must open a noun phrase (an article); the reviewer's lookahead is not one Grep runs. A line in `LEFT_ALONE` |
| F23 | minor | PR #55's description | Stale: 10 signs, `pt-filler-hinges`, cruciais, the dropped closing-offer branch, F2's old wording, the native-read list, the counts, the try's cluster | fixed: the description is rewritten for the head |

Refuted: the strong branches on eight more plain lines (only classes rounds 1 to 3 accepted fire); clusters that need
the dash plus a phrase F21 cuts (gone with it); cliché posts with three stock phrases (what the weak rule is for);
"vamos mergulhar" in a dive school's post (2 at most). Python and ripgrep agree on 108 pairs. Of the reviewer's 18
paragraphs, after the fix one reaches 3, a contrived one (Em suma, a real foil contrast and enfatizando).

| Improvement | Answer |
|---|---|
| Write the new `REPORTS` paragraphs without a spaced dash until #13's `conftest.py` change lands | taken |

## Round 5

A fresh reviewer, on b4c5a99 (the fixes since ec3b614, in 1163aca). Verdict: needs-fixes. F21 and F22 hold, each line
the fixes added failing on the ec3b614 catalogue and passing now; F23 holds, checked by hand against the head (signs,
forms, counts, the review's tallies).

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F24 | major | `pt.toml`, `pt-inflated-stakes` (na era da inteligência artificial) and `pt-ai-vocabulary` (ecossistema digital) | F21's class: a 2026 title phrase and a policy term, resting only on the two skills, made clusters with Em suma and enfatizando in plain abstracts, reviews and policy briefs | fixed in b4d3514: both cut; a dissertation abstract and a policy note in `REPORTS`, the phrases in `LEFT_ALONE`, the flags and the counting test rewritten |
| F25 | major | `pt.toml`, `pt-false-contrast` | F22's article rule lost most model foils: 8 of 24 found ("Não são apenas números, são histórias de vida", "não é apenas sobre resultados, é sobre pessoas", "é seu parceiro") | fixed in b4d3514: the second clause must not start ta… (é também, é tão), written `(?:[^t\s]\|t[^a])` and not the reviewer's `[^\Wt]`, as #13 will refuse a `\W` in a class; three `FORMS` lines. It fires on 14 of the reviewer's 15 plain contrastive lines, the class rounds 1 to 3 accept for a weak sign |
| F26 | minor | `any.toml`, `any-unfilled-placeholder`, inserir and insira | A manual's bracketed button fired the usual sign alone ("clique em [Inserir] e escolha Tabela") | fixed in b4d3514: a word must follow the verb; the manual's line is in `REPORTS`. "[Inserir linha]" as a button still fires, English's "[Insert …]" class |

Refuted: clusters only the rendered rule counts, through the dash (F18's gap, and each stacks the dash with two other
tells); two stock cheers in one sentence; the bold label list (a probe artefact, counting one label twice); the strong
branches on 14 more plain lines (only the recorded classes fire). Python and ripgrep agree on 78 pairs.

## Round 6

A fresh reviewer, on 7036648 (the fixes since b4c5a99, in b4d3514). Verdict: needs-fixes. F24, F25 and F26 hold, each
line round 5 added failing on the b4c5a99 catalogue and passing now.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F27 | major | `pt.toml`, `pt-false-contrast` | F25's ending fired on clauses that add or explain (é ainda, é que, é preciso), so a plain summary with Em suma and enfatizando reached 3 in 9 of 14 paragraphs, against 0 at b4c5a99 | fixed in 464e1ec: the sign keeps no check. Portuguese writes one shape to add, to correct and as a model's foil, and the checks of rounds 1, 4 and 5 each missed one or fired on another; `any-negative-parallelism` has no check either. Two of the summaries are in `REPORTS`; the sign's `FORMS` and `LEFT_ALONE` lines go with its pattern |
| F28 | minor | `any.toml`, `any-unfilled-placeholder` | F26's fix lost "[Inserir: morada completa]" and "[Insira: nome da empresa]" | fixed in 464e1ec: an optional colon after the verb; a `MACHINE` line |

Refuted: the clusters left by the reviewer's own candidate fix (a real contrast stacked with a cheer or enfatizando, the
class round 4 called contrived); the ta… foils the round-5 check missed (moot now); "[Inserir imagem]" as a button
(F26's recorded class); "[Inserir_link]" (missed before b4d3514 too); the strong and usual branches on 12 more plain
lines (only recorded classes fire); comment lines' wrap (taste). Python and ripgrep agree on 82 pairs.

## Round 7

A fresh reviewer, on cfd8b79 (the fixes since 7036648, in 464e1ec). Verdict: needs-fixes. F27 holds by the test's
count (both summaries 3 at 7036648, 2 now); F28 holds for inserir. The sign with no pattern renders as the others do,
no test asserts on nothing, and no doc still speaks of a false-contrast check. The PR description matched the head.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F29 | major | `pt.toml`, `pt-false-contrast`'s `what`, as rendered | With no check, the rendered line gave only the bare shape (não é apenas… é…), so a model reading F27's own summary ("não é apenas abusiva, é ainda nula") counts a third hit; round 6's reason sat in a comment, never rendered (F16's class). 5 of 14 plain paragraphs | fixed in 5086400: the sign is cut. `any-negative-parallelism` holds the habit for every language, counts a real foil alone, and leaves out a correction in its own words; the header says so |
| F30 | minor | `tests/test_office_pt.py`, `MACHINE` | No line had "[Insira", so dropping that branch passed every test | fixed in 5086400: "Cliente: [Insira: nome da empresa]" |

Refuted: the strong and usual branches on 18 more person's lines (2 fire, both a bracketed button, F26's class); one
paragraph that clusters through `any-raw-markdown` stacked with two tells (the refuted class). Python and ripgrep
agree on 230 pairs.

## Round 8

A fresh reviewer, on 1a22a94 (the fixes since cfd8b79, in 5086400). Verdict: clean. F29 holds: the sign is gone from
the catalogue and the rendered files, and both summaries count 2 by the test and by the rendered rule. F30 holds:
dropping the insira branch fails exactly the new `MACHINE` line. Nothing dangles; every comment line is 120
characters or fewer; the PR description matches the head.

No new finding. On 20 more person's lines, 3 strong or usual hits, all in recorded classes (a closing offer in a
document, two bracketed buttons); of 24 plain paragraphs from Brazil and Portugal, two reach 3, each three different
stock tells stacked (the refuted class); no sign with no pattern adds a third hit on a routine shape by its rendered
text. Refuted: `any-negative-parallelism` on an additive clause (unchanged by this PR, and its text names a claim
nobody made); the description's wording on F29; the header's finding range. Python and ripgrep agree on 340 pairs.

| Improvement | Answer |
|---|---|
| Cite wikipedia-pt's Paralelismos negativos and evitar-escrita-ia section 2 on `any-negative-parallelism`, which the cut left cited nowhere | taken in e3b1f0f |
| Name the findings the header means (F22, F25, F27, F29), not a range | taken in e3b1f0f |

The review ends here: no blocker or major is open. Left, with their reasons: F18 (wontfix here, #13's `conftest.py`)
and F19 (two dash misses, accepted for a weak sign).
