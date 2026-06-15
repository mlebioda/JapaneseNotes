# Plan: Mnemonic-Driven Component Discovery for kanji-file

## Status
DRAFT

## Problem Statement

The current `kanji-file` skill (Step 3) derives component parts exclusively from the
`idFeldErlaeter` element fetched from kanji-trainer.org. It scans that text for positional
keywords (`Left:`, `Right:`, `Top:`, etc.) to identify CJK component characters.

This approach has two weaknesses:

1. **Web dependency**: every run requires a successful network fetch, even when the user has
   already written a custom `### Mnemonic` section in the kanji file.
2. **Keyword brittleness**: the positional keyword parser fails silently when the web page
   uses different phrasing, is unavailable, or returns an unexpected structure.

The user wants a mnemonic-driven alternative: treat the `### Mnemonic` section as the single
source of truth for component discovery. If a mnemonic is already present, skip the fetch
entirely. Components are discovered by scanning the mnemonic text for CJK characters — no
positional keywords needed.

---

## Solution Overview

Replace the current Step 1 → Step 3 pipeline with a conditional flow:

- **Mnemonic absent/empty** → fetch from web (current behavior), write mnemonic, then scan
  the written mnemonic for CJK characters to populate `### Parts`.
- **Mnemonic already present** → skip web fetch entirely, scan the existing mnemonic text for
  CJK characters to populate `### Parts`.

In both cases, `### Parts` is always derived from the settled mnemonic text, never directly
from the raw web `idFeldErlaeter` element.

---

## Detailed Implementation Steps

### Step A — Check `### Mnemonic` before fetching

At the start of the skill run, read the kanji file and check whether a `### Mnemonic` section
exists and contains non-empty content (ignoring blank lines).

- **Empty or absent** → proceed to Step B (web fetch).
- **Non-empty** → skip Step B and Step C entirely; proceed to Step D using the existing text.

### Step B — Web fetch (conditional, replaces current Step 1)

Only runs when Step A determined the mnemonic is absent or empty.

Fetch `https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html` (X = Unicode decimal code
point of the kanji).

Extract:
- `id="idFeldErklar"` → mnemonic phrase
- `id="idFeldErlaeter"` → component explanation (used to build the mnemonic text written in
  Step C)

**On fetch failure**: log a warning, skip Steps C and D for this kanji; do not abort the run.

### Step C — Write `### Mnemonic` from web data (conditional)

Only runs after a successful Step B.

Write to `### Mnemonic`:
1. Component explanation text (from `idFeldErlaeter`) on the first line.
2. Mnemonic phrase text (from `idFeldErklar`) on the next line.

This overwrites any previously empty `### Mnemonic` section.

After writing, the mnemonic text is now the settled text for Step D.

### Step D — Scan mnemonic for CJK characters (replaces current Step 3)

Scan the settled `### Mnemonic` text (either written in Step C or already present from Step A)
for CJK characters in the Unicode ranges:

- CJK Unified Ideographs: U+4E00–U+9FFF
- CJK Unified Ideographs Extension A: U+3400–U+4DBF
- CJK Radicals Supplement / Kangxi Radicals: U+2E80–U+2FFF
- Katakana/Hiragana are NOT components — skip them

For each CJK character found:

1. **Already linked in `### Parts`** → skip (no duplicate).
2. **Not yet in `### Parts`**:
   a. Search `Caligraphy/Primitives/` recursively for a file whose name starts with that
      character. If found, add wikilink to `### Parts`.
   b. If not found, search `Caligraphy/Kanji/` recursively. If found, add wikilink to
      `### Parts`.
   c. If not found in either location:
      - Extract the English name from the word **immediately adjacent** to the CJK character
        in the mnemonic text (prefer the word that follows; fall back to the word before).
        Example: `"axe 斤"` → name = `axe`; `"斤 axe"` → name = `axe`.
      - Create `Caligraphy/Primitives/<character>-<name>.md` with minimal content:
        ```
        # <character>
        ## Occurences
        [[<current-kanji-filename>]]
        ```
      - Add wikilink `[[<character>-<name>]]` to `### Parts` of the current kanji file.

**Cycle guard**: before creating or recursively processing any new primitive file, verify the
target character is not already in the current call stack. If it is, skip and log:
`CYCLE GUARD: skipped [character] — already in progress`.

Write the final `### Parts` section:
- Use exact filename (no path, no `.md`).
- De-duplicate: each wikilink appears at most once.
- Preserve links already present in `### Parts` that were not derived from this scan
  (e.g. manually added links).

---

## Steps Unchanged From Current Skill

- **Step 4 — Link verification**: no change.
- **Step 5 — Bare link migration**: no change.
- **Step 6 — Consistency check**: no change.
- **Section placement order**: no change (`## Occurences` → `### Parts` → `### Mnemonic`).

---

## Edge Cases

| Case | Handling |
|------|----------|
| `### Mnemonic` exists but contains only the component explanation (no mnemonic phrase) | Still treated as non-empty → skip fetch; scan whatever text is present |
| Mnemonic text contains a CJK character that is the kanji itself (self-reference) | Skip — do not add the kanji as its own component |
| Adjacent word extraction yields a non-English or empty string | Fall back to the hex code point as the name: `<char>-u<XXXX>.md` |
| Two CJK characters appear adjacent with no separating Latin word | Skip name extraction for both; log warning: `WARN: no adjacent English word for [char]`; do not create the primitive file |
| New primitive file already exists by the time the write is attempted (race / duplicate) | Do not overwrite; just add wikilink to `### Parts` |
| `Caligraphy/Primitives/` directory does not exist | Create it before writing the new primitive file |
| Web fetch succeeds but `idFeldErlaeter` is empty | Write only the mnemonic phrase to `### Mnemonic`; Step D finds no CJK characters → `### Parts` left empty |
| Kanji file has `### Parts` with existing links before this run | Preserve existing links; only add newly discovered ones |

---

## Files to Modify

- `.cowork/skills/kanji-file.md` — replace Steps 1–3 with Steps A–D as described above;
  update the completion report format to reflect new step names.

## Files Not Modified

- `.claude/agents/` — no agent changes required
- Any lesson file under `JPLessons/` — never touched
- Existing kanji/primitive files in `Caligraphy/` — only created or appended, never overwritten

---

## Completion Report Format (updated)

```
kanji-file: 斤
  Step A — mnemonic check: non-empty (skipping web fetch)
  Step D — ### Parts: 2 components found in mnemonic ([[木-tree]], [[口-mouth]])
  Step 4 — link verification: 3 links checked, 0 fixed
  Step 5 — bare link migration: 0 links moved
  Step 6 — consistency check: OK
  Warnings: none
```

```
kanji-file: 近
  Step A — mnemonic check: empty
  Step B — web fetch: OK
  Step C — ### Mnemonic: written
  Step D — ### Parts: 1 component found ([[斤-axe]]), 1 primitive created (Caligraphy/Primitives/斤-axe.md)
  Step 4 — link verification: 2 links checked, 0 fixed
  Step 5 — bare link migration: 0 links moved
  Step 6 — consistency check: OK
  Warnings: none
```
