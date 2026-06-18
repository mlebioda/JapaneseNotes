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
| `.cowork/progress/grammar-state.json` | SRS state file. Read for collision detection; written by load-control.py during redistribution. |
| `.cowork/progress/load-control-rules.json` | Load control constants and holidays_file path. Passed via `--rules` to every load-control.py invocation. |
| `.cowork/scripts/load-control.py` | Redistribution engine. Invoked to move colliding reviews off holiday dates. |

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

4. **Write updated holidays.json** -- merge new dates into the array, sort chronologically, deduplicate, and write the file. This write happens BEFORE any redistribution so that `load-control.py` sees the updated holidays list when it runs and will not place topics on any of the new holiday dates.

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

   a. Group colliding topics by their `next_review` date.

   b. Process each date group in **chronological order** (earliest holiday first). For each date group:
   
      - Build the input JSON array. For each colliding topic in the group, construct one element:
        ```json
        {
          "key": "<existing key from grammar-state.json>",
          "lesson_file": "<existing lesson_file>",
          "grammar_header": "<existing grammar_header>",
          "interval_days": 1,
          "score": "<existing last_score>"
        }
        ```
        Note: `interval_days` is set to `1` regardless of the topic's actual interval. Combined with `--today` set to one day before the holiday, this makes the algorithm's candidate date land on the holiday, which is now blocked, forcing it to search forward to the next valid day. `merge_and_write()` only updates `next_review` for existing entries, so the real `interval_days` in `grammar-state.json` is never overwritten.

      - Invoke `load-control.py` with `--today` set to the day before this holiday date:
        ```bash
        echo '<json_array>' | python3 .cowork/scripts/load-control.py \
          --state .cowork/progress/grammar-state.json \
          --rules .cowork/progress/load-control-rules.json \
          --today <YYYY-MM-DD of holiday minus 1 day>
        ```

      - Wait for the invocation to complete before processing the next date group. Each invocation writes `grammar-state.json`, so the next invocation sees the previous placements and avoids creating new conflicts.

   c. **Verification** -- after all redistribution invocations complete, read `grammar-state.json` one final time. Check every entry: if any topic has `next_review` matching any date in the full holidays list (not just the newly added dates), print:
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
   - `SUMMARY: Japanese Grammar Review -- N point(s)`
   - `DESCRIPTION:` newline-separated list of `grammar_header` values for that date (joined with `\\n` in the ICS DESCRIPTION field).
   - `DTSTART;VALUE=DATE:YYYYMMDD` / `DTEND;VALUE=DATE:YYYYMMDD+1` (all-day events, no time zone).
   - `UID: <YYYYMMDD>-full-export-<8-char-uuid>@japanese-notes`

5. **Generate holiday VEVENTs** -- read `.cowork/progress/holidays.json`. For each holiday date >= today:
   - `SUMMARY: Holiday -- No Review`
   - `DESCRIPTION: Holiday -- no grammar reviews scheduled.`
   - `DTSTART;VALUE=DATE:YYYYMMDD` / `DTEND;VALUE=DATE:YYYYMMDD+1` (all-day event).
   - `UID: <YYYYMMDD>-holiday-<8-char-uuid>@japanese-notes`

6. **Write .ics file** -- write to vault root: `japanese-grammar-full-calendar-<YYYYMMDDTHHMMSS>.ics`

   Use the following Python code (same `fold()` function as the practice-grammar calendar sync):

   ```python
   import json
   import uuid
   from datetime import date, timedelta
   from collections import defaultdict

   VAULT_ROOT = "/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP"
   json_path = f"{VAULT_ROOT}/.cowork/progress/grammar-state.json"
   holidays_path = f"{VAULT_ROOT}/.cowork/progress/holidays.json"
   session_ts = date.today().strftime("%Y%m%dT%H%M%S")
   ics_path = f"{VAULT_ROOT}/japanese-grammar-full-calendar-{session_ts}.ics"
   today_str = date.today().isoformat()

   # Load grammar state
   try:
       with open(json_path) as f:
           gp = json.load(f).get("grammar_points", {})
   except (FileNotFoundError, json.JSONDecodeError):
       gp = {}

   # Load holidays
   try:
       with open(holidays_path) as f:
           holidays = sorted(json.load(f))
   except (FileNotFoundError, json.JSONDecodeError):
       holidays = []

   # Group future reviews by date
   by_date = defaultdict(list)
   for gid, entry in gp.items():
       nr = entry.get("next_review", "")
       if nr and nr >= today_str:
           by_date[nr].append(entry.get("grammar_header", gid))

   def fold(line: str) -> str:
       """Fold a single ICS content line to max 75 octets per RFC 5545."""
       encoded = line.encode("utf-8")
       if len(encoded) <= 75:
           return line
       out = []
       while len(encoded) > 75:
           chunk = encoded[:75].decode("utf-8", errors="ignore")
           while len(chunk.encode("utf-8")) > 75:
               chunk = chunk[:-1]
           out.append(chunk)
           encoded = b" " + encoded[len(chunk.encode("utf-8")):]
       out.append(encoded.decode("utf-8"))
       return "\r\n".join(out)

   lines = [
       "BEGIN:VCALENDAR",
       "VERSION:2.0",
       "PRODID:-//Japanese Grammar Review//EN",
       "CALSCALE:GREGORIAN",
   ]

   # Review events
   for d in sorted(by_date):
       headers = by_date[d]
       dt_date = date.fromisoformat(d[:10])
       dtstr = dt_date.strftime("%Y%m%d")
       dt_end = (dt_date + timedelta(days=1)).strftime("%Y%m%d")
       lines += [
           "BEGIN:VEVENT",
           f"DTSTART;VALUE=DATE:{dtstr}",
           f"DTEND;VALUE=DATE:{dt_end}",
           f"SUMMARY:Japanese Grammar Review -- {len(headers)} point(s)",
           "DESCRIPTION:" + "\\n".join(headers),
           f"UID:{dtstr}-full-export-{str(uuid.uuid4())[:8]}@japanese-notes",
           "END:VEVENT",
       ]

   # Holiday events
   for h in holidays:
       if h >= today_str:
           dt_date = date.fromisoformat(h)
           dtstr = dt_date.strftime("%Y%m%d")
           dt_end = (dt_date + timedelta(days=1)).strftime("%Y%m%d")
           lines += [
               "BEGIN:VEVENT",
               f"DTSTART;VALUE=DATE:{dtstr}",
               f"DTEND;VALUE=DATE:{dt_end}",
               "SUMMARY:Holiday -- No Review",
               "DESCRIPTION:Holiday -- no grammar reviews scheduled.",
               f"UID:{dtstr}-holiday-{str(uuid.uuid4())[:8]}@japanese-notes",
               "END:VEVENT",
           ]

   lines.append("END:VCALENDAR")

   with open(ics_path, "w", encoding="utf-8") as f:
       f.write("\r\n".join(fold(l) for l in lines) + "\r\n")

   review_count = len(by_date)
   holiday_count = sum(1 for h in holidays if h >= today_str)
   print(f"Full calendar exported: {review_count} review event(s) + {holiday_count} holiday event(s) written to {ics_path}")
   ```

7. **Report** -- print the output from the script: `Full calendar exported: N review event(s) + M holiday event(s) written to <filename>.`

---

## Never touch

- Lesson files under `JPLessons/` (read-only -- never write)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- Do not run `git push` or any remote git operation
- Do not modify other skill files or `.cowork/instructions.md`
