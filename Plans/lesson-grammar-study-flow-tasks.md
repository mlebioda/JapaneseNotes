# Lesson Grammar Practice — Study-Mode-First Flow — Tasks

- [x] Re-read `.cowork/skills/practice-grammar/lesson-grammar-practice.md` in full immediately before editing.
- [x] Rewrite `## Workflow` steps 4–7 in `lesson-grammar-practice.md`:
  - [x] Step 4 — print numbered topic list from step 3, confirm/cancel prompt, cancel = no writes.
  - [x] Step 5 — enter `practice-grammar-study-mode.md` directly at its Step 2 for every topic in lesson order; document that its Step 1 is bypassed entirely; pass `batch_topics`, `user_answers: {}`, `vocab_pool`; load `.cowork/progress/grammar-state.json` weak_points inline before entering (create-as-empty if missing); if the user stops/ends mid-loop, end the session immediately with nothing written.
  - [x] Step 6 — document that control returns here when Study Mode's last-topic "Continue" would otherwise proceed to its Step 3 (never entered for this trigger); print topic list again; collect bare-number self-eval scores 1–4 in order (same reply convention as today's exercise self-scoring); weak_points always `[]`; invalid/out-of-range reply → re-prompt once → still invalid → cancel without writing.
  - [x] Step 7 — build `session_scores` (`{min_score, weak_points: [], grammar_header, lesson_file}` per point, reusing the existing extracted_file_path substitution rule) and call `practice-grammar-srs.md` directly with `scope="lesson"`.
  - [x] Remove references to `num_batches`, Batch-loop mechanics, Exercise generation, Interaction flow, Grading from this file's Workflow section.
- [x] Rewrite `## Session header and footer` section — replace exercise-count formats with topic-list-confirm format, self-eval-scores prompt format, and session-complete footer (topic count only, no exercise count); state the footer fully replaces the old Solid/Needs-practice breakdown for this trigger.
- [x] Update `## Study Mode` section — note direct entry at Study Mode's Step 2, bypassing its Step 1, never reaching its Step 3; point to Workflow step 5 for the invocation contract.
- [x] Update `## Persistence` section — note persistence is invoked from the new Workflow step 7 (after Study Mode + self-eval), not before Study Mode.
- [x] Make the two one-line corrections in `practice-grammar-study-mode.md` (`### Trigger`: name the lesson-flow second entry path; `## Context required`: note lesson-grammar-practice.md may invoke Step 2 directly) — confirm no other line in that file changes; confirm `_practice-grammar-common.md` and `scheduled-grammar-practice.md` remain untouched.
- [x] Confirm no edits needed to `.claude/commands/lesson-grammar-practice.md` or `.claude/commands/scheduled-grammar-practice.md` (thin pointer stubs, already verified).
- [x] Re-read `scheduled-grammar-practice.md` after implementation to verify zero behavioral diff from this plan.
