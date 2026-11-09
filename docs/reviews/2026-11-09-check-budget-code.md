---
subject: "Key the shared signs' checks by language in the catalogue's schema, and give the patterns only to scan (PR #86)"
base: main (1d270df)
head: c5849a4
date: 2026-11-09
round: 1
tier: split (two fresh reviewers: the package and plugin, the catalogue and its forms; findings checked by the main session)
verdict: clean (round 6, 9ec8535)
---

# Forms by language and patterns only in scan: code review

67 files, about 1,300 changed lines, most of them rendered sign files, so the lenses were split. The first reviewer
took plan-and-intent, implementation, plugin-contract, tests, docs-freshness, simplicity, compatibility and
harness-integrity on the package, the skill, the agent and the docs; it ran `byhand render --check`, `validate`, the
render, catalogue, copycheck and English office tests, and a probe of the rendered sizes. The second took
catalogue-contract, privacy-and-sources and tests on `any.toml`, `fi.toml` and the office tests; it split the old and
new `any.toml` into their top-level branches with a script, read the fetched sources at their pinned commits, and
probed each new form with `as_grep`. One major, F5: fixed, so a second round reads the fixes.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | commit 9416444; the plan's Out of scope | The deferred it, vi, tr, id and fi forms came in this PR, which the plan left to later ones, with no note of the departure | fixed: asked for when the work was handed over; the PR's Plan section and the plan's new Built section say so (c058825) |
| F2 | minor | `docs/USAGE.md`, What a skill reads | "only languages that have signs get a folder": `id/` now holds a `scan.md` alone | fixed: a language with forms alone has a `scan.md` and no `check.md` (c058825) |
| F3 | minor | `any.toml`, `any-assistant-preamble`, `check.tr` | Any three words before hâli: "Elbette, işte e-postanızın orijinal hali:", "…ilk hali:" fired, though every other language needs a reworked or register word | fixed: a register word after daha, or düzeltilmiş, düzenlenmiş, kısaltılmış, yeniden yazılmış; "orijinal hali", "ilk hali" and "daha önceki hali" in `office_tr.toml`'s replies (c058825) |
| F4 | minor | `any.toml`, `any-assistant-closing-offer`, `check.vi`; `tests/test_office_vi.py` | "Nếu bạn cần, tôi có thể bổ sung thêm số liệu quý 3." and "…chỉnh sửa lại hợp đồng…" fired, offers about data or a contract; the person's line sat mid-line, where `^\W*` passed it whatever the verb | fixed: the verb, then the text (đoạn, bài viết, nội dung, văn bản); bổ sung dropped; the three person's lines at a line's start in `REPORTS` (c058825) |
| F5 | major | `any.toml`, `any-chatgpt-citation-markup`, `check.fi` | `[^\W\d_]{2}\+[1-9]` fired on a person's sign-up list, a score or code ("Ilmoittautuneet: Matti+1, Liisa, Pekka+2", "HIFK+3", "count+1"), a strong sign every family reads unless the user names one | fixed: the chip follows a sentence's full stop, as every chip on wikipedia-fi does (`\.\s(?:[^\W\d_]+\s){0,2}[^\W\d_]{2,}\+[1-9](?:\D|$)`); the four lines in `office_fi.toml`'s chat (c058825) |
| F6 | minor | `any.toml`, `any-flattering-agreement`, `check.tr` | humanizer-tr 23's own example, "Harika soru!", was missed: the form needed "bir" | fixed: `har[iİ]ka (?:b[iİ]r )?soru!`, with its machine line (c058825) |

## Refuted

- The `ran` contract: no hit answers with `ran` alone; a rejected id is never in `ran`; a missing `scan.md` is skipped
  and `any/scan.md` always exists; `zh-Hant` reads `any`, `zh` and `zh-Hant` (`test_a_chinese_form_reaches_a_traditional_chinese_scan`);
  no `ran` line counts as no scan.
- `id` and check's step 4, "use `any` alone": still right, as `any/check.md` holds every shared sign and step 5 names
  `<language>/scan.md` whether or not a `check.md` exists.
- `learn`'s screen: it reads check's `SKILL.md`, whose step 5 now hands over the scan paths.
- The budgets: Japanese's check 15,412 + 512 under 16 KB, English's scan 8,241 + 512 under 9 KB; `budget_problems`
  names a scan over budget, tested.
- `Sign.forms` with `hash=False`: equal signs still hash alike, and nothing mutates the forms.
- The global-flag refusal: `(?:(?s)…)` raises on Python 3.11 and later; tested.
- Lost or moved branches: every old branch is under its language's key; the leftovers every language meets under
  `any`; the eight German, Russian and Chinese lines moved from `test_office.py` to their files.
