# Manage Holidays — Holiday-Aware Load Control

## Goal
Make the SRS load control system holiday-aware and centralize its configuration. Holidays are treated identically to Saturdays — no reviews placed on them. A new manage-holidays skill lets the user add/remove holidays, detects collisions with already-scheduled reviews, redistributes colliding topics through the existing placement algorithm, and generates a full-calendar .ics export so the user can replace their calendar entirely.

## Approach

Three parts, built in order because each depends on the previous:

1. **Shared rules file** — extract hardcoded constants from `load-control.py` into `.cowork/progress/load-control-rules.json`. The Python script reads this file at startup. The practice-grammar skill references this file instead of duplicating the constants table.

2. **Holiday-aware blocking** — extend `is_blocked()` in `load-control.py` to check dates against `.cowork/progress/holidays.json`. Add a `--holidays` CLI argument (path derived from rules file by default). Add tests for holiday blocking. Update summary lines to label holiday shifts distinctly.

3. **manage-holidays skill** — new skill at `.cowork/skills/manage-holidays.md` for adding/removing holidays, collision detection, redistribution, and full .ics export.

Key trade-off: the rules file introduces a runtime dependency (the script fails if the file is missing or malformed). Mitigated by having the script fall back to built-in defaults if the file is absent, and by validating the JSON schema on load.

---

## Part 1 — Shared Load Control Rules File

### File: `.cowork/progress/load-control-rules.json`

```json
{
  "DAILY_CAP": 10,
  "WEAK_CAP": 4,
  "BLOCKED_WEEKDAY": 5,
  "SEARCH_WINDOW": 30,
  "holidays_file": ".cowork/progress/holidays.json"
}
```

All paths in the rules file are relative to CWD. The script is always invoked from the vault root, so CWD = vault root. No alternative resolution strategies — CWD is the single source of truth for path resolution.

### Changes to `load-control.py`

1. Add a `--rules` CLI argument (default: `.cowork/progress/load-control-rules.json`).
2. Add a `load_rules(path)` function that:
   - Reads the JSON file.
   - Validates expected keys exist and have correct types (int for caps/window, int for weekday, string for holidays_file).
   - Returns a dict with the parsed values.
   - On file-not-found: logs a warning to stderr, returns built-in defaults (current hardcoded values). This prevents breakage if the file is accidentally deleted.
   - On parse error: prints error to stderr, exits 1.
3. Replace module-level constants (`DAILY_CAP`, `WEAK_CAP`, `BLOCKED_WEEKDAY`, `SEARCH_WINDOW`) with values loaded from the rules file. Pass them through function parameters rather than relying on globals — this keeps the functions testable.
4. Define a `Config` dataclass to bundle all constants and pass it as a single parameter:
   ```python
   @dataclasses.dataclass
   class Config:
       daily_cap: int = 10
       weak_cap: int = 4
       blocked_weekday: int = 5
       search_window: int = 30
       holidays: set[date] = field(default_factory=set)
       holidays_file: str = ".cowork/progress/holidays.json"
   ```
   Note: `holidays_file` is included in Config so the manage-holidays skill can derive the path from the same rules file the script uses.
5. Update function signatures to accept an **optional** Config parameter (defaults to `Config()`). This ensures existing calls without Config still work — critical for keeping existing tests unmodified as a regression safety net:
   - `is_blocked(d, config=None)` — checks weekday and holidays. `config` defaults to `Config()` if None.
   - `find_placement_date(candidate, is_weak, day_counts, today, config=None)` — uses Config for caps, window, blocking.
   - `place_topics(topics, grammar_points, today, config=None)` — passes Config through.
   - `build_day_counts(grammar_points, today)` — unchanged (no config dependency).
6. Update the summary line in `merge_and_write()` to check holidays and label shifts appropriately:
   - If the raw date was a blocked weekday (Saturday): `(shifted from DATE, Saturday)`
   - If the raw date was a holiday: `(shifted from DATE, holiday)`
   - If shifted for capacity reasons only: `(shifted from DATE)` (no special label — the shift was due to caps, not blocking)
   
   Current code hardcodes `', Saturday'` — this must check `config.holidays` and `config.blocked_weekday` to pick the correct label. The `merge_and_write` function needs access to Config for this.

### Changes to `practice-grammar.md`

Replace the hardcoded constants table in the `## Persistence` section:

