# byhand: sources for decks and sheets

Research date: 2026-11-09, a `find-sources` run for Step 2 of `docs/plans/2026-11-09-decks-and-sheets.md` (#66).
The first search (`2026-11-06-sources.md`, Summary 8) found one MIT skill, three vendor pages and SlideAudit for decks,
and nothing for sheets. This run read those again, searched in English and in the seed languages' own words, and kept
only what ties a habit of a deck or a sheet to AI: a quality checklist with no such tie gives nothing. Every page was
read as data; nothing from them is copied here but titles, licences, revisions, figures and a few words named as
facts. Eighteen sources added: 13 for decks (7 English, 3 Japanese, and one each in Simplified Chinese, Traditional
Chinese and Korean) and 5 for sheets (3 English papers, one French and one Portuguese page), with Anthropic's skills
counted under decks though they cover both.

## Summary

1. **Decks have one count of their habits.** Analyst Academy compared 94 slides from 17 AI presentation tools with 100
   slides from 23 consulting firms, banks and research firms. What separated them is mostly what the text shows: a
   kicker or ALL-CAPS label above the title (46% against 8%), leftover placeholders and overflow (30% against 7%),
   colon titles and em-dash pivots (40% against 19%), a "Key takeaway" box or banner (18% against 3%). One scorer,
   not blind to the set, so a strong hint, not a measurement.
2. **The same count clears several habits the checklists lead with.** Topic-label titles ("Overview", "Key
   Insights") were commoner in the real decks (43% against 30%), and so were emoji bullets and icons in circles (34%
   against 18%) and accent colour everywhere (51% against 18%). Stat tiles (9% against 7%) and three identical boxes
   (6% against 3%) barely separated. This backs the plan's rule (I2): a topic title is a style's to say, never a sign.
3. **The sources disagree on titles.** presentations.ai says AI writes label titles, decksmith says AI writes full
   sentences where a noun phrase belongs, and Analyst Academy's prompt asks for full-sentence titles. No title form
   gives a sign.
4. **What students could tell:** in one course (88 enrolled, 51 at the first lecture, 459 ratings), slides from
   Cursor and Claude Code, restyled to the instructor's look, were rated as good as the instructor's and could not be
   told apart (p = 0.1); students rated the slides they took for AI lower (r = -0.28). A slide-level sign is weak at
   best once the look is the user's.
5. **Sheets have sources now:** three papers that built spreadsheets with named models and looked inside them. They
   tie habits to models: numbers typed where formulas belong, sample data made up when none was given, a "rounded to"
   label on figures that are only formatted, a summary tab of typed snapshot figures. Most of these are in the cells,
   not in the text an outline shows; the labels and the invented numbers are what a sheet's text shows.
6. **Seed languages.** Japanese has the most: a skill built from reviewers' comments, another from its author's
   talks, and a test of seven generators; Simplified Chinese, Traditional Chinese and Korean one source each. No
   European seed language has a deck source of its own: what came up was vendors' translations of English posts and
   Russian SEO pages. Several habits meet across languages: a label above the title (en, ja), a takeaway bar that
   restates the slide (en, ko), groups of three by habit (en, ja), titles in one repeated frame (colon titles in en
   and ja, "A가 아니라 B" in ko), invented or doubtful numbers (en, ja). Those are the `any` candidates.
7. **Sheets in other languages:** one habit with worked examples, a formula in English Excel's form (English
   function names, commas) in a French or Portuguese sheet. Nothing for sheets in de, es, it, hu, ru, tr, vi, ar, zh,
   zh-Hant, ja or ko beyond formula errors, which are no habit a sheet's text shows.

## Searched

