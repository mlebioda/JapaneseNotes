# lesson-to-web Refactor — Task Checklist

Slug: `lesson-to-web-refactor`
Plan: `Plans/lesson-to-web-refactor-plan.md`
Implementer: skill-implementer

Tasks are ordered: shared files first, then skill modifications. Do not modify any skill file before both shared files exist.

---

## Phase 1 — Create shared files

- [ ] **Task 1** — Create `.cowork/skills/lesson-to-web/_conventions.md`
  - Frontmatter: `name: _conventions`, `description: Shared output contract for all lesson-to-web skills. Load upfront.`
  - Sections: Canonical furigana format, File locations and naming, Frontmatter conventions, File structure rules (grammar point file), proofread: true guard (full behavioral text), Never touch rules (full list)
  - See plan "New Shared Files — _conventions.md" for exact content

- [ ] **Task 2** — Create `.cowork/skills/lesson-to-web/_patterns.md`
  - Frontmatter: `name: _patterns`, `description: Input recognition registry for unexpected source formats. Load lazily, only when encountering unrecognised input.`
  - Sections: Lazy-load rule, one seed entry for the trailing furigana pattern with example, decision, and apply instruction
  - See plan "New Shared Files — _patterns.md" for exact content

---

## Phase 2 — Modify skill files

### preprocess-grammar.md

- [ ] **Task 3** — Add `## Shared files` section at the top of the workflow (before Step 1). Content: load `_conventions.md` upfront; load `_patterns.md` lazily when Step 3 encounters an unrecognised input format.
- [ ] **Task 4** — Replace the proofread guard prose block (the full paragraph and code block before Step 1) with a one-line reference: "Check the proofread: true guard (see _conventions.md) before processing each file."
- [ ] **Task 5** — Remove the `## Never touch` section entirely.
- [ ] **Task 6** — In Step 3, remove the Input/Output example block and the trailing-format description that documents what counts as a known pattern — this moves to `_patterns.md`. Keep the algorithm steps 1–9 and the mismatch warning intact.

### review-grammar.md

- [ ] **Task 7** — Add `## Shared files` section at the top of the workflow. Content: load `_conventions.md` upfront.
- [ ] **Task 8** — Add one-line proofread guard reference before Step 5.
- [ ] **Task 9** — Remove the `## Never touch` section entirely.

### structure-grammar.md

- [ ] **Task 10** — Add `## Shared files` section at the top of the workflow. Content: load `_conventions.md` upfront.
- [ ] **Task 11** — Add one-line proofread guard reference before Step 7.
- [ ] **Task 12** — Remove the `## Never touch` section entirely.
- [ ] **Task 13** — Fix Bug 1: in the handoff summary, change the `Run see-also-grammar` prompt from `(yes / no)` to `(yes / no / all)` and add the `all` bullet matching the pattern in preprocess-grammar and review-grammar handoffs.

### see-also-grammar.md

- [ ] **Task 14** — Add `## Shared files` section at the top of the workflow. Content: load `_conventions.md` upfront.
- [x] **Task 15** — Remove the `## Never touch` section entirely.
- [x] **Task 16** — Fix Bug 2: in Step 8, Algorithm for grammar point files, bullet 1, change the scan path from `grammar-index/` non-recursively to `grammar-index/grammar/`. Update the surrounding prose to match (remove "do not descend into `grammar/`"; say "Scan all files in `grammar-index/grammar/`").

### extract-grammar.md

- [ ] **Task 17** — Add `## Shared files` section at the top of the workflow. Content: load `_conventions.md` upfront.
- [ ] **Task 18** — Remove the `## Never touch` section entirely.
- [x] **Task 19** — Remove the `## File placement` section (file locations move to `_conventions.md`).

### update-grammar.md

- [ ] **Task 20** — Add a one-line load instruction at the top of the workflow: "Load `.cowork/skills/lesson-to-web/_conventions.md` before starting."

---

## Constraints

- Do not touch `extract-vocabulary.md` or `.cowork/instructions.md` at any point.
- Do not implement any logic changes beyond what is listed above.
- The two bug fixes (Tasks 13 and 16) are the only behavioral changes in this refactor; all other tasks are structural moves.
- After each file is modified, call scribe in capture mode.
