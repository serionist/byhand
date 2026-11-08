# byhand: new sources for Spanish

Research date: 2026-11-09, the first run of `find-sources` (#32). Spanish is the second most spoken language with no
source in `sources.toml` (Hindi is first). Every page was read as data; nothing from them is copied here but titles,
licences and revisions.

## Searched

| Where | Queries or pages |
|---|---|
| the web, in Spanish | "señales de texto generado por IA en español frases típicas ChatGPT"; "rasgos lingüísticos de textos generados por ChatGPT en español estudio corpus"; the RAEL paper's title |
| the web, in English | "arXiv Spanish LLM-generated text stylometric vocabulary analysis" |
| es.wikipedia | the project and help namespaces for "inteligencia artificial", "texto generado", "chatbots", "IA generativa", "LLM" |
| Wikidata | the sitelinks of `Q136117782` (Signs of AI writing) |
| GitHub | repositories for "humanizer-es", "humanizar texto español", "escritura IA español patrones", "señales IA español", "humanizalo", "spanish ai writing patterns", "ai-tells spanish" |
| Hugging Face | datasets for "autextification", "spanish machine generated text" |

## Kept

| Id | What it shows | For `propose-signs` |
|---|---|---|
| `humanizer-es` | A Spanish skill and checker (MIT, commit `ac2a31be1a71`), its tells written in Spanish and ranked by strength: chatbot theatre, calques of English, grammar and rhythm, inflation, formatting, process leftovers. It tested itself blind against blader/humanizer and three Spanish skills, on texts from Claude and GPT. It says it does not try to beat detectors. Built on blader/humanizer's framework, so facts only. | the calques and the grammar and rhythm sections, which are Spanish's own |
| `alonso-simon-2025-spanish` | Alonso Simón et al., RAEL 23(1), 2025 (CC BY-NC 4.0): 17 lexical, punctuation and sentence-structure variables differ significantly between human Spanish and GPT-3.5 and GPT-4. The abstract doesn't name them. | the 17 variables, from the full text; scoped to `gpt` |
| `resende-castilho-2026-style` | Resende and Castilho, StyGenAI 2026: GPT-4o's original and translated text in English, Brazilian Portuguese and Spanish has higher lexical density and richness, rarer words, and more em dashes than human text. The paper's notice is CC BY-ND 4.0. | a `gpt` sign in `es` or `pt`, or evidence for an `any` one beside other languages' sources |

## Dropped

| What | Why |
|---|---|
| es.wikipedia: `Wikipedia:Comunicación mediante mensajes generados por inteligencia artificial` (`WP:Chatbots`, rev. 175850486) and `Wikipedia:Redacción con modelos de lenguaje grandes` (rev. 175831506) | Policy pages: no AI text in articles or on talk pages, and only "formal polish and commonplaces" as a trait. Too thin. Wikidata lists no Spanish version of Signs of AI writing. |
| Hainrixz/humanizalo (MIT, 97 stars) | Its word list is English's (blader/humanizer's), and its Spanish examples translate English ones: little Spanish of its own in what was read. |
| mattc95/Humanizer-es, Milevan/humanizer-es, alvaromieres9/humanizer-es, madebydiego/humanizador, omelyanchuk2593/humanizer-es | Small, one to five stars; `humanizer-es` credits all but mattc95's for its Spanish layer; omelyanchuk2593's is a port of blader/humanizer and humanizer-ru. madebydiego's country packs (Mexico, Bolivia) are worth a look when a variety matters. |
| ToniPerea/humanizar-texto-es, josedelsol1/escritura-humana, LucassToledo/anti-texto-basura, Carlosyekana/antislop | No licence or NOASSERTION, a few commits, no evidence behind the rules. |
| ljmor/my-humanizer-es-en, kevin0818-lxd/turnitout-essay-humanizer | Detector evasion: sold to get past stylometric detectors and Turnitin. |
| ROBOT-TALK corpus (Complutense, 5,017 Spanish texts by people and by Gemini, Claude, GPT, Mixtral and DeepSeek) | No download and no licence on its page. The RAEL paper is its team's; watch it for a release. |
| symanto/autextification2023 (Hugging Face) | CC BY-NC-SA, 2023 models only. |
| Press and blogs: pasqualepillitteri.it, wwwhatsnew, INESEM, Decrypt, El Heraldo | SEO content or retellings of English Wikipedia and Pangram; no evidence of their own. |

## Next

- Wikidata lists Signs of AI writing in Portuguese, Hebrew, Thai and Finnish too; none is in `sources.toml`. The
  2026-11-06 record calls the Portuguese and Thai ones translations.
- Hindi, the most spoken language with no source, was not searched here.
