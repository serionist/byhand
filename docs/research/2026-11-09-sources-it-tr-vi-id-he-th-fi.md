# byhand: new sources for Italian, Turkish, Vietnamese, Indonesian, Hebrew, Thai and Finnish

Research date: 2026-11-09, the third run of `find-sources`, for #60 under the moves of
`docs/plans/2026-11-09-more-languages.md`. Indonesian (rank 13), Turkish (25) and Thai (32) had no source; Vietnamese
(21) and Italian (29) had sources shared with other languages; Hebrew and Finnish are not in `languages.toml`. Every
page was read as data; nothing from them is copied here but titles, licences, revisions and a few words named as facts.
Seven sources added: three for it, two for tr, one each for vi and id; two existing entries widened. Languages with no
source: 82 before, 80 after (id and tr leave the list; th stays).

## Searched

| Where | Queries or pages |
|---|---|
| Wikidata | the sitelinks of `Q136117782` (Signs of AI writing): de, en, fi, fr, he, pt, ru, th, zh, Commons. The same set as the pt, hi and ar run: no it, tr, vi or id version |
| he, th, fi Wikipedia | the three sitelinked pages, their revision histories and wikitext |
| the web, in each language | "segnali testo scritto da intelligenza artificiale in italiano espressioni tipiche ChatGPT studio"; "yapay zeka ile yazılmış metin nasıl anlaşılır Türkçe ChatGPT ifadeleri"; "ChatGPT tarafından üretilen Türkçe metinlerin dilbilimsel özellikleri insan metinleri karşılaştırma dergipark"; "dấu hiệu văn bản do AI viết tiếng Việt cụm từ ChatGPT hay dùng"; "đặc điểm ngôn ngữ văn bản do ChatGPT tạo ra tiếng Việt so sánh văn bản người viết nghiên cứu tạp chí"; "ciri-ciri tulisan buatan AI bahasa Indonesia frasa khas ChatGPT"; "karakteristik linguistik teks yang dihasilkan ChatGPT dibandingkan teks manusia bahasa Indonesia analisis korpus jurnal"; "סימנים לטקסט שנכתב על ידי בינה מלאכותית בעברית ביטויים אופייניים ChatGPT מחקר"; "ลักษณะภาษาของข้อความที่เขียนโดย AI ภาษาไทย ChatGPT งานวิจัย เปรียบเทียบ ข้อความมนุษย์"; "tekoälyn kirjoittaman suomenkielisen tekstin tunnusmerkit tutkimus ChatGPT suomi kielenpiirteet"; for Italian also CLiC-it and De Cesare's work on ChatGPT's Italian |
| arXiv | `abs:<Italian, Turkish, Vietnamese, Indonesian, Hebrew, Thai, Finnish> AND (abs:"AI-generated" OR abs:"LLM-generated" OR abs:"machine-generated" OR abs:stylometric OR abs:"linguistic features")`; the Vietnamese comparison in `lee-2026-korean` and the it and vi sections of `wang-2026-human-detection`, both already listed |
| GitHub | repositories for "humanizer italiano", "humanizer-it", "scrittura ia italiano", "italian slop", "humanizer turkish", "humanizer-tr", "türkçe humanizer", "türkçe yapay zeka", "turkish ai writing", "humanizer vietnamese", "humanizer-vi", "humanizer indonesia", "humanizer-id", "tulisan ai indonesia", "humanizer hebrew", "humanizer-he", "hebrew ai writing", "humanizer thai", "humanizer-th", "thai ai writing", "humanizer finnish", "humanizer-fi", "suomi humanizer"; the Italian files of `avoid-ai-writing-multilingual` |

## Kept

