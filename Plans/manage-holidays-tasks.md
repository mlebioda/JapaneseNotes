# Manage Holidays — Tasks

## Part 1 — Shared rules file

- [x] Create `.cowork/progress/load-control-rules.json` with constants (DAILY_CAP=10, WEAK_CAP=4, BLOCKED_WEEKDAY=5, SEARCH_WINDOW=30) and `holidays_file` path
- [x] Add `Config` dataclass to `load-control.py` — bundles all constants + holidays set + holidays_file path
- [x] Add `load_rules(path)` to `load-control.py` — reads JSON, validates types, falls back to defaults on missing file, exits 1 on parse error
- [x] Add `--rules` CLI argument to `load-control.py` (default: `.cowork/progress/load-control-rules.json`)
- [x] Refactor `is_blocked()` to accept optional Config parameter (defaults to `Config()`) — existing calls without Config still work
- [x] Refactor `find_placement_date()` to accept optional Config — uses config for caps, search window, and blocking
- [x] Refactor `place_topics()` to accept optional Config and pass it through to called functions
- [x] Refactor `merge_and_write()` to accept optional Config and label shifts correctly: "(shifted from DATE, Saturday)" for blocked weekday, "(shifted from DATE, holiday)" for holiday dates, "(shifted from DATE)" for capacity-only shifts
- [x] Run existing tests UNMODIFIED — they must pass as-is to confirm refactoring didn't break anything
- [x] Add NEW tests for `load_rules()`: valid file, missing file (defaults + warning), malformed JSON (exit 1), missing key (uses default)
- [x] Add NEW tests for summary line labels: Saturday shift label, holiday shift label, capacity-only shift (no label)
- [x] Run all tests (old + new) and verify they pass
- [x] Update constants table in `practice-grammar.md` `## Persistence` section to reference rules file as single source of truth
- [x] Update shell invocation command in `practice-grammar.md` `### Load control` section to include `--rules .cowork/progress/load-control-rules.json`

## Part 2 — Holiday-aware blocking

- [x] Add `load_holidays(path)` to `load-control.py` — reads JSON array of ISO dates, returns `set[date]`, graceful on missing/malformed file
- [x] Update `is_blocked()` to check `config.holidays` in addition to `config.blocked_weekday`
- [x] Wire holiday loading into `main()`: load rules, derive holidays path from rules (resolved relative to CWD), load holidays, construct Config
- [x] Add holiday tests: date in holidays is blocked, non-holiday not blocked, Saturday+holiday, holiday skip in placement, consecutive holidays, empty file, missing file, malformed file
- [x] Run all tests (old + new) and verify they pass

## Part 3 — Manage-holidays skill

- [x] Create `.cowork/skills/manage-holidays.md` with full workflow: show/add/remove holidays, collision detection, redistribution via load-control.py, full .ics export
  - [x] Write holidays.json BEFORE redistribution (so load-control.py sees new holidays)
  - [x] One load-control.py invocation per distinct holiday date, chronological order
  - [x] Include `--rules` flag in all load-control.py invocations
  - [x] Add verification step after redistribution: read grammar-state.json, confirm no topic has next_review on any holiday date
- [x] Update `.cowork/instructions.md` vault root exception to include `japanese-grammar-full-calendar-<timestamp>.ics` (requires user permission)
- [x] Update `.cowork/instructions.md` skill list to add manage-holidays entry with exact text: `manage-holidays — manage holiday dates for the SRS load control system. Add/remove holidays (treated as blocked days like Saturdays), detect and redistribute colliding reviews, export a full-calendar .ics with all future review events and holidays. Reads/writes .cowork/progress/holidays.json. Trigger: "manage holidays", "add holiday <date>", "remove holiday <date>", "show holidays", "export calendar"` (requires user permission)

## Part 4 — FIFO-sweep redistribution (replaces Part 3 steps 6-7 mechanism)

