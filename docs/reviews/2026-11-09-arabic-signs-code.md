---
subject: "Seed the Arabic signs (PR #58)"
base: main (2786619)
head: 40b5d5c
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: needs-fixes
---

# Seed the Arabic signs: code review

The reviewer ran the Arabic office test, `byhand validate` and `byhand render` (no diff), and Python against ripgrep
14.1.1 on 106 probe lines with the right-to-left mark, the tatweel, shadda, fathatan and ، ؛ ؟ (no disagreement). It
read al-Shaibani and Ahmed's tables from the rendered pages, and scanned the office test for 4-word runs shared with
humanizer-ar. The main session reproduced F1 and F2 before fixing them.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | `any.toml`, `any-closing-summary`, the Arabic branch, with `ar-shed-light` | The most ordinary closing sentence of a person's thesis or report, "وفي الختام، يمكن القول إن هذه الدراسة سلطت الضوء على…", made 2 of the 3 weak hits a cluster needs, and a heading or a reading sign (`ar-narrow-vocabulary` on a repeated الدراسة) made the third. The form rests on humanizer-ar alone, which lists وفي الختام among the connectors `ar.toml` leaves out | fixed in 5aeb2bd: the Arabic branch and its citation are cut; the conclusion is in `REPORTS`, and "وفي الختام، يمكن القول…" is in `LEFT_ALONE` |
| F2 | major | `any.toml`, `any-ai-self-reference`, the Arabic branch | It took any object after لا أملك القدرة على, so a person's verdict on a tool after a full stop fired: "جربنا Gemini أسبوعين. كمساعد ذكاء اصطناعي، لا أملك القدرة على تقييمه بعد…" (#53's N4-1 class) | fixed in 5aeb2bd: the lack must be one a model claims (إبداء, التنبؤ, الوصول إلى الإنترنت, تصفح); the reviewer's three lines are in `REPLIES` |
| F3 | minor | `tests/test_office_ar.py`, `ar-shed-light`'s `flags` | Five office lines followed humanizer-ar's examples with words dropped or swapped (the dash around three goals, نقلة نوعية beside حجر الزاوية, تم with SPSS, تجدر الإشارة with a test's results, a rise in sales with مما), and the flags kept a source example's subject | fixed in 5aeb2bd: each rewritten on our own subject and shape |
| F4 | minor | `ar.toml`, `ar-narrow-vocabulary`'s citation | "Each model's top words above 3,000" is wrong for Jais, and the reviews' tail is put down to length | fixed in 5aeb2bd: ALLaM, GPT-4 and Llama; the reviews dropped |
| F5 | minor | `ar.toml`'s header | It didn't say why humanizer-ar's other patterns were skipped, overstated its tatweel test (only هـ), and put the religious-phrase cue on news alone | fixed in 5aeb2bd |
| F6 | minor | `ar-shed-light`, `any-assistant-preamble` | Misses: two joined clitics (ولتسليط), shadda with fatha or full marks, four words between, tanween; in the preamble مُحسَّنة, نصّك, the feminine إليكِ… رسالتكِ, other openers | fixed in part in 5aeb2bd: two clitics, with two `FORMS` lines. The rest accepted: model text rarely carries full marks, a strong sign wants precision, and the source names only بالطبع |

## Refuted

- The preamble on a colleague returning the reader's text: the cost #24, #53 and #55 accept; a copy (نسخة من رسالتك)
  and other nouns pass.
- The self-reference on a quoted bot reply: by design in every language. Other roles, the bare لا أملك القدرة على and
  dialect lines pass.
- `ar-shed-light` on سلطة, السلطات, سلطان, سلطنة and the rest: none of 19 lines fires. The noun تسلّط with الضوء
  within three words fires, an edge case for a weak sign.
- `any-flattering-agreement` mid-sentence: weak, and no Arabic pattern clusters in chat.
- Python against Grep, NFC, the invisible marks; the citations of الضوء, Markdown, generic lines and Qwen2's dialect
  mixing; the alphabetical order; copying at 4 words (only fixed phrases and alphabetical lists); the docs.

## Improvements

| Improvement | Answer |
|---|---|
| `test_the_arabic_checks_read_posts_and_documents` hides that the Arabic forms of weak `any` checks read every kind | taken: its comment names سؤال رائع!, now the only one, and the person's comma in `CHAT` |
| `ar.toml` line 19 was 124 characters | taken |

## Not covered

Whether a native speaker finds the signs and the person's lines natural; the plugin sessions, which the main session
ran; `gate.py full` on the reviewer's side (CI passed on 40b5d5c).

## Round 2

A fresh reviewer, on 13194ff (the fixes since 40b5d5c, in 5aeb2bd). Verdict: clean. F1 to F6 hold: each line the
fixes added fails on the 40b5d5c catalogue and passes now (the conclusion in `LEFT_ALONE` for F1, the three verdicts in
`REPLIES` for F2, the two clitics in `FORMS` for F6), and the rewritten office lines share no shape with humanizer-ar's
examples. Python and ripgrep 14.1.1 agree on all 33 probe lines for each Arabic pattern.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F7 | minor | `ar.toml`, `ar-shed-light`, the past-tense branch | F6's two-letter clitic let in ال, so the town of al-Salt before "the green light" fired: "منحت وزارة التربية مدارس السلط الضوء الأخضر…" | fixed in 0f34c4f: one letter there, two only before تسليط; the line is in `LEFT_ALONE` |
| F8 | minor | `CHANGELOG.md` | Still "four" shared signs after F1 | fixed in 0f34c4f: three |
| F9 | minor | PR #58's description | Stale on the closing summary, the self-reference, the clitics, the citation, the counts and the try | fixed: the description is rewritten for the head, and the check try ran again |
| F10 | minor | `ar.toml`'s header | humanizer-ar's padded three (6) and tacked-on clauses (4, مما يعكس) were not accounted for | fixed in 0f34c4f: both named, with `any-rule-of-three` and `any-tacked-on-analysis` |

Refuted: the self-reference on a person's verdict that uses a listed lack ("…لا أملك القدرة على إبداء رأي فيه قبل أن
أجربه"), the trade-off #53 and #55 accept; a quoted bot reply (by design); the preamble on a colleague returning the
reader's text (the accepted class); two of 13 fresh paragraphs reaching 3 by stacking two formatting tells with one
`ar-shed-light`, the class #55 refuted, and 3 on 40b5d5c too; the render's "Words:" display (display only).

| Improvement | Answer |
|---|---|
| Read الانترنت without its hamza in the self-reference | taken in 0f34c4f, with a `MACHINE` line |
| Name all four lacks in the self-reference's comment | taken in 0f34c4f |

The review ends here: no blocker or major is open. The commits are named as rebased on 042f824 (#57), which changed
how `tests/conftest.py` counts a weak cluster; the Arabic office test passes under it unchanged.
