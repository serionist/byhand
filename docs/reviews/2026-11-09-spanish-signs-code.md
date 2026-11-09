---
subject: "Seed the Spanish signs (PR #53)"
base: main (52331c8)
head: 220f326
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: needs-fixes
---

# Seed the Spanish signs: code review

The reviewer ran `gate.py quick`, the office, order, catalogue and render tests, and Python against ripgrep 14.1.1 on
every Spanish and `any` pattern over 284 Spanish lines (they agree). It also ran the old `_weak_hits` of each office
file on `origin/main` against the shared one in `tests/conftest.py` over every string, whole and in paragraphs, for
every kind: 11,970 comparisons, no difference.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `any.toml`, `any-ai-self-reference`, the Spanish branch | A strong sign that reads every kind fired on a person's contrast: "Usamos Copilot como asistente de IA, no como sustituto…", "Lo venden como inteligencia artificial, no como…". A bare `no` after the role is not the model's first person; the source shows "Como modelo de lenguaje, no puedo…" | fixed: the branch needs `(yo) no dispongo/puedo/soy/tengo`; three contrast lines in `REPLIES` of `tests/test_office_es.py` |
| F2 | minor | `tests/test_office_es.py` | About 18 lines were humanizer-es's own test fixtures, verbatim or with words swapped, not invented text | fixed: rewritten on our own subjects, with the Colombian and Lucía mails, the commission report and `es-filler-hinges`' `passes`, which a 4-word scan against every humanizer-es file also found; only the fixed phrases the checks find are still shared |
| F3 | minor | `any.toml`, `any-unfilled-placeholder`'s citation | "[Tu nombre] 15 times": `raw/` holds it 8 times | fixed: "8 times" |
| F4 | minor | `es.toml`, `es-service-script`'s `instead` | It translated humanizer-es D11's closing sentence, in its order | fixed: "Name the cause and the date that now holds, then sign off once." |
| F5 | minor | `any.toml`, `any-knowledge-cutoff`, the Spanish branch | The year form caught a person's own note ("Hasta mi última actualización en marzo de 2025, …") | fixed: only `de conocimientos?`; the person's line is in `REPLIES` |
| F6 | minor | the PR body | It said every Spanish form had a `MACHINE` line: the two weak ones are in `FORMS`, and `[Su nombre]` had none | fixed: a `[Su nombre]` line, and the body says where the weak forms are |

## Refuted

- A preamble false positive on a colleague's "Claro, aquí tienes tu texto corregido:": the French rule (#24) accepts
  this cost, a reworked version that names the reader's text, and the Spanish branch follows it.
- `any-assistant-closing-offer` on "¿Quieres que lo resuma para el comité?": it fires, but the sign reads documents only.
- The placeholder on an aside such as "[su empresa ya lo tiene]": rare in mail, and a slot in a person's template fires
  on purpose.
- Grep compatibility, the citations, copying (no 6-word run; at 4 only the fixed phrases), the alphabetical order, the
  budgets, the docs and the PR's counts: as claimed.

## Improvements

| Improvement | Answer |
|---|---|
| `test_a_spanish_sign_that_counts_alone_has_no_pattern` asserts no usual or strong Spanish sign at all: name it for that | taken: `test_every_spanish_sign_is_weak_until_a_native_review`, with why it is stricter than the plan |
| CHANGELOG's "each Spanish sign" read as if the Spanish forms in the `any` signs were weak too | taken: "each of Spanish's own signs" |

## Not covered

Whether a native speaker finds the signs right; the plugin sessions, which the main session ran. The "4 of 30 model
texts" behind `es-service-script` was unclear: the main session counted the apology for the inconvenience (lamentamos,
inconvenientes, sentimos las molestias), and the citation now says so.

## Round 2

