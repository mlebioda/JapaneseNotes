# Practice Grammar — Batch Mode for Scope Sessions

## Goal
When a scope session ("practice today's topics" or "practice overdue topics") contains more than a small number of topics, the current single-pass flow asks the user to rate every topic in one go. This becomes unwieldy for large sets. The goal is to split scope sessions into manageable batches of up to 5 topics each, so the user drills and rates one batch at a time, receives a full session summary only after the last batch, and has persistence and .ics export deferred until all batches are complete.

## Approach
Add a single branching step inside `practice-grammar.md` immediately after the topic list is assembled (step 6, scope sessions only). If the topic count exceeds 5, divide the list into ordered batches of 5. Run the existing drill-and-rate loop once per batch. After the final batch, print the session summary and trigger persistence and .ics export as today. Non-scope sessions ("let's practice UNGL14") are unaffected.

## Steps

1. **Step 6b — batch-split prompt** (`/.cowork/skills/practice-grammar.md`)
   After step 6 assembles the topic list for a scope session, insert step 6b:
   - If topic count > 5: divide into batches of 5 (last batch may be smaller). Inform the user: "X topics found. Splitting into Y batches of up to 5."
   - If topic count <= 5: proceed as today (no batching).
   - This step runs only for scope sessions; direct-lesson sessions skip it entirely.

2. **Batch loop replacing single-pass interaction** (`/.cowork/skills/practice-grammar.md`)
   Replace the current single drill-and-rate pass with a loop:
   - For each batch: display batch number (e.g. "Batch 1 / 3"), run the full drill-and-rate sequence for those topics, then ask "Ready for the next batch? (yes / stop)" before proceeding.
   - If the user types "stop", exit the loop early (topics not yet drilled are skipped; no SM-2 update for them).
   - If only one batch exists, the "Ready for next batch?" prompt is skipped.

3. **Session summary after last batch** (`/.cowork/skills/practice-grammar.md`)
   Move the session summary printout (score, per-topic results) to fire once after the batch loop ends, not after each individual batch.

4. **Persistence deferred until all batches complete** (`/.cowork/skills/practice-grammar.md`)
   The SM-2 state write to `.cowork/progress/grammar-state.json` currently happens at end of session. Confirm it fires only once, after the batch loop, covering all batches' ratings together. No per-batch partial writes.

5. **`.ics` written after all batches complete** (`/.cowork/skills/practice-grammar.md`)
   The `.ics` calendar export also fires once after the batch loop, using the next-review dates computed across all batches in the session.

6. Create `.claude/commands/practice-grammar.md` — slash command stub pointing to the skill (if not already present).

## Risks
- Scope sessions that the user stops mid-batch will only persist SM-2 ratings for completed batches. Topics in the interrupted batch are skipped silently — this is acceptable and consistent with "stop" being an explicit user action.
- The `.ics` file will only reflect topics that were actually drilled. If the user stops early, future overdue sessions will surface the skipped topics again, which is the correct behaviour.
- No changes to `# Summary`, `TARGET DECK`, or `<!--ID:-->` lines — fill-templates data is untouched.
