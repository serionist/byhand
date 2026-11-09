# byhand: new sources for Portuguese, Hindi and Arabic

Research date: 2026-11-09, the second run of `find-sources`, Step 2 of `docs/plans/2026-11-09-more-languages.md`
(#49). Hindi (rank 3) and Arabic (rank 5) had no source; Portuguese (rank 9) had one shared paper
(`resende-castilho-2026-style`). Every page was read as data; nothing from them is copied here but titles, licences,
revisions and a few words named as facts. Eight sources added: four for pt, two for ar, one for hi, one for ar and hi
together. Languages with no source: 85 before, 82 after (hi, ar and kk leave the list).

## Searched

| Where | Queries or pages |
|---|---|
| Wikidata | the sitelinks of `Q136117782` (Signs of AI writing): de, en, fi, fr, he, pt, ru, th, zh, Commons. No hi or ar version |
| pt.wikipedia | A7, its revision history; the project namespace for "inteligência artificial", "LLM", "ChatGPT" |
| hi.wikipedia | the project namespace for "कृत्रिम बुद्धिमत्ता", "चैटजीपीटी", "एलएलएम", "AI" |
| ar.wikipedia | the project namespace for "ذكاء اصطناعي", "نماذج لغوية", "شات جي بي تي", "مولد بالذكاء" |
| arXiv | `abs:<Portuguese, Hindi, Arabic> AND (abs:"AI-generated" OR abs:"LLM-generated" OR abs:"machine-generated" OR abs:stylometric)`; P18 and P19 by id |
| ACL Anthology | PROPOR 2024 and 2026, STIL 2025 volumes, titles with generated, LLM, GPT or detect |
| the web, in each language | "características linguísticas textos gerados por ChatGPT português"; "como identificar texto escrito por IA em português expressões típicas do ChatGPT"; "एआई द्वारा लिखा गया हिंदी टेक्स्ट कैसे पहचानें"; "علامات النص المكتوب بالذكاء الاصطناعي بالعربية عبارات شات جي بي تي"; in English, "Hindi LLM-generated text stylistic linguistic analysis" |
| GitHub | repositories for "humanizer pt", "humanizer-br", "humanizador", "escrita ia portugues", "evitar escrita ia", "anti-slop portugues", "sinais ia", "humanizer hindi", "hindi slop", "हिंदी", "humanizer arabic", "humanizer-ar", "arabic ai writing", "arabic slop", "arabic ai tells", "indic ai writing", "hinglish humanizer" |
| Hugging Face | datasets for "hindi ai generated", "AG_hi", "arabic ai generated", "ALHD", "Ar-APT", "portuguese ai generated", "abjadgeneval", "arageneval" |

## Kept

| Id | What it shows | False positives it lists | For `propose-signs` |
|---|---|---|---|
| `wikipedia-pt` | A7 at revision 73274816 (23 Oct 2026), CC BY-SA 4.0: a full translation and adaptation of the English page (oldid 1381575954), its examples translated. It says English word lists don't carry over to Portuguese and adds no measured Portuguese word. Six revisions, so weekly | Yes: perfect grammar, mixed registers, "robotic" or formal text, lone connectors ("além disso"), and any variety of Portuguese (Brazilian, European, African) are not signs; its "signs of human writing" list plain "é" and "tem" | a translated page, so the evidence for an `any` sign beside other languages' sources; little of pt's own |
| `evitar-escrita-ia` | B18, now read: mariorabeloneto/evitar-escrita-ia, one commit (`a4b596e6f8b0`). Its LICENSE is MIT, adapted from `avoid-ai-writing` (MIT, listed); GitHub reads NOASSERTION. A European Portuguese skill with a lexicon rebuilt for Portuguese in three tiers, connectors, openers and closers, typography (title case and a full stop after a list label are English habits), and Brazilian forms in text meant for Portugal. No evidence behind its lists | Yes, its own section: funding applications (FCT, Portugal 2030), legal and administrative formulas, technical "poderá", academic nominalisation and the passive | its typography and closers, each beside a second source; the Brazilian-forms section is a variety, not a sign of AI |
| `humanizer-pt-br` | eurafaeldecarvalho/humanizer-pt-br (MIT, `a18e130ad39e`): 45 Brazilian Portuguese patterns, each counted on 30 texts Grok 4.7 wrote for the repo and on 30 public-domain paragraphs from before 1930 (Machado de Assis, Lima Barreto and others): 5.93 marks a text against 0.03. Its own originality check found nothing shared with blader/humanizer or two other pt skills. Its texts were written for it by one model, and its blind reader test isn't done | Yes: "no que diz respeito a" fired once in the human control, and its notes call that a formal formula, not a model's | the patterns with several hits and none in the control, scoped to `grok` |
| `andrade-2026-portuguese` | Andrade, Silva and Pardo, PROPOR 2026 vol. 2, pp. 148-158: fake news written by Sabiá-3 against human Brazilian fake news (Fake.br, FakeTrueBR). The machine's words are longer, it uses more adjectival modifiers and intensifying adverbs and adjectives, shows less syntactic variety, and its most distinctive terms include "fontes anônimas", "revelação bombástica", "debates acalorados", "enfatizando" and "cruciais". Human texts vary more. The paper says only ©2026 ACL; the Anthology's footer says CC BY 4.0: the stricter holds | No list; it says the part-of-speech difference, though significant, is negligible in size | the modifier density and a few terms; Sabiá is not a family in `models.toml`, so `any` or a new family |
| `al-shaibani-2025-arabic` | P18, Al-Shaibani and Ahmed, arXiv 2505.23276 v2 (CC BY-NC-SA 4.0): Arabic academic abstracts and book and hotel reviews, human against ALLaM, Jais, Llama and GPT-4, generated from a title, from title and content, or by polishing. All four models overuse their top words and drop off faster in the long tail; human abstracts use more domain and regional terms. Frequent model words include تعزيز, الضوء (from تسليط الضوء), بشكل, يمكن and منهجية. Model reviews are 25 to 72% of human length | No | a frequent-word sign scoped to `gpt` and `llama`; ALLaM and Jais are not families in `models.toml` |
| `humanizer-ar` | hazemshan1-rgb/humanizer-ar (MIT, `5289d4a60aa5`, written in one day): 27 Arabic patterns, not a translation of the English list, citing P18, ALHD and Arabic collocation work: stock connectors (تجدر الإشارة إلى, علاوة على ذلك), "تم + مصدر", light-verb calques (قام بإجراء), Western dashes and quotation marks, mixed digit systems. Its catalogue rests on "direct observation" with no published data | Yes, tested on samples: partial diacritics are normal Arabic, long و-joined sentences are the norm in formal Arabic (median 35 words), and the tatweel in هـ (Hijri year) is not decoration | the connectors and typography, each beside a second source; a calque needs evidence models write it more (the plan's rule) |
| `wang-2026-human-detection` | Wang et al., arXiv 2502.11614 v3, ACL 2026 Main (CC BY 4.0): 19 annotators told human from machine text in 16 datasets and 9 languages (87.6% on average), and wrote down the cues. Hindi (BBC news against GPT-4o): the machine names fewer people and dates, uses no idioms and almost no Urdu-origin words, and drops in English words. Arabic (GPT-4o, Qwen2): formulaic emoji in tweets, Qwen2 mixing dialects and other languages, news cut into short sections where people write one block, generic lines, fewer numbers, URLs and dates, no English terms, Markdown in summaries | Partly: typos, messy spacing, sporadic English terms and hashtags were human cues; human Arabic tweets were taken for machine text 36% of the time | the Arabic segmentation and Markdown cues and the Hindi English-word cue, scoped to `gpt` (and `qwen` for dialect mixing) |
| `agrahari-2026-shakti` | Agrahari, Kumar and Singh, arXiv 2610.41232 v1 (arXiv's licence): SHAKTI, Hindi essays, news, Wikipedia and answers from eight model families (GPT-3.5 and GPT-5, Gemini 2.5 Flash, Llama, Mistral, Gemma, Aya, Sarvam). Model Hindi is longer, with more sentences, paragraphs and punctuation, simpler by readability scores, with more varied sentence lengths; averages only, no words or phrases | No | at most a structure sign beside `wang-2026-human-detection`; nothing with a pattern |

## Each language's style guide

What people write in each language, which the office tests (move 3) start from. None is a source of signs, so none is
in `sources.toml`.

| Language | Guide | What it gives the plain-text guard |
|---|---|---|
| pt | Ciberdúvidas da Língua Portuguesa (ciberduvidas.iscte-iul.pt), the nearest to Fundéu, answering usage questions for both varieties; for Brazilian office text, the Manual de Redação da Presidência da República, 3rd ed., 2018 (gov.br, reuse allowed with credit) | the formulas of official letters and mail, which are normal; both varieties' spelling and forms, which are never signs. Not read in full this run |
| hi | Central Hindi Directorate, देवनागरी लिपि तथा हिंदी वर्तनी का मानकीकरण, revised 2024 (chd.education.gov.in); the Department of Official Language (rajbhasha.gov.in) for office Hindi | the danda and standard spelling. Not a guide to what people write: office Hindi is often Sanskritised, and messages mix English or are typed in Roman script (Hinglish), both normal and both to be passed |
| ar | no Fundéu for Arabic: the Arabic Language Academy in Cairo (arabicacademy.gov.eg) for usage; Microsoft's Arabic localisation style guide (ara-sau, download.microsoft.com) and Mozilla's for typography | Arabic punctuation (، ؛ ؟), digit systems, long joined sentences in formal Modern Standard Arabic, dialect in messages |

## Dropped

| What | Why |
|---|---|
| P19, CT² for Hindi (arXiv 2407.15694, CC BY-SA 4.0) | Detection only, as the plan said: 26 models ranked by how detectable their Hindi is, no stylistic finding. Its dataset, `ishank31/CT2_AG_hi`, is a pointer for #50 |
| IndicDetect (arXiv 2608.29919) | Detection only, Hindi, Telugu, Tamil |
| Almohaimeed et al. (arXiv 2511.16690, CC BY 4.0) | Detectors, not signs: they flag human Arabic lightly polished by a model. A caution for the plain-text guard, recorded here |
| Alsadhan (arXiv 2603.23251) | Says no Arabic linguistic analysis was done |
| ALHD (arXiv 2510.03502), KFUPM-JRCAI/arabs-dataset (AGPL-3.0) | Datasets with no signs named: pointers for #50 |
| pt.wikipedia: `Wikipédia:Grandes modelos de linguagem` (rev. 73268669), `Wikipédia:Inteligência artificial` (rev. 73196230), an Esplanada thread of Aug 2025 | Policy, a translated essay and the discussion that led to A7: no signs of their own |
| ar.wikipedia: `ويكيبيديا:الذكاء الاصطناعي التوليدي` (rev. 76950630), `ويكيبيديا:المحتوى المولد بالذكاء الاصطناعي` (rev. 75050670), `ويكيبيديا:الإزالة الاحترازية للمحتوى المولد بالذكاء الاصطناعي` (rev. 77008427), `ويكيبيديا:لا تكتب ردودك بالذكاء الاصطناعي`, `ويكيبيديا:الترجمة بمساعدة نموذج لغوي كبير` | Policy and essays: a ban, a removal procedure, "unencyclopedic style" as the only trait. Too thin |
| hi.wikipedia | No page on AI writing; hits were deletion discussions and village-pump archives |
| carlosafjr-dev/humanizer-br (99 stars), mackswendhell/humanizer-pt-br (64), rpiochi/humanizer-pt-br, opaulomarcondes/humanizador-pt, zanonicode/anti-slop-ptbr, dpnascimento/escrita-anti-slop-ptbr | MIT, but each says it adapts English Wikipedia or blader/humanizer, with no Portuguese evidence: translations that add nothing |
| profdorly/humanizador, Blackspirits/humanizer-pt-pt, JoaoAreias/escrita-natural, msigor/humanizer-br, geovani-ariel/humanizer-pt-br | MIT, built on blader/humanizer or about translationese; read no further than the README, no evidence named |
| AndreAlmeidaDC/humanizador, fernandoms88-ui/humanizer-pt, gabrielkashimarki/humanizer-ptbr, invidtiv/humanizer-pt-pt, cfoschiera/humanizer-ptbr | No licence or NOASSERTION, few stars |
| MrBridgeHQ/human-writer-hi (and its family in six other languages) | Detector evasion: it targets a score under 25% on Copyleaks and GPTZero |
| ashstrc/hindi-ai-slop-detector, slop-slappy/slopslappy | No licence, a classifier; a toy that plays sounds |
| turky015-oss/Arab-Writer (23 stars) | No licence, no evidence behind its 11 groups |
| OthmanAdi/humanizer-semitic, finestructure-ai/humanizer-multilingual, batuhan-bas/trilingua | MIT, structured on blader/humanizer; trilingua's Arabic cites P18, now listed, and Wikipedia |
| drxvb/arabic-ai-text-humanizer | MIT (NOASSERTION on GitHub), but its "empirical" file profiles human Arabic only (Quran among it), with no AI text beside it |
| ahmeddabak/claude-arabic-writing, JoeUX97/arabic-ai-detox, karem505/arabic-humanizer, ziadfaisalaljdy-beep/arabic-humanizer | About machine-translation Arabic, or a few commits with no evidence |
| Press and blogs: aljarida.com (E5), Pangram's pt and ar pages, Brazilian how-to posts (Forbes Brasil, Olhar Digital, Hora de Codar), Hindi detector pages | SEO content or vendor translations of English lists; no evidence of their own |

## Notes for the next steps

- No family in `models.toml` for ALLaM, Jais, Sabiá, Aya or Sarvam: a sign from them is `any` or waits for a family.
- `-I` makes Python ignore `PYTHONIOENCODING`; this run used `-X utf8`. The skill's Traps row now says so.
- Text in PDFs of Arabic papers extracts in visual order (letters reversed): read the words back before using one.

## Recommended order for seeding

Most evidence first; Step 3 (#13) comes before hi or ar whichever is next.

| Order | Language | Why |
|---|---|---|
| 1 | pt | Five sources: two measured studies with words (`andrade-2026-portuguese`, `resende-castilho-2026-style`), a counted pattern set with a human control (`humanizer-pt-br`), and two false-positive lists for the guard (`wikipedia-pt`, `evitar-escrita-ia`). It needs no #13 |
| 2 | ar | Three sources: measured overused words over four models (`al-shaibani-2025-arabic`), annotators' cues (`wang-2026-human-detection`), and a native catalogue whose false positives are tested (`humanizer-ar`). Tanween needs #13 first |
| 3 | hi | Thin: two papers, cues and averages, no phrase a pattern could match. It can carry a few structure signs (English words mid-sentence, short sections), `usual` at most; if `propose-signs` finds no sign two sources back, record hi in the plan as having nothing to seed from |

None of the three has nothing at all; Hindi is the closest.