| Where | Queries or pages |
|---|---|
| The first search's deck sources | `analystacademy/flight-check` at its head; plusai.com, presentations.ai and uxdesign.cc (E6) |
| Web, English | "signs a slide deck was made with AI ChatGPT Claude Gamma tells"; "AI-generated presentation dead giveaway slides emoji titles key takeaways"; "AI-generated spreadsheet tells ChatGPT Claude Excel formulas hardcoded hallucinated functions"; "uxdesign.cc de-slopify your designs"; "presentations.ai common mistakes AI generated presentations" |
| arXiv | `abs:spreadsheet AND (abs:ChatGPT OR abs:LLM OR abs:"large language") AND (abs:errors OR abs:quality OR abs:formulas)`; `(abs:slides OR abs:presentation OR abs:deck) AND (abs:"AI-generated" OR abs:"LLM-generated" OR abs:"machine-generated")`; `(ti:slide OR ti:slides OR ti:presentation) AND (abs:human-made OR abs:"human-designed" OR abs:"human-authored") AND (abs:LLM OR abs:agent)` |
| GitHub | `anthropics/skills` at its head, `skills/pptx` and `skills/xlsx`: the skills that make the file in a Claude session |
| zh | "一眼看出是AI做的PPT 特征"; "AI味 PPT 怎么去掉 标题 emoji 总结页"; "AI生成PPT 通病 知乎"; "AI做的PPT 一眼就能看出来 AI味 标题 金句 三段式"; "AI味 PPT 去除 指南 豆包 Kimi 谢谢观看 目录页"; "ChatGPT Excel 公式 幻觉 不存在的函数"; "AI做的Excel表格 一眼看出 公式 写死"; CNKI for "AIGC 演示文稿 同质化"; GitHub code for "AI味" PPT and for hardcoded formulas in generated xlsx |
| zh-Hant | "AI 簡報 一看就是 AI 做的"; "AI 簡報 AI感 標題 條列 emoji 謝謝聆聽"; "簡報 AI味 去除 投影片 標題 破折號"; "AI Excel 試算表 公式 錯誤 幻覺" |
| ja | "AIっぽいスライド 特徴"; "生成AI パワポ バレる 特徴"; "AIが作ったスライド 見分け方 AIっぽさ note"; Zenn and Qiita for "AIっぽい スライド 絵文字 見出し Claude"; "ChatGPT Excel 関数 存在しない 嘘 数式 間違い"; "AIが作ったExcel 特徴 ハードコード"; "Copilot Excel 数式 間違い 実際に試した"; J-STAGE for "生成AI スライド 評価"; GitHub code for "AIっぽ" スライド |
| ko | "AI가 만든 PPT 티 나는 특징"; "AI PPT 특징 티난다 챗GPT 슬라이드 이모지 제목"; "AI로 만든 PPT 티 나는 이유"; "챗GPT 발표자료 AI 티 문구"; "챗GPT 엑셀 수식 오류 없는 함수 틀린 수식"; "코파일럿 엑셀 수식 틀림 직접 테스트"; KCI for "생성형 AI 프레젠테이션"; GitHub code for "AI 티" 슬라이드 |