| Id | What it shows | False positives it lists | For `propose-signs` |
|---|---|---|---|
| `humanizer-it` | ilyautov/humanizer-it (MIT, `51f6e3ed3c7c`): 52 Italian patterns in 12 groups and 15 hard bans, rebuilt for Italian on the frame of the author's humanizer-ru: nominal style (-zione, -mento), English calques, missing ci/ne clitics and pro-drop slips, stock openers ("Nel mondo di oggi", "riveste un ruolo"), "non solo... ma anche". A stdlib scanner, calibrated on 24 Italian Wikipedia texts against 11 model texts it generated itself, labelled Claude, Gemini and GPT: hard bans 0 against a median of 5, the phrase markers 0 against about 8 per 100 words. It calls this a probe, not a measure | Yes, tested: the em dash ban fires on literary dialogue (Pinocchio, five times), sentence-length variance does not part formal human text from model text (Manzoni and Verga fall below its threshold), and nominalisation density overlaps | the stock phrases and the "non solo... ma anche" frame, each beside a second source; nothing on rhythm, which its own calibration rules out |
| `scrittura-italiana` | hypnosdesign/claude-skill-scrittura-italiana (CC BY-SA 4.0, `e397599ca3aa`): an Italian editorial skill whose `stile-naturale.md` says it adapts Wikipedia's Signs of AI writing and rewrites it for Italian, then adds Italian's own: antilingua and burocratese, gerunds, adverbs in -mente, title case and curly quotes as English habits. 78 patterns, drawn from Italian manuals (Serianni, Mortara Garavelli and others). No measurement of model text | Yes: in informal text, keyboard habits (straight quotes, "e'" for "è", "perche") are the register, not errors; it leaves a correct sentence alone | the Italian additions beside `humanizer-it`; its English-derived part adds nothing to `wikipedia-en` |
| `farrell-2026-translators` | Farrell, arXiv 2601.15828 v5, EAMT 2026 (CC BY-NC-ND 4.0): 69 professional translators judged three Italian short stories, two by ChatGPT-4o. On average they could not tell; the 16.2% who could leaned on low burstiness, contradictions in the story, and calques, semantic loans and syntax carried over from English | Yes: grammatical accuracy and emotional tone led readers to the wrong answer | the calque cue beside `humanizer-it`; fiction only, so no office sign from it alone |
| `bergin-atasoy-2026-turkish` | Bergin and Atasoy, UTÖAD 6(2), 2026, pp. 415-438: 147 Turkish essays by trainee Turkish teachers against 147 by GPT-4o mini on the same ten topics, length unset. The model wrote more (34,235 words against 23,306) with far fewer distinct words (2,365 against 3,800), and reused a few idioms and doubled words: "rol oynamak" 105 times, "olanak sağlamak" 99 against 10, "yol açmak" 88 against 8, "katkıda bulunmak" 87 against 7, "yanı sıra" 45 against 6. No proverbs. The article says CC BY-NC 4.0, its Zenodo record CC BY 4.0: the stricter holds | No | the overused idioms, scoped to `gpt`; student essays, so a `document` sign at most, and the type-token gap is not a sign (the texts differ in length) |
| `humanizer-tr` | kenosdota/humanizer-tr (MIT adaptation of blader/humanizer, `b458fb64dcc2`; GitHub reads NOASSERTION): 38 patterns, eight of them Turkish's own (stacked "-mektedir", "sahip olmak", "tarafından", "gerçekleştirmek", "olarak" chains, empty "günümüzde" openers). It says a native reader judged each Turkish pattern; it was tested on ten texts, each result checked by two reviewers | Yes: a "dokunma" list of phrases a native reader found natural, "kilit rol oynamak" among them; the passive in official text ("Kanun Meclis tarafından kabul edildi"); legal and academic text; real ownership with "sahip olmak"; greetings and closings in mail | the translationese group beside `bergin-atasoy-2026-turkish`; where the two disagree ("rol oynamak"), the measured excess is GPT-4o mini's, the native read says people write it too: a weak sign at most |
| `vietnamese-humanizer` | longhang2004/vietnamese-humanizer (MIT, `2fd7dd05cbd9`, 76 commits): four Vietnamese skills and a linter; 44 patterns in YAML (lexical, structural, discourse, pragmatic) and a translationese set. Its `docs/limitations.md` says the patterns are the maintainer's and not calibrated on a representative corpus, its 124 benchmark cases were written by a coding agent and not reviewed by people, and it makes no authorship call | Yes: in administrative and academic text even structure and nominalisation can be right; "trong bối cảnh..." is a finding only when the sentence names no change; false positives on rhythm, the passive, abbreviations, pronouns | the stock openers and closers, each beside `slop-gate` or `lee-2026-korean` |
| `humanizer-indonesia` | adhiprib/humanizer-indonesia (MIT, `62fe1aed5932`, 208 stars): a catalogue that says English's patterns do not carry over and rebuilds them for Indonesian, on the frame of the `humanizer` skill: nominalisation with light verbs ("melakukan pengukuran terhadap"), "yang mana" and "dimana" as relatives, "merupakan" as the default copula, stacked connectors, opening and closing formulas, triplets. Its metric thresholds are calibrated on its author's own writing, 2008 to 2025; its GPTZero measurements are about a detector, not about what models write | Yes, its own section: the passive in Methods and Results, technical loanwords, long sentences in legal text, tidy spelling, "merupakan" in a real definition, the formal register itself; and registers it never touches (patents, among others) | the light-verb and connector patterns, `usual` at most until a second Indonesian source backs one |