A fresh reviewer, on 8d22e0a (the fixes since 220f326). Verdict: needs-fixes. F2 to F5 and both improvements hold; F1
held only in part.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `any.toml`, `any-ai-self-reference`, the Spanish branch | Still open: the branch started anywhere in a line, so a person's comma splice after a verb fired ("Lo venden como IA, no puedo creer que sea solo un buscador", "La contratamos como asistente de IA, no tengo queja de ella") | fixed: the role opens a sentence or follows "pero"; three such lines in `REPLIES` |
| N1 | minor | the PR body | Stale on F1, F3, F5 and F6, and its Review section empty, while round 1 called F6 fixed | fixed: the body is updated |
| N2 | minor | `tests/test_office_es.py`, `FORMS` | The rewritten `es-false-contrast` line used a semicolon, so no test held the comma, the usual way to write it | fixed: the line has its comma, and a semicolon line beside it |
| N3 | minor | `any-ai-self-reference`, the Spanish branch | It missed "como modelo de lenguaje de IA", "Como IA no puedo" without the comma, and no poseo, no cuento con, no me es posible | fixed: all in the branch, each with a `MACHINE` line |

Refuted: that the round-1 swaps in `LEFT_ALONE` made a test weaker (they test the same edges, or stricter ones); a
Grep incompatibility in the new branch (ripgrep 14.1.1 agrees with Python).

## Round 3

A fresh reviewer, on 2c940d5 (the fixes since 8d22e0a). Verdict: needs-fixes. N2 and N3 hold, and N1 but for two byte
counts; F1 held only in part again.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| R3-1 | major | `any.toml`, `any-ai-self-reference`, the Spanish branch | A person's verdict on a tool has the model's words: "Como asistente de IA, no tengo queja de ella", "Como IA, no puedo pedirle más", "Como IA no tengo en el trabajo". The branch took any words after `no puedo` or `no tengo` | fixed: the verb must name what a model says it lacks (no tengo acceso, opiniones, emociones; no puedo acceder, verificar, navegar; no dispongo de; no cuento con; no poseo; no me es posible; no soy capaz); four such lines in `REPLIES` |
| R3-2 | minor | the same branch | It missed "modelo de IA", "asistente de inteligencia artificial", "desarrollado por OpenAI", and the role after "sin embargo" or "que" | fixed: each in the branch, with a `MACHINE` line. Still missed, and accepted for a strong sign: "carezco de", "al ser una IA", "soy un modelo de lenguaje y no puedo", "no estoy en condiciones de" |
| R3-3 | minor | the PR body | Two byte counts stale, and the branch described more loosely than the code | fixed |

On the round-3 reviewer's own probes the branch now finds 10 of its 16 model lines and none of its 25 person's lines,
and ripgrep 14.1.1 agrees with Python on each.

## Round 4

A fresh reviewer, on f3ab1a5 (the fixes since 2c940d5). Verdict: needs-fixes. R3-2 and R3-3 hold; R3-1 held only in
part.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| N4-1 | major | `any.toml`, `any-ai-self-reference`, the Spanish branch | Spanish says "como IA" for "as for AI", of the tools people use at work, and the objects the branch listed are what they say of them: "Como IA no tengo acceso a ninguna en el trabajo", "Como asistente de IA, no tengo acceso a la versión Pro", "Como IA no tengo preferencias, uso la que me pongan" | fixed: the branch keeps only the role the source shows, como (un, gran) modelo de lenguaje; "como IA" and "como asistente de IA" are out, and four such lines are in `REPLIES` |
| N4-2 | minor | the same branch | The listed verbs dropped stock refusals: no puedo proporcionar, no puedo garantizar, no tengo experiencias, creencias, un cuerpo | fixed: in the branch, with `MACHINE` lines |

Four rounds narrowed this branch, each finding a person's line the last one let through. It now finds the source's
role and nothing wider: on every probe line of rounds 3 and 4, 2 of 65 person's lines fire (a quoted bot reply, which
fires by design in every language, and the contrived "Como modelo de lenguaje, no dispongo de tiempo para probarlo"),
and 10 of 36 model lines. "Como IA, no puedo…" from a model is missed, and accepted: a strong sign counts alone, so
precision comes first. ripgrep 14.1.1 agrees with Python on every probe.
