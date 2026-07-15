# Add 命令形 (Imperative Form) to #wc Verb Card Template

## Goal
The `#wc` (verb) Anki card template currently has 14 conjugation form rows (て形 through おう形, including the recently-added 使役形) but is missing the imperative form (命令形 — blunt command form, e.g. "eat!", "go!"). This plan adds 命令形 as a 15th canonical form, positioned at the very end of the form list — after おう形 (let's) and before the `<a href>` mnemonic link line — labeled `命令形 (imperative)` to match the existing `形 (gloss)` naming convention. This is a reference-data and template change only — it does not touch any lesson files or run any backfill against existing cards.

## Approach
Same four shared reference files as the 使役形 change: `card-templates.md` (canonical block + alias table), `verb-conjugation.md` (conjugation rules), `label-aliases.json` (label normalization), and `fill_extract.py` (skeleton field list). Plus the worked example embedded in `fill-templates.md` and the "N form labels" counts in `templates-update.md`. All six files currently enumerate the same 14 forms in the same order, so 命令形 must be appended at the end of each to keep `fill-templates`, `templates-update`, and the extraction script consistent.

Conjugation rules (confirmed with user):
- **Godan**: drop the final u-row kana, replace with the e-row kana directly — no suffix added (same e-row kana already tabulated as the first character of the existing 可能形/ば形 columns, just without the trailing る/ば). E.g. 書く→書け, 飲む→飲め, 話す→話せ, 買う→買え, 渡る→渡れ, 走る→走れ.
- **Ichidan**: drop る, add ろ (canonical colloquial form; よ is the literary/classical alternative and is not used here — same single-canonical-form approach used for 使役形).
  E.g. 食べる→食べろ, 見る→見ろ.
- **する** → しろ. **来る** → 来い（こい）.

Worked example (食べる, mirrors the causative plan's worked example):
```
おう形 (let's): 食べよう
命令形 (imperative): 食べろ
```

## Steps

1. **`.cowork/skills/fill_extract.py`** (`#wc` skeleton block list, currently ends with `"おう形 (let's): "` at line 119) — append `"命令形 (imperative): "` as the new last line of the list. This makes the script write the blank 命令形 row for every newly generated `#wc` skeleton.

2. **`.cowork/skills/references/card-templates.md`** — in the "Canonical #wc (verb) template" code block, insert `命令形 (imperative): [value]` between `おう形 (let's): [value]` and the `<a href="...">` line. Update the note "The 14 form lines appear in the exact order above." → "The 15 form lines appear in the exact order above."

3. **`.cowork/skills/references/verb-conjugation.md`**:
   - Frontmatter description: "all 14 conjugation forms" → "all 15 conjugation forms".
   - Canonical label list (currently ends `... 可能形 (can), おう形 (let's)`): append `命令形 (imperative)` at the end; "The 14 form labels" → "The 15 form labels".
   - Godan table: add a `命令形` column, values = bare e-row kana (う→え, く→け, ぐ→げ, す→せ, つ→て, ぬ→ね, ぶ→べ, む→め, る→れ). Add a note: "`命令形 (imperative)` = e-row kana alone (same row as 可能形/ば形, no る/ば suffix)."
   - Ichidan table: add a row `命令形 (imperative) | stem + ろ | 食べろ`.
   - Add a new "## 命令形 — special cases" section (mirroring the existing 使役形 section) documenting: Godan rule (e-row substitution), Ichidan rule (stem + ろ), する→しろ, 来る→来い（こい）, with example verbs 書く/飲む/話す/買う for godan and 食べる/見る for ichidan.
   - 来る fixed-forms block: append `命令形 (imperative): 来い（こい）` as the new last line, after the `おう形 (let's): 来よう` line.

4. **`.cowork/skills/references/label-aliases.json`** — add alias entries mapping common variant spellings to the canonical `命令形 (imperative):` label, following the existing style (English + Polish variants), e.g.:
   - `"imperative:": "命令形 (imperative):"`
   - `"命令形:": "命令形 (imperative):"`
   - `"ろ形:": "命令形 (imperative):"`
   - `"命令 (imperative):": "命令形 (imperative):"`
   - `"Forma rozkazująca:": "命令形 (imperative):"`

5. **`.cowork/skills/fill-templates.md`** — in the "Card format reference" section, "#wc — godan / ichidan verb (fully filled)" example block: insert `命令形 (imperative): ...` between `おう形 (let's): ...` and the `<a href="...">` line (matching the new canonical order). No workflow-step changes needed — Step 4 already defers to `verb-conjugation.md` and will pick up the new rule automatically once step 3 is done.

6. **`.cowork/skills/templates-update.md`**:
   - Line ~28 (skill summary of `verb-conjugation.md`): "all 14 conjugation form rules" → "all 15 conjugation form rules".
   - Line ~131–132 (Repair 3 expected labels): append `命令形 (imperative)` at the end of the list (after `おう形 (let's)`); "Expected 14 form labels" → "Expected 15 form labels".
   - Line ~150 (Repair 3b): "For each of the 14 form labels" → "For each of the 15 form labels".
   - Line ~161 (risk note): "replace all 14 forms" → "replace all 15 forms".

## Risks
- `card-templates.md`, `verb-conjugation.md`, `label-aliases.json`, `fill_extract.py`, `fill-templates.md`, and `templates-update.md` must all stay in sync on field order and naming — a partial edit would cause `fill-templates` and `templates-update` to disagree on the canonical block shape. All six files are included in this plan's steps for that reason.
- This plan does **not** touch any existing lesson files under `JPLessons/`. Existing `#wc` cards filled before this change will not have a 命令形 row. Running `templates-update` on those files afterward will treat the missing row as Repair 3 (fill missing forms) and add it — expected behavior of the existing skill, not something this plan needs to implement, but the user should be aware already-filled lessons will need a `templates-update` pass to backfill 命令形 if desired.
- No `<!--ID: -->` lines, `TARGET DECK` lines, or `# Summary` separators are touched by this plan — all edits are confined to `.cowork/skills/` reference and script files.
- Because 命令形 is appended at the very end (not inserted mid-list like 使役形 was), the diff surface per file is smaller — no downstream line shifts to re-verify beyond the last row and the `<a href>` boundary.
