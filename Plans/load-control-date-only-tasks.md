# Load Control Date-Only Merge Fix -- Tasks

- [x] Fix `merge_and_write()` in `.cowork/scripts/load-control.py` -- make the field copy loop conditional: existing entries get only `next_review` + identity fields (`lesson_file`, `grammar_header`); new entries get full copy of all fields. Capture `original_keys = set(grammar_points.keys())` at the top to distinguish.
- [x] Run `python3 -m pytest test_load_control.py -v` -- all 45 tests must pass (43 existing + 2 new `TestMergeWriteOnlyChangesDate` tests)
- [x] Update "### Load control (TODAY / OVERDUE scope only)" section in `.cowork/skills/practice-grammar.md` -- replace single-pipe approach with two-step write: Step A writes SM-2 fields directly to grammar-state.json (no next_review), Step B pipes minimal JSON (key, interval_days, score) to load-control.py for date placement only
- [x] Simplify `.cowork/skills/manage-holidays.md` step 7b -- remove the note about saving original `interval_days` before building the redistribution array
- [x] Remove step 7c ("Restore original interval_days") from `.cowork/skills/manage-holidays.md` -- no longer needed since `merge_and_write()` won't persist `interval_days` from input for existing entries. Renumber step 7d to 7c.
- [x] Verify no other callers of `merge_and_write()` depend on SM-2 field copying for existing entries (read-only check)