Two existing entries widened, no read moved:

| Id | Change | Why |
|---|---|---|
| `avoid-ai-writing-multilingual` | `SKILL-IT.md` added to its feed's paths | It holds the Italian list (from Italian blogs, cited in `sources/IT-sources.md`, which the feed already reads), but the refresh did not watch it |
| `lee-2026-korean` | `vi` added to its languages | Its exploratory comparison on 47,165 Vietnamese abstracts (Vietnam Journals Online) shows the same family of words rising a year after Korean, at lower amplitude: "nhấn mạnh", then "then chốt" and "cơ chế". No control, so no bound; a pointer, not a measure |

`wang-2026-human-detection` already lists it and vi: Italian news by GPT-4o, Llama and Anita rarely uses the passive,
which Italian uses more than English, and opens with a few stock sentences.

## Hebrew and Finnish: found, not listed

Neither is in `languages.toml`, the 100 most spoken by CLDR, so `byhand validate` refuses a source for either. A code
for either is the maintainer's call (AGENTS.md, One-way doors); until then, what this run found waits here.

| Language | What there is | Would it seed? |
|---|---|---|
| he | `ויקיפדיה:סימנים לכתיבה מבוססת בינה מלאכותית`, revision 43047872 (8 Apr 2026), 42 revisions, CC BY-SA 4.0: created by translating en oldid 1323439249, its phrase lists rendered in Hebrew. Its own lines: the em dash is not used in Hebrew, so a good sign of AI or machine translation; and many of the signs also turn up in articles machine-translated from English, a false positive. No GitHub skill, no paper | No: a translated page, the bar Hindi set |
| fi | `Wikipedia:Merkkejä tekoälyn kirjoittamasta tekstistä`, revision 23993692 (10 May 2026), 35 revisions since Sep 2025, CC BY-SA 4.0: not a translation, its examples taken from Finnish Wikipedia: "ei ole vain X, vaan Y", the rule of three ("Stubbismi"), title case in subheadings as an anglicism, wrong inflection in translated text, chat citation residue ("+1"). Unfinished. Hakku/finnish-humanizer (MIT, `7a151e26b263`, 21 stars): 12 Finnish patterns (passive overuse, missing particles, translation structures) beside 15 general ones. A Tampere thesis on 15 texts, too thin | Yes, if fi gets a code: an original wiki page and a native list |

## Each language's style guide

What people write, which the office tests (move 3) start from. None is a source of signs, so none is in
`sources.toml`; none was read in full this run.