- The comments: each language's note sits above its form, and none cites the check budget.
- The added forms' citations, the Turkish i classes, the alternation order, the Italian and Indonesian person's lines,
  and the forms left out: as claimed.
- Privacy: the test text is invented, and only short tokens are quoted from the sources.

## Improvements

| Improvement | Answer |
|---|---|
| `_file` takes the header lines as a list, dropping `_scan_rules`' unused argument | taken |
| Fold `test_a_scan_line_prints_its_form_in_nfc` into `test_every_pattern_prints_as_written_in_nfc`, which compares with the TOML in NFC | taken |
| scan: an id with one form rejected stays out of `ran`, even when another ran | taken |
| `tr.toml` records why the Turkish self-reference, cut-off and closing offer are left out, as `fi.toml` does | taken |
| The Arabic preamble note's "by the same rule" now comes before English's | taken: "by English's rule, below" |
| A line-start "Başka bir şey ister misin?" in a document | left: people write it, and the English form needs "you'd like me to" |

## Not covered

The by-hand part of the plugin-contract and tests lenses, which the main session ran (the PR's Tested by); `gate.py
full` on the reviewers' side (the main session ran it, and CI passed on c5849a4).

## Round 2

A fresh reviewer, on c058825, the fixes since c5849a4. It probed the old and new forms side by side with `as_grep`,
ran `byhand validate`, `render --check`, the render, catalogue and fi, tr and vi office tests, and gate quick. F1 to
F6 hold: each new person's line in `office_fi.toml`, `office_tr.toml` and `test_office_vi.py` fires under c5849a4's
form and passes now, and F6's machine line is found. The `_file` change, the folded test, scan's clause and the plan's
Built section, which passes the gate's plan rules, are sound. Verdict: needs-fixes, two majors.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F7 | major | `any.toml`, `any-chatgpt-citation-markup`, `check.fi` | `\.\s` took a list number's, a date's or a time's full stop: "1. Matti+1", "la 12.10. Matti+1", "klo 9. Tiimi+2" fired, F5's sign-up list numbered | fixed: a word or a year before the full stop; the three lines in `office_fi.toml`'s chat; "esim. Matti+1" still fires, rare, named in the note (522201b) |
| F8 | major | `any.toml`, `any-assistant-preamble`, `check.tr` | F3's fix cut model lines the old form found: "daha profesyonel bir hali", "gözden geçirilmiş", "iyileştirilmiş", "yeniden düzenlenmiş" | fixed: `(?:b[iİ]r )?` after the register word, and the three participles, each with its machine line (522201b) |
| F9 | minor | `any.toml`, `any-assistant-closing-offer`, `check.vi` | "chỉnh sửa nội dung hợp đồng", "viết lại văn bản đề nghị" still fired: a noun after the text word | fixed: the text is the whole object, ending there or at này, trên or cho; đoạn văn added; both lines in `REPORTS` (522201b) |

Refuted: the Turkish i classes on capitals; "Tulossa: minä+1. Kiitos kutsusta! Mä+1" (no + after ". Kiitos"); USAGE
against the rendered tree; `_file`'s default.

The fixes were checked in the main session: the suite (4,020), `byhand validate` and `render`, gate quick, and Claude
Code's Grep (ripgrep) on each changed form's machine and person's lines, which agrees with Python on every line.

## Round 3

A fresh reviewer, on 522201b, the fixes since c058825. F7 to F9 hold: `office_fi.toml`'s three numbered, dated and
timed lines fire under c058825's form and pass now; the four Turkish machine lines are found, and the person's lines
pass; the two Vietnamese contract lines pass. The Turkish i classes hold. Verdict: needs-fixes, one major.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F10 | major | `any.toml`, `any-chatgpt-citation-markup`, `check.fi` | A name+1 opening the next sentence still fired: "Kiitos kutsusta. Matti+1 tulee.", "Mökki varattu. Matti+1" | fixed: only two or more chips glued in a row (`[^\W\d_]{2}\+[1-9][^\W\d_]{2}`), as four of wikipedia-fi's six are; a lone chip is left out, named in the note; both lines in `office_fi.toml`'s chat, and the single-chip machine line now a chain (3e9cc57) |
| F11 | minor | `any.toml`, `any-assistant-closing-offer`, `check.vi` | F9's ends cut model offers c058825 found: "rút gọn văn bản xuống còn 200 từ", "mở rộng bài viết thành…", "…theo phong cách…", "…với giọng điệu…", "…để phù hợp hơn…", "…hoặc bổ sung…" | fixed: the ends take thành, theo, với, để, xuống and hoặc, each with its machine line (3e9cc57) |
| F12 | minor | `any.toml`, `check.fi` | F7's guard missed a chip after ")." or "%." | fixed by F10: the chain needs no full stop; "Väkiluku kasvoi 3 %. Tilastokeskus+1", a lone chip, passes as the note says |

Refuted: "gözden geçirilmiş hali" as a person's reply (the class "düzeltilmiş hali" is, by design); Turkish modifier
chains, a recall gap there before; "Juhlat 12.10.2024. Matti+1", moot with F10; "đoạn mã này", which passes.

The fixes were checked in the main session: the suite (4,032), `validate`, `render`, gate quick, and Claude Code's Grep
on the chain and the Vietnamese ends, which agrees with Python.

## Round 4

A fresh reviewer, on 3e9cc57, the fixes since 522201b. F10 and F11 hold: "Kiitos kutsusta. Matti+1 tulee." and
"Mökki varattu. Matti+1" fire under 522201b's form and pass now; the six Vietnamese machine lines miss under it and fire
now. F12 holds by design: the chain needs no full stop. Verdict: needs-fixes, one major.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F13 | major | `any.toml`, `any-chatgpt-citation-markup`, `check.fi` | The chain fired on unit sums written without spaces: "10km+5km", "20min+5min", "3dl+1dl", "80kg+2kg", "1kk+1kk", "6kpl+2kpl", "VPN+2FA:n", "XL+2XL" | fixed: a name standing on its own and a next one of three letters or more (`(?:^\|\W)[^\W\d_]{2,}\+[1-9][^\W\d_]{3}`); the eight lines in `office_fi.toml`'s chat; a two-letter next name ("+5HS") is no longer found, a minor gap |
| F14 | minor | `any.toml`, `any-assistant-closing-offer`, `check.vi` | thành and theo begin compounds that name another document: "văn bản thành lập công ty", "văn bản theo dõi công nợ" fired | fixed: thành only before một or bản, theo only before giọng or phong cách; both lines in `REPORTS` |

Refuted: "chỉnh sửa nội dung theo hợp đồng" and "viết lại văn bản để gửi Sở", the text reworked, the class English's form
accepts; glued chemistry, sign-up lists and scores, which people don't write; two-digit unit sums, versions and phone
numbers, which pass.

The fixes were checked in the main session: the suite (4,052), `validate`, `render`, gate quick, and Claude Code's Grep
on both forms, which agrees with Python.

## Round 5

A fresh reviewer, on b368ed7, the fixes since 3e9cc57. F13 and F14 hold: the eight unit sums in `office_fi.toml`'s
chat fire under 3e9cc57's form and pass now, and so do the two Vietnamese compounds in `REPORTS`. Verdict:
needs-fixes, one major.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F15 | major | `any.toml`, `any-chatgpt-citation-markup`, `check.fi` | Finnish home-sale listings glue their rooms ("Myydään omakotitalo 6h+k+khh+2kph+s"), and hardware specs their ports ("VGA+2xHDMI", "HDMI+2xUSB"): each fired | fixed: the form, its citation and its machine lines go. Five rounds found a person's line in every form tried, so no regex keeps the chip a machine's alone; `fi.toml`'s header says so, and the person's lines stay in `office_fi.toml` (9ec8535) |
| F16 | minor | `any.toml`, `any-assistant-closing-offer`, `check.vi` | F14's narrowing cut rework offers: "thành tiếng Anh", "thành các ý chính", "theo hướng trang trọng hơn", "theo văn phong…" | fixed: thành before bản, các, dạng, một or tiếng, theo before cách, giọng, hướng, phong cách, văn phong or yêu cầu, with three machine lines (9ec8535) |

Refuted: glued sports times, scores, orders and years (Kärpät+2Ilves, Python+3vuotta), which people space; Ctrl+Alt+2,
Alt+F4, GMT+3h, Wifi+4G, which passed; "thành bản cứng" and "thành bản trình chiếu", the text reworked, as the form
means.

## Round 6

A fresh reviewer, on 9ec8535, the fixes since b368ed7. F15 holds: the Finnish form, its comment, its citation and its
machine lines are gone, `fi/scan.md` no longer holds it, CHANGELOG and `fi.toml`'s header say what is true, and a grep
of the repo finds no other claim but the dated research record of #75, which lists the chips as deferred. F16 holds:
the three new machine lines are found; of 22 probe lines, those found are each an offer to rework a text, the class
English's form accepts, and "văn bản thành lập công ty", "theo dõi công nợ", "thành phố" pass. `validate`, `render
--check` and the suite (4,057) pass. No new finding. Verdict: clean.
