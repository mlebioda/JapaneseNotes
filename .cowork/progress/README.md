# Progress — grammar practice state

This folder tracks spaced-repetition state for grammar practice. Written by
`practice-grammar` and read by `repeat-grammar` (future skill).

## Files

- `grammar-state.json` — single source of truth for which grammar points are
  tracked, their current ease/interval, and when each is next due. Machine-only.
- `sessions/YYYY-MM-DD-<lesson-code>.md` — human-readable session logs. One file
  per practice session. Includes score table and full exercise transcript.

## Contract for grammar-state.json

```
{
  "grammar_points": {
    "<lesson-code>::<slug>": {
      "lesson_file":     "<relative path to lesson>",
      "grammar_header":  "<original Japanese heading>",
      "last_reviewed":   "YYYY-MM-DD",
      "next_review":     "YYYY-MM-DD",
      "interval_days":   <int>,
      "ease":            <float, default 2.5, floor 1.3>,
      "streak":          <int>,
      "total_reviews":   <int>,
      "last_score":      <1..4>,
      "weak_points":     [<short category strings>]
    }
  }
}
```

## SM-2 lite update rules

| Score | interval_days                                | ease                 | streak |
|-------|----------------------------------------------|----------------------|--------|
| 1     | reset to 1                                   | ease - 0.2 (min 1.3) | 0      |
| 2     | max(1, round(interval * 1.2))                | ease - 0.15 (min 1.3)| +1     |
| 3     | max(1, round(interval * ease))               | unchanged            | +1     |
| 4     | max(1, round(interval * ease * 1.3))         | ease + 0.15          | +1     |

First-ever review: force interval_days = 1 unless score is 1.

`next_review = last_reviewed + interval_days`

## repeat-grammar reads this folder to decide what's due

A future `repeat-grammar` skill will:
1. Load `grammar-state.json`
2. Filter entries where `next_review <= today`
3. Sort by: most overdue first, tie-broken by lowest ease
4. For each due entry, open `lesson_file`, pull the grammar point + Summary vocab
5. Generate exercises (biased toward `weak_points`)
6. Write updates back into this same state file + new session log

That's the whole contract between the two skills.
