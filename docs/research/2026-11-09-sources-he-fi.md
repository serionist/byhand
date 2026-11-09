# byhand: sources for Hebrew and Finnish

Research date: 2026-11-09, the fourth run of `find-sources`, for #60. The maintainer agreed that day to add `he` and
`fi` to `languages.toml` as extras outside the hundred, so the sources the third run found for them
(`2026-11-09-sources-it-tr-vi-id-he-th-fi.md`, "Hebrew and Finnish: found, not listed") can be listed. This run read
them again and searched once more for anything newer. Every page was read as data; nothing from them is copied here
but titles, licences, revisions and a few words named as facts. Three sources added: two for fi, one for he.

## Searched

| Where | Queries or pages |
|---|---|
| CLDR 49 | `cldr-localenames-full` (en, he, fi) and `cldr-core`'s `territoryInfo.json`, for the names and speakers in `languages.toml`: Hebrew, עברית, 9 million (Israel); Finnish, suomi, 6 million (Finland, Estonia, Sweden). The same sum gives Xhosa, rank 100, its 11 |
| Wikidata | the sitelinks of `Q136117782` (Signs of AI writing): de, en, fi, fr, he, pt, ru, th, zh, Commons, as in the third run |
| he and fi Wikipedia | the two sitelinked pages: their latest revision, history and wikitext |
| GitHub | repositories for "finnish humanizer", "humanizer-fi", "suomi tekoäly teksti", "finnish ai writing", "hebrew humanizer", "humanizer-he", "hebrew ai writing", "עברית בינה מלאכותית כתיבה"; Hakku/finnish-humanizer at its head |
| arXiv | `abs:<Finnish, Hebrew> AND (abs:"AI-generated" OR abs:"LLM-generated" OR abs:"machine-generated" OR abs:stylometric OR abs:"linguistic features")`: three results, none about the language of model text |

## Kept

