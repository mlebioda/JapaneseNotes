# Practice Grammar — Gate 1 answer-leak fix — Tasks

- [x] Read `.cowork/skills/_practice-grammar-common.md` and locate the
      current Gate 1 block (starts `**Gate 1 — Prompt does not leak the
      answer — grammar point name must not appear anywhere...**`, ends
      `...never before.`, currently lines 286–295)
- [x] Replace that block with the rewritten two-item Gate 1 text from the
      plan (`Plans/practice-grammar-gate1-answer-leak-plan.md`, Step 2),
      preserving surrounding blank lines and leaving the Gate 2 block that
      follows untouched
- [x] Diff the file before/after to confirm the only change is the Gate 1
      block — Gates 2 and 3, the checklist lead-in, and every other section
      are byte-identical
- [x] Confirm no other file in `.cowork/skills/` (e.g.
      `lesson-grammar-practice.md`, `scheduled-grammar-practice.md`) needs
      changes — they load Gate 1 from this shared file, no direct edits
      required
- [x] Do not touch the stale root-level `practice-grammar.md` — out of scope
      for this plan
