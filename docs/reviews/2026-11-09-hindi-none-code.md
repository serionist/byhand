---
subject: "Record Hindi as having no source to seed from (PR #59)"
base: main (4fc5a9c)
head: 97bb66e
date: 2026-11-09
round: 1
tier: standard (one fresh reviewer; findings checked against the sources by the main session)
verdict: clean
---

# Record Hindi as having no source to seed from: code review

A docs-only change: no `hi.toml`, the plan's progress log, and a follow-up in the research record. The reviewer read
both Hindi sources again (Wang et al. v3 from a text extraction, C.4, D.2 to D.4, E.4; SHAKTI v1 HTML, Tables 4 and 6,
3.2, 4.1, 5.1, 5.3) and checked every claim against them. No sign is backed and dropped; three claims in the record's
reasoning were wrong or loose. Minors only, fixed in this session: no second round.

| # | Severity | Where | Finding | Status |
|---|---|---|---|---|
| F1 | minor | the research follow-up, first row; the plan's hi row; the PR body | SHAKTI's length gap was put down to section 4.1's 1,000-character minimum for model texts, but five of the eight models' means in Table 4 fall below it (GPT 740, Sarvam 693), and 4.1 lists a length check on both sides with no number for people's. A later reader would distrust the record | fixed in 49bc62f: the row leads with the unmatched lengths (human texts of about one sentence) and says the stated minimum and the table disagree |
| F2 | minor | the same row; the PR's Tested by | Readability and sentence-length variance are in Table 6 and 5.3, not Table 4, and readability doesn't follow from length (human words per sentence sit inside the models' range) | fixed in 49bc62f: Table 6 and 5.3 cited, readability called mixed, as the authors say; only the variance put down to one-sentence texts |
| F3 | minor | the research follow-up, names-and-dates row | `any-generic-over-specific` holds fewer names and dates, not D.4's keeping strictly to the topic, which went without a reason | fixed in 49bc62f: its own row, left out as one model's news, and office writing keeps to its topic too |

## Refuted

- Wang's "shorter" misread: D.4 says the machine's news was more concise, with less in it; the "longer human texts"
  sentence before it is D.2's, Chinese.
- A missed Hindi cue of bold and English words: that line ends D.2. D.4's own English cue is in the record.
- The idiom, colloquial and Urdu cues, and C.4's "concise and formal" prompt: as the paper says.
- The model: C.4 says GPT-4o, the dataset table says GPT-4; "one model" holds either way.
- The English-words cue backed and dropped: one model's news alone, which the Arabic seed also left out, and the
  record's order asked for two sources.
- A weak sign with no pattern for the idiom or Urdu cue: one model's news, against office Hindi's Sanskritised register.
- Missing `any` forms: neither source names a Hindi phrase.
- The docs: Step 3 merged (#54), pt #55 and ar #58 right; AGENTS.md, CONTRIBUTING.md, CHANGELOG.md and README.md need no
  change; `Closes #49` matches the plan's Goal; no em dashes, banned words or copied text beyond short facts cited.

## Improvements

| Improvement | Answer |
|---|---|
| Push the local PR body, which names #59, to GitHub | taken |
| The progress-log row's "other cues clash" was loose: names and dates are held by an `any` sign | taken in 49bc62f |

## Not covered

catalogue-contract, privacy-and-sources, plugin-contract, tests, compatibility, harness-integrity and implementation:
nothing in the scope for them. The reviewer ran no gate (coverage writes files); the gate full and CI passed on
97bb66e. The SHAKTI page was read through its first 100 KB, which holds every table and section cited.
