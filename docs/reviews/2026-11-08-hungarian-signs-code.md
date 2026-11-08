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
