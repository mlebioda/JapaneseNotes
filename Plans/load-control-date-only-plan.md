# Load Control Date-Only Merge Fix

## Goal
Fix `merge_and_write()` in `load-control.py` so it only updates `next_review` for existing grammar-state entries, never overwriting SM-2 fields (interval_days, ease, streak, total_reviews, weak_points, last_score, last_reviewed, score). This eliminates the need for the `manage-holidays` skill to save/restore `interval_days` after redistribution, and enables a cleaner two-step write in `practice-grammar.md` where SM-2 fields are written first and load control only places dates.

## Background
Currently `merge_and_write()` (lines 355-362 in load-control.py) copies ALL fields from the input topic into the grammar-state entry, overwriting whatever was there. This design assumed the script is the sole writer and receives the authoritative field values. In practice, this creates two problems:

1. **manage-holidays redistribution trick** -- sets `interval_days=1` to force a holiday collision, but `merge_and_write` persists that fake value. The skill has to save and restore the original `interval_days` after every redistribution (step 7c in manage-holidays.md).
2. **practice-grammar race** -- the skill computes SM-2 fields and sends them as input, but if anything is lost or stale in transit, `merge_and_write` overwrites the authoritative state.

The fix: for EXISTING entries, `merge_and_write()` only sets `next_review` (and identity fields `lesson_file`/`grammar_header`). For NEW entries (key not in grammar_points), copy all fields from input as a safety net.

## Approach
Three coordinated changes across three files:

1. **load-control.py** -- make `merge_and_write()` conditional: existing entries get only `next_review` + identity fields; new entries get full copy.
2. **practice-grammar.md** -- split the TODAY/OVERDUE scope write into two steps: (A) write SM-2 fields directly to grammar-state.json, (B) pipe minimal JSON to load-control.py for date placement only.
3. **manage-holidays.md** -- remove the save/restore `interval_days` workaround (steps 7b note and 7c), since `merge_and_write` no longer persists the trick value.

## Steps

### 1. Fix `merge_and_write()` in `.cowork/scripts/load-control.py` (lines 349-367)

Current code (lines 355-362):
```python
# Overwrite with all provided fields
for field in (
    "lesson_file", "grammar_header", "last_reviewed", "score",
    "interval_days", "ease", "streak", "total_reviews",
    "weak_points", "last_score",
):
    if field in topic:
        entry[field] = topic[field]
```

Replace with conditional logic:
```python
is_new = key not in grammar_points_original
if is_new:
    # New entry: copy all provided fields (safety net)
    for field in (
        "lesson_file", "grammar_header", "last_reviewed", "score",
        "interval_days", "ease", "streak", "total_reviews",
        "weak_points", "last_score",
    ):
        if field in topic:
            entry[field] = topic[field]
else:
    # Existing entry: only update identity fields
    for field in ("lesson_file", "grammar_header"):
        if field in topic:
            entry[field] = topic[field]
```

Implementation notes:
- The function needs to know which keys existed BEFORE the loop started. Either snapshot `grammar_points.keys()` before the loop, or pass a reference set. Simplest: capture `original_keys = set(grammar_points.keys())` at the top of the function, then use `key not in original_keys`.
- `place_topics()` still reads `interval_days` and `score` from input for placement calculation -- this is unchanged. The fix only affects what gets persisted.
- `entry["next_review"] = placed_date.isoformat()` line stays as-is (line 365).

### 2. Verify existing tests still pass

The 43 existing tests that call `merge_and_write` use keys that are NEW (not pre-existing in `grammar_points`), so they hit the full-copy path. They should all pass without changes.

The 2 new failing tests (`TestMergeWriteOnlyChangesDate`) use keys that ARE pre-existing in `grammar_points`, so they test the date-only path. They should pass after the fix.

Run: `python3 -m pytest test_load_control.py -v` from `.cowork/scripts/`.

### 3. Update practice-grammar.md -- two-step write for TODAY/OVERDUE scope

File: `.cowork/skills/practice-grammar.md`, section "### Load control (TODAY / OVERDUE scope only)" (lines 585-618).

Replace the current single-pipe approach with a two-step write:

**Step A -- Write SM-2 fields directly to grammar-state.json:**
After computing SM-2 fields for all session topics, read `grammar-state.json`, update each practiced entry's SM-2 fields (interval_days, ease, streak, total_reviews, weak_points, last_reviewed, last_score, score), and write the file. Do NOT compute or write `next_review`.

**Step B -- Pipe minimal JSON to load-control.py for date placement:**
Build a minimal JSON array with only the fields load-control.py needs for placement:
```json
[
  {
    "key": "<grammar_point_id>",
    "interval_days": "<computed_interval>",
    "score": "<min_score>"
  }
]
```
Run load-control.py as before. The script reads the updated state (which now has the correct SM-2 fields from Step A), computes `next_review` via `place_topics()`, and writes only `next_review` (plus identity fields) via `merge_and_write()`.

This means `lesson_file` and `grammar_header` can be omitted from the Step B input -- they are already in the state file from Step A. However, including them is harmless (identity fields are always copied for existing entries).

Also update the JSON example block and the explanatory text to reflect the two-step approach.

For lesson-triggered sessions: behavior is unchanged -- the skill writes everything directly including `next_review`.

### 4. Simplify manage-holidays.md redistribution (steps 7b-7c)

File: `.cowork/skills/manage-holidays.md`

**In step 7b (line ~107):** Remove the note about saving original `interval_days`:
- Delete: `**Save each topic's original `interval_days` before building this array** -- it will be restored in step 7c after redistribution.`
- The note about setting `interval_days` to `1` and the rationale for why stays (it's still correct for placement calculation).

**Remove step 7c entirely** (lines 119-119, "Restore original interval_days"):
- This step is no longer needed because `merge_and_write()` will not persist `interval_days` from input for existing entries.
- Delete the entire paragraph starting with `c. **Restore original \`interval_days\`**` through the end of that step.

**Renumber:** Current step 7d (Verification) becomes step 7c. Update the reference in step 6 ("skip to step 8") if needed -- actually step 6 says "skip to step 8" which refers to the Confirm step, so that reference stays valid.

### 5. Verify no other callers are affected

Confirm that no other code depends on `merge_and_write()` copying SM-2 fields from input for existing entries. Known callers:
- `practice-grammar.md` -- updated in step 3
- `manage-holidays.md` -- simplified in step 4
- `test_load_control.py` -- verified in step 2

## Risks
- **New entry path correctness** -- if a grammar point is genuinely new (first time appearing in grammar-state.json), the full-copy path must fire. This is the case for lesson-triggered sessions that add new grammar points via load-control. Verify via existing tests that create new entries.
- **Step A/B ordering in practice-grammar** -- Step A must complete (file written and closed) before Step B runs, since load-control.py reads the state file. The skill must not interleave these writes.
- **manage-holidays redistribution still works** -- `interval_days=1` trick still works for `place_topics()` (which reads from input, not state). The only change is that `merge_and_write()` no longer persists the trick value, which is the desired behavior.