The searches in languages other than English were run by two helper agents of this session, one for zh, zh-Hant, ja
and ko and one for the European languages, Russian, Turkish, Vietnamese and Arabic; each kept source here was then
read again at its head or on its page.
| de | "KI-Präsentation erkennen typische Merkmale Folien ChatGPT"; "KI-generierte Präsentation erkennen Emojis Überschriften Aufzählung Fazit Folie"; "Lehrer erkennen KI Referat Präsentation Folien"; "c't Test KI-Präsentationstools"; t3n on AI decks; "ChatGPT Excel Formeln erfundene Funktionen Fehler KI"; "Copilot Excel Fehler KI Tabelle halluziniert Werte"; "ChatGPT Excel Formel englische Funktionsnamen Komma statt Semikolon"; GitHub code for "KI-Präsentation" Folien, "AI slop" Folien, "KI-typisch" Folien and "Vielen Dank für Ihre Aufmerksamkeit" in `SKILL.md` |
| fr | "présentation générée par IA reconnaître slides signes"; Blog du Modérateur on Gamma and Copilot decks; "diaporama fait avec ChatGPT ça se voit"; "ChatGPT Excel formules inventées fonction inexistante #NOM?"; GitHub code for "Merci de votre attention" in `SKILL.md` and "typique de l'IA" diapositives |
| es | "presentación hecha con IA cómo se nota diapositivas"; Xataka on AI decks; "profesor detectar presentación PowerPoint hecha con ChatGPT"; "ChatGPT fórmulas Excel inventa funciones"; "ChatGPT fórmula Excel coma en lugar de punto y coma"; GitHub code for "Gracias por su atención" in `SKILL.md` |
| pt | "slides feitos por IA como identificar apresentação ChatGPT sinais"; "apresentação feita com IA dá pra perceber"; "ChatGPT Excel fórmulas erradas inventa função planilha" |
| it | "slide fatte con l'intelligenza artificiale come riconoscerle"; "presentazioni generate con IA errori tipici slide ChatGPT Gamma"; "ChatGPT Excel formule sbagliate funzioni inesistenti" |
| hu | "MI-vel készült prezentáció jelei felismerni"; "AI-s diasor ChatGPT prezentáció tipikus hibák"; "ChatGPT Excel képlet hibás magyar függvénynevek pontosvessző" |
| ru | "как понять что презентацию сделала нейросеть признаки"; habr and vc.ru on generated decks ("Спасибо за внимание", emoji, titles, "три пункта"); CyberLeninka for studies of generated presentations; "ГигаЧат OR YandexGPT презентация недостатки"; "нейросеть Excel формулы ошибки выдумывает функции"; "ChatGPT формула Excel английские названия функций запятая"; GitHub code for "Спасибо за внимание", "ИИ-презентац", "признаки ИИ" слайд and "ИИ-слоп" |
| tr | "yapay zeka ile hazırlanmış sunum nasıl anlaşılır"; "yapay zeka sunum slayt belli oluyor hatalar"; "ChatGPT Excel formül hatalı olmayan fonksiyon" |
| vi | "dấu hiệu slide do AI tạo nhận biết bài thuyết trình ChatGPT"; "ChatGPT công thức Excel sai hàm không tồn tại" |
| ar | "علامات العرض التقديمي المولد بالذكاء الاصطناعي شرائح"; "أخطاء ChatGPT في صيغ Excel دوال غير موجودة" |

## Kept: decks

