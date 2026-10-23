---
name: manage-holidays
description: >
  Manage holiday dates for the SRS load control system. Add/remove holidays
  (treated as blocked days like Saturdays), detect and redistribute colliding
  reviews, export a full-calendar .ics with all future review events and holidays.
  Reads/writes .cowork/progress/holidays.json.
---

# Manage Holidays Skill

## Trigger

User says any of:
- "manage holidays"
- "add holiday <date(s)>"
- "remove holiday <date(s)>"
- "show holidays"
- "export calendar" / "full calendar export"

---

## Paths

| File | Purpose |
|---|---|
| `.cowork/progress/holidays.json` | JSON array of ISO date strings (`["2026-07-04", ...]`). Single source of holiday dates. |
| `.cowork/progress/grammar-state.json` | SRS state file. Read for collision detection; written by holiday-cascade.py during redistribution. |
| `.cowork/progress/load-control-rules.json` | Load control constants and holidays_file path. Passed via `--rules` to every load-control.py invocation. |
| `.cowork/scripts/load-control.py` | Normal day-to-day SRS scheduling engine. Not used for holiday redistribution (see `holiday-cascade.py` below). |
| `.cowork/scripts/holiday-cascade.py` | Holiday redistribution engine. Single-pass FIFO sweep that moves colliding reviews off holiday dates -- no caps, no score sorting. Invoked once per add-holiday operation. |

---

## Workflow

### 1. Show current holidays

1. Read `.cowork/progress/holidays.json`.
   - If the file does not exist: print `No holidays file found -- starting fresh.` and stop.
   - If the file is empty (`[]`): print `No holidays configured.` and stop.
2. Sort dates chronologically (ascending).
3. Display the list as a numbered table:

```
Current holidays:
  1. 2026-07-04 (Saturday)
  2. 2026-12-25 (Thursday)
  3. 2026-12-31 (Wednesday)
```

Include the day-of-week name in parentheses for each date.

---

### 2. Add holidays

User provides one or more dates. Accept ISO format (`2026-07-04`) or natural language (`July 4`, `next Friday`). Parse all dates to ISO strings (YYYY-MM-DD).

#### Steps

1. **Parse dates** -- convert each user-provided date to an ISO string. If a date cannot be parsed, report the specific input that failed and skip it. Continue processing the remaining dates.

2. **Read current holidays** -- load `.cowork/progress/holidays.json`. If missing, start with an empty array `[]`.

3. **Check for duplicates** -- for each new date, if it already exists in the array, print `<date> is already a holiday -- skipping.` and exclude it from further processing. If all dates are duplicates, print `All dates are already holidays -- nothing to add.` and stop.

4. **Write updated holidays.json** -- merge new dates into the array, sort chronologically, deduplicate, and write the file. This write happens BEFORE any redistribution so that `holiday-cascade.py` sees the updated holidays list when it runs and will not place topics on any of the new holiday dates.

5. **Collision detection** -- read `.cowork/progress/grammar-state.json`. For each entry in `grammar_points`, check whether `next_review` matches any of the newly added holiday dates. Collect all matches.

6. **Report collisions** -- if collisions are found, list them:

```
N topic(s) have reviews scheduled on new holiday dates:

  <grammar_header> -- next_review: 2026-07-04
  <grammar_header> -- next_review: 2026-12-25
  ...

Move these to the next available date? (yes/no)
```

If no collisions: print `No existing reviews fall on the new holiday dates.` and skip to step 8.

