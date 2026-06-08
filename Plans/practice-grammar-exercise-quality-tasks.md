# Tasks: Practice Grammar — Exercise Quality & Use-Case Coverage

**Date:** 2026-06-06
**Plan:** `Plans/practice-grammar-exercise-quality-plan.md`
**Target file:** `.cowork/skills/practice-grammar.md`
**Status:** in progress

---

## Task list

| # | Section | Change | Status |
|---|---------|--------|--------|
| 1 | **Workflow, step 6** | Change "one exercise per grammar point" → "one exercise per use case per grammar point" | [x] |
| 2 | **Parsing — Grammar topics** | Add use case extraction sub-step after building the `{grammar_header, body_text, source_section}` triple | [x] |
| 3 | **Exercise generation — header** | Replace the single-exercise-per-point rule at the top with per-use-case rule | [x] |
| 4 | **Exercise generation — anti-trivial** | Replace "Avoid trivial fill-the-blank" paragraph with three-gate non-trivial checklist (Gates 1–3) | [x] |
| 5 | **Interaction flow — Batch mode** | Update session header format and progress indicator total to use exercise count, not grammar-point count | [x] |
| 6 | **Session summary** | Update to show per-grammar-point roll-up with per-use-case scores; update header count label | [x] |
| 7 | **Persistence** | Add minimum-score rule for multi-exercise grammar points | [x] |

---

## Notes

- Tasks 3 and 4 are both within the Exercise generation section; they are listed separately to isolate the two distinct changes (per-use-case rule vs anti-trivial checklist).
- Do not add a new field to `grammar-state.json` — state stays at grammar-point granularity.
- Do not modify the SM-2 algorithm table, JSON schema, grading logic, furigana rule, vocabulary rule, or interactive mode.
- Gate 3's exception for explicit single-distinction tests (rendaku, sound changes) must be preserved.