**Before:**
```markdown
### Load control constants

| Constant | Value | Meaning |
|---|---|---|
| DAILY_CAP | 10 | Max topics on any single day |
| WEAK_CAP | 4 | Max topics with evaluation score 1 or 2 on any single day |
| BLOCKED_DAY | Saturday (weekday 5) | No reviews placed on Saturdays |
| SEARCH_WINDOW | 30 | Max days to search forward before fallback |
```

**After:**
```markdown
### Load control constants

Constants are defined in `.cowork/progress/load-control-rules.json` (single source of truth). The Python script reads this file at startup. Current defaults:

| Constant | Default | Meaning |
|---|---|---|
| DAILY_CAP | 10 | Max topics on any single day |
| WEAK_CAP | 4 | Max topics with evaluation score 1 or 2 on any single day |
| BLOCKED_WEEKDAY | 5 (Saturday) | No reviews placed on this weekday (Monday=0) |
| SEARCH_WINDOW | 30 | Max days to search forward before fallback |
| holidays_file | .cowork/progress/holidays.json | Path to holiday dates list |

Additionally, dates listed in the holidays file are blocked identically to Saturdays.
```

Also update the shell invocation command in the `### Load control (TODAY / OVERDUE scope only)` section to include `--rules`:

```bash
echo '<json_array>' | python3 .cowork/scripts/load-control.py \
  --state .cowork/progress/grammar-state.json \
  --rules .cowork/progress/load-control-rules.json \
  --today <today_ISO>
```

Note: `--rules` defaults to `.cowork/progress/load-control-rules.json` when CWD is vault root, so the explicit flag is optional but included for clarity.

### Changes to `test_load_control.py`

**Existing tests must NOT be modified.** They serve as a regression safety net — if refactoring breaks the existing behavior, these tests catch it. The refactored functions must remain backwards-compatible so existing tests continue to pass without changes.

To achieve this, the Config dataclass uses sensible defaults matching the current hardcoded values. Functions that previously used module-level constants now accept an optional `config` parameter that defaults to `Config()` — this way existing test calls (without Config) still work.

**New tests are added separately** for the new functionality:
1. Tests for `load_rules()`:
   - Valid file loads correctly.
   - Missing file returns defaults with warning.
   - Malformed JSON exits 1.
   - Missing key uses default for that key.
2. Tests for summary line labels:
   - Topic shifted from Saturday: summary says "(shifted from DATE, Saturday)".
   - Topic shifted from holiday: summary says "(shifted from DATE, holiday)".
   - Topic shifted from capacity: summary says "(shifted from DATE)" with no blocking label.

---

## Part 2 — Holiday-Aware Blocking

### File: `.cowork/progress/holidays.json`

```json
[
  "2026-07-04",
  "2026-12-25",
  "2026-12-31"
]
```

Simple JSON array of ISO date strings. No metadata, no names — just dates. Empty array `[]` is valid (no holidays). File absence is equivalent to `[]`.

**This file is NOT created as an initial task.** It does not need to exist before first use — `load_holidays()` treats a missing file as an empty set, and the manage-holidays skill creates the file on first `add holiday` invocation.

### Changes to `load-control.py`

