---
subject: "Bootstrap step 4, propose-signs, the sources and the first signs (PR #15)"
base: main (9e4cdde)
head: b71d02b
date: 2026-11-07
round: 1
tier: standard (a fresh reviewer per round on Claude Opus 5.5, every lens; fixes verified by the main session, with mutants)
verdict: needs-fixes
---

# Review: Bootstrap step 4, propose-signs, the sources and the first signs (PR #15)

Round 1 read 67 signs and 26 sources at `b71d02b`: shared runs of 5 to 7 words against 1,690 downloaded files, 30
signs opened against the sections they cite, every pattern under Python and ripgrep. A blocker and six majors, so a
second round followed, and after its blocker and major a third check in the main session.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | blocker | 15 sign fields | `flags`, `what` and `instead` copied from or modelled on source examples: an 11-word run from Wikipedia's placeholder example, close paraphrases of real people's text, translated paraphrases from ru, fr and zh | fixed: new invented text; `tools/copycheck.py` finds 0 runs of 6 words |
| F2 | major | 11 `any` signs | They rest on de and ru pages that translate the English one | wontfix: the maintainer's call, a translated page counts as its language |
| F3 | major | any-assistant-closing-offer | A `strong` sign fired on "Is there anything else we should know before the audit?" | fixed: the chatbot's form only, at a line's start; office lines hold it |
| F4 | major | en-trailing-participle | `usual` on "Sales fell 8%, reflecting the weaker dollar" | fixed: merged into any-tacked-on-analysis, which a model reads |
| F5 | major | en-stock-openers | "Can we do a deep dive on Friday?" fired alone | fixed: `deep dive` and `let's dive in` are weak |
| F6 | major | en-significance-phrases | Ordinary praise fired alone | fixed: weak |
| F7 | major | any-over-attribution | Honest sourcing in mail fired | fixed: narrowed, weak, `document` |
| F8 | minor | any-assistant-preamble | "Of course, here is where it gets harder." fired strong | fixed, then reopened as F21 |
| F9 | minor | any-emoji-markers | ✓, ☐ and 👍 fired | fixed: the marker required, the class narrowed |
| F10 | minor | the didactic signs | "It's important to remember your passport" fired | fixed |
| F11 | minor | en-corrective-framing | Plain scientific caution fired | fixed: merged into any-defensive-qualification |
| F12 | minor | the weak rule | Three of what was undefined; a heading can't cluster | fixed: hits of weak signs in a paragraph or section |
| F13 | minor | `underscore` terms | The verb's plural was missed | fixed |
| F14 | minor | any-overstructured-short-text | The sources say long, not short | fixed: renamed any-overstructured-note, "short" dropped |
| F15 | minor | mixed apostrophes, copula, Llama phrases | Scoped wider than the sources | fixed: the first cut, the others scoped to what the sources show |
| F16 | minor | `sources.toml`, slop-forensics | Its feed watched paths that don't exist | fixed: `results_by_domain/essays`, `data` |
| F17 | minor | models.toml, models.py, render.py, AGENTS.md | Stale comments, and "where the work stands" | fixed |
| F18 | minor | propose-signs | No rule for `usual`, for `flags` and fixed strings | fixed: four lines, adjusted for F2's call |
| F19 | minor | the PR's text | No list of what was skipped; `since` unnamed | fixed |
| F20 | minor | en-stock-openers, any-false-range | A source's alternation order kept, and an MIT source's sentence | fixed: reordered and reworded |

Round 1's owner calls, answered by the maintainer on 2026-11-07: a translated page counts as a language; an `artefact`
with a `check` may be `any` on one source; the cut from 67 signs to 55; the office-mail test; the copying check; and
the six smaller calls (the weak rule by hits, `flags` holding only the string a check needs, old word lists cut first,
`read_at` as pinned, bold lead-in weak, invented sources called unverified in Step 5).

## Round 2

