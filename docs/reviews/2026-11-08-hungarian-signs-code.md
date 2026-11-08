---
subject: "Bootstrap step 4, the Hungarian signs (PR #28)"
base: main (a38d7ee)
head: 498611f
date: 2026-11-08
round: 1
tier: standard (a fresh reviewer per round on Claude Opus 5.5, every lens; the fixes verified by their mutants)
verdict: needs-fixes
---

# Review: Bootstrap step 4, the Hungarian signs (PR #28)

Round 1 read the 11 Hungarian signs and the Hungarian branches of two `any` signs at `498611f`, against humanizer-hu at
`3b021d28638c`, Novák & Novák's control contexts and Hun_ai_test, and ran every pattern on the reviewer's own plain
Hungarian lines. The fixes are in `c22aa02`, "Fix the Hungarian signs from review round 1", rebased onto #24.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | blocker | hu-explicit-subject-repeat, hu-em-dash, hu-promo-adjectives, hu-title-case-headings, hu-address-switching | Built on humanizer-hu's frames: §7's before and after, its remedies in its order, and a `what` that translates its reason; §8's "Ne írd" line; §16's remedy translated; §20's "Adj Noun És Noun" heading; §26's Ön sentence then a te imperative | fixed, the maintainer's rule: each written anew with its own subject, shape and remedy. The restated subject is a pronoun now (Én … Én …), mended by leaving it out, not by joining; the dash flags one aside about candidates; the heading is a bold label; the switch runs from te to Ön and is mended to te. Remedies listed in alphabetical order |
| F2 | major | hu-place-name-suffix | Fired on right Hungarian, as the source's own control contexts show (pp. 43-44): Győrön keresztül, Debrecenen át, a Debrecenről szóló jelentés, Veszprémre esett a választás, Büszkék vagyunk Sopronra, Elegem van Budapestből; and `MACHINE` held a right line, "Veszprémen keresztül megyünk." | fixed: only the -ban/-ben form of the nine towns that take -on, -en or -ön; their -ba/-be and -ból/-ből forms go too (beleszeret Budapestbe, elege van Budapestből), and every form of the -ben towns. The `instead` names the other endings as right, so a model leaves Győrön keresztül alone. The nine lines, the Veszprém line and Budapestbe in `OFFICE` |
| F3 | major | hu-hyphenated-case-ending | Fired on KATA, the tax, rightly hyphenated (KATA-ból, KATA-t, KATA-val); Novák's footnote 5 names it | fixed: kata dropped. The list was read for others: Éva keeps its accent, so EVA, the other tax, passes; no other name is a common acronym or word. Three KATA lines in `OFFICE` |
| F4 | minor | any-tacked-on-analysis | Counts alone, and fired on mirroring an icon ("…, tükrözve a függőleges tengelyre") and on a predicate ("…, biztosítva a kivetítő és a flipchart is") | fixed: biztosítva and elősegítve need an accusative after them, hozzájárulva a -hoz/-hez/-höz, and tükrözve an abstract noun (érték, szándék, elkötelezettség …). Both lines in `OFFICE`; a Hungarian line in `passes`, so `validate` tests the check |
| F5 | minor | hu-ai-vocabulary, hu-promo-adjectives | Five terms rest on thin counts | kept, the maintainer's call: nélkülözhetetlen, aspektus, perspektív, magával ragad and kulcsszerep stay. Each term's own count is in its `where` and the PR; kulcsszerep's count is even (0.2 and 0.2), and it rests on the wikipedia-hu patrol board, which says so |
| F6 | minor | hu-calque-phrases | Cited segít with any infinitive, 0.7 and 7.9 | fixed: the term's own count, 0.1 and 2.9 per 100,000 characters, in the sign and the PR |
| F7 | minor | AGENTS.md, the plan | "Where the work stands" and the plan's Step 4 row don't name `hu` | refuted: the maintainer's session adds both at merge, as other languages land beside this one |

The maintainer's calls in round 1:

- any-didactic-aside's Hungarian branch fires only where "fontos megjegyezni / hangsúlyozni / kiemelni, hogy" opens a
  sentence. "A meghívóban fontos kiemelni, hogy …" and "Most nem fontos kiemelni, hogy …" are in `OFFICE`.
- The five thin terms stay (F5).
- A two-sentence report with átfogó, elengedhetetlen and beleértve is machine-made: three different weak phrases are
  the cluster. A line of that shape is in the weak tests as one that reaches 3.
- Every group of plain words in a check or term, every term list and every list of examples runs in alphabetical order,
  accents and case ignored, for every language. hu.toml and the Hungarian branches in `any.toml` follow it, and
  `tests/test_office_hu.py` holds it. To keep a term's start plain, the optional superlative leg- is gone
  (`(?:leg)?átfogó\w*` is `átfogó\w*`): a superlative of these words is rare, and átfogóbb still matches.

