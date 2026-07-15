# Add 使役形 (Causative Form) to #wc Verb Card Template

## Goal
The `#wc` (verb) Anki card template currently has 13 conjugation form rows (て形 through おう形) but is missing the causative form (使役形 — "to make/let someone do something"). This plan adds 使役形 as a 14th canonical form, positioned directly after あれる形 (passive) and before 尊敬語 (honorific), labeled `使役形 (make/let)` to match the existing `形 (gloss)` naming convention. This is a reference-data and template change only — it does not touch any lesson files or run any backfill against existing cards.

## Approach
`fill-templates` and `templates-update` both defer to three shared reference files under `.cowork/skills/references/`: `card-templates.md` (canonical block + alias table), `verb-conjugation.md` (conjugation rules), and `label-aliases.json` (label normalization). `fill_extract.py` independently hardcodes the skeleton field list it writes for new `#wc` cards. All four files — plus the worked example embedded in `fill-templates.md` itself — currently enumerate the same 13 forms in the same order, so 使役形 must be inserted at the same position in each to keep the three skills (`fill-templates`, `templates-update`, the extraction script) consistent. `templates-update.md` also has three textual references to "13 form labels" that must become "14".

Conjugation rules (confirmed):
- **Godan**: stem used for ない形 (う-row exception: わ not あ) + せる. E.g. 書く→書かせる, 飲む→飲ませる, 話す→話させる, 買う→買わせる. (This is the same stem already tabulated in the existing ない形 column, just swapping the ない suffix for せる.)
- **Ichidan**: drop る, add させる. E.g. 食べる→食べさせる, 見る→見させる.
- **する** → させる. **来る** → 来させる(こさせる).

Worked example (飲む, approved by user):
```
あれる形 (passive/honorific): 飲まれる
使役形 (make/let): 飲ませる
尊敬語 (honorific): 召し上がる
```

## Steps

1. **`.cowork/skills/fill_extract.py`** (around lines 103–119) — in the `#wc` skeleton block list, insert `"使役形 (make/let): "` immediately after `"あれる形 (passive/honorific): "` (line 114) and before `"尊敬語 (honorific): "` (line 115). This makes the script write the blank 使役形 row for every newly generated `#wc` skeleton.

2. **`.cowork/skills/references/card-templates.md`** — in the "Canonical #wc (verb) template" code block, insert `使役形 (make/let): [value]` between `あれる形 (passive/honorific):  [value]` and `尊敬語 (honorific): [value]`. Update the note "The 13 form lines appear in the exact order above." → "The 14 form lines appear in the exact order above."

3. **`.cowork/skills/references/verb-conjugation.md`**:
   - Frontmatter description: "all 13 conjugation forms" → "all 14 conjugation forms".
   - Line 33 canonical label list: insert `使役形 (make/let)` between `受身形 (passive)` and `尊敬語 (honorific)`; "The 13 form labels" → "The 14 form labels".
   - Godan table (the ending-kana table): add a `使役形` column, derived as the same stem as the `ない形` column with せる instead of ない (う→わせる, く→かせる, ぐ→がせる, す→させる, つ→たせる, ぬ→なせる, ぶ→ばせる, む→ませる, る→らせる). Add a note: "`使役形 (make/let)` = ない形 stem (あ/わ row) + せる."
   - Ichidan table: add a row `使役形 (make/let) | stem + させる | 食べさせる`.
   - Add a new "## 使役形 — special cases" section (mirroring the existing 可能形 section) documenting: Godan rule + う-ending exception, Ichidan rule, する→させる, 来る→来させる(こさせる), with the four example verbs from the conversation (書く, 飲む, 話す, 買う) plus 食べる/見る for ichidan.
   - 来る fixed-forms block: insert `使役形 (make/let): 来させる（こさせる）` between the `あれる形 (passive)` line and the `尊敬語 (honorific)` line.

4. **`.cowork/skills/references/label-aliases.json`** — add alias entries mapping common variant spellings to the canonical `使役形 (make/let):` label, following the existing style (English + Polish variants), e.g.:
   - `"causative:": "使役形 (make/let):"`
   - `"使役形:": "使役形 (make/let):"`
   - `"せる形:": "使役形 (make/let):"`
   - `"させる形:": "使役形 (make/let):"`
   - `"Forma sprawcza:": "使役形 (make/let):"`

5. **`.cowork/skills/fill-templates.md`** — in the "Card format reference" section, "#wc — godan / ichidan verb (fully filled)" example block: insert `使役形 (make/let): ...` between `あれる形形 (passive): ...` and `尊敬語 (honorific): ...` (matching the new canonical order). No workflow-step changes are needed — Step 4 ("fill all blank fields... using the verb type heuristic in the reference file") already defers to `verb-conjugation.md`, so it will pick up the new rule automatically once step 3 is done.

6. **`.cowork/skills/templates-update.md`**:
   - Line 28 (skill summary of `verb-conjugation.md`): "all 13 conjugation form rules" → "all 14 conjugation form rules".
   - Line 131–132 (Repair 3 expected labels): insert `使役形 (make/let)` between `受身形 (passive)` and `尊敬語 (honorific)` in the list; "Expected 13 form labels" → "Expected 14 form labels".
   - Line 150 (Repair 3b): "For each of the 13 form labels" → "For each of the 14 form labels".
   - Line 161 (risk note): "replace all 13 forms" → "replace all 14 forms".

## Risks
- `card-templates.md`, `verb-conjugation.md`, `label-aliases.json`, `fill_extract.py`, `fill-templates.md`, and `templates-update.md` must all stay in sync on field order and naming — a partial edit (e.g. updating the script but not the reference doc) would cause `fill-templates` and `templates-update` to disagree on the canonical block shape. All six files are included in this plan's steps for that reason.
- This plan does **not** touch any existing lesson files under `JPLessons/`. Existing `#wc` cards that were already filled before this change will not have a 使役形 row. Running `templates-update` on those files afterward will treat the missing row as Repair 3 (fill missing forms) and add it — that is expected behavior of the existing skill, not something this plan needs to implement, but the user should be aware that already-filled lessons will need a `templates-update` pass to backfill 使役形 if desired.
- No `<!--ID: -->` lines, `TARGET DECK` lines, or `# Summary` separators are touched by this plan — all edits are confined to `.cowork/skills/` reference and script files.
