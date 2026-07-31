# Practice Grammar — Persist Before Study Mode (last batch) — Tasks

- [x] Rewrite Workflow step 7e's last-batch branch (`.cowork/skills/practice-grammar.md`, currently lines 150–157) so steps 8–10 (write session summary, persist `grammar-state.json`, write calendar `.ics`) run unconditionally immediately after self-evaluation scores are collected for the last batch, before any prompt appears
- [x] Replace the `Study mode / Save & finish` prompt with `Study mode / Finish`, and rewrite its two option descriptions: "Study mode" → supplementary practice only, ends session on exit (nothing left to persist); "Finish" → ends session immediately
- [x] Confirm the "prompt must always appear" rule is preserved in the rewritten bullet
- [x] Add the new guard: "stop"/"end" typed in reply to the `Study mode / Finish` prompt is a no-op alias for "Finish" (end session, do not re-invoke `practice-grammar-srs.md`, do not rewrite `grammar-state.json`, do not write a second `.ics` file) — it must NOT trigger the general Early-exit re-persist path
- [x] Confirm the Early exit sub-bullet's behavior for all other (pre-persistence) mid-session points is left unchanged
- [x] Add a note to Workflow step 8 (currently line 160) clarifying that steps 8–10 execute automatically as part of step 7e's last-batch branch, not as a separate phase gated behind a user choice
- [x] Update the opening line of the Persistence and Calendar sync section (currently lines 502–513) to note persistence now happens immediately upon last-batch self-evaluation completion, before the Study mode/Finish prompt
- [x] Clarify the `weak_points` bullet in the Study Mode section (`.cowork/skills/practice-grammar.md`, currently line 444) to specify it is the value loaded once at Workflow step 5 / accumulated in-memory during the session — never a fresh re-read of `grammar-state.json` after persistence
- [x] Fix the `is_last_batch` bullet in the Study Mode section (`.cowork/skills/practice-grammar.md`, currently line 441) — replace "proceed to post-session" wording with "Next batch / Finish" vs. "end the session (already saved)"
- [x] Fix `.cowork/skills/practice-grammar-study-mode.md` Step 3, last-batch case (currently line 153) — replace "proceed directly to post-session (write state + calendar)" with "session already saved before Study Mode was entered — end the session now; do NOT re-invoke `practice-grammar-srs.md`, do not rewrite `grammar-state.json`, do not write a second `.ics` file"
- [x] Confirm the non-last-batch case in `practice-grammar-study-mode.md` Step 3 (currently lines 150–152, "Next batch / Finish") is left unchanged — it's a genuine early exit with real unsaved data
- [x] Update the standalone sentence below the Step 3 bullets in `practice-grammar-study-mode.md` (currently line 155, "The 'Finish' option in Step 3 is a full early exit...") to scope it explicitly to the non-last-batch case only
- [x] Sync the `weak_points` bullet in `practice-grammar-study-mode.md`'s Context required section (currently line 19) with the same wording fix applied to `practice-grammar.md` line 444
- [x] Fix the `is_last_batch` bullet in `practice-grammar-study-mode.md`'s Context required section (currently line 17) to match the `practice-grammar.md` line 441 fix
- [x] Verify the non-last-batch branch of `practice-grammar.md` step 7e (`Next batch / Study mode`, lines 142–149) is untouched
- [x] Verify `.cowork/skills/practice-grammar-srs.md` is NOT modified (its internal logic and inputs are unaffected by this reorder)
- [x] Verify no `<!--ID:-->` lines, `TARGET DECK` lines, or lesson files were touched
- [x] Confirm `.cowork/instructions.md` does not need updating for this change
- [x] Re-check for a double-persistence path end-to-end: last batch → Study mode → exit Study mode → session ends without a second write to `grammar-state.json` or a second `.ics` file; and last batch → "stop"/"end" at the `Study mode / Finish` prompt → session ends without a second write
</content>
