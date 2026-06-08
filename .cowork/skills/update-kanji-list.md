# Skill: update-kanji-list

## Purpose
Search files with calligraphy lessons to update the list of known kanji, then create or update individual kanji files used for cross-referencing.

## Trigger phrases
User says: "Update kanji list [file]"

## Input
- `[file]` — a calligraphy lesson file (e.g. UNK5L9-Basic-Nouns)
- `[KanjiList.md]` — file with all known kanji, in ObsidianJP root directory
- `[kanji-file-map]` *(optional)* — map of `character → filename (no .md)` pre-computed by `kanji-headers`. When provided, skip the `Caligraphy/Kanji/` search in Step 2 for characters present in the map.

---

## Pre-flight check

Before processing any kanji, verify that `[file]` exists and is readable.
If the file cannot be found, stop immediately and report:

  ERROR: Source file "[file]" not found — aborting. No files were modified.

Do not proceed to Step 0 or any subsequent step.

---

## Processing order

```
Phase I — Fetch (all kanji, no file writes):
  Step 0 for kanji-1
  Step 0 for kanji-2
  …
  Step 0 for kanji-N

Phase II — Write (all kanji, using cached fetch data):
  For each kanji: Step 1 → Step 2 → Step 3 (using cached result) → Step 4

After all kanji:
  Step 5 — Consistency check
  Completion report
```

Run all Step 0 web fetches for every kanji before any file writing begins. Store each result in a `fetch-results` map keyed by kanji character. Then, in Phase II, execute Steps 1–4 for each kanji using the pre-fetched data — no web fetches occur during Phase II.

---

## Step 0 — Web fetch from kanji-trainer.org

**This step runs for ALL kanji in Phase I, before any file writing begins. Results are cached in a `fetch-results` map and consumed during Phase II.**

### URL pattern

```
https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html
```

where `X` is the kanji character itself (e.g. `熱` → `Mnemonic_熱.html`, `電` → `Mnemonic_電.html`).

Use the `WebFetch` tool to retrieve the page.

### Extracting the Mnemonic

The mnemonic phrase is in the HTML element with `id="idFeldErklar"`. Extract the text content verbatim. It will be written under `### Mnemonic` in the kanji file (Step 3).

Example for 熱:
> "Earth in eight layers around the fire: This will be a heat."

### Extracting the Explanation (component source)

The component breakdown is in the HTML element with `id="idFeldErlaeter"`. Extract the text content verbatim. It is the **sole source** for component characters used in Step 3.

Example for 熱:
> "Left: 坴 (earth 土, eight 八, earth 土), right: round 丸 (...), bottom: fire 灬"

### Failure handling

If the fetch fails for any reason (network error, HTTP error, 404, malformed page, kanji not found):

- Skip both `### Mnemonic` and `### Parts` for that kanji.
- Do **not** abort the run — continue processing remaining kanji.
- Record the warning for the completion report:
  ```
  WARN: kanji-trainer.org fetch failed for X — Mnemonic and Parts skipped.
  ```

---

## Step 1 — Update KanjiList.md

**Phase A — Read once (before the loop):** Read the full contents of `KanjiList.md` and hold it in memory as `kanjilist-content`. Also collect the full extracted kanji list from `[file]` (from all `##` headers) and de-duplicate it.

**Phase B — One pass per kanji:** For each kanji character, check `kanjilist-content` for an exact character match (one character per line — do **not** rely on substring matching). Collect all characters that are not present into a `to-add` list.

**Phase C — Single write:** After all kanji are checked, append every character in `to-add` to `KanjiList.md` in one write operation. Never add a kanji that is already present.

---

## Step 2 — Update individual kanji files

For each kanji in `[file]`, derive its header text (e.g. `電 - electricity・デン`).

### Routing rule (NEW — additive)

Determine the target directory for the kanji file:

- **Primitive/radical** (not a standalone learnable kanji) → `Caligraphy/Primitives/`
- **Standalone kanji** (appears in JLPT lists or is a learnable character, e.g. 土, 人, 口) → `Caligraphy/Kanji/`

Heuristic: if the character already appears as a kanji entry in `Caligraphy/Kanji/` (any subdirectory), treat it as a standalone kanji. Otherwise, treat it as a primitive and place the new file in `Caligraphy/Primitives/`.

When in doubt, default to `Caligraphy/Primitives/`.

This routing rule applies when **creating** new files during this run. It does not affect files that already exist.

### File name rule (UPDATED — spaces around hyphen)

`character - name.md` — kanji character + space + hyphen + space + first English word of the meaning (lowercase).

Examples:
- `電 - electricity・デン` → `電 - electricity.md`
- `方 - direction, way・かた、-がた・ホウ` → `方 - direction.md`
- `社 - company, shrine・シャ、-ジャ` → `社 - company.md`

The rename rule (spaces around hyphen) applies **only to files created or modified during the current run**. Do not rename pre-existing untouched files.

When creating a new file, always use the `character - name.md` format from the start.

### File location

`Caligraphy/Kanji/[filename].md` for standalone kanji (flat, no subdirectories within a new file).
`Caligraphy/Primitives/[filename].md` for primitives/radicals.

### Check if kanji file exists

If `[kanji-file-map]` was provided and contains an entry for this kanji character, use that entry directly — skip the `Caligraphy/Kanji/` and `Caligraphy/Primitives/` searches. A `null` entry means no Kanji file was found; still search `Caligraphy/Primitives/` for possible routing.

Otherwise, search `Caligraphy/Kanji/` and `Caligraphy/Primitives/` (including subdirectories) for any file whose **filename starts with the kanji character** — regardless of what follows. Do not require an exact title match.

