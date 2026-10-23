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

     > **SUPERSEDED by Part 4.** This `load-control.py`-via-`--today`-trick redistribution mechanism was found to silently violate `DAILY_CAP`/`WEAK_CAP` when a 30-day search window is already saturated (the fallback dumps topics onto the least-crowded day even if it's already at or over cap, with no warning). Part 4 below replaces this mechanism with a dedicated cascade-shift script. `load-control.py` itself is unchanged and still used as-is for normal day-to-day SRS scheduling (see Part 4 scope boundary).
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

## Part 4 — FIFO-Sweep Redistribution (replaces Part 3 steps 6-7 mechanism)

### Problem

The `load-control.py`-via-`--today`-trick redistribution used in Part 3 reuses the cap-based `place_topics`/`find_placement_date` algorithm designed for day-to-day SRS scheduling. When the 30-day search window is already saturated (heavily-loaded month), the algorithm's fallback dumps the topic onto the least-crowded day in the window even if that day is already at or over both `DAILY_CAP` and `WEAK_CAP` — silently, with no warning in the output. Verified directly: a topic landed on a day already at `{"total": 10, "weak": 4}` with the shift reported as `"(shifted from X, holiday)"`, no indication the destination was already full. This is unacceptable for holiday redistribution specifically.

### New design — single-pass FIFO sweep, no caps, no score sorting

Confirmed replacement algorithm, scoped ONLY to holiday redistribution. This supersedes an earlier "per-batch independent forward search + recursive displacement" draft, which was ambiguous about how far a single batch's search could reach and did not guarantee strict chronological order preservation.

1. **Scope**: `sweep_start` = the earliest date among the holiday date(s) being added in this operation. `holidays.json` is just a flat list of dates with no "added when" metadata, so `sweep_start` can NOT be computed by scanning that file (the earliest date in the whole file could be an unrelated holiday added months earlier, which would resurrect the exact scope-mismatch bug this redesign exists to fix). Instead, the script takes the newly-added date(s) explicitly via a `--new-dates` CLI argument (comma-separated ISO dates, populated by `manage-holidays.md` from the dates it already parsed in its own Part 3 step 1/2 "Parse dates" step) and computes `sweep_start = min(new_dates)`. Entries with `next_review < sweep_start` are completely out of scope — never touched, never even inspected — regardless of whether they happen to sit on some older, unrelated blocked day.
2. **Blocked** = Saturday (`weekday() == 5`) OR present in the fully-merged `holidays.json` set (old holidays + all newly-added dates/ranges in this operation, since the file is written before this script runs). A day already holding a lot of content does NOT make it blocked — there is no cap of any kind.
3. **The sweep**: walk forward one calendar day at a time starting at `sweep_start`, maintaining a single FIFO queue of "batches" (a batch = the full list of grammar-point keys originally scheduled on one particular original day, moved together, never split). For each day `D` in order:
   a. If `D` has original content (from the pre-operation snapshot) → append that content as one batch to the **back** of the queue. (Do this before step b for the same `D`.)
   b. If `D` is **not** blocked AND the queue is non-empty → pop the batch at the **front** of the queue and set `next_review = D` for every key in that batch.
   c. If `D` is blocked → no assignment happens on `D` this step, regardless of queue state; content just keeps waiting in the queue.
   Continue until the queue is empty (content is finite, so this terminates naturally), bounded by the safety cap in point 6.
4. Because this is **one single global sweep** over the whole timeline (not independent per-source-day searches), multiple holiday ranges added in the same operation resolve correctly automatically — there is no "which range gets processed first" question, because there's no per-range processing at all. Order-independence for multi-range cases is inherent to the design, not a separately-guaranteed property.
5. No `DAILY_CAP`/`WEAK_CAP` enforcement anywhere in this path. No sorting by score/weakness. Days can end up holding more entries than the old caps once queued content lands together — this is intentional.
6. Safety bound: cap the sweep at 365 days past `sweep_start` — if the queue still isn't empty by then, error out rather than looping forever. One number reused for both the day-walk and the implicit queue-drain, not two separate bounds.
7. Only `next_review` is ever written for a shifted key. All other fields (`interval_days`, `ease`, `streak`, `last_score`, `total_reviews`, `weak_points`, `lesson_file`, `grammar_header`, etc.) are left completely untouched — mirroring `merge_and_write()`'s existing guarantee of never overwriting SM-2/identity fields on existing entries.
8. Snapshot step: entries with a missing or unparseable `next_review` are skipped the same way `load-control.py`'s `build_day_counts()` does (try/except around `date.fromisoformat`, continue on failure) — they are never added to the queue and never touched.

**Worked example (verified by hand, matches the user's own trace exactly):** holiday 14-27 Sept 2026 (14 days, `sweep_start` = Sept 14). Original content: Sept 14 (5 items), Sept 16 (2 items), Sept 20 (4 items), Sept 28 (6 items), Sept 29 (some items), Sept 30 (some items). Sweep result:
- Sept 14's batch (5 items) → lands Sept 28 (first unblocked day reached by the sweep with a non-empty queue).
- Sept 16's batch (2 items) → lands Sept 29.
- Sept 20's batch (4 items) → lands Sept 30.
- Sept 28's *original* content (displaced because its slot got taken by Sept 14's batch when the sweep reached Sept 28) → lands Oct 1.
- Sept 29's original content → lands Oct 2.
- Sept 30's original content → next candidate Oct 3 is a Saturday (blocked, skipped) → lands Oct 4.

Use this example in the script's docstring/comments and in test construction where useful.

### File: `.cowork/scripts/holiday-cascade.py` (CREATE)

Standalone script, independent of `load-control.py`'s cap-based placement logic (that logic is not touched — see Scope boundary below). Reuses `load_holidays()`, `load_rules()`, and `is_blocked()` from `load-control.py` via `importlib.util` (same pattern already used by `test_load_control.py` to import the hyphenated filename), so the blocked-day definition (weekday + holidays set) stays a single source of truth rather than being duplicated.

CLI:
```bash
python3 .cowork/scripts/holiday-cascade.py \
  --state .cowork/progress/grammar-state.json \
  --rules .cowork/progress/load-control-rules.json \
  --new-dates 2026-09-14,2026-09-15 \
  [--dry-run]
```
- `--new-dates` (required, comma-separated ISO dates) — the holiday date(s) added in THIS specific `add holiday` operation (a single date, or every date in a range). `sweep_start = min(new_dates)`. This is the only reliable source for `sweep_start`: `holidays.json` has no "added when" metadata, so scanning the file for the earliest date would incorrectly include unrelated holidays added in earlier, separate operations. `manage-holidays.md` passes the exact list it already parsed in its own Part 3 step 1/2 ("Parse dates to ISO strings").
- No separate `--holidays` flag — the holidays file path is derived from `--rules`'s `holidays_file` key via `load_rules()`, matching `load-control.py`'s own pattern, so the two scripts can never drift out of sync on which holidays file they read.
- No stdin input needed (unlike `load-control.py`) — operates on every entry in `grammar-state.json` directly, not a per-session topic list.
- `--dry-run` prints the intended shifts without writing the state file (useful for testing/preview).
- stdout: one summary line per shifted key, e.g. `<key>: <old_date> -> <new_date> (sweep)`, plus a final `N topic(s) shifted.` (or `0 topic(s) shifted -- no collisions.`).
- Exit 0 on success, 1 on error (malformed state file, 365-day safety bound exceeded, etc. — errors to stderr).

### File: `.cowork/scripts/test_holiday_cascade.py` (CREATE)

Same `unittest` + `importlib.util` + `make_topic`-style helper pattern as `test_load_control.py`. Runnable via `python3 -m pytest test_holiday_cascade.py -v` or `python3 test_holiday_cascade.py`. Must cover this confirmed test matrix:

1. Holiday day has content, next day empty → lands there, sweep ends (queue empty).
2. Holiday day has content, next day occupied, day after empty → two-step queue drain.
3. Long run of occupied days after the holiday → queue drains over many days before emptying.
4. All content on one blocked day moves together as a single batch (not split).
5. Landing day would be a Saturday → skipped by the sweep.
6. Landing day would be a pre-existing (not newly-added) holiday → also skipped.
7. Holiday ends immediately before a Saturday → correct skip-over.
8. Multi-day range (e.g. 13-14 Sept) → content from both days queues in chronological order, lands on consecutive first-available days after the range.
9. Two separate ranges added in one call (e.g. 13-14 Sept + 2-3 Oct) → resolved correctly by the single sweep, no special-casing needed.
10. One range's displacement "tail" reaches far enough to intersect a second range → still resolves correctly with no double-shifting, because it's one FIFO queue, not separate per-range runs.
11. Long holiday spanning one or more Saturdays (e.g. a 2-week holiday) → the in-range Saturdays don't need separate handling, they just extend the blocked stretch the sweep passes over.
12. Only `next_review` changes on any shifted entry — `interval_days`, `ease`, `streak`, `last_score`, `total_reviews`, `weak_points`, `lesson_file`, `grammar_header` all untouched.
13. No collisions at all (nothing scheduled in the holiday period or its displacement chain) → no-op, 0 shifted, file unchanged.
14. Safety bound: if the queue never empties within 365 days of `sweep_start` (data anomaly) → error out instead of looping forever.
15. A day has its own original content, is not blocked, and the queue is empty when the sweep reaches it → stays completely unchanged (nothing displaces it, since there's nothing ahead of it in the queue).
16. Content scheduled before `sweep_start` (the earliest newly-added holiday date) → completely untouched, even if it happens to sit on some older, unrelated holiday date elsewhere in the file.

### Changes to `.cowork/skills/manage-holidays.md` (MODIFY)

- Steps 5-6 (collision detection against the newly-added dates, and the yes/no confirmation prompt) are unchanged.
- Step 7's redistribution mechanism (the per-date-group JSON construction + `--today`-trick loop calling `load-control.py`) is replaced with a single invocation:
  ```bash
  python3 .cowork/scripts/holiday-cascade.py \
    --state .cowork/progress/grammar-state.json \
    --rules .cowork/progress/load-control-rules.json \
    --new-dates <comma-separated ISO dates parsed in step 1/2>
  ```
  `--new-dates` is populated from the exact date list `manage-holidays.md` already parsed earlier in its own workflow (Part 3 step 1/2, "Parse dates to ISO strings") — not re-derived from `holidays.json`. No per-date looping, no `--today` argument, no per-topic JSON payload construction needed, no separate `--holidays` flag (the holidays file path comes from `--rules`) — the script reads the full state file directly and handles the whole sweep in one pass.
- Step 7's verification sub-step (re-read `grammar-state.json`, warn if anything is still on a holiday date) is unchanged.
- The "Paths" table gets one new row for `.cowork/scripts/holiday-cascade.py`.
- Keep this edit concise — describe the invocation, don't re-derive the cascade algorithm in skill-file prose (it lives in this plan and in the script's own docstring/comments).

### Scope boundary

`load-control.py`'s cap-based `place_topics()`/`find_placement_date()` logic is **unchanged** and continues to be used as-is for normal day-to-day SRS scheduling after practice sessions (`practice-grammar/lesson-grammar-practice.md`, `practice-grammar/scheduled-grammar-practice.md`, `practice-grammar/practice-grammar-srs.md`). None of those skills or that code path are touched by this plan.

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
| `.cowork/skills/manage-holidays.md` | CREATE (Part 3), MODIFY (Part 4) | New skill: add/remove holidays, collision detection, full .ics export. Part 4 swaps step 7's redistribution mechanism for the `holiday-cascade.py` invocation. |
| `.cowork/instructions.md` | MODIFY | Add vault root exception for full-calendar .ics, add manage-holidays to skill list |
| `.cowork/scripts/holiday-cascade.py` | CREATE (Part 4) | Pure cascade-shift redistribution engine for holiday-blocked dates — no caps, no score sorting. Reuses `load_holidays`/`load_rules`/`is_blocked` from `load-control.py` via `importlib`. Does not touch `load-control.py`'s cap-based logic. |
| `.cowork/scripts/test_holiday_cascade.py` | CREATE (Part 4) | Test suite for the 16 confirmed FIFO-sweep cases (single/range/multi-range holidays, Saturday interaction, out-of-scope entries, unaffected days, field preservation, safety-bound fallback). |

---

## Risks

- **Breaking existing tests** — all existing tests pass Config through function parameters now. Each test must construct a Config object (or use defaults). Migration is mechanical but touches every test.
- **Rules file missing in production** — mitigated by fallback to built-in defaults. The script logs a warning but continues.
- **Holidays file corruption** — graceful degradation: skip bad entries, warn, continue. Never block a practice session because of a malformed holidays file.
- **Collision redistribution race** — mitigated by writing holidays.json BEFORE running redistribution. The script sees the updated holidays list and avoids placing topics on newly added holidays.
- **Calendar file proliferation** — full exports create a new file each time. User is responsible for deleting old files. This matches the existing pattern (per-session .ics files).
- **interval_days=1 trick for redistribution** — SUPERSEDED by Part 4. This workaround silently violated `DAILY_CAP`/`WEAK_CAP` when the 30-day search window was already saturated (fallback placement onto an already-full day, no warning). Kept here for historical context only; Part 4's FIFO-sweep script replaces this mechanism entirely for holiday redistribution.
- **Multi-holiday chronological processing** — no longer applicable to holiday redistribution after Part 4: the sweep is a single global pass over the whole timeline, not independent per-range searches, so multiple holidays/ranges added in one operation resolve correctly with no "which range first" question at all. Still applies to `load-control.py`'s own cap-based scheduling path, which is unchanged.
- **Sweep correctness (Part 4)** — mitigated by the 16-case test matrix in `test_holiday_cascade.py`, covering single/range holidays, adjacent Saturdays, multi-range interference, batch atomicity, out-of-scope and unaffected entries, field preservation, and the 365-day safety bound (no infinite loop).
- **Scope creep into load-control.py** — Part 4 must not modify `load-control.py`'s `place_topics`/`find_placement_date`/cap logic, since `practice-grammar/lesson-grammar-practice.md`, `practice-grammar/scheduled-grammar-practice.md`, and `practice-grammar/practice-grammar-srs.md` depend on that exact cap-based behavior for day-to-day scheduling. Only the read-only helpers (`load_holidays`, `load_rules`, `is_blocked`) are reused via import.
