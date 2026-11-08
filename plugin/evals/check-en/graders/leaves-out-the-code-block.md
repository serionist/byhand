---
type: llm
---

PASS if the answer does not count the line inside the code block ("As an AI language model, I cannot run this") as a
sign of the user's writing, or says it left the code block out.
FAIL if the answer counts that line, or any-ai-self-reference, as a sign found in the user's text.