Examples: `電` matches `電-electricity.md`, `電 - electricity.md`, `雨/電-electricity.md` etc.

---

**If a matching file EXISTS:**

Append a new occurrence link under `## Occurences`:
```
[[FileName#Header text]]
```

Example:
```
[[UNK5L9-Basic-Nouns#電 - electricity・デン]]
```

If `## Occurences` section doesn't exist yet in the file, add it first.

When creating or deriving the wikilink, use the **actual filename** (post-creation/post-rename), not a pattern.

---

**If NO matching file EXISTS:**

Create `Caligraphy/Kanji/[kanji] - [first-meaning-word].md` (or `Caligraphy/Primitives/` per routing rule) with this structure:

```
電 - electricity・デン

## Occurences
[[UNK5L9-Basic-Nouns#電 - electricity・デン]]
```

Note: the first line is the plain header text (no `##`), copied exactly from the source lesson header.

---

Process all kanji from the lesson file before finishing.

---

## Step 3 — Component linking

**Runs after Step 2, only when the `fetch-results` map contains a valid Explanation text for this kanji.**

### 3a — Parse components from the Explanation text

The Explanation text uses a consistent natural-language pattern:

```
Left: 坴 (earth 土, eight 八, earth 土), right: round 丸 (...), bottom: fire 灬
Top: rain 雨 (...), below: 电 (rice field 田 ...)
```

Parse rule: extract every CJK character (Unicode range U+4E00–U+9FFF, U+3400–U+4DBF, and supplementary CJK planes) that appears:
- **immediately after** a positional keyword (`Left:`, `Right:`, `Top:`, `Bottom:`, `Below:`, `Above:`, `Inside:`, `Outside:`, `Center:`)
- **or** immediately after a comma+space inside the top-level parenthetical breakdown

Extract all CJK characters that appear as the **first character** of a named component entry. Sub-components of already-listed components should also be extracted if they appear in the breakdown.

If the Explanation text cannot be parsed (no recognisable positional pattern), skip `### Parts` for this kanji and log a warning in the completion report.

### 3b — Resolve each component

For each component character extracted:

1. Search `Caligraphy/Primitives/` recursively for any file whose name starts with that character.
2. If not found in Primitives, search `Caligraphy/Kanji/` recursively with the same rule.
3. If still not found, create a new file per routing rule (Step 2 routing and naming rules apply).

The English name for a newly created component file: take it from the Explanation text — the word immediately following the character in the Explanation (e.g. `灬` → "fire", `丸` → "round").

### 3c — Write Mnemonic and Parts sections to the kanji file

In the kanji file, write both sections:

**`### Mnemonic`** — add or overwrite with **both** the Explanation text and the Mnemonic phrase from Step 0. Write the Explanation first, then the Mnemonic phrase on a new line below:

```markdown
### Mnemonic

Left: 坴 (earth 土, eight 八, earth 土), right: round 丸 (sth. nine-九-sided needs an extra stroke 丶 to become round.), bottom: fire 灬

Earth in eight layers around the fire: This will be a heat.
```

Never write only the Mnemonic phrase and omit the Explanation — both must be present.

**`### Parts`** — ensure a `### Parts` section exists. Under it, add a wikilink to each resolved component file using the **exact filename** (no path). De-duplicate links already present:

```markdown
### Parts

[[坴 - eightfold earth]]
[[丸 - round]]
[[灬 - fire]]
```

Section placement order in the kanji file:

```
## Occurences
### Parts
### Mnemonic
```

(`### Parts` and `### Mnemonic` are subsections at the same level, placed after `## Occurences`.)

---

## Step 4 — Bare link migration

**Applies only when reading an existing kanji or primitive file during the current run.**

### Definition of "bare"

A wikilink line is bare if there is no `##` section header between it and the start of the file (or the preceding `##` header is not a named section like `## Occurences`, `## Parts`, etc.).

### Migration rule

Collect all bare wikilinks. Insert or extend a `## Occurences` section at the top of the file (before `### Parts`, if present) and move the bare links under it. Preserve existing section contents.

Example — before:
```
# 上 - above
[[UN5KL2#上 - above, on・うえ、あ（がる）・ジョウ]]
[[Caligraphy_to_print#上 - na  うえ、あ・げる、あがる,のぼ／じょう]]
```

After:
```
# 上 - above

## Occurences
[[UN5KL2#上 - above, on・うえ、あ（がる）・ジョウ]]
[[Caligraphy_to_print#上 - na  うえ、あ・げる、あがる,のぼ／じょう]]
```

Do not migrate links that are already under a named `##` section.

---

## Step 5 — Consistency check (touched files only)

After all other steps, for every file touched during the current run:

1. Verify a `## Occurences` section exists. If missing, add an empty one.
2. Verify all lines under `## Occurences` are valid wikilinks (start with `[[` and end with `]]`). If a line is plain text or a malformed link, log it in the completion report as a warning — do not auto-fix plain text (it may be intentional prose).
3. Verify all lines under `### Parts` are valid wikilinks. Same rule as above.

Fixes are silent. Warnings are reported in the completion summary.

---

## Completion report

After the run, emit a summary in this format:

```
update-kanji-list — [SourceFile]
  Kanji processed: N
  KanjiList.md: N added, N skipped
  Kanji files: N created, N updated
  Web fetch: N succeeded, N failed
    WARN: kanji-trainer.org fetch failed for X — Mnemonic and Parts skipped.
  Mnemonics written: N
  Bare links migrated: N (in M files)
  Component files: N created (X in Primitives/, Y in Kanji/)
  Consistency warnings: [none | list of file + issue]
```
