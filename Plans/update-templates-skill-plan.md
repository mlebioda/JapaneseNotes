# update-templates Skill

## Goal

Create `.cowork/skills/update-templates.md` — a skill that audits and repairs already-filled Anki card templates in a lesson file's `# Summary` section so they conform to current rules. This covers: normalizing field names to the canonical labels defined in `references/card-templates.md` (e.g. `Tłumaczenie:` → `ほんやく:`, `て-form:` → `て形:`, `negative:` → `ない形:`, `translation:` → `ほんやく:`, and any other variant), filling missing or blank verb/adjective conjugation forms, correcting kanji trainer links (scope: ほんやく: value only), and repairing `<!--ID:-->` placement — all while leaving every ID value and everything above `# Summary` untouched.

Alongside the new skill, shared conjugation/link rules are extracted into a `.cowork/skills/references/` directory so that both `fill-templates.md` and `update-templates.md` reference a single authoritative source rather than duplicating tables.

## Approach

`update-templates` works card-by-card inside the `# Summary` section. For each card block (separated by blank lines) it runs a fixed sequence of repair checks, then rewrites only the lines that changed. `<!--ID:-->` lines are treated as anchors: the repair algorithm detects their current position, moves them to the canonical position (immediately after the last form/link line, before the blank separator), and preserves their value verbatim.

No new Python script is strictly required — Claude applies the repairs directly by reading and writing the file with Edit calls. However, an optional `update_templates.py` helper can scan a file and emit a machine-readable diff of which cards need which repairs, making Claude's job mechanical. The plan covers both approaches and leaves the choice to the implementer.

## Steps

### 1. Create `.cowork/skills/references/` and populate shared rule files

Create the directory `.cowork/skills/references/` (new, does not exist).

**`.cowork/skills/references/verb-conjugation.md`**
Extract from `fill-templates.md`:
- Verb type heuristic (ichidan / godan endings / kuru / suru)
- Godan conjugation table (all ending kanas × all 13 forms)
- Ichidan rules (drop る + suffixes)
- 可能形 special cases
- そう form rules (godan / ichidan / kuru)
- 来る fixed form table
- 尊敬語 and お〜になる derivation rules

**`.cowork/skills/references/adj-forms.md`**
Extract from `fill-templates.md`:
- い-adjective form derivations (過去形, 否定形, 副詞形, そう)
- Special case: いい/よい → よかった / よくない / よく / よさそう
- な-adjective rule (all forms → —, そう = base + そう)
- Non-adjective/adverb rule (all fields → —)