1. Add `load_holidays(path)` function:
   - Reads the JSON file.
   - Validates it's a list of strings, each parseable as ISO date.
   - Returns a `set[date]`.
   - On file-not-found: returns empty set (no holidays).
   - On parse error: prints warning to stderr, returns empty set (graceful degradation — don't block the whole session because of a bad holidays file).
   - Invalid individual dates: skip with warning, continue loading the rest.
2. Update `is_blocked(d, config)`:
   ```python
   def is_blocked(d: date, config: Config) -> bool:
       return d.weekday() == config.blocked_weekday or d in config.holidays
   ```
3. The `main()` function:
   - Loads rules via `load_rules()`.
   - Derives holidays path from `rules["holidays_file"]` (resolved relative to CWD).
   - Loads holidays via `load_holidays()`.
   - Constructs Config with all values.
   - Passes Config to `place_topics()` and `merge_and_write()`.

### New tests in `test_load_control.py`

- **Holiday blocked**: a date in the holidays set returns `is_blocked = True`.
- **Non-holiday not blocked**: a regular weekday not in holidays returns `is_blocked = False`.
- **Holiday + Saturday**: Saturday that is also a holiday — still blocked (no double-counting issue).
- **Holiday skip in placement**: topic candidate falls on a holiday, gets shifted forward.
- **Multiple holidays in a row**: e.g. Dec 31 + Jan 1 — topic skips both.
- **Empty holidays file**: no dates blocked beyond the regular weekday.
- **Missing holidays file**: treated as empty, no error.
- **Malformed holidays file**: graceful degradation, empty set returned.

---

## Part 3 — Manage-Holidays Skill

### File: `.cowork/skills/manage-holidays.md`

### Trigger

- "manage holidays"
- "add holiday <date(s)>"
- "remove holiday <date(s)>"
- "show holidays"
- "export calendar" / "full calendar export"

### Workflow

#### 1. Show current holidays

Read `.cowork/progress/holidays.json`. If missing, report "No holidays file found — starting fresh." Display the list sorted chronologically. If empty: "No holidays configured."

#### 2. Add holidays

User provides one or more dates (ISO format, or natural language like "July 4", "next Friday"). Claude parses to ISO dates.

Steps:
1. Parse dates to ISO strings.
2. Read current `holidays.json` (or `[]` if missing).
3. Check for duplicates — skip any date already in the list, inform user.
4. **Write updated `holidays.json` first** — add the new dates, sort, deduplicate, and write the file BEFORE any redistribution. This ensures `load-control.py` sees the updated holidays list when it runs, preventing topics from being moved onto another new holiday.
5. **Collision detection** — read `grammar-state.json`, find all entries where `next_review` matches any of the new holiday dates.
6. If collisions found:
   - List them: "N topics have reviews scheduled on these dates:"
   - For each: `<grammar_header> — next_review: <date>`
   - Ask: "Move these to the next available date? (yes/no)"
   - If yes: redistribute via `load-control.py`, **one invocation per distinct holiday date, processed in chronological order**. Each invocation writes `grammar-state.json`, so the next invocation sees the previous placements and avoids creating new conflicts.
     
     For each distinct holiday date with collisions, collect the colliding topics for that date and build the input JSON. For each colliding topic:
     ```json
     {
       "key": "<existing key>",
       "lesson_file": "<existing>",
       "grammar_header": "<existing>",
       "last_reviewed": "<existing last_reviewed>",
       "score": "<existing last_score>",
       "interval_days": 1,
       "ease": "<existing ease>",
       "streak": "<existing streak>",
       "total_reviews": "<existing total_reviews>",
       "weak_points": "<existing weak_points>",
       "last_score": "<existing last_score>"
     }
     ```
     Run with `--today` set to one day before that specific holiday:
     ```bash
     echo '<json_array_for_date>' | python3 .cowork/scripts/load-control.py \
       --state .cowork/progress/grammar-state.json \
       --rules .cowork/progress/load-control-rules.json \
       --today <holiday_date - 1 day>
     ```
     This makes `candidate = (holiday-1) + max(1, 1) = holiday_date`, which is now blocked (holidays.json was already updated in step 4), so the algorithm searches forward to the next valid day.
     
     **Process dates in chronological order.** Example: adding Dec 25 and Dec 26 as holidays. First invocation handles Dec 25 collisions with `--today 2026-12-24`. Second invocation handles Dec 26 collisions with `--today 2026-12-25`. The second invocation reads the updated grammar-state.json from the first, so it knows Dec 25 already has its new placements.
   - If no: leave reviews in place (user accepts they'll be overdue).
7. **Verification** — after all redistribution invocations complete, read `grammar-state.json` and verify no topic has `next_review` on any holiday date. If any remain (should not happen, but defensive check), warn the user: "Warning: N topic(s) still scheduled on holiday dates after redistribution — manual review may be needed."
8. Confirm: "Added N holiday(s). M topic(s) redistributed."

#### 3. Remove holidays

User provides dates to remove.

Steps:
1. Parse dates.
2. Read `holidays.json`.
3. Remove matching dates. Warn if a date wasn't in the list.
4. Write updated `holidays.json`.
5. Note: removing a holiday does NOT retroactively move topics back to that date. Reviews stay where they are. Inform user: "Removed N holiday(s). Existing review dates are unchanged."

#### 4. Full .ics export

Generate a single `.ics` file containing ALL future scheduled review events from `grammar-state.json` (not just a single session).

Steps:
1. Read `grammar-state.json`.
2. Filter: keep entries where `next_review >= today`. Exclude entries where `next_review < today` (overdue — they'll be picked up by the next practice session, not shown as future calendar events).
3. Group by `next_review` date.
4. Generate one VEVENT per date:
   - `SUMMARY: Japanese Grammar Review -- N point(s)`
   - `DESCRIPTION:` newline-separated list of `grammar_header` values.
   - `DTSTART;VALUE=DATE:YYYYMMDD` / `DTEND;VALUE=DATE:YYYYMMDD+1` (all-day events).
   - `UID: <date>-full-export-<uuid8>@japanese-notes`
5. Also include holidays as separate events:
   - `SUMMARY: Holiday -- No Review`
   - `DESCRIPTION: Holiday -- no grammar reviews scheduled.`
   - Only include future holidays (>= today).
6. Write to vault root: `japanese-grammar-full-calendar-<YYYYMMDDTHHMMSS>.ics`
7. Use the same `fold()` function and ICS structure as the existing calendar sync code.
8. Report: "Full calendar exported: N review events + M holiday events written to <filename>."

---

## Changes to `.cowork/instructions.md`

Two updates required (both need user permission before modifying):

### 1. Vault root exception

Add `japanese-grammar-full-calendar-<timestamp>.ics` to the approved vault root exceptions. The updated block:

```markdown
- Never create files directly in the vault root (`/ObsidianJP/`) unless explicitly asked
  - Approved exception: `.ics` calendar files written by the practice-grammar skill (`japanese-grammar-review-<timestamp>.ics`) and manage-holidays skill (`japanese-grammar-full-calendar-<timestamp>.ics`). These are intentionally placed at the vault root for easy drag-and-drop calendar import.
```

### 2. Skill list entry

Add the following entry to the `## Available skills` section, after the `reading-jlpt` entry:

```markdown
- manage-holidays — manage holiday dates for the SRS load control system. Add/remove holidays (treated as blocked days like Saturdays), detect and redistribute colliding reviews, export a full-calendar .ics with all future review events and holidays. Reads/writes `.cowork/progress/holidays.json`. Trigger: "manage holidays", "add holiday <date>", "remove holiday <date>", "show holidays", "export calendar"
```

---

## File change summary

| File | Action | Description |
|---|---|---|
| `.cowork/progress/load-control-rules.json` | CREATE | Constants + holidays_file path |
| `.cowork/scripts/load-control.py` | MODIFY | Read rules from JSON, Config dataclass, holiday-aware `is_blocked()`, holiday-aware summary labels |
| `.cowork/scripts/test_load_control.py` | MODIFY | Update tests for Config parameter, add rules/holiday/summary-label tests |
| `.cowork/skills/practice-grammar.md` | MODIFY | Replace hardcoded constants table with reference to rules file, add `--rules` to invocation command |
| `.cowork/skills/manage-holidays.md` | CREATE | New skill: add/remove holidays, collision detection, full .ics export |
| `.cowork/instructions.md` | MODIFY | Add vault root exception for full-calendar .ics, add manage-holidays to skill list |

---

## Risks

- **Breaking existing tests** — all existing tests pass Config through function parameters now. Each test must construct a Config object (or use defaults). Migration is mechanical but touches every test.
- **Rules file missing in production** — mitigated by fallback to built-in defaults. The script logs a warning but continues.
- **Holidays file corruption** — graceful degradation: skip bad entries, warn, continue. Never block a practice session because of a malformed holidays file.
- **Collision redistribution race** — mitigated by writing holidays.json BEFORE running redistribution. The script sees the updated holidays list and avoids placing topics on newly added holidays.
- **Calendar file proliferation** — full exports create a new file each time. User is responsible for deleting old files. This matches the existing pattern (per-session .ics files).
- **interval_days=1 trick for redistribution** — setting interval_days=1 with --today=holiday-1 is a workaround that reuses the existing algorithm. It means the topic lands on the nearest valid day after the holiday, which may not preserve the original interval spacing. This is acceptable because the alternative (leaving it on a holiday) is worse.
- **Multi-holiday chronological processing** — if holidays are not processed in chronological order, a later holiday's redistribution could unknowingly place topics on an earlier holiday that hasn't been processed yet. Chronological ordering eliminates this risk since earlier holidays are already in holidays.json and processed first.
