# Practice-Grammar SRS Load Control

## Goal
Prevent review pile-ups by adding date-placement logic after SM-2 computes review dates. Only applies to TODAY/OVERDUE scope sessions. Lesson-file triggers are unchanged.

## Approach
Extract load control into a standalone Python script (`.cowork/scripts/load-control.py`) with tests (`.cowork/scripts/test_load_control.py`). The skill computes SM-2 fields as before, then calls the script to place dates and write JSON.

**Separation of concerns:**
- **Skill** (practice-grammar.md): collects evaluations, computes SM-2 fields (interval, ease, streak, etc.)
- **Script** (load-control.py): receives all computed fields, applies load control rules, writes grammar-state.json (sole writer)

Structure as importable module: placement logic in functions, `main()` entry point. Tests import functions directly.

## Constants

| Constant | Value | Meaning |
|---|---|---|
| DAILY_CAP | 10 | Max topics on any single day |
| WEAK_CAP | 4 | Max topics with evaluation score 1 or 2 on any single day |
| BLOCKED_DAY | Saturday (weekday 5) | No reviews placed on Saturdays |
| SEARCH_WINDOW | 30 | Max days to search forward before fallback |

## Script interface

**Input:** JSON array on stdin — each element is a fully computed topic update from the current session. The script is the sole writer — it receives all fields and merges them into grammar-state.json:
```json
[
  {
    "key": "UN4GL5::tara-verb",
    "lesson_file": "JPLessons/Udemy/N4/Grammar/UN4GL5.md",
    "grammar_header": "たら (Vた form)",
    "last_reviewed": "2026-06-18",
    "score": 2,
    "interval_days": 5,
    "ease": 2.35,
    "streak": 4,
    "total_reviews": 5,
    "weak_points": ["..."]
  }
]
```

**Arguments:**
- `--state PATH` — path to grammar-state.json (default: `.cowork/progress/grammar-state.json`)
- `--today DATE` — override today's date for testing (default: actual today, ISO format)

**Output:** Writes updated grammar-state.json. Prints placement summary to stdout:
```
UN4GL5::tara-verb: 2026-06-25 (shifted from 2026-06-24, Saturday)
UN4GL5::tsumori-neg: 2026-06-25 (no shift)
```

**Exit codes:** 0 = success, 1 = error. Errors printed to stderr. Missing grammar-state.json → create with `{"grammar_points": {}}`.

**Algorithm (pseudocode):**
```
1. Read grammar-state.json, build day_counts from next_review dates >= today
   day_counts = { date: { total: N, weak: N } }

2. Sort input topics by score: 1 → 2 → 3 → 4

3. For each topic:
   a. candidate = max(today + 1, today + interval_days)
   b. is_weak = score in [1, 2]
   c. Search from candidate forward (up to SEARCH_WINDOW days):
      - Skip Saturdays
      - Skip if day_total >= DAILY_CAP
      - Skip if is_weak and day_weak >= WEAK_CAP
   d. Fallback: earliest non-Saturday day with lowest total in window
   e. Set next_review = candidate (interval_days stays unchanged — preserves SM-2 base)
   f. Update day_counts in memory

4. Merge all fields into grammar-state.json and write:
   - For each input topic: overwrite its entry with all provided fields + computed next_review
   - Entries not in session input remain unchanged
```

## Steps

### 1. Create `.cowork/scripts/load-control.py`
The script implementing the algorithm above. Pure Python, no external dependencies. Importable module structure: placement logic in functions, `main()` entry point.

### 2. Create `.cowork/scripts/test_load_control.py`
Tests importing functions directly from load-control.py. Test cases:

- **Basic placement**: topic lands on a day with room → no shift
- **Saturday skip**: raw date is Saturday → shifted to next valid day
- **Daily cap**: day has 10 topics → shifted forward
- **Weak cap**: day has 4 weak topics (score 1 or 2), new weak topic → shifted forward
- **Weak cap not applied to strong**: day has 4 weak topics, score-3 topic → placed (total < 10)
- **Priority ordering**: score-1 topics placed before score-3 → weak slots filled first
- **Fallback**: all days in 30-day window are full → picks earliest least-loaded non-Saturday
- **interval_days preserved**: shifted topic keeps original SM-2 interval_days, only next_review changes
- **Multiple topics same session**: second topic sees first topic's placement
- **Saturday + full Sunday**: raw date Saturday, Sunday also full → searches further
- **Existing JSON preserved**: topics not in session input remain unchanged in JSON
- **Minimum candidate date**: interval_days=0 → candidate becomes today+1, never today
- **Count includes today**: topics already on today in JSON are counted correctly
- **Error handling**: malformed input → exit 1, missing state file → creates empty

### 3. Update `## Persistence` section in `.cowork/skills/practice-grammar.md`
- Add constants table immediately after the `## Persistence` heading
- Add `## Load control` subsection after the SM-2 table and `next_review` computation
- Content: "For TODAY/OVERDUE scope only — after computing SM-2 fields for all session topics, pipe them as JSON to `.cowork/scripts/load-control.py`. The script applies date placement rules and writes grammar-state.json."
- Remove or simplify the existing JSON write instructions for TODAY/OVERDUE scope (the script handles it now)

### 4. Verify calendar sync is unaffected
The .ics generation reads `next_review` after the JSON write — no changes needed. Confirm during implementation.

## Risks
- **First-review override**: existing "force interval_days=4 on first review" runs before the script. The script may shift the date further. This is correct behavior — interval_days stays at 4 (SM-2 base preserved), only next_review moves.
- **Existing pile-ups**: old dates in grammar-state.json are not retroactively rebalanced. They thin out naturally as topics are reviewed.
