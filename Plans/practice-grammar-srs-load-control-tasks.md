# Practice-Grammar SRS Load Control — Tasks

- [ ] Create `.cowork/scripts/load-control.py` — importable module with `main()` entry point. Reads stdin JSON + grammar-state.json, applies load control (Saturday block, daily cap, weak cap, priority sorting, forward search, fallback), writes updated grammar-state.json. Exit 0 on success, 1 on error, errors to stderr.
- [ ] Create `.cowork/scripts/test_load_control.py` — imports functions directly from load-control. 14 test cases: basic placement, Saturday skip, daily cap, weak cap, weak cap not applied to strong, priority ordering, fallback, interval_days preserved (not overwritten), multiple topics in session, Saturday+full Sunday, existing JSON preserved, minimum candidate date, count includes today, error handling.
- [ ] Run tests and verify all pass
- [ ] Add constants table and `## Load control` subsection to Persistence section in `.cowork/skills/practice-grammar.md` — instruct skill to pipe session results to the script for TODAY/OVERDUE scope
- [ ] Verify calendar sync section reads next_review after JSON write (read-only check, no changes expected)
