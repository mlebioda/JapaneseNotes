---
name: templates-update
description: >
  Audits and repairs already-filled Anki card templates in a lesson file's
  # Summary section. Mechanical label renames are handled first by
  preprocess-templates.py (alias table, all 34 known variants). Claude then
  performs reasoning-heavy repairs: positional matching for surviving unknown
  labels, filling missing forms, verifying conjugation correctness, fixing kanji
  links, and repositioning <!--ID:--> lines — all without modifying anything
  above # Summary or changing any ID value.
---

# Skill: templates-update

## Trigger phrases

- "templates-update [file/lesson]"
- "update templates [file/lesson]"
- "repair templates [file/lesson]"
- "fix templates [file/lesson]"

---

## References

This skill defers to:
- `.cowork/skills/references/card-templates.md` — canonical block structures and label alias table
- `.cowork/skills/references/verb-conjugation.md` — verb type detection and all 15 conjugation form rules
- `.cowork/skills/references/adj-forms.md` — adjective form derivation rules
- `.cowork/skills/references/kanji-links.md` — kanji link generation procedure

Load all four reference files before starting any repair work.

---

## Workflow

### Step 1 — Locate the file and run preprocessing

1. Find the lesson file by lesson number or path (same lookup logic as fill-templates).
2. Verify `# Summary` exists without reading content:
   ```
   grep -n "^# Summary" <file>
   ```
   If no match, stop and report: "This file has not been filled yet — run fill-templates first."
3. Run the preprocessing script immediately — before reading any card content:
   ```
   python .cowork/scripts/preprocess-templates.py <file>
   ```
   This applies all 34 alias-table renames mechanically (`label-aliases.json`), including `そう:` → `そう (looks):` for both `#wc` and `#wp` cards. The file on disk now has canonical labels for every known variant.
   If the script reports an error, stop and report it to the user. Do not proceed.

---

### Step 2 — Read and parse the Summary section

Read the file **from the `# Summary` line to EOF**. Do not read lines above it — they are off-limits.

Everything below the `# Summary` line is the **working zone**; the `# Summary` line itself is **off-limits**.

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

#### Parsing rules for structural lines

The working zone may contain structural lines that are **not** card content. Do not include them in any block:

| Line | Treatment |
|------|-----------|
| `---` (three dashes alone on a line) | Section separator between block groups. Marks a block boundary but is **not** a card delimiter — skip it, do not include in any block. |
| `Rzeczowniki:` | Legacy section label. Treat as a plain skippable line — **not** a block start. This label may be removed from files in a future cleanup pass. |
| `Czasowniki:` | Section label for verb blocks. Skippable — not a block start. |
| `Przymiotniki:` | Section label for adjective blocks. Skippable — not a block start. |

Block boundaries are determined solely by `#card` lines (block start) and blank lines (block end), regardless of any section labels or `---` separators.

---

### Step 3 — Run repair checks for each block

Process each block in order. Apply repairs 1 through 6 in sequence.

---

#### Repair 1 — Field name normalization

Alias-table renames (all 34 known variants) were already applied by `preprocess-templates.py` in Step 2.5. Any label that survived preprocessing unmodified is either already canonical or is an unknown variant not in `label-aliases.json`.

For every field line in the block, apply positional matching for surviving unrecognized labels:

1. Attempt positional matching: line N in the block → field N in the canonical template for this card type.

Rules:
- If a label matches by position but not by name, and the intent is unambiguous, apply the rename and record it in the repair summary.
- Before applying positional renames, verify the block's total field count matches the canonical template count. If counts differ, fall back to name-only matching and flag unmatched lines for user review.
- If a label is unrecognized by both alias (confirmed already applied) and position, do not rename it. Flag it in the post-run report.
- Applies to all card types. For `#w` there are no form lines; the only label potentially in scope is an erroneous `ほんやく:` prefix.

---

#### Repair 2 — Identify card type

Determine card type from the (now-normalized) block:

| Condition | Card type |
|-----------|-----------|
| Title line contains `#wc` AND block has `ます形:` or `て形:` rows | `#wc` verb (non-suru) |
| Title line contains `#wc` AND no form rows | `#wc` suru verb — skip Repairs 3 and 3b |
| Title line contains `#wp` | `#wp` adjective |
| Title line contains neither `#wc` nor `#wp` | `#w` noun/expression — skip Repairs 3, 3b, 4, and 4b |

Note: `#w` blocks in existing files often carry a `ほんやく:` label on the second line as a legacy fill artifact. This does **not** make them suru verbs — the title marker is the authoritative type signal. Do not strip the `ほんやく:` label from `#w` blocks; the canonical template simply does not require it.

---

#### Repair 3 — Fill missing verb forms (`#wc` non-suru only)

