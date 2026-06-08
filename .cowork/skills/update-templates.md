---
name: update-templates
description: >
  Audits and repairs already-filled Anki card templates in a lesson file's
  # Summary section. Normalizes field names, fills missing forms, verifies
  conjugation correctness, fixes kanji links, and repositions <!--ID:--> lines —
  all without modifying anything above # Summary or changing any ID value.
---

# Skill: update-templates

## Trigger phrases

- "update templates [file/lesson]"
- "repair templates [file/lesson]"
- "fix templates [file/lesson]"

---

## References

This skill defers to:
- `.cowork/skills/references/card-templates.md` — canonical block structures and label alias table
- `.cowork/skills/references/verb-conjugation.md` — verb type detection and all 13 conjugation form rules
- `.cowork/skills/references/adj-forms.md` — adjective form derivation rules
- `.cowork/skills/references/kanji-links.md` — kanji link generation procedure

Load all four reference files before starting any repair work.

---

## Workflow

### Step 1 — Locate and scope the file

1. Find the lesson file by lesson number or path (same lookup logic as fill-templates).
2. Read the full file.
3. Find the `# Summary` line. Everything below it is the **working zone**; everything above (including the `# Summary` line itself and `TARGET DECK`) is **off-limits**.
4. If no `# Summary` line exists, stop and report: "This file has not been filled yet — run fill-templates first."

---

### Step 2 — Parse the Summary section into card blocks

Split the working zone into individual card blocks. Rules:

- A block starts with a line ending in `#card` (the translation/Polish line).
- A block ends just before the next blank-line separator.
- The `<!--ID: ...-->` line (if present) belongs to the block it immediately precedes the blank separator for.
- Blank lines between blocks are separators — not part of any block.

Canonical block structure:
```
<translation line>              ← line 1: ends with #card
<japanese / ほんやく: line>     ← line 2
[form lines...]                 ← lines 3–N (wc/wp only)
[<a href=...> lines...]         ← kanji links (all card types)
<!--ID: ...-->                  ← ID anchor (may be misplaced — repair later)
```

---

### Step 3 — Run repair checks for each block

Process each block in order. Apply repairs 1 through 7 in sequence.

---

#### Repair 1 — Field name normalization

For every field line in the block, compare its label to:
1. The alias table in `references/card-templates.md`.
2. If no alias match: positional matching (line N in the block → field N in the canonical template for this card type).

Rules:
- If a label matches a known alias, replace the label with the canonical form. Preserve the value after the colon verbatim (including leading space).
- If a label matches by position but not by name, and the intent is unambiguous, apply the rename and record it in the repair summary.
- Before applying positional renames, verify the block's total field count matches the canonical template count. If counts differ, fall back to name-only matching and flag unmatched lines for user review.
- If a label is unrecognized by both alias and position, do not rename it. Flag it in the post-run report.
- Applies to all card types. For `#w` there are no form lines; the only label potentially in scope is an erroneous `ほんやく:` prefix.

---

#### Repair 2 — Identify card type

Determine card type from the (now-normalized) block:

| Condition | Card type |
|-----------|-----------|
| Has `ほんやく:` AND has `ます形:` or `て形:` rows | `#wc` verb (non-suru) |
| Has `ほんやく:` AND has `過去形:` row | `#wp` adjective |
| Has `ほんやく:` only (no form rows) | `#wc` suru verb — skip Repairs 3 and 3b |
| No `ほんやく:` line | `#w` noun/expression — skip Repairs 3, 3b, and 4 |

---

#### Repair 3 — Fill missing verb forms (`#wc` non-suru only)

Expected 13 form labels in canonical order (from `references/card-templates.md`):
`ます形`, `て形`, `た形`, `ない形`, `なかった形`, `ば形 (if)`, `可能形 (can)`, `られる形 (is done by)`, `出す形 (start)`, `尊敬語 (honorific)`, `お〜になる (honorific)`, `そう (looks like)`, `おう (let's)`

For each expected label:
- If the label line is present but its value is blank (e.g. `た形: `), compute the value and fill it.
- If the label line is absent entirely, insert it in the correct canonical position with the computed value.

To compute forms: read the `ほんやく:` value, strip furigana, determine verb type using the heuristic in `references/verb-conjugation.md`. Apply the godan table or ichidan rules as appropriate. For 来る use the fixed form table.

If verb type is uncertain after applying the heuristic, web-search `[verb] godan ichidan` before filling.

---

#### Repair 3b — Verify conjugation correctness (`#wc` non-suru only)

After Repair 3 ensures all form lines exist, recompute every conjugation from scratch and compare.

