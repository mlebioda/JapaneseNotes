---
name: update-grammar
description: >
  Full post-processing pipeline for grammar files under grammar-index/grammar/.
  Chains: preprocess-grammar → review-grammar → structure-grammar →
  register-confusability-grammar → see-also-grammar.
  Trigger: "update grammar <file>" or called from extract-grammar.
---

# Update Grammar Skill

## Trigger

- "update grammar `<slug>`" — filename without `.md`
- "update grammar grammar-index/grammar/`<slug>`.md" — full relative path
- (called automatically from extract-grammar step 11 — Offer chain — with a list of file paths)

---

## Workflow

Load `.cowork/skills/lesson-to-web/_conventions.md` before starting.

Load `.cowork/skills/lesson-to-web/preprocess-grammar.md` and pass it the file list.

Tell preprocess-grammar to run in **all** mode — meaning each skill in the chain will automatically continue to the next without prompting at handoffs, asking only for the user gates within each skill (correctness check, missing info, structure confirmation).

The five skills run in order: preprocess → review → structure → register-confusability → see-also.

| Skill | Steps | What it does |
|---|---|---|
| preprocess-grammar | 1–4 | Tag removal, Polish detection, furigana, typos — all silent |
| review-grammar | 5–6 | Correctness check, missing info — user gates |
| structure-grammar | 7 | Structure enforcement — user confirmation |
| register-confusability-grammar | 8–9 | Register research, often-confused-with backlinks — web search + cross-file writes |
| see-also-grammar | 10–11 | See also population, proofread: true |

To run a single step, invoke the corresponding skill directly instead.