| Id | What it shows | Ties to AI | For `propose-signs` |
|---|---|---|---|
| `flight-check` | Analyst Academy's deck review skill (MIT, `ca975a186188`, 13 May 2026, 25 stars). Six checks; one is AI authorship: every framework three steps or a 2x2 whatever the logic, bullets that all open with the same verb form, filler slides headed "Overview", "Context" or "Background", a closing slide that restates the agenda, em dashes on every slide, a slide that still reads true with another company's name in it. Its false-positive guard: one em dash or one "leverage" is no sign, the pattern on every slide is. The source check says AI-assisted decks invent plausible citations, real organisations with report titles that don't exist. The other checks (action titles, specificity, MECE, 3D charts, `[TBD]`) are quality checks | The authorship check and the citations, by its own word; no evidence or count | the structural tells as `en` signs beside a second source: the three-by-habit lists (Analyst Academy counts them), the filler slide titles; the quality checks give none (plan, I2) |
| `analyst-academy-not-ai-decks` | The same company's page "Remove the AI slop from your decks" (© 2026 Analyst Academy; Last-Modified 9 Nov 2026), 30 tells, each rated by a count of 94 AI slides (frames of a video comparing 17 tools) against 100 real slides (sampled from SlideStart, 23 firms, 90 decks, no covers). Strong: anything above the title (46/8), production slips with leftover placeholders such as "Click to add" or "[Detail]" (30/7), colon titles and em-dash pivots (40/19), a full-height coloured edge strip (17/1), a takeaway box or bottom banner (18/3); 80% of AI slides had one, 21% of real ones. Some signal: groups of three by habit (21/11), "unlock, elevate, delve" words (15/8), inflated significance (3/0), everything centred (6/0). Not measured: the same layout on every slide, a "challenges and future prospects" ending, a full-sentence subtitle on the cover | Its own count, with its limits stated: one scorer who knew the set, and the AI set from video frames | the first source of deck signs with a count: the label above the title, the takeaway box and the colon or dash titles as `en` signs; the placeholders as an artefact; its "commoner in real decks" list as what a `passes` outline holds |
| `plusai-2026-slides` | Dan Li, Plus AI, 15 Jul 2026 (all rights reserved; the page has changed since the first search). Four patterns from "hundreds of decks" made with Claude, ChatGPT and Plus AI: an italic serif phrase at the end of titles, a coloured bar and an ALL-CAPS "eyebrow" label on every block, data as a row of dashboard stat tiles that invite plausible round numbers, a cream background with muted red accents | Names Claude and ChatGPT; opinion, no count. A vendor of a deck generator | the eyebrow label, beside Analyst Academy's count; the stat tiles only as invented numbers (the count clears the tiles); the rest is look, outside the plan |
| `presentations-ai-2026-mistakes` | Dhruv Saxena, Presentations.AI, updated 30 Oct 2026 (all rights reserved; the old "common mistakes people make" URL now redirects here). Twelve mistakes of AI-built decks: text overload because the tool tries to be complete, label titles such as "Market Overview", "Key Benefits" or "Next Steps", invented statistics formatted like the real ones, a topic list with no build, a slide for every sub-point, decorative icons and stock images | Says AI does each; opinion, no count. A vendor of a deck generator; the page has translations in ten languages, the vendor's own, so they count as English | the invented statistics and the slide per sub-point beside a second source; its label titles are contradicted by Analyst Academy's count |
| `decksmith-2026-seven-signs` | decksmith on DEV, 14 Sep 2026 (no licence stated). Seven failures its render checks kept finding in generated decks: everything centred, three cards whatever the number of items, a full sentence as the title, a big number with no year or source ("models are good at filling in plausible figures"), an icon on every bullet, text that clips, margins that drift between slides | From its own automated checks of generated slides; no count published | three cards for two or five items, beside `flight-check` and Analyst Academy; its sentence titles contradict presentations.ai |
| `leinonen-2026-slides` | Leinonen, Zhang and Hellas, "AI-Generated Slides: Are They Good? Can Students Tell?" (WCCCE 2026, arXiv v1, CC BY 4.0). Slides from NotebookLM, M365 Copilot, Claude, Cursor and Claude Code, from one instructor's notes: Copilot gave irrelevant large images and too much text, NotebookLM a long-winded introduction, Claude Code and Cursor slides "too complete"; Cursor added presenter notes unasked; the instructor deleted the generated "learning objectives" slides. Students rated AI and human slides alike (median 5 of 7) and could not tell them apart; they took the slides they rated lower for AI | Per tool, by educators' narrative review and a student survey; one course, one institution | evidence for caution: a sign on slide text is weak once the look is the user's; the added "learning objectives" slide and unasked notes as candidates beside a second source |
| `anthropic-skills` | Anthropic's `pptx` and `xlsx` skills (Apache 2.0, `2c5958ecac7c`, 6 Nov 2026), what makes the file in a Claude session. `pptx` tells the model that every slide needs a visual element and no slide is text only, offers icon-and-text rows, 2x2 grids and large stat callouts, and says accent lines under titles and coloured edge stripes read as AI-generated; `xlsx` asks for formulas, never typed results, the unit in the header ("Revenue ($mm)"), a source note for every typed number, blue inputs | Instructions to a generator, not observations: what a Claude deck holds by default, and what Anthropic itself calls an AI look | not a sign source alone: it shows what a maker adds that `write`'s outline doesn't (the plan's I3), and the defaults a sign beside a measured source could name |

## Kept: decks in other languages

