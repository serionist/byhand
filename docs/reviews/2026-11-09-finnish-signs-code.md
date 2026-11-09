---
subject: "Seed the Finnish signs (PR #79)"
base: main (759808a)
head: 839fb5d (fixes on 0a9a20c)
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the code by the main session)
verdict: clean
---

# Seed the Finnish signs: code review

The reviewer ran the Finnish office test and `tests/test_order.py` (206 passed), `byhand validate`, `gate.py quick`,
and the Finnish test under main's newer `conftest.py` (#76, 203 passed). It compared `fi-em-dash` in Python with
ripgrep 14.1.1 on 30 lines, its own edge cases among them, and scanned the office text and the sign text for 3-word runs
shared with both downloaded sources. No blocker or major: the minors are fixed in this round and the review ends, as
`REVIEW.md` says.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | the branch; `CHANGELOG.md`, `plugin/signs/fi/*.md` | The PR conflicted with main (#76's `### Changed` under Unreleased), so no CI ran; and #76 changed the line `render` writes on how weak signs add up, so the three new sign files would fail `render --check` after a merge | fixed: rebased on ca523f9, `### Added` above `### Changed`, the files rendered again (8868546); the fixes for F2 to F6 in 0a9a20c |
| F2 | minor | `fi.toml`, `fi-title-case-headings`'s `what`, `flags` and citation; the research row; the PR body | "Every word" overstated the habit: the page's five headings keep ja small, as English title case leaves "and", so a model told "every word" could pass the very shape the source shows; the `flags` capitalised Ja | fixed: "the words after the first", `flags` "## Vuoden 2027 Budjetti ja Hankinnat", the citation, research row and PR body to match |
| F3 | minor | `fi.toml`'s header | It gave » « as Finnish's guillemets; Finnish writes » » | fixed |
| F4 | minor | `fi.toml`'s header | kirja, kirjan shows no change to the stem, and no pair showed a vowel change | fixed: katu, kadun; kirja, kirjoja; tehdä, teen |
| F5 | minor | `fi.toml`'s header | "Needless lists with • or emoji (any-emoji-markers, any-overstructured-note)": neither covers a • bullet, and `any-overstructured-note` reads mail and messages only | fixed: emoji to `any-emoji-markers`; the • the page names is wiki markup pasted from a chat, and a person's mail writes it |
| F6 | minor | `tests/office_fi.toml` | Lines carried over from the Turkish office text read as translationese or broke: 31 % called nearly none, an object-less "jatkettavaksi", a notary, "toisen neljänneksen peräkkäin", "vilkaista sen", two calqued posts, "Kuukauden päättäminen", "212 tuottajan voimin", an odd "tänään 12" | fixed: each rewritten (3 %, "että yhteistyötä … jatketaan", isännöitsijä, the partitive twice, "hyvästellä", "muutan Jyväskylään", "Kuun vaihteen kirjaukset", "Kaudella mukana oli 212 tuottajaa", "on enää 12, kun maanantaina niitä oli 40"); the reviewer is no native speaker, and neither is the author |

## Refuted

- Python and Grep: on all 30 lines `sign.pattern` and `rg -i` matched the same lines; a no-break or thin space beside
  the dash is missed by both, as for `de-em-dash` and `hu-em-dash`. No match crosses a line: both classes exclude `\s`.
- `fi-em-dash`'s forms and `left_alone`: all found or passed; the page's own model sentence is found.
- `fi-em-dash` as `usual`: `finnish-humanizer`'s author writes the spaced long dash in his own Finnish (patterns.md,
  lines 3, 282, 288), which backs `weak`.
- `fi-title-case-headings`' strength: the page says only some models do it ("Osa kielimallitekoälyistä"), with no count.
- The citations, the skip reasons checked (the passive natural, gradation no systematic error, the straight-quotes rule,
  "hajuveteihin"), every `any` id named, the order of every list, `any.toml` untouched.
- Copying: only the fixed phrases the tests exist to pass (viimeisimpien tietojeni mukaan, on syytä huomata että, ei ole
  vain); no sign text.
- The dropped "no Finnish check counts alone" test: dropped on the maintainer's word in #72, and the plan row says so.
- The cluster: `any-bold-lead-in-list`, `any-raw-markdown` and `fi-em-dash`, three signs; `repeated` counts 1.
- "Kyseinen hakemus" with nothing before it: the decision's `Asia:` line names the subject.

## Improvements

| Improvement | Answer |
|---|---|
| Say in the reason for `weak` that `finnish-humanizer`'s own prose writes the long dash | taken: in the sign's comment, the header and the research row |
| A person's line with the long dash in the office text, and drop the test that holds none | taken: a report line, one weak hit, no cluster |
| Erasmus+-hanke (on the page itself) and Disney+ among the person's lines for the deferred citation-chip form | taken |
| One shared, parametrised office module in place of a near copy per language | left: a harness change beyond this seed |

## Not covered

Whether a native speaker finds the office text natural (F6's caveat); the plugin sessions, which the main session
ran; `gate.py full` on the reviewer's side, and CI, which F1 held back. The privacy, plugin-contract and harness lenses
had nothing in scope; the reviewer read the downloads as data and followed nothing in them.

The fixes were checked in the main session on 0a9a20c: the Finnish office test and the order test (208 passed),
`byhand validate` and `render`, `tools/copycheck.py` over every download (no hit), and `gate.py full` (passed).