**`.cowork/skills/references/kanji-links.md`**
Extract from `fill-templates.md` (## Kanji trainer links section):
- CJK range definition (U+4E00–U+9FFF only)
- Source text rule: for `#wc`/`#wp` use ほんやく: value only (strip furigana 〇（〇）/ 〇(〇) before collecting kanji); for `#w` use the Japanese field line
- Link format: `<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>`
- Deduplication: per-template, first-occurrence order
- Placement: immediately after last conjugation/adjective row, before blank separator line

**`.cowork/skills/references/card-templates.md`**
New file. Contains a canonical template block for each card type. This is the single source of truth that `update-templates` compares every existing card block against. It defines:
- The exact field label for each line (e.g. `ほんやく:`, `ます形:`, `て形:`, …, `おう (let's):`)
- The exact order of all fields
- Where kanji `<a href>` links appear in the block
- Where `<!--ID:-->` appears

The file should contain three sections:

```
### Canonical #wc (verb) template
[translation] #k #card
ほんやく: [japanese]
ます形: [value]
て形: [value]
た形: [value]
ない形: [value]
なかった形: [value]
ば形 (if): [value]
可能形 (can): [value]
られる形 (is done by): [value]
出す形 (start): [value]
尊敬語 (honorific): [value]
お〜になる (honorific): [value]
そう (looks like): [value]
おう (let's): [value]
<a href="...">kanji</a>
<!--ID: ...-->

### Canonical #wp (adjective) template
[translation] #k #card
ほんやく: [japanese]
過去形: [value]
否定形: [value]
副詞形: [value]
そう: [value]
<a href="...">kanji</a>
<!--ID: ...-->

### Canonical #w (word/expression) template
[translation] #k #card
[japanese]
<a href="...">kanji</a>
<!--ID: ...-->
```

Beside the canonical blocks, the file should also contain a **label alias table** mapping known variant spellings to their canonical label. Examples:

| Variant | Canonical |
|---|---|
| `Tłumaczenie:` | `ほんやく:` |
| `translation:` | `ほんやく:` |
| `ほんやく：` (full-width colon) | `ほんやく:` |
| `て-form:` | `て形:` |
| `ta-form:` | `た形:` |
| `negative:` | `ない形:` |
| `past negative:` | `なかった形:` |
| `conditional:` | `ば形 (if):` |
| `potential:` | `可能形 (can):` |
| `passive:` | `られる形 (is done by):` |
| `inceptive:` | `出す形 (start):` |
| `honorific:` | `尊敬語 (honorific):` |
| `volitional:` | `おう (let's):` |
| `looks like:` | `そう (looks like):` |
| `past:` | `過去形:` |
| `adverb:` | `副詞形:` |

Implementer note: this table is not exhaustive. If a field label in an existing card does not appear in the alias table but its intent can be inferred (e.g. by position or partial name match), add it to the table and apply the rename. When intent is ambiguous, ask the user before renaming.

### 2. Update `fill-templates.md` to reference extracted rules

In `fill-templates.md`:
- Replace the inline godan conjugation table, ichidan rules, 可能形 cases, そう form rules, and 来る fixed forms with a single sentence: "See `.cowork/skills/references/verb-conjugation.md` for all conjugation tables and rules."
- Replace the inline adjective form rules (## Step 5) with: "See `.cowork/skills/references/adj-forms.md` for い/な/non-adj rules."
- Replace the inline ## Kanji trainer links section with: "See `.cowork/skills/references/kanji-links.md` for the kanji link procedure."
- All functional behavior stays unchanged — this is documentation reorganization only.
- Do NOT modify `fill_extract.py`, `TARGET DECK` lines, `<!--ID:-->` lines, or the `# Summary` sections of any lesson file.

### 3. Create `.cowork/skills/update-templates.md`

File: `.cowork/skills/update-templates.md`

#### Trigger phrases
"update templates [file/lesson]", "repair templates [file/lesson]", "fix templates [file/lesson]"

#### Workflow

**3a. Locate and scope the file**
- Find the lesson file by lesson number or path (same lookup as fill-templates).
- Read the file. Identify the `# Summary` line. Everything below it is the working zone; everything above is off-limits.
- If no `# Summary` line exists, stop and report: the file has not been filled yet — run fill-templates first.

**3b. Parse the Summary section into card blocks**
Split the Summary section into individual card blocks. Each block is delimited by one or more blank lines. A block starts with a translation line (ends in `#card`) and ends just before the next blank-line separator. The `<!--ID: ...-->` line, if present, belongs to the block it immediately precedes the separator for.

Block structure (canonical):
```
<translation line>           ← line 1: ends with #card
<japanese / ほんやく: line>  ← line 2
[form lines...]              ← lines 3–N (wc/wp only)
[<a href=...> lines...]      ← kanji links (all card types)
<!--ID: 1780863216819-->

<!--ID: ...-->               ← ID anchor (may be misplaced)
```

Blank line after `<!--ID:-->` is the block separator — not part of the block.

**3c. For each card block, run repair checks in order**

Repair 1 — Field name normalization
For every field line in the block, match its label against the canonical template defined in `references/card-templates.md`. Matching uses the alias table in that file; when no alias entry exists, use positional matching (line N in the block → field N in the canonical template for this card type).

- If a label matches a known alias (e.g. `Tłumaczenie:`, `translation:`, `て-form:`, `negative:`, full-width colon variants, etc.), replace it with the canonical label. Preserve the value after the colon verbatim.
- If a label matches by position but not by name, and the intent is unambiguous, apply the rename and record it in the repair summary.
- If a label is unrecognized and cannot be matched by position or alias, do not rename it — flag it in the post-run report for user review.
- Applies to all card types. For `#wc` and `#wp` this covers ほんやく: and all form lines. For `#w` there are no form lines, so only the ほんやく: label (if somehow present) is in scope.

Repair 2 — Identify card type
Determine card type from the block:
- Has `ほんやく:` line AND has `ます形:` or `て形:` rows → `#wc` verb
- Has `ほんやく:` line AND has `過去形:` row → `#wp` adjective
- Has `ほんやく:` line only (no form rows) → `#wc` suru verb (no conjugation needed)
- Has no `ほんやく:` line → `#w` noun/expression

Repair 3 — Fill missing verb forms (`#wc` non-suru only)
The authoritative field order is defined in the canonical `#wc` template in `references/card-templates.md`. Expected 13 form labels (in order):
`ます形`, `て形`, `た形`, `ない形`, `なかった形`, `ば形 (if)`, `可能形 (can)`, `られる形 (is done by)`, `出す形 (start)`, `尊敬語 (honorific)`, `お〜になる (honorific)`, `そう (looks like)`, `おう (let's)`

Run Repair 1 before Repair 3: by the time Repair 3 executes, all field labels should already have been normalized to canonical names. Repair 3 therefore only needs to check for presence/absence, never for name variants.

For each expected label:
- If the label line is present but its value is blank (e.g. `た形: `), compute and fill the value.
- If the label line is absent entirely, insert it in the correct position with the computed value.

To compute forms: read the ほんやく: value, strip furigana, determine verb type using the heuristic in `references/verb-conjugation.md`. If uncertain, web-search `[verb] godan ichidan`.

Repair 3b — Verify conjugation correctness (`#wc` non-suru only)
After Repair 3 ensures all form lines are present and labeled correctly, recompute every conjugation value from scratch using the rules in `references/verb-conjugation.md` and compare each computed value to the value currently in the file.

Steps:
1. Re-read the ほんやく: value (already stripped of furigana for Repair 3), and confirm verb type (godan / ichidan / kuru / suru — same detection used in Repair 3).
2. For each of the 13 form labels, compute the expected value using the verb type and the appropriate table in `references/verb-conjugation.md`.
3. Compare computed value to stored value. If they differ, overwrite the stored value with the computed one.
4. Record each overwritten field in the repair summary (label + old value → new value).

Skip conditions:
- `#w` cards — no conjugation rows, skip entirely.
- Suru verb cards (`#wc` with no form rows) — skip entirely.
- Cards where Repair 3 already filled a field from blank — those values were just computed in Repair 3, so they are already correct; the comparison for those fields will be a no-op (stored == computed). No special handling needed.

Purpose: catches partial manual fills or older-script output where the verb type or stem was wrong (e.g. `た形: 通た` → `通った`, `ない形: 通ない` → `通わない`, `可能形 (can): 通れ` → `通える`).

Repair 4 — Fill missing adjective forms (`#wp` only)
The authoritative field order is defined in the canonical `#wp` template in `references/card-templates.md`. Expected 4 form labels (in order): `過去形`, `否定形`, `副詞形`, `そう`

Same logic as Repair 3: Repair 1 runs first, so labels are already normalized. Fill blank values, insert missing labels in canonical order. Rules for computing values in `references/adj-forms.md`.

Repair 6 — Fix kanji links
Compute the correct set of kanji links for this card using the procedure in `references/kanji-links.md`.

Steps:
1. Collect any existing `<a href=...>` lines in the block.
2. Compute expected links from the card's source text (ほんやく: value for wc/wp; Japanese field line for w).
3. If existing links differ from expected (wrong kanji, wrong order, missing, or extra): replace the entire link block with the newly computed set.
4. If existing links match expected: leave untouched.

Repair 7 — Reposition `<!--ID:-->` line
The `<!--ID:-->` line must appear as the last non-blank line of the block, after all form lines and kanji links, immediately before the blank separator.

If the `<!--ID:-->` line is in any other position (e.g. between form lines, before links):
1. Remove it from its current position.
2. Append it after the last kanji link line (or after the last form line if no links).
3. Preserve the ID value exactly — never alter the number inside.

If no `<!--ID:-->` line exists in the block: leave as-is (the Anki plugin will generate one on next sync).

**3d. Write repairs back**
Use Edit calls to apply changes. Prefer targeted Edit calls (replace the minimal changed block) over full-file rewrites.

After all cards are processed, report a summary: how many cards were checked, how many had each repair type applied.

**3e. What never to touch**
- TARGET DECK line
- Everything above `# Summary`
- The `# Summary` line itself
- `<!--ID:-->` values (only position may change)
- Suru verb cards (no conjugation rows — repair 3 does not apply)
- Cards that already conform — no unnecessary edits

#### Verb type ambiguity handling
Same rule as fill-templates: ends in `える`/`いる` → ichidan; ends in other kana + `る` → godan; known exceptions (帰る, 走る, 切る, 知る, 入る, 要る) → godan. If still uncertain, web-search `[verb] godan ichidan` before filling.

### 4. Optional helper script: `update_templates.py`

If the implementer judges that a helper script would reduce error risk (especially for ID repositioning across many cards), create `.cowork/skills/update_templates.py`.

Script responsibilities:
- Accept `<lesson.md>` as argument.
- Parse the `# Summary` section into card blocks (same delimiter logic as 3b above).
- For each block, detect which repairs are needed (field rename, missing form lines, wrong kanji links, misplaced ID).
- Output a JSON report to stdout: list of `{block_index, card_type, repairs: [...]}` objects.
- Do NOT write to the file — Claude applies the actual edits using the report as a guide.

This separates detection (script, reliable) from editing (Claude, context-aware).

If no script is created, Claude performs detection and repair in a single pass by reading the file and applying Edit calls directly.

## Risks

- `<!--ID:-->` line repositioning is the highest-risk operation. Moving it to the wrong line would corrupt Anki's card identity mapping. The rule is strict: it goes after the last `<a href>` line (or last form line if no links), before the blank separator. Always verify by counting lines in a block before and after.
- Verb form computation errors (wrong godan ending row, ichidan vs godan misclassification) would silently produce wrong cards. Use the lookup tables in `references/verb-conjugation.md` character by character — do not guess. This applies equally to Repair 3b: a wrong verb-type classification will cause all 13 forms to be overwritten with incorrect values, replacing whatever the user had — including values the user intentionally corrected manually. When verb type is uncertain, do not overwrite; report the uncertain card for user review instead.
- Field-name normalization via the alias table (Repair 1) is safe only when intent is unambiguous. An incorrect positional match could rename a field to the wrong canonical label, silently corrupting card structure. The rule is: when positional matching is used, verify that the block's total field count matches the canonical template count before applying renames; if the counts differ, fall back to name-only matching and flag unmatched lines for user review.
- The alias table in `references/card-templates.md` is not exhaustive. Lesson files from different import sources may use spellings not in the table. The implementer should scan at least 2–3 representative lesson files before finalising the alias table, and expand it as new variants are discovered.
- Updating `fill-templates.md` to reference `references/` files: this is a documentation change only. Verify that no functional rule text is accidentally dropped during the extraction. The implementer should diff the functional content before and after.
- The `references/` files (including the new `card-templates.md`) must exist before `fill-templates.md` or `update-templates.md` reference them. Create all of them in Step 1 before editing fill-templates in Step 2.
- Do not run `fill_extract.py` as part of this skill — that script aborts if `Rzeczowniki:` is already filled, which it will be for any file this skill operates on.