| Id | What it shows | False positives it lists | For `propose-signs` |
|---|---|---|---|
| `wikipedia-fi` | `Wikipedia:Merkkejä tekoälyn kirjoittamasta tekstistä`, revision 23993692 (10 May 2026), 35 revisions since Sep 2025, CC BY-SA 4.0. Not a translation: each example comes from Finnish Wikipedia. Filled sections: superficial analysis with unnamed places and people, "ei ole vain X, vaan Y", promotional tone, the rule of three ("Stubbismi"), chat-style lists with • and emoji, reportage instead of encyclopaedic style, capitals on every word of a subheading as an anglicism, wrong inflection in translated text, and chat citation residue ("+1" or "+5" after a source's name). Several headings are still empty; an edit in May 2026 tried to freeze it as a record of what was seen by 14 Jan 2026 and was reverted | Yes: people write like this too, bold and needless lists included; a sign is a reason to look, not proof | the subheading capitals, Finnish's own, beside `de-title-case-headings` and `hu-title-case-headings` as a pattern, but needing a second Finnish source; the rest is held by `any` signs |
| `finnish-humanizer` | Hakku/finnish-humanizer (MIT, `7a151e26b263`, 21 stars): 12 Finnish patterns, each with a before and after: passive overuse, nominal constructions with a light verb ("suorittaa tarkistuksen"), needless pronouns, missing particles (-han, -pa, kyllä, vaan), English word order, genitive chains, stacked adjectives, over-long sentences, chained joka and jotka clauses, officialese out of place ("kyseinen", "edellä mainittu"), avoiding consonant gradation, English politeness. Then 15 patterns that follow the groups of Wikipedia's Signs of AI writing without saying so, and typography: the em dash, where Finnish writes a spaced en dash (SFS 4175). No evidence or method behind any pattern, and no test on human text | Partly: it says the passive is natural in Finnish and the particles are normal written Finnish, overused or missing only by degree. It also says Finnish uses straight quotes, where Finnish typography writes ” ”: a sign from it needs a second source | the Finnish patterns, each only beside a second source; the universal half adds nothing to `wikipedia-en` and the `any` signs |
| `wikipedia-he` | `ויקיפדיה:סימנים לכתיבה מבוססת בינה מלאכותית`, revision 43047872 (8 Apr 2026), 42 revisions, CC BY-SA 4.0: created by translating en oldid 1323439249, its phrase lists rendered in Hebrew (promotional words, didactic asides, closing summaries, "לא רק... אלא גם"), though its section on typical vocabulary gives English words only. Its own lines: the em dash is not used in Hebrew, so it is a good sign of AI writing or machine translation | Yes: many of the signs also turn up in Hebrew articles machine-translated from English | evidence for an `any` sign beside other languages' sources, as `wikipedia-pt` is; nothing of Hebrew's own to seed from |

All three feeds read with the refresh's own readers on 2026-11-09: each unchanged since the revision or commit above.

## Dropped

| What | Why |
|---|---|
| yair-zehavi/claude-code-skills, `skills/humanizer-he` (MIT, 0 stars, one commit, Oct 2026) | It says it is derived from blader/humanizer and Wikipedia's page; its Hebrew additions (מהווה as the copula, slash gender, smichut chains, niqqud) have no evidence and no false positives tested: the bar the Thai ports failed |
| galasulin/linkedin-agent-he (MIT, 0 stars) | One person's LinkedIn agent with a scoring script; its own README calls its checks local heuristics |
| shalhevetvardi/humanizer-he-download | A download page, no list (as in the third run) |

## Seeding

| Language | Enough to seed from? | Why |
|---|---|---|
| fi | Enough to run `propose-signs`, likely for few signs of its own | Two sources of its own, an original wiki page and a native list, but they share little that no `any` sign holds: "ei ole vain X, vaan Y" and the rule of three are `any-negative-parallelism` and `any-rule-of-three`. Finnish's own candidates (subheading capitals, light verbs, officialese, the em dash) each rest on one of the two, so `weak` at most, or recorded as nothing to seed, as Indonesian was |
| he | No | One translated page; its em dash line is evidence for an `any` sign, not a Hebrew one. The `any` signs carry Hebrew |

Both style guides stand as the third run named them: the Academy of the Hebrew Language for Hebrew punctuation, the
Kielitoimiston ohjepankki of Kotimaisten kielten keskus for Finnish.

## Follow-up, 2026-11-09: Finnish's signs and deferred `any` forms

Move 2 of `docs/plans/2026-11-09-more-languages.md` for fi, under #60, with #72's change: no native-review gate, so
each sign is as strong as its sources make it. `wikipedia-fi` at 23993692 and `finnish-humanizer` at `7a151e26b263`,
both still their heads, were read in full: the page, `references/patterns.md` and `SKILL.md`. Finnish is seeded with
two signs of its own, both formatting and both weak, as neither source measures how often people do them:

| Sign | Strength | Evidence |
|---|---|---|
| `fi-em-dash` (a check) | weak | `finnish-humanizer`'s typography notes say models write the long dash where Finnish writes the spaced short one (SFS 4175); the page's second example of model text sets a list off between spaced long dashes, though it quotes it for something else. `de-em-dash` and `hu-em-dash` hold the habit weak too, and `finnish-humanizer`'s own Finnish prose writes it |
| `fi-title-case-headings` (for the model's read) | weak | The page's section on anglicisms: capitals on the words after the first in a model-written article's subheadings, after English titling, with ja left small, five of them in one example. `de-title-case-headings` and `hu-title-case-headings` hold it weak too |

No structure sign of Finnish's own: what the page shows of structure is held by `any` signs (negative parallelism, the
rule of three, promotional tone, unnamed places and people, needless lists), and `finnish-humanizer`'s Finnish
patterns (light verbs, officialese, the passive, genitive chains, joka chains, long sentences, missing particles,
needless pronouns, English word order and politeness) rest on its word alone and are written by people at work. The
header of `signs/fi.toml` has each reason.

Finnish forms in the `any` checks, deferred: `any.toml` is held for the check budget (#71), as for Indonesian and
Turkish. Each would come with a `machine` line and the person's line beside it in `tests/office_fi.toml`.

| `any` sign | Form | Source | The person's line it must pass |
|---|---|---|---|
| `any-chatgpt-citation-markup` | a source's name with +1, +2 or +5 glued on, ChatGPT's citation chips pasted as text (Oulun kaupunki+1) | `wikipedia-fi`, Virheelliset tai erikoiset viitteet | C++; Disney+; Erasmus+-hanke (on the page itself); Puh. +358 40 123 4567; tarjous 2+1 |
| `any-flattering-agreement` | Hyvä kysymys!; Erinomainen huomio! | `finnish-humanizer` 15 | Hyvä kysymys, en oikeastaan tiedä; Erinomainen huomio, korjaan sen |
| `any-knowledge-cutoff` | Viimeisimpien tietojeni mukaan | `finnish-humanizer` 26 | Likely none: a person writes it of their own latest news, as in `office_fi.toml` |
| `any-didactic-aside` | On syytä huomata, että | `finnish-humanizer` 17 | Likely none: reports write it, as in `office_fi.toml` |

`wikipedia-fi` could also be cited by `any-negative-parallelism` (ei ole vain X, vaan Y), `any-rule-of-three`
("Stubbismi") and `any-promotional-tone`, and `finnish-humanizer` 20 by `any-challenges-formula`; none has a check.