Expected 15 form labels in canonical order (from `references/card-templates.md`):
`て形`, `た形`, `ます形`, `出す形 (start)`, `そう (looks like)`, `お〜になる (honorific)`, `ない形`, `なかった形`, `受身形 (passive)`, `使役形 (make/let)`, `尊敬語 (honorific)`, `ば形 (if)`, `可能形 (can)`, `おう形 (let's)`, `命令形 (imperative)`

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
2. For each of the 15 form labels, compute the expected value using the verb type rules in `references/verb-conjugation.md`.
3. Compare computed value to stored value (character by character).
4. If they differ, overwrite the stored value with the computed one. Record in the repair summary: label + old value → new value.

**Uncertainty rule:** If verb type cannot be determined with confidence (the heuristic is ambiguous and web-search is unavailable or inconclusive), do NOT overwrite any existing values. Instead, flag the entire card for user review with a note: "Uncertain verb type — conjugations not verified."

Skip conditions:
- `#w` cards — no conjugation rows, skip entirely.
- Suru verb cards (`#wc` with no form rows) — skip entirely.
- Fields that were blank and just filled by Repair 3 — already correct, comparison is a no-op.

**Risk note:** An incorrect verb-type classification will replace all 15 forms including any values the user manually corrected. Only apply Repair 3b when verb type is certain.

---

#### Repair 4 — Fill missing adjective forms (`#wp` only)

Expected 4 form labels in canonical order: `過去形`, `否定形`, `副詞形`, `そう (looks like)`

Same logic as Repair 3: Repair 1 has already normalized labels. Fill blank values; insert missing labels in canonical position. Use rules from `references/adj-forms.md`.

---

#### Repair 4b — Verify adjective form correctness (`#wp` only)

After Repair 4 ensures all form lines are present and labeled correctly, recompute every adjective form value from scratch using the rules in `references/adj-forms.md` and compare each computed value to the value currently in the file.

Steps:
1. Re-read the `ほんやく:` value (furigana stripped) and determine adjective type: い-adjective, special-case い-adjective (いい/よい), な-adjective, or non-adjective/adverb (all fields → `—`).
2. For each of the 4 form labels (`過去形`, `否定形`, `副詞形`, `そう (looks like)`), compute the expected value using the adjective type and the appropriate rule in `references/adj-forms.md`.
3. Compare computed value to stored value. If they differ, overwrite the stored value with the computed one.
4. Record each overwritten field in the repair summary (label + old value → new value).

Skip conditions:
- `#w` cards — no adjective rows, skip entirely.
- `#wc` cards — this repair is for `#wp` only, skip entirely.
- Fields that were blank and just filled by Repair 4 — those values were just computed in Repair 4 and are already correct; the comparison will be a no-op for those fields.

**Uncertainty rule:** When adjective type is uncertain (e.g. a word that could be either い or な), do NOT overwrite — flag the card for user review instead.

**Risk note:** Misclassifying a な-adjective as an い-adjective (or vice versa) causes all 4 forms to be overwritten with wrong values. Only apply Repair 4b when adjective type is certain.

---

#### Repair 5 — Fix kanji links (all card types)

Use the procedure in `references/kanji-links.md`.

Steps:
1. Collect all existing `<a href=...>` lines in the block.
2. Determine the source text for link generation (per `references/kanji-links.md`):
   - `#wc` / `#wp`: `ほんやく:` value — strip furigana first
   - `#w`: the Japanese field line (second line of block) — used as-is
3. Call `.cowork/scripts/kanji-links.py` with the (furigana-stripped) source text to generate the expected link lines:
   ```
   python3 .cowork/scripts/kanji-links.py "<source_text>"
   ```
   The script's stdout is the complete expected link block (one `<a href>` line per unique kanji, first-occurrence order).
4. Compare the script's output to the existing `<a href=...>` lines in the block.
5. If they differ (wrong kanji, wrong order, missing, or extra): replace the entire link block with the script's output.
6. If they match: leave untouched.

---

#### Repair 6 — Reposition `<!--ID:-->` line

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


### Step 4 — Write repairs back

Apply changes using targeted Edit calls — replace only the lines that changed within each block. Prefer block-level Edit calls over full-file rewrites when possible.

After all blocks are processed, output a **repair summary**:
- Total cards checked
- Cards with field name renames (Repair 1): count and list of renames
- Cards with missing forms filled (Repair 3): count
- Cards with incorrect forms corrected (Repair 3b): count, with old → new values
- Cards with missing adjective forms filled (Repair 4): count
- Cards with incorrect adjective forms corrected (Repair 4b): count, with old → new values
- Cards with kanji links fixed (Repair 5): count
- Cards with ID repositioned (Repair 6): count
- Cards flagged for user review: list with reasons

---

## What never to touch

- `TARGET DECK` line at the top of the file
- Everything above `# Summary` (including the `# Summary` heading itself) — lesson files under `JPLessons/` are read-only above that boundary
- `<!--ID:-->` values anywhere — only position may change, never the number inside
- Suru verb cards — Repairs 3 and 3b do not apply
- Cards that already conform — no unnecessary edits
- Do not run `fill_extract.py` — that script aborts if `Rzeczowniki:` is already filled
- Do not run `git push` or any remote git operation

---

## Verb type ambiguity handling

Apply the heuristic in `references/verb-conjugation.md` in order.
