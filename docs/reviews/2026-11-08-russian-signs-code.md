---
subject: "Bootstrap step 4, the Russian signs (PR #22)"
base: main (3263b22)
head: b9589f6
date: 2026-11-08
round: 1
tier: standard (a fresh reviewer per round on Claude Opus 5.5, every lens; the last fixes verified by their mutants)
verdict: needs-fixes
---

# Review: Bootstrap step 4, the Russian signs (PR #22)

Round 1 read the 19 Russian signs and the five narrowed Russian branches of `any` signs at `b9589f6`, with the
reviewer's own 51 plain Russian texts (mail на вы and на ты, Telegram, contracts, notices, reports, minutes) and
chatbot lines, every pattern under Python and Claude Code's Grep, and copycheck at 6, 5 and 4 words over wikipedia-ru,
humanizer-ru and slop-gate. No licence blocker: no copied or translated sentence; the pins read back as the PR says.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F1 | major | ru-title-case-headings | Usual, and fired on headings in capitals, standard in contracts and notices (`## ПРАВА И ОБЯЗАННОСТИ СТОРОН`) | fixed: each word a capital, then lower case; contract headings in `OFFICE` |
| F2 | major | any-assistant-preamble, Russian branch | Fired strong on a person returning a corrected file: «Конечно! Вот исправленный вариант договора:» | fixed: the maintainer's call, narrowed as Chinese was; fires only when the user's text is named (вашего письма, твоего поста, ваш отредактированный текст) or on «более … версия»; four of the person's lines in `OFFICE` |
| F3 | major | the weak cluster on reports | Plain reports reached 3 different phrases: стоит отметить, эксперты отмечают, по мнению экспертов, сталкивается с серьёзными вызовами | fixed: the maintainer's call, those terms cut and bare «важно отметить» with them; the source frames stay (рядом вызовов, несмотря на эти вызовы, будущее выглядит, продолжает процветать); the three paragraphs, written anew, and REPORT_PRICES with one phrase more, each at 1 hit |
| F4 | minor | ru-title-case-headings | Missed «Ранняя Жизнь и Образование»; fired on a bold signature «**Отдел Продаж И Маркетинга**» and on «## Поздравляем С Новым Годом» | fixed in part: bold lines aren't read and С is no function word, each line in `OFFICE`; a small и between capitalised words is left to the model's read, as «## Анна Иванова и Пётр Смирнов» looks the same, in `OFFICE` |
| F5 | minor | ru-calques | «адресовать этот вопрос» is standard Russian; «доставке ценностей» is cash collection | fixed: вопрос dropped; доставлять only as a verb with singular ценность; both lines held plain |
| F6 | minor | term forms | Missed символизировало, столкнулась с … вызовами, выглядит многообещающе, по мнению ряда экспертов; matched the plain «не может похвастаться» | fixed: each form in `FORMS`; «не может похвастаться» held plain |
| F7 | minor | ru-tacked-on-participles | укрепляя and свидетельствуя are in neither cited source | fixed: dropped |
| F8 | minor | any-unfilled-placeholder | Fired on Markdown link text, «[вашем личном кабинете](…)», as English «[your …](…)» does on main | fixed: a bracket with ( after it passes, in every branch; link lines in Russian, English and Japanese; the maintainer's call, a person's template slot ([имя], [Your Name]) fires on purpose, and the bare имя is back |
| F9 | minor | any-source-gap-disclaimer, any-knowledge-cutoff | The narrowed branches still reach a person, rarely: «сведения скудны в предоставленных источниках», «…обновления моей базы данных клиентов» | left: the maintainer's call; named in the PR's list for a native speaker |
| F10 | minor | AGENTS.md, the plan | "Where the work stands" and the Step 4 row deferred | refuted: the maintainer's session adds both at merge, as other languages land beside this one |

The maintainer also had `ru-paragraph-stack`'s examples rewritten: they mirrored humanizer-ru 34's before and after.
They now have their own subject, order and repair. `ru-office-register` stays for the model's read only, as the PR had it.

## Checks

- 18 mutants of round 1's changes, one at a time, each killed: words with capitals inside, bold lines read, С a function
  word, case-insensitive title case; the preamble back to any reworked text; link text read in the Russian and
  Japanese branches, the bare имя narrowed again; вопрос back, any доставка, «не может» back; стоит отметить, bare
  важно отметить, эксперты отмечают, по мнению экспертов and серьёзными вызовами back; the cutoff and closing-offer
  branches back.
- `uv run tools/copycheck.py` over the 11 Russian downloads: 0 hits at 6; at 5 one, `en-em-dash`, outside this change.
- `uv run byhand validate`, `uv run byhand render`, `uv run tools/gate.py full --base origin/main`: all pass.

## Round 2

**Where:** `b9589f6..f2e7744`, a fresh reviewer, with new plain report paragraphs and chatbot lines, every changed
pattern under Python and Grep. **Verdict:** needs-fixes, on one major. F1 to F8 held.

| # | Sev | Where | Finding | Status |
|---|---|---|---|---|
| F11 | major | ru-didactic-phrases, ru-vague-authority | Plain report paragraphs still reached 3 different weak phrases: «нельзя не отметить», «ряд источников (экспертов)» and a participle (способствуя, отражая) or «поворотный момент» | fixed: under the maintainer's round-1 call, «нельзя не …» and «ряд …» cut; three paragraphs of that shape, written anew, join `REPORTS` at 1 or 2 hits; both lines held plain |
| F12 | minor | any-unfilled-placeholder, Japanese branch | The link guard took a full-width （ too, so «【ここに会社名を入力】（正式名称）» stopped firing | fixed: only an ASCII ( after the bracket passes, as Markdown links use; the line in the Japanese `MACHINE` |
| F13 | minor | any-assistant-preamble, Russian branch | «более … версия» fired on a person's «Конечно! Вот более свежая версия прайса:» | fixed: the maintainer's call, более only with a word of register (официальн, формальн, вежлив, дружелюбн, лаконичн, кратк, профессиональн and the like); two recency lines in `OFFICE` |

Four mutants, one at a time, each killed: «нельзя не» back, «ряд …» back, the full-width bracket read as a link, any
word after более. copycheck over the Russian downloads: 0 hits at 6; at 5 the same `en-em-dash` hit, outside this change.
`validate`, `render` and `gate.py full --base origin/main` pass.

## Closed

Round 2's fixes are each held by a test that fails without them. The maintainer verifies them in the main session; no
third round unless a major is left.
