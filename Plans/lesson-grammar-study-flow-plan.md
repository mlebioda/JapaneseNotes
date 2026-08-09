# Lesson Grammar Practice — Study-Mode-First Flow

## Goal
Simplify `lesson-grammar-practice.md` so a lesson-triggered session ("practice
UN5GL14") becomes: confirm the topic list → walk every topic through Study
Mode's existing explanation loop → re-show the topic list and collect a
per-topic self-eval score → persist. This removes the batch/exercise-
generation/grading machinery from this trigger entirely, while leaving
`scheduled-grammar-practice.md` (TODAY/OVERDUE sessions) completely
untouched — it keeps its existing batch-split, exercise-generation, and
grading flow exactly as it works today.

## Approach
Only `.cowork/skills/practice-grammar/lesson-grammar-practice.md` changes.
Its steps 1–3 (resolve file, load slice, parse grammar topics + vocab pool)
stay exactly as today, calling the same shared routines in
`_practice-grammar-common.md`. Steps 4–7 are rewritten to orchestrate a
direct call into `practice-grammar-study-mode.md`'s existing per-topic loop
(Step 2: explanation → `Practice/Next topic/Questions`) — entered directly,
bypassing that file's own Step 1 (topic-selection prompt) and never
proceeding to that file's own Step 3 (batch-routing) — followed by a
post-study self-eval step and persistence, both owned by
`lesson-grammar-practice.md` itself.

This is achieved purely through `lesson-grammar-practice.md`'s own
instructions to the executor (Claude at runtime): it documents which
sub-section of `practice-grammar-study-mode.md` to enter, which sub-sections
to skip, and where control returns — without adding any parameter or branch
to either file's actual mechanics, aside from two one-line factual
corrections in `practice-grammar-study-mode.md` (step 6 below), needed
because the new second entry path makes its existing Trigger/Context-required
text false. Both of those files were re-verified against their actual
current text to confirm they are generic enough to support this: Study
Mode's Step 2 loop only assumes "a list of selected topics processed in
sequence" (it doesn't hardcode that the list came from its own Step 1), and
`practice-grammar-srs.md`'s Persistence directive is already caller-agnostic
(takes `session_scores`/`scope`, no assumption about when in a session it's
invoked). `scheduled-grammar-practice.md` and `_practice-grammar-common.md`
are not touched by this plan at all.

## Steps

1. **Read current state** — `.cowork/skills/practice-grammar/lesson-grammar-practice.md`
   (steps 1–3, Workflow section, Session header and footer section, Study
   Mode section, Persistence section) — this plan's design already reflects
   a full read of this file plus `practice-grammar-study-mode.md` and
   `_practice-grammar-common.md`, so no new exploration is needed before
   editing; re-read immediately before editing per the Edit tool's own
   requirement.

2. **Rewrite the `## Workflow` section** in
   `.cowork/skills/practice-grammar/lesson-grammar-practice.md`. Keep steps
   1–3 verbatim (resolve lesson file; load slice via the common file's
   **Loading a lesson file slice** routine; parse grammar topics + vocab pool
   via the common file's **Parsing** routines, including use-case extraction
   and extracted-file linkage as today). Replace today's steps 4–7 with:

   - **Step 4 — Confirm topic list.** Print the full numbered list of
     grammar headers discovered in step 3 (no subset selection — the whole
     list). Ask the user to confirm before proceeding. On cancel, end the
     session with no writes (no state file changes, no `.ics` file).
   - **Step 5 — Study Mode, every topic, in order.** On confirmation, load
     `.cowork/skills/practice-grammar/practice-grammar-study-mode.md` and
     enter directly at its **Step 2** (`2a` explanation → `2b` choice prompt
     → `2c` branch, including the optional `2d` Practice sub-loop exactly as
     it works today) — for every topic from step 3, in lesson order, treated
     as already "selected." Document explicitly: that file's own **Step 1**
     (topic-selection prompt) is never shown and never executed for this
     trigger — this skill supplies the full topic list directly instead.
     Pass the same context Study Mode already expects: `batch_topics` (the
     step-3 topic list), `user_answers: {}` (always empty for this trigger —
     Study Mode's existing "answer retrieval fallback" in `2a` already
     handles an empty/missing answer with no change needed there),
     `vocab_pool` (the step-3 vocab pool). Before entering Study Mode, load
     `.cowork/progress/grammar-state.json` (create-as-empty if missing) to
     pick up prior `weak_points` per grammar point — this load was
     previously done by `_practice-grammar-common.md`'s Batch-loop
     mechanics, which this trigger no longer invokes at all, so
     `lesson-grammar-practice.md` performs it directly as part of this step.
     If the user stops/ends mid-loop, end the session immediately — nothing
     is written, since no self-eval scores exist yet.
   - **Step 6 — Return control after the last topic; collect self-eval.**
     Document explicitly: when Step 2's loop reaches "Continue" on the last
     topic (which `practice-grammar-study-mode.md`'s own `2c` text says would
     "proceed to Step 3"), control returns here instead — that file's own
     **Step 3** (batch/"Next batch/Finish" routing) is never entered for this
     trigger. Once control returns: print the topic list again (same
     numbered format as step 4). Ask for a self-eval score per topic, 1–4
     scale (1=fail, 2=hard, 3=good, 4=easy — same scale/meaning as today's
     exercise self-scoring), reply as bare numbers in order (e.g. `3 4 2`),
     same batch-reply convention as today's exercise self-scoring. No
     weak_points collected in this step — always `[]` for this trigger's
     entries (explicit decision: bare score only, no free-text reason
     capture). Invalid or out-of-range reply → re-prompt once → if still
     invalid, cancel without writing.
   - **Step 7 — Persist.** Build `session_scores`: one entry per grammar
     point → `{min_score: <step-6 score>, weak_points: [], grammar_header,
     lesson_file}`, using the same `extracted_file_path` substitution rule
     already documented in `_practice-grammar-common.md`'s Persistence
     section ("Per-point `lesson_file` source") — unchanged, just consumed
     from this trigger's own step-6 output instead of exercise-grading
     output. Call `.cowork/skills/practice-grammar/practice-grammar-srs.md`
     directly (same call already made today by this file, just now placed
     after step 6 instead of before Study Mode) with `scope="lesson"`. Same
     SM-2 write, same direct `next_review` computation, same `.ics` export
     via `ics-export.py` — no change to that file's own mechanics.

   Remove all references in this Workflow section to `num_batches`,
   Batch-loop mechanics, Exercise generation, Interaction flow, and Grading —
   this trigger no longer invokes any of those common-file sections.

3. **Rewrite the `## Session header and footer` section** in
   `lesson-grammar-practice.md` — replace the old exercise-count formats
   (`Session: <lesson-code> — N exercises across M grammar points...`) with
   three new formats matching the new flow:
   - Topic-list-confirm format (step 4) — numbered list + confirm/cancel
     prompt.
   - Self-eval-scores prompt format (step 6) — numbered list + `Score each
     1–4 (1=fail, 2=hard, 3=good, 4=easy). Reply with the N scores in order,
     e.g. \`3 4 2\`.`
   - Session-complete footer (after step 7 persistence) — reuse the same
     summary shape as today (`Session complete — <lesson-code> (N grammar
     points)`), adapted to have no exercise count (topic count only, since
     there are no exercises in this flow). This one-line footer fully
     replaces the old Solid/Needs-practice breakdown for this trigger — no
     per-point classification is shown.

4. **Update the `## Study Mode` section** in `lesson-grammar-practice.md` (
   currently just "handled entirely by the common file, no duplicate content
   here") — replace with a short note that this skill enters
   `practice-grammar-study-mode.md` directly at its Step 2 per the new
   Workflow step 5 above, bypassing that file's Step 1 and never reaching its
   Step 3, and point to step 5 for the exact invocation contract. No change
   to `practice-grammar-study-mode.md` itself.

5. **Update the `## Persistence` section** in `lesson-grammar-practice.md` —
   keep the existing one-line pointer to the common file's **Persistence and
   Calendar sync** directive with `scope="lesson"`, adding a note that for
   this trigger it is invoked from the new Workflow step 7 (after Study Mode
   and the post-study self-eval), not before Study Mode as in the old flow.

6. **Two one-line factual corrections only** to
   `.cowork/skills/practice-grammar/practice-grammar-study-mode.md` —
   required because its own text would otherwise be false, not new behavior:
   - `### Trigger` — add one sentence naming the second entry path:
     `lesson-grammar-practice.md`'s Workflow step 5 entering directly at
     Step 2.
   - `## Context required` line — add one parenthetical noting
     `lesson-grammar-practice.md` may invoke Step 2 directly, skipping Step 1.

   Nothing else in that file changes. `_practice-grammar-common.md` and
   `.cowork/skills/practice-grammar/scheduled-grammar-practice.md` remain
   fully untouched.

7. **Verify no slash-command stub changes needed** —
   `.claude/commands/lesson-grammar-practice.md` and
   `.claude/commands/scheduled-grammar-practice.md` are both thin pointers
   ("Read `.cowork/skills/practice-grammar/<file>.md` and follow its
   instructions exactly...") with no behavior encoded — confirmed via direct
   read, no edit needed.

## Risks
- Must not alter `scheduled-grammar-practice.md`'s behavior in any way — it
  and `_practice-grammar-common.md` are untouched by this plan, and
  `practice-grammar-study-mode.md`'s two one-line corrections (step 6) don't
  alter any existing mechanics; verify after implementation by re-reading
  `scheduled-grammar-practice.md` and confirming zero diff.
- `practice-grammar-srs.md`'s persistence mechanics (SM-2 table, `next_review`
  write, `.ics` export, `<!--ID:-->`/`TARGET DECK` never-touch rules) must not
  be modified — only the timing of the call within
  `lesson-grammar-practice.md`'s own Workflow changes, not the directive
  itself.
- Lesson files under `JPLessons/` remain read-only throughout — no change to
  that rule.
- Skill-file edits typically trigger an automatic documentation-agent call
  from `skill-implementer`; per standing user preference, that call (and any
  scribe call) must be gated behind explicit user confirmation, not
  auto-invoked.