Steps:
1. Re-read the `ほんやく:` value (furigana stripped). Confirm verb type (godan / ichidan / kuru / suru — same detection as Repair 3).
2. For each of the 13 form labels, compute the expected value using the verb type rules in `references/verb-conjugation.md`.
3. Compare computed value to stored value (character by character).
4. If they differ, overwrite the stored value with the computed one. Record in the repair summary: label + old value → new value.

**Uncertainty rule:** If verb type cannot be determined with confidence (the heuristic is ambiguous and web-search is unavailable or inconclusive), do NOT overwrite any existing values. Instead, flag the entire card for user review with a note: "Uncertain verb type — conjugations not verified."

Skip conditions:
- `#w` cards — no conjugation rows, skip entirely.
- Suru verb cards (`#wc` with no form rows) — skip entirely.
- Fields that were blank and just filled by Repair 3 — already correct, comparison is a no-op.

**Risk note:** An incorrect verb-type classification will replace all 13 forms including any values the user manually corrected. Only apply Repair 3b when verb type is certain.

---

#### Repair 4 — Fill missing adjective forms (`#wp` only)

Expected 4 form labels in canonical order: `過去形`, `否定形`, `副詞形`, `そう`

Same logic as Repair 3: Repair 1 has already normalized labels. Fill blank values; insert missing labels in canonical position. Use rules from `references/adj-forms.md`.

---

#### Repair 6 — Fix kanji links (all card types)

Use the procedure in `references/kanji-links.md`.

Steps:
1. Collect all existing `<a href=...>` lines in the block.
2. Compute expected links from the card's source text:
   - `#wc` / `#wp`: from `ほんやく:` value (furigana stripped)
   - `#w`: from the Japanese field line (second line of block)
3. Compare existing links to expected links (set equality and order).
4. If they differ (wrong kanji, wrong order, missing, or extra): replace the entire link block with the newly computed set.
5. If they match: leave untouched.

---

#### Repair 7 — Reposition `<!--ID:-->` line

The `<!--ID:-->` line must be the **last non-blank line** of the block, placed:
- After the last kanji `<a href>` line (if any links exist)
- After the last form/adjective line (if no links)
- Immediately before the blank separator

If the `<!--ID:-->` line is in any other position:
1. Record the ID value exactly as it appears (never alter the number).
2. Remove the line from its current position.
3. Re-insert it at the canonical position (after last link or last form line).

If no `<!--ID:-->` line exists in the block: leave as-is. The Anki plugin will generate one on next sync.

**Critical invariant:** The ID value (the number inside `<!--ID: 12345-->`) must never change. Only the line's position within the block may change.

---

### Step 4 — Write repairs back

Apply changes using targeted Edit calls — replace only the lines that changed within each block. Prefer block-level Edit calls over full-file rewrites when possible.

After all blocks are processed, output a **repair summary**:
- Total cards checked
- Cards with field name renames (Repair 1): count and list of renames
- Cards with missing forms filled (Repair 3): count
- Cards with incorrect forms corrected (Repair 3b): count, with old → new values
- Cards with missing adjective forms filled (Repair 4): count
- Cards with kanji links fixed (Repair 6): count
- Cards with ID repositioned (Repair 7): count
- Cards flagged for user review: list with reasons

---

## What never to touch

- `TARGET DECK` line at the top of the file
- Everything above `# Summary` (including the `# Summary` heading itself)
- `<!--ID:-->` values — only position may change, never the number inside
- Suru verb cards — Repairs 3 and 3b do not apply
- Cards that already conform — no unnecessary edits
- Do not run `fill_extract.py` — that script aborts if `Rzeczowniki:` is already filled

---

## Verb type ambiguity handling

Apply the heuristic from `references/verb-conjugation.md` in order:
1. Ends in `える`/`いる` → ichidan
2. Ends in other kana + `る` → godan
3. Ends in `く`,`ぐ`,`す`,`つ`,`ぬ`,`ぶ`,`む`,`う` → godan
4. `来る` → kuru
5. `する` or compound `〜する` → suru
6. Known godan exceptions (帰る, 走る, 切る, 知る, 入る, 要る) → godan

If still uncertain after the heuristic, web-search `[verb] godan ichidan`.
If web-search is unavailable or inconclusive, do not overwrite — flag for user review.

---

## Never touch

- Lesson files under `JPLessons/` outside the `# Summary` section (read-only above that boundary)
- `<!--ID: -->` values anywhere
- `TARGET DECK` lines
- Do not run `git push` or any remote git operation
