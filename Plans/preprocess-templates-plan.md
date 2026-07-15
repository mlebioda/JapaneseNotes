# preprocess-templates

## Goal

Save Claude context by automating safe, repetitive label-rename actions via a preprocessing script, so `templates-update` only needs to handle reasoning-heavy repairs. All 31 known alias-table renames are applied mechanically by a Python script before Claude touches the file. After the script runs, Repair 1 in `templates-update` only needs positional matching and flagging of unknown labels — the alias-table work is already done.

---

## Components

### Component 1 — `label-aliases.json`

**File:** `.cowork/skills/references/label-aliases.json`

A flat JSON dictionary mapping every known variant label to its canonical form. All 31 entries from the alias table currently in `.cowork/skills/references/card-templates.md` (lines 89–124) are included verbatim. The `そう:` → `そう (looks):` mapping is an unconditional entry — no block-type qualifier, no special handling.

This file must exist before any other component is written or modified.

Example structure:
```json
{
  "Tłumaczenie:": "ほんやく:",
  "translation:": "ほんやく:",
  "そう:": "そう (looks):",
  ...
}
```

---

### Component 2 — `preprocess-templates.py`

**File:** `.cowork/scripts/preprocess-templates.py`

CLI: `python preprocess-templates.py <lesson-file-path>`

Behaviour:
- Loads `label-aliases.json` from a path relative to the script (`../skills/references/label-aliases.json`).
- Reads the target lesson file.
- Aborts without writing if `# Summary` is not found in the file; exits with a clear error message.
- Writes output to a temp file, then atomically replaces the original using `os.replace` — no partial writes.
- Processes the file line by line. Lines above `# Summary` are copied verbatim (never modified).
- For each line below `# Summary`:
  - If the line starts with `<!--`, copy verbatim — never touch `<!--ID:-->` lines.
  - Otherwise, attempt a label match: strip whitespace, extract the text before the first `:`, look up `"<text>:"` in the alias dict.
  - Lookup is case-sensitive first. On miss, if the key contains only ASCII characters, retry with `.lower()` (romaji/Latin keys are case-insensitive; Japanese keys are case-sensitive only).
  - On match: replace the label, preserve `: <value>` verbatim.
  - On no match: copy the line verbatim.
- Prints a summary to stdout: count of replacements per canonical label, total lines changed.

---

### Component 3 — Update `card-templates.md` and `adj-forms.md`

**Files:** `.cowork/skills/references/card-templates.md` and `.cowork/skills/references/adj-forms.md`

#### `card-templates.md` — two changes

1. **Remove the alias table inline content.** Replace the entire "Label alias table" section body (the Markdown table and usage rules, approximately lines 84–132) with:
   ```
   ## Label alias table

   See `.cowork/skills/references/label-aliases.json`.
   ```
   The section heading is kept; only the table and usage rules are replaced.

2. **Fix the `#wp` canonical template.** In the canonical `#wp` block, the form line currently reads `そう: [value]`. Change it to `そう (looks): [value]` to match the canonical label used by `#wc` and the alias table.

All other sections remain unchanged.

#### `adj-forms.md` — rename `そう:` label throughout

The file currently uses `そう:` as the field label in all four rule blocks (い-adjective, special-case いい/よい, な-adjective, non-adjective). After this plan the canonical label for that field is `そう (looks):`.

Replace every occurrence of `そう:` with `そう (looks):` in the four code blocks. The section heading `## な-adjective — fill dashes (except そう)` uses `そう` as a concept name in prose — leave that unchanged. Only the label column entries inside code blocks are renamed.

---

### Component 4 — Update `templates-update.md`

**File:** `.cowork/skills/templates-update.md`

Three changes:

1. **Add Step 0 before existing Repair 1.** Insert a new step at the top of the per-card repair sequence:
   > Step 0 — Run `python .cowork/scripts/preprocess-templates.py <file>` on the target file before beginning any card-by-card repairs. This applies all alias-table renames mechanically. After this step, Repair 1 only needs positional matching and flagging of labels that remain unknown.

2. **Update Repair 1 description** to note that alias-table renames are already handled by the script. Repair 1 now covers: positional matching for labels that survived Step 0 unmatched, and flagging of any unrecognized labels for user review.

3. **Update the skill intro/description** to state that mechanical label renames are handled by `preprocess-templates.py` before Claude begins its reasoning-heavy repair pass.

---

### Component 5 — Update `fill-templates.md`

**File:** `.cowork/skills/fill-templates.md`

Update any reference to the alias table in `card-templates.md` to point to `label-aliases.json` instead. If `fill-templates.md` currently instructs Claude to consult the alias table in `card-templates.md`, replace that reference with: "See `.cowork/skills/references/label-aliases.json` for the label alias table."

If no such reference exists, no change is needed for this component.

---

## Dependencies / ordering constraints

Components must be implemented in strict order:

1. **Component 1 first** — `label-aliases.json` must exist on disk before the script (Component 2) or any skill file (Components 3–5) references it.
2. **Component 2 second** — the script must be written and tested before the skills are updated to call it.
3. **Component 3 third** — `card-templates.md` is updated to defer to `label-aliases.json` only after that file exists.
4. **Component 4 fourth** — `templates-update.md` adds the Step 0 script call only after the script exists.
5. **Component 5 last** — `fill-templates.md` is updated last; it has no dependencies on Components 3–4.

Do not skip ahead. A skills file referencing a JSON or script file that does not yet exist would leave the vault in an inconsistent state.

---

## Out of scope

- No changes to any lesson file content or structure.
- No changes to the `# Summary` section of any lesson file.
- No changes to `<!--ID:-->` values or positions.
- No changes to `fill_extract.py` or any other existing script.
- No changes to `.cowork/instructions.md` (the skill entry for `templates-update` already exists there).
- No new repair logic in `templates-update.md` beyond the Step 0 addition.
- The existing `Plans/fix_kanji_links.py` batch script is not affected.

---

## Risks

- If `os.replace` is called with a temp file on a different filesystem than the target, the atomic swap may fail on some systems. Use `tempfile.NamedTemporaryFile` with `dir=os.path.dirname(target)` to keep temp and target on the same filesystem.
- The `そう:` → `そう (looks):` entry is unconditional across all block types. This is correct as designed (both `#wc` and `#wp` now use `そう (looks):`), but implementers should confirm the `#wp` canonical template in `card-templates.md` is updated in Component 3 before relying on this.
- Case-insensitive fallback for ASCII keys must not apply to Japanese keys (e.g. `ほんやく：` with a full-width colon must remain an exact match, not lowercased). The script must check whether a key contains only ASCII before enabling the case-insensitive retry.
- If `fill-templates.md` has no reference to the alias table, Component 5 requires no edit. The implementer must read the file before deciding.
- Removing the alias table body from `card-templates.md` (Component 3) must not accidentally remove the section heading or any other section. The implementer must use a targeted Edit replacing only the table and usage rules, not the entire file.
- In `adj-forms.md`, only the label entries inside code blocks should be renamed. The prose heading `## な-adjective — fill dashes (except そう)` and any other prose references to `そう` as a concept name must not be changed.