| Id | What it shows | Ties to AI | For `propose-signs` |
|---|---|---|---|
| `jinba-consulting-pptx` | Carnot's consulting-deck skill (MIT, `60affb5ea3fe`, 8 Nov 2026, about 1,500 stars), `ai-smell-lexicon.md` and `slide-rules.md`, in Japanese. Says its core comes from comments real reviewers made on decks as "AIくさい": over-polite wording that explains everything, the same stock line repeated, traffic-light tables and emoji before headings; then a list of Japanese markers: empty intensifiers, katakana business words, nominalised verbs (最適化, 推進, 実現), "ポイントは3つあります" frames, まず・次に・最後に numbering, titles that state how many items the slide holds ("3つの理由"), which it says AI tends to write, a "label：" prefix on every title, which it says plain AI writes on every page. Its deck check fails a deck with a placeholder left in (`◯◯`, `Text N`) and warns when one sentence pattern makes six titles in ten | Review comments, by its own word, and thresholds in a script; no count published | the count-in-the-title and the label prefix as `ja` deck signs; the three-frame beside `en`'s groups of three |
| `lt-slide-skills` | kakira9618's lightning-talk skill (MIT, `202873468ef5`, Aug 2026), `compose.md`: invented parts, card grids, box-and-arrow flows, English kicker labels and decorative quote marks, turn a slide into an "AIスライド" at once; also bans the AI stock phrases 〜することができます, 〜を実現, 様々な, 効率的 | The author's rules, drawn from two of their own talks; one sentence of ties | the English kicker label in a Japanese deck, beside Analyst Academy's label above the title: a second language for that sign |
| `kiyo-2026-ai-slides` | KIYO, "AIっぽいスライド大全", note.com, 23 May 2026 (no licence stated). One prompt run through Microsoft 365 Copilot (three models), Claude, Genspark, Manus and Gemini, then the author's notes on what made the output AI-like: long sentences with few noun endings, unclear katakana, abstract terms, vague conclusions, no numbers, no comparison or alternative, the same rhythm in every bullet list, circled numerals, charts with numbers the reader doubts, colour bars and icons with no meaning | Seven named generators, one prompt, the outputs shown; no count | uniform bullet rhythm and doubtful chart numbers as `ja` candidates beside a second source |
| `report-de-ai-voice` | ashleyw57's skill for taking the AI tone out of report text, `SKILL.zh.md` (no LICENSE file, `fd1503eb8fab`, Aug 2026). Its PPT scene: slogan titles ("本周硕果累累") detached from the content, cards stacked with adjectives and no action or number, status labels no one can check ("稳步推进", "积极对接"), cards all of one length and shape, evaluative words in tables and chart notes ("显著", "大幅"), next steps that fit anything ("持续推进"). It says bureaucratic jargon (抓手, 闭环) is not AI tone but Chinese officialese, a false positive it names | Its author's rules; the long-text scene follows Wikipedia's Signs of AI writing through Humanizer-zh, the PPT scene is its own | slogan titles and uncheckable status labels as `zh` deck candidates, with its jargon note for `passes` |
| `managertoday-2026-decks` | 尤韻蓉, 經理人, "簡報該怎麼「去 AI 味」", 4 Aug 2026 (all rights reserved; reprinted by TechNews). After the book 《超有料！職場第一實用的AI簡報術》 and the presentation coaches 張忘形 and 王永福: AI deck text stacks ornate adjectives and stock phrases (瞬息萬變, 前所未有), ends on overheated rally lines, stays bland to suit everyone, has "design but no realness", and crams one slide | A book and two coaches, by their observation; no count | rally-line closings and stacked ornate adjectives as `zh-Hant` candidates, beside the `zh-Hant` prose sources |
| `agent-kit-briefing` | kimjisub's agent kit (MIT, `91836f5bd825`, 8 Nov 2026), the briefing-deck review's section 7, "AI 티 나는 문장 점검": self-praise lines ("정직하게", "숨기지 않고"), a bottom bar that restates the subtitle or body, weighty modifiers (본질적, 근본적), "X가 아니라 Y" pairs again and again, slogan lines ("~가 곧 ~다") | A checklist, by its author; no evidence | the restating bottom bar, beside Analyst Academy's takeaway box: a second language for that sign |

## Kept: sheets