| Language | Guide | What it gives the plain-text guard |
|---|---|---|
| it | Accademia della Crusca (its language advice); for office text, the Guida alla redazione degli atti amministrativi (ITTIG-CNR and the Crusca, 2011) | the formulas of administrative letters; the dash that opens dialogue in fiction, which `humanizer-it` found flagged; guillemets and straight quotes both in use |
| tr | Türk Dil Kurumu, Yazım Kılavuzu and Güncel Türkçe Sözlük; for office text, the 2020 regulation on official correspondence (Resmî Yazışmalarda Uygulanacak Usul ve Esaslar Hakkında Yönetmelik) | the passive and "-mektedir" in official letters, which are normal; English-laced office Turkish ("plaza dili": "toplantı set etmek", "feedback") is what many people write, never a sign of a model |
| vi | Decree 30/2020/NĐ-CP on administrative documents, which haunguyendev/humanizer-vi follows | the set forms of official text ("Căn cứ...", "Kính gửi:", "Nơi nhận:", "Trân trọng"), which a sign must pass |
| id | Badan Bahasa: KBBI and EYD, fifth edition (2022) | the passive and formal register of academic and official Indonesian; "pun" written joined in conjunctions (`humanizer-indonesia` F10) |
| th | Office of the Royal Society (ราชบัณฑิตยสภา): its dictionary and punctuation rules; for office text, the Prime Minister's Office regulation on correspondence (ระเบียบสำนักนายกรัฐมนตรีว่าด้วยงานสารบรรณ, 1983) | Thai is written without spaces between words (`spaces = false`), so `\b` patterns need care; English loanwords mixed in are normal in office Thai |
| he | Academy of the Hebrew Language: punctuation, the maqaf against the dash | (no code) |
| fi | Kotimaisten kielten keskus, Kielitoimiston ohjepankki | (no code) |

## Dropped

| What | Why |
|---|---|
| th.wikipedia `วิกิพีเดีย:สัญญาณของการเขียนด้วยปัญญาประดิษฐ์` (rev. 13277686, 17 Sep 2026, 9 revisions) | Created by translating en oldid 1351507306; it even keeps English sections untranslated; nothing Thai of its own |
| citelogics-th/thai-humanizer (MIT, 16 stars, 2 commits) | Thai words, but laid out on blader/humanizer's groups, with no evidence and no false positives tested |
| nattkarn/humanizer-thai, inatbalthazar/humanizer-th | A port of blader/humanizer 3.1.0 with a Thai style note; a translation skill |
| Kasetsart N-gram paper (JMHS 8(1-2), 2025) and the Thai abstract move-structure study | Word substitution in eight children's stories; abstract structure, no sign |
| Persuaficial (arXiv 2601.04925, CC BY-SA 4.0) | Its linguistic analysis is English only; Italian is in its detection results alone |
| Garassino et al. (arXiv 2411.18403), Farrell's other two studies (2504.09164, 2601.17363) | Presuppositions in political text; 23 students and a reader-preference test, both covered by `farrell-2026-translators` |
| De Cesare's work on ChatGPT's Italian (Chimera; Lingue e culture dei media, CC BY-SA; Linguistik Online, CC BY; the 2026 book) | The articles found are about how biographies name women and about fables; the Chimera paper's page was behind a bot wall. Worth a look when the Generate-IT project (TU Dresden, from Sep 2025) publishes |
| Puricons/ai-italian-deslop (MIT, 1 star) | A linter whose accent rules flag what people type ("perche"), no evidence |
| bushrabeg/turkce-humanizer (MIT, 101 stars) | A journalist's taxonomy with no evidence; its five bans include the semicolon and fragments, which are style, not signs |
| DevVettel/turkish-humanizer (MIT), YusufGUNEL/humanizer-tr (MIT) | No evidence; YusufGUNEL's is built on DevVettel's and bushrabeg's. Its per-pattern "dokunma" lines are a pointer for the Turkish office test |
| coskuncay/humanizer-tr | Empty repository |
| Ozdemir (arXiv 2602.13504), IndoBERT and SVM theses, VietBinoculars and VietAIDetector (2509.26189, 2608.25478, 2405.03206) | Detection only |
| Turkish learner comparisons (DEvAD 12(1), 2026), Dervişcemaloğlu (2025) | Learners of Turkish as a foreign language; free indirect speech in fiction |
| Indonesian journal papers (Kopula, Predikat, Literasi) | Poetry, syntax of model text with no human baseline, morphology in chat: no comparison that names a sign |
| apissaj/humanizer-id (MIT, 29 stars) | An editorial guide for academic Indonesian whose rules trace to textbooks on effective sentences: a style guide, not evidence about models |
| ardha27/humanizer-id, williamkho77/claude-humanizer-id, dhank77/academic-humanizer-id | One commit, slang control, or "inspired by" an English skill |
| haunguyendev/humanizer-vi (MIT), Cand01t/viet-ai-humanizer, cthpAiden/humanizer-vi, Cat1m/humanizer-vi | A Vietnamese fork of blader/humanizer for administrative text, no evidence (its decree is in the style guides above); the others small, with no evidence |
| ContextBoxAI/vi-humanizer, duynguyen31241020400-lang/student-voice | A local rewriter; a student humaniser extension: rewriting tools, not lists |
| Press and blogs: studenti.it, punto-informatico, pasqualepillitteri.it, Pangram's it and tr pages, tamindir, howmanywords, lilys.ai, quantrimang, vnreview, findskill, detik, Jawa Pos, eraspace, Startup for Startup (he), insanelymac (fi) | SEO content, vendor translations of English lists, or forum advice; no evidence of their own |
| shalhevetvardi/humanizer-he-download | A download page, no list |

