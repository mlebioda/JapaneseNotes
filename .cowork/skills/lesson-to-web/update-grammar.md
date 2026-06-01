---
name: update-grammar
description: >
  Full post-processing pipeline for grammar files under grammar-index/grammar/.
  Chains: preprocess-grammar → review-grammar → structure-grammar → see-also-grammar.
  Trigger: "update grammar <file>" or called from extract-grammar.
---

# Update Grammar Skill

## Trigger

- "update grammar `<slug>`" — filename without `.md`
- "update grammar grammar-index/grammar/`<slug>`.md" — full relative path
- (called automatically from extract-grammar step 10 with a list of file paths)

---

## Workflow

Load `.cowork/skills/lesson-to-web/_conventions.md` before starting.

Load `.cowork/skills/lesson-to-web/preprocess-grammar.md` and pass it the file list.

Tell preprocess-grammar to run in **all** mode — meaning each skill in the chain will automatically continue to the next without prompting at handoffs, asking only for the user gates within each skill (correctness check, missing info, structure confirmation).

The four skills run in order:

| Skill | Steps | What it does |
|---|---|---|
| preprocess-grammar | 1–4 | Tag removal, Polish detection, furigana, typos — all silent |
| review-grammar | 5–6 | Correctness check, missing info — user gates |
| structure-grammar | 7 | Structure enforcement — user confirmation |
| see-also-grammar | 8–9 | See also population, proofread: true |

To run a single step, invoke the corresponding skill directly instead.