**Where:** the delta `b71d02b..4e29dce`, a fresh reviewer, copycheck at 5 and 6 words, 12 invented AI-flavoured texts
run at both heads, mutants on a scratch copy. **Verdict:** needs-fixes: a blocker on one field, a major, and a blocker by
the harness rule.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | blocker | any-significance-inflation `flags` | Still Wikipedia's frame: "marks a pivotal moment in the town's evolving story" | fixed: a new text; three `what` and `instead` fields reworded from their sources |
| F3 | minor | any-assistant-closing-offer | "A hope that it helped" left `what` | fixed: back in `what`, for a model's read; the check stays narrow |
| F21 | major | any-assistant-preamble | `email` added, so "Sure! Here's the link." in a reply fired strong | fixed: only a handover line that names what it made and ends on a colon; office lines in four languages hold it |
| F22 | minor | any-didactic-aside | No leading edge: "The audit is worth noting" fired | fixed: `\b`, office lines |
| F23 | minor | any-negative-parallelism | `instead` named an X and Y the line no longer had | fixed |
| F24 | minor | en-vague-connection | `what` quoted words the source doesn't report | fixed: no quoted words |
| F25 | minor | the weak rule | One phrase could be a whole cluster | fixed: one phrase counts once, the maintainer's call; a test |
| F26 | minor | `tools/copycheck.py` | Chinese, Japanese and Thai were one token a clause; a Devanagari vowel sign split a word | fixed: a token a character there, marks kept in words; tests in zh and hi |
| F27 | minor | `tools/copycheck.py` | It took a check's matches out of every field, and whole long matches | fixed: only in `flags`, only up to a run's length |
| F28 | minor | the PR's text | Counts, and KB mixed with KiB | fixed in the PR body |
| F29 | blocker | `tools/gate.py`, `check_sign_ids` | The fix loosens the check at pre-push, unnamed | fixed: the maintainer's yes, in the PR and the plan |
| F30 | minor | `tests/test_office.py` | Four mutants survived: bold lead-in back to `usual`, the preamble narrowed, the emoji class narrowed, the preamble without `email` | fixed: each now fails a test |

Round 2's owner calls, answered by the maintainer on 2026-11-07: the sign ids fix agreed; the last example rewritten;
one phrase counts once; the closing offer stays off `email`.

Improvements taken: sparkles, high voltage, star and numbered items in any-emoji-markers; `online` in en-gpt-5's
presence term; a line per branch of each check that counts alone, in the office test. Left: tagging the office lines by
kind, as a sign's `kinds` doesn't narrow the test today and that is the stricter way.

Refuted in round 2: `any` on de or ru (the maintainer's call); dropped ids (none reached main); en-copula-avoidance
losing Claude (the source names GPT and Gemini); "It's worth noting" accusing mail (no hit in 828K words).

## Round 3

**Where:** the delta `4e29dce..f765c63`, read by a fresh reviewer, mutants on a scratch copy. **Verdict:** needs-fixes.
F1's last field holds: copycheck finds no run of 6, and at 5 only ordinary English and the checks' own strings. F22 to
F30 hold, each with its test.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F21 | major | `any-assistant-preamble` | Still open: any eager yes ending on a colon fired strong. "Sure! Here's the email from the landlord:", "Natürlich! Hier ist der Link:", "Конечно! Вот ссылка:", "当然可以！链接在这里：" | narrowed in the main session to a thing a chatbot makes; still open, see round 4 |
| N1 | minor | the same check | `absolutely` had no test | fixed: a line in `MACHINE`, its mutant killed |
| N3 | minor | this record | Round 1's verdict read `clean` | fixed: `needs-fixes` |

## Round 4

**Where:** the delta `f765c63..0223b25`, read by a fresh reviewer, 46 probe lines and mutants on a scratch copy.
**Verdict:** needs-fixes, on F21 alone.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F21 | major | `any-assistant-preamble` | Round 3's fix still fired on a person handing over their own draft: 20 of 30 plain replies, in all four languages ("Sure! Here's a draft of the agenda for Monday:", "Конечно! Вот черновик договора:", "当然可以！这是合同的草稿："). A word for any draft can't tell a colleague from a chatbot | fixed: each branch needs reworked text, a revised, polished or shorter version, "a rewrite", or "an email you can send", as the reviewer's scratch variant showed; fourteen of the person's drafts join `OFFICE`, and four chatbot lines `MACHINE`. A bare "here's a draft:" would belong in a weak sign; none is added |
| N4 | minor | this record | Round 3 marked F21 fixed though it wasn't, counted a line that kills no mutant, and missed that at `640cae2` the Chinese line was an escaped backslash that could not fail | fixed: round 3's row says what was done; `0223b25` holds the full-width marks |

Refuted: N5, a stale `round: 1` and `head` in the frontmatter. `docs/reviews/README.md` says the frontmatter describes
the first round, and later rounds are sections.

## Checks

- After round 2's fixes: `uv run tools/gate.py full`; copycheck over 1,690 files: 0 runs of 6 words, and 58 hits of 5
  over 10 strings, each ordinary English or a check's own watch string.
- The 12 AI-flavoured texts, before and after: no sign lost; `en-gpt-5-vocabulary` gained on the hedged report.
- Seven mutants of round 2's fixes, one at a time: the preamble without `email`, bold lead-in back to `usual`, the
  preamble narrowed, the emoji class narrowed, the render line's "once", copycheck reading every field, copycheck's old
  tokens. Each fails a test.
- The baseline of 828K words written before ChatGPT: no strong or usual sign fires.