Left for the maintainer: hu-place-name-suffix still fires where a verb governs -ban/-ben with a town ("csalódtam
Budapestben", "bízom Szegedben"); these read rare, but they are right Hungarian, and the check can't see the verb.

## Checks

- 41 mutants, one at a time, of every changed check: the fontos phrase anywhere, after a full stop only, at a line's
  start only, without hogy, its adverbs or kiemelni; the participle on any word, with r before the -t, tükrözve on any
  word, without its comma, ezzel is, hozzájárulva or tükrözve; kata back, the -e particle, any a/e word; each wrong place
  form brought back (budapestből, budapestbe, győrön, debrecenről, sopronra) and Szeged dropped; two names, two
  infinitives, two terms and two nouns out of order; and the earlier round's. Each fails a test.
- Every Hungarian pattern under Python and Claude Code's own ripgrep, line by line over every test text and example:
  2,187 cases, no disagreement.
- copycheck over 57 downloads: no run of 6 words; at 5 and 4 only existing English signs against the English quotations
  in a huwiki translation of the English page, none on a Hungarian field.
- `uv run byhand validate`, `uv run byhand render`, `uv run tools/gate.py full --base origin/main`.

## Round 2

**Where:** `498611f..82f6a68`, then main's #27 and #29 merged in. F1 to F7 held: copycheck finds no run at 6 or 5, and
no frame is left.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F8 | major | hu-place-name-suffix | Its check fired on right Hungarian, mostly names: a hotel's (a Hilton Budapestben, a Hotel Kecskemétben), a venue's (a Müpa Budapestben), a club's (a Pick Szegedben, a Kaposvárban játszott), a county (Jász-Nagykun-Szolnokban), and a verb that takes -ban/-ben (csalódtam Budapestben) | fixed, the maintainer's call: the model's read only, usual with no check, as hu-address-switching; its `instead` names these right uses so a model leaves them alone. The lines are in `OFFICE` as reminders; its `MACHINE` lines and pattern tests are gone, and a test holds it has no check |
| F9 | minor | `tests/test_office_hu.py` | The order test skipped a group holding `[` or `\`: the hyphen check's suffixes reversed, or `(?:ezzel is\s+|így\s+)` reversed, passed it | fixed: every group is read, nested ones too, by each alternative's literal start up to the first `[`, `(` or `\`, as the term-list test reads a term; a test holds both reversals failing. any-didactic-aside's start group now reads `(?:[.!?]\s+|^)`, the same matches in order |
| F10 | minor | three `what` and `instead` | Prose lists out of order: hu-promo-adjectives' place, event, product; hu-title-case-headings' heading, bold label; hu-place-name-suffix's -on, -en, -ön | fixed: an event, a place or a product; a bold label or a heading, and proper names and the first word; -en, -on or -ön |
| F11 | minor | hu-address-switching | Its `flags` opened on "Köszi", an informal word people pair with Ön, not a te form: the sign would teach a model to move a client to te | fixed: "Köszönöm, hogy ilyen gyorsan válaszoltál!" carries the te, and the Ön after it is the switch |

The maintainer's calls in round 2:

- hu-place-name-suffix is for the model's read only (F8).
- The Hungarian participle branch leaves any-tacked-on-analysis, which is main's again, for a weak Hungarian sign,
  `hu-tacked-on-participle`, with its own examples and the same sources; its exact check finds 2 of 1,000 human texts
  and none of the AI ones in Hun_ai_test. "A műszakot átszerveztük, biztosítva a hétvégi ügyeletet is." is in the plain
  reports, under 3.
- Kept: any-didactic-aside's sentence-start branch (1 human text, 6 AI) and hu-hyphenated-case-ending (its one human
  hit, "Mária-val", is a novel's title).

### Checks

- 39 mutants, one at a time: the place check back; the participle sign usual, on any object, with r before the -t,
  without its comma, ezzel is, hozzájárulva or tükrözve; the hyphen suffixes and `(?:ezzel is\s+|így\s+)` reversed,
  the sentence-start group reversed, two names, infinitives, terms and nouns out of order; the fontos phrase anywhere,
  after a full stop only, at a line's start only, without hogy, adverbs or kiemelni; the hyphen without -n, with the
  -e particle, kata or any a/e word; the earlier round's. Each fails a test.
- Every Hungarian pattern under Python and Claude Code's own ripgrep: 1,896 cases, no disagreement.
- copycheck over 57 downloads at 6, 5 and 4 words: none on a Hungarian field.
- `uv run byhand validate`, `uv run byhand render`, `uv run tools/gate.py full --base origin/main`.

## Closed

The maintainer verifies round 2's fixes in the main session.
