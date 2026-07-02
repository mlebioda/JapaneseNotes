---
name: practice-grammar-srs
description: >
  Sub-skill for practice-grammar. Handles SM-2 state persistence and .ics calendar
  file generation. Loaded once at session end (or on "stop" early exit).
  Study Mode exercises are excluded — only self-evaluation scores from main batch exercises.
---

# Practice Grammar — Persistence and Calendar Sync

## Context required (passed by practice-grammar.md)

- `session_scores`: dict keyed by grammar_point_id →
    `{min_score, weak_points[], grammar_header, lesson_file, interval_days}`
- `session_grammar_ids`: ordered list of grammar_point_ids practiced this session
- `today`: ISO date (YYYY-MM-DD)
- `scope`: "lesson" | "TODAY" | "OVERDUE"
  - "lesson" → write next_review directly (today + interval_days), skip load-control.py
  - "TODAY" or "OVERDUE" → two-step write: SM-2 fields first, then load-control.py for next_review

---

## Persistence

**Batch sessions:** accumulate all self-scores and weak_points across batches in memory during the session. Write grammar-state.json once — after the last batch completes, or immediately when the user types "stop". Only grammar points with collected self-scores are written; topics in batches never started are not written. Study Mode exercises are excluded from grammar-state.json — only self-evaluation scores from the main session exercises are written.

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

One write at the end of the session: update `.cowork/progress/grammar-state.json`.

Read the file (create with `{"grammar_points": {}}` if missing). For each practiced grammar point:

- If no prior entry: create one with defaults — `interval_days: 1`, `ease: 2.5`, `streak: 0`, `total_reviews: 0`.
- Apply the algorithm based on the score the user gave:

| Score | interval_days update                         | ease update        | streak          |
|-------|----------------------------------------------|--------------------|-----------------|
| 1     | reset to 1                                   | `ease - 0.2` (min 1.3) | reset to 0  |
| 2     | `max(1, round(interval * 1.2))`              | `ease - 0.15` (min 1.3) | +1          |
| 3     | `max(1, round(interval * ease))`             | unchanged          | +1              |
| 4     | `max(1, round(interval * ease * 1.3))`       | `ease + 0.15`      | +1              |

- **Multi-exercise grammar points** — if a grammar point had more than one exercise in the session (multiple use cases), use the **minimum** self-score across all its exercises as the SM-2 input score. Rationale: if the user aced two of three use cases but failed one, they have not mastered the grammar point and should review it sooner. The `weak_points` are the union of all exercises' weak points for that grammar point.
- If it's the first review (streak was 0 before), force `interval_days = 4` regardless of score (score ≥ 2 only; a score-1 first review still resets to 1 per the table).
- Compute `next_review = today + interval_days` (ISO date, YYYY-MM-DD).
- Set `last_reviewed = today`, `last_score`, `total_reviews += 1`.
- Merge weak_points: union with existing `weak_points`, deduped, keep most recent 5.

### Load control (TODAY / OVERDUE scope only)

For TODAY/OVERDUE scope sessions only — after computing SM-2 fields for all session topics, use a two-step write. The skill writes SM-2 fields first, then load-control.py places review dates.

**Step A — Write SM-2 fields directly to grammar-state.json:**

Read `grammar-state.json` (create with `{"grammar_points": {}}` if missing). For each practiced grammar point, update its entry with the computed SM-2 fields: `interval_days`, `ease`, `streak`, `total_reviews`, `weak_points`, `last_reviewed`, `last_score`, `score`. Also write identity fields `lesson_file` and `grammar_header`. Do NOT compute or write `next_review` — that is handled by Step B. Write the file (pretty-printed, 2-space indent).

**Step B — Pipe minimal JSON to load-control.py for date placement:**

Build a minimal JSON array with only the fields load-control.py needs — one element per grammar point in the session:

```json
[
  {
    "key": "<grammar_point_id>",
    "lesson_file": "<lesson_file>",
    "grammar_header": "<grammar_header>",
    "interval_days": "<computed_interval>",
    "score": "<min_score>"
  }
]
```

Always include `lesson_file` and `grammar_header` (identity fields — harmless for existing entries, required safety net for any edge case).

Run:

```bash
echo '<json_array>' | python3 .cowork/scripts/load-control.py \
  --state .cowork/progress/grammar-state.json \
  --rules .cowork/progress/load-control-rules.json \
  --today <today_ISO>
```

The script reads the updated state (SM-2 fields from Step A), computes `next_review` via `place_topics()`, and writes only `next_review` (plus identity fields) via `merge_and_write()`. Step A must complete (file written and closed) before Step B runs, since load-control.py reads the state file.

The script prints a placement summary to stdout. Use the summary in the session output.

For lesson-triggered sessions (not TODAY/OVERDUE): write grammar-state.json directly as before, including `next_review = today + interval_days` — load control does not apply.

Example entry shape:

```json
{
  "grammar_points": {
    "UN5GL14::vnaide-kudasai": {
      "lesson_file": "JPLessons/Udemy/N5/Grammar/UN5GL14.md",
      "grammar_header": "Vないで ください",
      "last_reviewed": "2026-04-21",
      "next_review": "2026-04-24",
      "interval_days": 3,
      "ease": 2.5,
      "streak": 1,
      "total_reviews": 1,
      "last_score": 3,
      "weak_points": []
    }
  }
}
```

Keep JSON pretty-printed with 2-space indent so diffs are readable.

No transcript file is written — the state JSON is the only output of a session.

---

## Calendar sync

**Batch sessions:** write the .ics file once, immediately after grammar-state.json is written — whether the session completed normally or the user typed "stop". Only grammar points with collected self-scores are included.

After every session, write a new timestamped file `japanese-grammar-review-<YYYYMMDDTHHMMSS>.ics` at the vault root. Each session file is self-contained — only the grammar points practiced this session are included. The user imports the new file after each session; old files are left untouched and do not need to be deleted. This is the only file Claude writes outside `.cowork/progress/`.

**Only include grammar points practiced in the current session** — not everything in the JSON.

Rules:
- The set of session grammar point IDs is known at persistence time (the same set just written to JSON).
- Read their new `next_review` dates from the freshly updated JSON.
- Group grammar headers by date — one VEVENT per date, with headers in DESCRIPTION.
- Use `DTSTART;VALUE=DATE:YYYYMMDD` (all-day events, no time zone).
- SUMMARY: `Japanese Grammar Review — N point(s)`.
- DESCRIPTION: newline-separated list of `grammar_header` values due that day.
- PRODID: `-//Japanese Grammar Review//EN`

Run the following shell command (substitute `SESSION_IDS_JSON_ARRAY` with the actual JSON array of grammar point IDs from this session). Use `datetime.now().strftime("%Y%m%dT%H%M%S")` for `SESSION_TS` to avoid same-day filename collisions:

```bash
echo '<SESSION_IDS_JSON_ARRAY>' | python3 .cowork/scripts/ics-export.py \
  --mode session \
  --state .cowork/progress/grammar-state.json \
  --output "<VAULT_ROOT>/japanese-grammar-review-<SESSION_TS>.ics"
```

Note: `--today` is not passed in session mode (it is ignored -- session mode exports all requested keys regardless of date). The script prints a summary to stdout (e.g. `Written N event(s) to <path>`) -- use it in the session output.

After running, print a one-line confirmation: `Calendar updated — N event(s) written to japanese-grammar-review-<timestamp>.ics`.

---

## Never touch

- Lesson files under `JPLessons/` (read-only — never write)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- Do not run `git push` or any remote git operation