| Id | What it shows | Ties to AI | For `propose-signs` |
|---|---|---|---|
| `grossman-2025-spreadsheets` | Grossman, Chen and Datuashvili, "Spreadsheet Modeling Experiments Using GPTs" (EuSpRIG 2025, arXiv v1, CC BY 4.0). Eight small problems put to the "Excel AI" GPT, judged on each input in a cell, formulas, no hardwired numbers, labels, accuracy. When no data was given it either left blank input cells or made up representative data (daily apple prices for a month); one model had a column of typed numbers where formulas belonged; "Create an Excel model. Use cell formulas." still gave a sheet with no formulas; runs did not reproduce | A named GPT tool, with the prompts and figures; ChatGPT-4o run on the same eight for comparison | invented sample data in a sheet, beside the plan's own rule (a sheet's text has the user's numbers or empty cells) |
| `yen-2026-mbabench` | Yen, Poeltl and others, "MBABench" (Columbia Business School, arXiv v5, 19 Aug 2026, CC BY 4.0). 18 agents building finance workbooks from scratch. Claude for Excel typed values where formulas belonged, a whole model at worst, and a ratio typed into a formula; GPT-5.4 typed 24.7% of answer cells as plain numbers; ChatGPT Pro sometimes shipped a model sheet of a few typed labels and numbers, and spread "ERR: Missing …" fallback strings down whole columns; Grok 4.20 and Kimi K2.5 wrote no formula on 5% and 17% of tasks, and Grok reported a "complete" model with invented answers | Per model, with task ids and counts | typed results and invented answers as model habits; few show in a sheet's text, so `weak` at most |
| `futura-2023-chatgpt-excel` | Daniel Ichbiah, Futura, "Comment utiliser ChatGPT avec Excel ?", 30 Nov 2023 (all rights reserved). Worked examples: ChatGPT first gave a formula for the English Excel, English function names with commas, and had to be told the sheet was in French Excel, which takes French names (VPM, ALEA.ENTRE.BORNES) and semicolons; the article says to repeat that reminder | ChatGPT, by name, in the author's own session | a formula in English Excel's form in a French sheet, beside `hashtag-2024-chatgpt-excel`: the same habit in two languages, so a candidate `any` sheet sign that a person's sheet in English never shows |
| `hashtag-2024-chatgpt-excel` | Diego Monutti, Hashtag Treinamentos, "Como Criar Fórmulas Complexas no Excel com ChatGPT", 3 Dec 2024, updated 24 Oct 2025 (all rights reserved; a training firm). Worked examples with screenshots: ChatGPT wrote a FILTRO formula with commas between the arguments, where Portuguese Excel takes semicolons, because the separator wasn't named in the prompt | ChatGPT, by name, with screenshots | as above, for Portuguese |
| `poeltl-2026-mbabench-2` | Poeltl, Yen, Shea and others, "MBABench-2.0" (arXiv v1, 22 Oct 2026, CC BY 4.0). 101 tasks, 129 criteria, 20+ agents on Claude, GPT, Gemini, Grok, Kimi and Qwen models, graded against a house standard every agent received. Appendix K per model: a "rounded to $0.01" label on figures that are only formatted (Fable 5.1 in three harnesses, GPT-6 Astra in ChatGPT Work, GPT-5.6 Sol), where GPT-6, Grok 4.6 and Kimi K3 write "shown to"; summary tabs of typed snapshot figures or narrative (Grok 4.6, Kimi K3, Gemini 3.8 Flash); sense checks that test outputs only against the workbook itself and say there is no outside benchmark (GPT-6 family); new blocks below an inherited "End Sheet" marker (GPT-6 family, Opus 5 in Cowork); merged titles and centred numbers (Grok 4.6). The cover, contents, check sheet and change log were asked for by the house standard, so they are no habit | Per model, against a stated standard, with task and attempt ids; the judge an agent validated against experts | the "rounded to" label as a sign a sheet's text shows, model-scoped; the typed summary as a candidate; the scaffold none |

## Dropped

