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