7. **Redistribute** -- if the user answers yes:

   a. Invoke `holiday-cascade.py` once, passing the exact date list already parsed in step 1 ("Parse dates to ISO strings") as `--new-dates`:
      ```bash
      python3 .cowork/scripts/holiday-cascade.py \
        --state .cowork/progress/grammar-state.json \
        --rules .cowork/progress/load-control-rules.json \
        --new-dates <comma-separated ISO dates parsed in step 1>
      ```
      This runs a single-pass FIFO sweep starting from the earliest of the newly added dates: it walks forward day by day, queueing displaced content and reassigning it to the next unblocked day (skipping Saturdays and any holiday, old or new), with no `DAILY_CAP`/`WEAK_CAP` and no per-date looping. Only `next_review` is ever changed on an existing entry. See the script's own docstring for the full algorithm.

   b. **Verification** -- after the invocation completes, read `grammar-state.json` one final time. Check every entry: if any topic has `next_review` matching any date in the full holidays list (not just the newly added dates), print:
   ```
   Warning: N topic(s) still scheduled on holiday dates after redistribution -- manual review may be needed:
     <grammar_header> -- next_review: <date>
   ```
   If no topics remain on holiday dates, print nothing (silent success).

   If the user answers no: print `Leaving reviews in place -- they will appear as overdue on those dates.` and skip verification.

8. **Confirm** -- print `Added N holiday(s). M topic(s) redistributed.` (M = 0 if no collisions or user declined redistribution).

---

### 3. Remove holidays

User provides one or more dates to remove.

#### Steps

1. **Parse dates** -- same parsing rules as Add (ISO or natural language).

2. **Read holidays.json** -- if missing, print `No holidays file found -- nothing to remove.` and stop.

3. **Remove matching dates** -- for each date:
   - If found in the array: remove it.
   - If not found: print `<date> is not in the holiday list -- skipping.`

4. **Write updated holidays.json** -- sorted, deduplicated.

5. **Inform user** -- print `Removed N holiday(s). Existing review dates are unchanged.` Removing a holiday does NOT retroactively move topics back to that date. Reviews stay where they are.

---

### 4. Full .ics export

Generate a single `.ics` file containing ALL future scheduled review events from `grammar-state.json`, plus holiday events.

#### Steps

1. **Read grammar-state.json**. If missing, treat as empty (no review events).

2. **Filter reviews** -- keep entries where `next_review >= today` (ISO string comparison). Exclude entries where `next_review < today` (overdue topics are not shown as future calendar events -- they will be picked up by the next practice session).

3. **Group by date** -- group remaining entries by `next_review` date.

4. **Generate review VEVENTs** -- one VEVENT per date:
   - `SUMMARY: Japanese Grammar Review — N point(s)`
   - `DESCRIPTION:` newline-separated list of `grammar_header` values for that date (joined with `\\n` in the ICS DESCRIPTION field).
   - `DTSTART;VALUE=DATE:YYYYMMDD` / `DTEND;VALUE=DATE:YYYYMMDD+1` (all-day events, no time zone).
   - `UID: <YYYYMMDD>-full-export-<8-char-uuid>@japanese-notes`

5. **Generate holiday VEVENTs** -- read `.cowork/progress/holidays.json`. For each holiday date >= today:
   - `SUMMARY: Holiday — No Review`
   - `DESCRIPTION: Holiday — no grammar reviews scheduled.`
   - `DTSTART;VALUE=DATE:YYYYMMDD` / `DTEND;VALUE=DATE:YYYYMMDD+1` (all-day event).
   - `UID: <YYYYMMDD>-holiday-<8-char-uuid>@japanese-notes`

6. **Write .ics file** -- write to vault root: `japanese-grammar-full-calendar-<YYYYMMDDTHHMMSS>.ics`

   Run the following shell command (`VAULT_ROOT`, `SESSION_TS`, and `TODAY_ISO` are substituted by Claude at runtime). Use `datetime.now().strftime("%Y%m%dT%H%M%S")` for `SESSION_TS`:

   ```bash
   python3 .cowork/scripts/ics-export.py \
     --mode full \
     --state .cowork/progress/grammar-state.json \
     --holidays .cowork/progress/holidays.json \
     --output "<VAULT_ROOT>/japanese-grammar-full-calendar-<SESSION_TS>.ics" \
     --today <TODAY_ISO>
   ```

   The script prints a summary to stdout (e.g. `Written N event(s) to <path>`) — use it in the report.

7. **Report** -- print the script's stdout output to the user.

---

## Never touch

- Lesson files under `JPLessons/` (read-only -- never write)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- Do not run `git push` or any remote git operation
- Do not modify other skill files or `.cowork/instructions.md`