| What | Why |
|---|---|
| SlideAudit (arXiv 2508.03630) | Design flaws in 2,400 slides, not who made them (the plan drops it) |
| uxdesign.cc, "How to de-slopify your designs" | About websites and apps a person vibe-codes, not decks; the host did not resolve from here and its Medium mirror refused the request, so it was not read in full |
| perceptis.ai, "How to Make AI Slides That Don't Look AI-Generated" (6 Nov 2026, all rights reserved) | One prompt run once in six tools, no count; what it ties to a tool is look (ChatGPT's cream and top bar, Gamma's lavender, Gemini's icon cards), and its text tells (descriptive titles, obvious bullets) are a checklist the Analyst Academy count contradicts |
| BetterPPT, "Why AI-Generated Presentations Have an 'AI Smell'" (19 Oct 2026) | A redesign service's advert; look only (equal weight, rounded cards, accent colour), and its accent-colour tell is commoner in real decks by the count |
| chatslide.ai, winningpresentations.com, mauriziolacava.com | Vendor or course pages: generic advice with nothing specific tied to AI beyond a Reddit quote ("three boxes with made-up percentages") |
| Reddit threads on r/powerpoint, r/ClaudeAI and others (the Analyst Academy page lists them) | Opinion, no method; Analyst Academy's count already weighs what they name |
| arXiv 2309.00095 (EuSpRIG 2023), ChatGPT and spreadsheet formulas | Whether formulas are right, not a habit a sheet shows |
| arXiv 2412.14062 (EuSpRIG 2024), trust in generated formulas | A framework, with no observations of model output |
| spreadapi.io, formulafoundry.io, howtogeek.com on AI and Excel | A vendor pitch for its own API (an invented `=FINANCECALC()` as an example), a how-to and an opinion piece; nothing measured |
| SpreadsheetBench 2 (arXiv 2606.29955) | Task accuracy and failure causes, not what the sheets hold |
| 2Slides, "12 common mistakes" and "AI slides that don't look AI-generated" (17 Apr 2026, all rights reserved), in de, fr, es, pt, it, ru, tr, vi and ar | The vendor's own translations of English posts, so no language's evidence; claims a sample of 300+ decks from five tools and a "Stanford HCI 2025" figure, with no method, data or citation that could be found |
| presentations.ai's pages in ar, tr, it, es and other languages | The vendor's translations of the page kept above |
| habr.com, StudyAI's "Нейросеть для презентаций 2026" (ru) | A corporate blog's ranking; its AI tells (topic titles «Преимущества», «Особенности», «Результаты», look-alike slides, an added fact) are opinion, and topic titles are commoner in real decks by the count |
| dtf.ru, "Презентация через нейросеть: 10 ИИ-сервисов" (ru) | A promotional ranking that says it is not independent testing; its Russian tells (anglicisms, odd government of cases) are prose signs the `ru` sources already hold |
| vc.ru, TOPSTUD on the dangers of generated decks (ru, Jan 2026) | SEO content: invented statistics and quotes with made-up examples |
| habr.com, Кэмп on decks from text (ru, 17 Nov 2025) | Marked as an advert; "10 tools tested" with nine described and no rubric |
| habr.com, Кампус's post on generic slide titles; sostav.ru, securitylab.ru, vc.ru (Tome), habr (Gamma tutorial) (ru) | Things to check, not habits tied to AI; affiliate pages; tutorials |
| t3n (de, 24 Sep 2026), wwwhatsnew (es, 28 Oct 2026), a Göttingen lecture PDF (de) | Prompt advice or workshop questions, no habit tied to AI |
| trabajarporelmundo.org (es, 6 Nov 2026) and findskill.ai (de, 9 Mar 2026) on AI and Excel formulas | The same locale habit as the two kept pages, as opinion with no worked example; "one formula in ten" wrong with no source |
| Blog du Modérateur on Excel's `=COPILOT()` function (fr, 21 Aug 2025) | How reliable a Microsoft function is, after Microsoft's own page; not a habit a sheet's text shows |
| borncity.com on Copilot cleaning a sheet (de, 10 Aug 2026) | A retelling of one How-To Geek test, of a behaviour, not of a sheet's text; the page says it was written with AI |
| GitHub: thevseprod/humanizer-ru, kilianvivien/insp-skills-ia, DigitalHumanitiesCraft's claim-check, NilsHellwig's guide, deck-building skills | A prose humaniser, a template spec, one look-only line, a seminar list and deck builders: none ties a deck or sheet habit to AI |
| PPTDetector, Copyleaks | Detectors, not sources of habits |
| nwiizo/3shake-marp-templates and yaenowa-yoshida/ailt-presentations (ja, no licence) | One team's and one person's writing rules for their own talks; what they tie to AI (three balanced bullets, まず・次に・最後に, dashes, "〜ではなく〜") the kept `ja` sources and `ja`'s prose signs already hold |
| note.com (吉村伸一, 30 Mar 2026; ワンホ, 2 Jul 2026; ふじくるり, 12 Jul 2026), zenn.dev (Kaz, 23 Feb 2026) (ja) | Promotional or mostly look (dark backgrounds, shadows, a rule under the title); the English heading labels in Claude's output one of them shows are in `lt-slide-skills` too; one is half paywalled |
| unite-365.co.jp on Copilot in Excel (ja, 6 Jan 2026); blog.kentarocku.com (ja, 2 Nov 2026) | Formula errors in a test (a boundary written as `>100000`, IF for IFS), not a habit a sheet's text shows; the second labels its outputs as expected, not seen |
| toutiao, 老骥, "AI 做 PPT 一眼AI味的 6 大特征" (zh, 19 Jul 2026); 二狗PPT's two posts (zh, Jul 2026) | Opinion that leads to the author's own skills, or a vendor's; forced "X步法" frameworks and broad label titles add nothing over the kept sources |
| alchaincyf/huashu-excel (zh, MIT) | Its measured run (a total 161% too high, with no error) is about a model analysing a Chinese sales sheet, not one making it; its "AI data report" defaults (a row of four KPI cards, an emoji before section titles) are for HTML reports |
| 2slides.com zh-TW, smzdm, keynote.org.cn, Daylily-Huang/Work-skills, tyxben/AI_novel, KY2026AI/proslide, volcengine, Ramsbaby/jarvis, shibayamalicht/apollo-patent-analysis (zh, zh-Hant) | A vendor citing an unsourced study; a page labelled as AI-written; prompt templates; no tie to AI; officialese the kept source says is not AI tone; one line; adverts; web design; a restatement of Anthropic's `pptx` skill |
| mii-lab.tw (zh-Hant, 3 Sep 2026); blog.104.com.tw (zh-Hant, 25 Jun 2025) | Look only and promotional; generic formula errors from a book excerpt |
| PhrenO0/CHAI-AI (ko, no licence, no stars) | A project's copy guide on a generated branch; it calls dashes the biggest AI signal in Korean decks and "A가 아니라 B" titles a template, from one reviewer's comments, which `agent-kit-briefing` and `ko`'s prose sources already hold |
| insightflo/edu-deck-skills, kangdacool/pptx-editing-skill (ko) | Translationese checks `ko`'s prose signs hold; one line |
| openads.co.kr (ko, 27 Oct 2026); brunch.co.kr (ko, 21 Apr 2026); emotionte.com (ko, 11 Jul 2026) | A firm's promotion with a generic contents order as its one specific; look-only anecdotes |
| clien.net forum (ko, 7 Jun 2025) | One formula error (cell references inside an array constant) |
| zhihu.com (two posts), wikidocs.net, afterworkai.club, Lifehacker Japan, IPSJ SSS2024033 | Not read: 403, DNS failure or 503 |

## Seeding

| Kind | Enough to seed from? | Why |
|---|---|---|
| deck, `en` | Yes, for a few signs | One count (Analyst Academy) and several opinions that meet on the label above the title, the takeaway box, groups of three by habit, leftover placeholders and invented numbers; each sign needs the count or two sources |
| deck, `any` | Perhaps two | A layout sign is `any` only when sources show it in two languages (`AGENTS.md`, Traps): the label above the title (`analyst-academy-not-ai-decks`, `plusai-2026-slides`; `lt-slide-skills`) and the takeaway bar that restates the slide (`analyst-academy-not-ai-decks`; `agent-kit-briefing`) |
| deck, `ja` | Yes, for a few | Three sources: the count in the title, the label prefix, uniform bullet rhythm |
| deck, `zh`, `zh-Hant`, `ko` | Weak at most | One source each, opinion; most of what they name is prose that those languages' signs hold already |
| deck, the European seed languages | No | No source of their own; the `any` deck signs carry them |
| sheet, `en` | Few, `weak` at most | Three papers, all English and all finance or modelling tasks; the habits they measure are mostly in formulas, which a sheet's text doesn't show. The "rounded to" label and invented sample data are what it shows |
| sheet, `fr` and `pt` | One candidate | English Excel's function names and commas in a French or Portuguese sheet, one page each with worked examples: two languages, but a habit English sheets can't show, so a sign for each language or an `any` sign whose check names the language's own functions |
| sheet, every other language | No | Recorded as having none, as Hindi was |

## Open

- The Analyst Academy count is one person's, not blind; a second count, or byhand's own (the first search's open
  question 6), would settle which deck signs are `usual` and which `weak`.
- The three sheet sources are about finance models built by agents in 2025 and 2026; none looks at a plain list or
  tracker a user asks for.