- [x] Create `.cowork/scripts/holiday-cascade.py`:
  - [x] Import `load_holidays`, `load_rules`, `is_blocked` from `load-control.py` via `importlib.util` (do not duplicate this logic)
  - [x] Derive the holidays file path from `--rules`'s `holidays_file` key via `load_rules()` — no separate `--holidays` CLI flag
  - [x] Snapshot original `next_review` -> keys from `grammar-state.json` before any mutation, skipping entries with missing/unparseable `next_review` (try/except around `date.fromisoformat`, continue on failure — same pattern as `load-control.py`'s `build_day_counts()`)
  - [x] Add a required `--new-dates` CLI argument (comma-separated ISO dates) — this is the ONLY valid source for `sweep_start`, since `holidays.json` has no "added when" metadata and scanning it for the earliest date would wrongly include unrelated holidays added in earlier, separate operations; compute `sweep_start = min(new_dates)`. Entries with `next_review < sweep_start` are out of scope and never inspected
  - [x] Implement the single-pass FIFO sweep: walk forward one day at a time from `sweep_start`; for each day `D`, first enqueue any original content on `D` as one batch to the back of the queue, then if `D` is not blocked and the queue is non-empty, pop the front batch and assign `next_review = D` to every key in it; if `D` is blocked, no assignment happens this step
  - [x] Bound the sweep at 365 days past `sweep_start` (one number, reused for both the day-walk and the implicit queue-drain) — error out if the queue is still non-empty at the bound, instead of looping forever
  - [x] Write only `next_review` for shifted keys; leave every other field (`interval_days`, `ease`, `streak`, `last_score`, `total_reviews`, `weak_points`, `lesson_file`, `grammar_header`, etc.) untouched
  - [x] CLI: `--state`, `--rules`, `--new-dates` (required), optional `--dry-run`; no stdin needed
  - [x] stdout: one summary line per shifted key + final count line; exit 0/1 per success/error
  - [x] Add the worked example (holiday 14-27 Sept 2026) from the plan as a docstring/comment illustrating the sweep
- [x] Create `.cowork/scripts/test_holiday_cascade.py` (same `unittest` + `importlib.util` + `make_topic`-style pattern as `test_load_control.py`), covering all 16 confirmed cases:
  - [x] Case 1: holiday day has content, next day empty -> lands there, sweep ends (queue empty)
  - [x] Case 2: holiday day has content, next day occupied, day after empty -> two-step queue drain
  - [x] Case 3: long run of occupied days after the holiday -> queue drains over many days before emptying
  - [x] Case 4: all content on one blocked day moves together as a single batch (not split)
  - [x] Case 5: landing day would be a Saturday -> skipped by the sweep
  - [x] Case 6: landing day would be a pre-existing (not newly-added) holiday -> also skipped
  - [x] Case 7: holiday ends immediately before a Saturday -> correct skip-over
  - [x] Case 8: multi-day range (e.g. 13-14 Sept) -> content from both days queues in chronological order, lands on consecutive first-available days after the range
  - [x] Case 9: two separate ranges added in one call (e.g. 13-14 Sept + 2-3 Oct) -> resolved correctly by the single sweep, no special-casing needed
  - [x] Case 10: one range's displacement tail reaches far enough to intersect a second range -> still resolves correctly with no double-shifting
  - [x] Case 11: long holiday spanning one or more Saturdays -> in-range Saturdays just extend the blocked stretch the sweep passes over
  - [x] Case 12: only `next_review` changes on any shifted entry -- `interval_days`, `ease`, `streak`, `last_score`, `total_reviews`, `weak_points`, `lesson_file`, `grammar_header` all untouched
  - [x] Case 13: no collisions at all (nothing scheduled in the holiday period or its displacement chain) -> no-op, 0 shifted, file unchanged
  - [x] Case 14: queue never empties within 365 days of `sweep_start` (data anomaly) -> error out instead of looping forever
  - [x] Case 15: a day has its own original content, is not blocked, and the queue is empty when the sweep reaches it -> stays completely unchanged
  - [x] Case 16: content scheduled before `sweep_start` -> completely untouched, even if it sits on some older, unrelated holiday date elsewhere in the file
- [x] Run `python3 -m pytest test_holiday_cascade.py -v` (or `python3 test_holiday_cascade.py`) from `.cowork/scripts/` and verify all 16 cases pass
- [x] Edit `.cowork/skills/manage-holidays.md`:
  - [x] Add a row for `.cowork/scripts/holiday-cascade.py` to the Paths table
  - [x] Replace step 7's per-date-group `--today`-trick loop (calling `load-control.py`) with a single `holiday-cascade.py` invocation (`--state`, `--rules`, `--new-dates`)
  - [x] Pass `--new-dates` from the exact date list already parsed in the skill's own Part 3 step 1/2 ("Parse dates to ISO strings") — do not re-derive it from `holidays.json`
  - [x] Keep steps 5-6 (collision detection, yes/no confirmation) unchanged
  - [x] Keep step 7's verification sub-step unchanged
  - [x] Confirm `load-control.py` itself is not modified by this edit