## Notes for the next steps

- The Turkish study and `humanizer-tr` disagree on "rol oynamak": an excess in one model's essays against a native
  reader who calls it natural. That is the case for a `weak` sign scoped to `gpt`, or none.
- `humanizer-it`'s calibration and `humanizer-tr`'s tests were run by their authors with models; none was read by
  this run's author as a native speaker. Each language still wants a native read (`CONTRIBUTING.md`).
- Thai is written without spaces: a Thai sign with `\b` would not work as written. Moot until Thai has a source.
- No family in `models.toml` for Anita (an Italian Llama tune) or Minerva.

## Recommended order for seeding

Most evidence first, one PR each.

| Order | Language | Why |
|---|---|---|
| 1 | it | Five sources: two measured or tested (`humanizer-it`'s calibration and false-positive tests, `farrell-2026-translators` with 69 readers), annotators' cues (`wang-2026-human-detection`), and three native lists (`scrittura-italiana`, `avoid-ai-writing-multilingual`, `humanizer-it`'s own). The most false positives on record of the seven |
| 2 | vi | Four sources: an exploratory excess-vocabulary comparison (`lee-2026-korean`), annotators' cues (`wang-2026-human-detection`), a native list whose false positives are stated (`vietnamese-humanizer`), and `slop-gate`'s Vietnamese rules. No study of office text |
| 3 | tr | Two sources: one measured study naming overused phrases with counts (`bergin-atasoy-2026-turkish`, GPT-4o mini, student essays) and a native list read by a native speaker, with a list of what not to touch (`humanizer-tr`). Few signs, `weak`, most of them `gpt` |
| 4 | id | One source (`humanizer-indonesia`), a native catalogue with false positives and excluded registers but no measure of what models write. If `propose-signs` finds no sign a second source backs, record id in the plan as having nothing to seed from |

Nothing to seed from:

- **th:** its only sources are a translated wiki page and skills built on blader/humanizer's groups with no evidence.
  The `any` signs carry Thai.
- **he:** its only source is a translated wiki page; and Hebrew has no language code.

Out of the catalogue's languages: **fi** has an original wiki page and a native list, enough to seed from, but no
language code. Adding he or fi to `languages.toml` is the maintainer's decision.
