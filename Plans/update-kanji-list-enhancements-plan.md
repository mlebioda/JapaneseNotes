# update-kanji-list & kanji-headers Enhancements — Design Plan

## Purpose

Extend the `update-kanji-list` and `kanji-headers` skills with six new capabilities:

1. **Web fetch (kanji-trainer.org)** — for each kanji being processed, fetch its mnemonic and component explanation from kanji-trainer.org. This is the **primary source** for both the `### Mnemonic` text and the `### Parts` component list.
2. **Component (parts) linking** — parse the **Explanation** text fetched from kanji-trainer.org to detect component characters, then add wikilinks to the referenced component files (in `Kaligrafia/Primitives/` or `Kaligrafia/Kanji/`).
3. **Component file routing** — new component files go to `Kaligrafia/Primitives/` if the component is a primitive/radical (not a standalone kanji); to `Kaligrafia/Kanji/` if it is a standalone kanji (e.g. 土).
4. **Rename rule** — kanji/primitive files must follow the naming pattern `character - name.md` (with spaces around the hyphen). Apply this rule on creation and when renaming files touched during the current run.
5. **Bare occurrence link migration** — if an existing kanji/primitive file contains wikilinks that are NOT under any section header, migrate them into a `## Occurences` section.
6. **Consistency check (touched files only)** — after all other steps, verify that every file touched during the current run has a `## Occurences` section and that all occurrence links are valid wikilinks (not plain text). Fix silently; report in the completion summary.

These changes must not break existing skill behavior.

---

## Constraint: no behavior regression

All six enhancements are purely additive. Existing logic (KanjiList.md update, occurrence appending, file creation at `Kaligrafia/Kanji/`) remains unchanged. New behavior fires only for situations not previously handled, or as a post-processing pass on touched files.

---

## Step 0 — Web fetch from kanji-trainer.org

**This step runs first, before any file writing, for each kanji being processed.**

### 0a — URL pattern

```
https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html
```

where `X` is the kanji character itself (e.g. `熱` → `Mnemonic_熱.html`, `電` → `Mnemonic_電.html`).

This URL pattern has been verified for multiple kanji. The page is publicly accessible with no authentication required.

### 0b — Extracting the Mnemonic

On the page, the section labelled **"Mnemonic"** contains a single sentence mnemonic phrase. In the HTML this is the element with `id="idFeldErklar"`.

Example for 熱:
> "Earth in eight layers around the fire: This will be a heat."

Example for 電:
> "When it rains in the rice field, you need a lightning arrester because of the electricity."

Extract this text verbatim. It will be written under `### Mnemonic` in the kanji file (see Step 1c).

### 0c — Extracting the Explanation (component source)

On the page, the section labelled **"Explanation"** contains a natural-language breakdown of the kanji's structural components. In the HTML this is the element with `id="idFeldErlaeter"`.

Example for 熱:
> "Left: 坴 (earth 土, eight 八, earth 土), right: round 丸 (sth. nine-九-sided needs an extra stroke 丶 to become round.), bottom: fire 灬"

Example for 電:
> "Top: rain 雨 (View out of a window 冂 with a cloud 一 from which it is raining =,=), below: 电 (rice field 田 with an extra stroke 乚 as a lightning arrester/rod)"

Extract this text verbatim. It is the **sole source** for the component characters used in Step 1.

### 0d — Failure handling

If the fetch fails for any reason (network error, HTTP error, kanji not found on site, malformed page):

- Skip both the `### Mnemonic` and `### Parts` steps for that kanji.
- Do not abort the run — continue processing remaining kanji.
- Add a warning to the completion report:
  ```
  WARN: kanji-trainer.org fetch failed for X — Mnemonic and Parts skipped.
  ```

---

## Step 1 — Component linking (new behavior in update-kanji-list)

After the existing occurrence-append/create logic for a kanji file, and after a successful Step 0 fetch, parse the **Explanation** text from Step 0c to extract component characters.

### 1a — Parsing components from the Explanation text

The Explanation text uses a consistent natural-language pattern:

```
Left: 坴 (earth 土, eight 八, earth 土), right: round 丸 (...), bottom: fire 灬
Top: rain 雨 (...), below: 电 (rice field 田 ...)
```

Parse rule: extract every CJK character (Unicode range U+4E00–U+9FFF and U+3400–U+4DBF and U+20000+) that appears **immediately after** a positional keyword (`Left:`, `Right:`, `Top:`, `Bottom:`, `Below:`, `Above:`, `Inside:`, `Outside:`, `Center:`) or **immediately after** a comma+space inside the top-level parenthetical breakdown.

For 熱, this yields: `坴`, `丸`, `灬` as the top-level components (土, 八, 土 are sub-components of 坴 and should also be extracted if they appear in the breakdown).

Practical rule: extract **all** CJK characters that appear as the first character of a named component entry in the Explanation. Ignore positional words (`earth`, `fire`, `eight`, etc. in English) and parenthetical sub-explanations when they only describe an already-listed component.

If the Explanation text cannot be parsed (no recognisable pattern), skip `### Parts` for this kanji and log a warning.

### 1b — Resolving each component

For each component character extracted from the Explanation text (e.g. `坴`, `丸`, `灬`):

1. Search `Kaligrafia/Primitives/` recursively for any file whose name starts with that character.
2. If not found in Primitives, search `Kaligrafia/Kanji/` recursively with the same rule.
3. If still not found, create a new file (see Step 2 — routing and naming rules).

The English name for a newly created component file should be taken from the Explanation text itself — the word immediately following the character in the Explanation (e.g. `灬` → "fire", `丸` → "round"). Use that as the `name` part of the `character - name.md` filename.

### 1c — Writing Mnemonic and Parts sections to the kanji file

In the kanji file (in `Kaligrafia/Kanji/` or `Kaligrafia/Primitives/`), write both sections obtained from Step 0:

**`### Mnemonic`** — add (or overwrite if already present) with the mnemonic phrase from Step 0b:

```
### Mnemonic

Earth in eight layers around the fire: This will be a heat.
```

**`### Parts`** — ensure a `### Parts` section exists. Under it, add a wikilink to each resolved component file using the **exact filename** (no path):

```
### Parts

[[坴 - eightfold earth]]
[[丸 - round]]
[[灬 - fire]]
```

Do not duplicate links that are already present. Section placement order in the kanji file:

```
## Occurences
### Parts
### Mnemonic
```

(`### Mnemonic` and `### Parts` are subsections at the same level, placed after `## Occurences`.)

---

## Step 2 — Component file routing and naming

### 2a — Routing rule

When a component file does not exist yet, determine its target directory:

- **Primitive/radical** (not a standalone learnable kanji) → `Kaligrafia/Primitives/`
- **Standalone kanji** (appears in JLPT lists or is a learnable character, e.g. 土, 人, 口) → `Kaligrafia/Kanji/`

Heuristic to distinguish: if the character already appears as a kanji entry elsewhere in `Kaligrafia/Kanji/` (any subdirectory), treat it as a standalone kanji. Otherwise, treat it as a primitive and create it in `Kaligrafia/Primitives/`.

If ambiguous, default to `Kaligrafia/Primitives/`.

### 2b — Rename rule (applies to both Kaligrafia/Kanji/ and Kaligrafia/Primitives/)

All file names must follow:

```
character - name.md
```

Rules:
- Single space before and after the hyphen.
- `name` = first English word of the meaning (lowercase), same derivation as the existing `Kanji-meaning.md` rule.
- Examples: `電 - electricity.md`, `土 - soil.md`, `厶 - private.md`

The rename rule applies **only to files created or modified during the current run**. Do not rename pre-existing untouched files.

When creating a new file, always use the correct `character - name.md` format from the start.

When `update-kanji-list` creates an occurrence link, derive the wikilink target from the **actual filename** (post-rename), not from a pattern.

### 2c — New component file structure

Newly created component files (primitive or kanji) follow the same structure as new kanji files in the existing skill:

```
character - name

## Occurences
[[SourceLesson#header text]]
```

The first line is the plain header text (no `##`), copied from the source lesson header if available; otherwise derived from the character + meaning.

---

## Step 3 — Bare occurrence link migration

### Trigger

When reading an **existing** kanji or primitive file during the current run, check whether any wikilinks appear outside of a named section header.

### Definition of "bare"

A wikilink line is bare if there is no `##` header between it and the start of the file (or the previous `##` header is not `## Occurences`, `## Parts`, or another named section).

### Migration rule

Collect all bare wikilinks. Insert or extend a `## Occurences` section at the top of the file (before `## Parts`, if present) and move the bare links under it. Preserve existing section contents.

Example — before:
```
# 上 - above
[[UN5KL2#上 - above, on・うえ、あ（がる）・ジョウ]]
[[Kaligrafia_to_print#上 - na  うえ、あ・げる、あがる,のぼ／じょう]]
```

After:
```
# 上 - above

## Occurences
[[UN5KL2#上 - above, on・うえ、あ（がる）・ジョウ]]
[[Kaligrafia_to_print#上 - na  うえ、あ・げる、あがる,のぼ／じょう]]
```

Do not migrate links that are already under a named `##` section.

---

## Step 4 — Consistency check (touched files only)

After all other steps, for every file touched during the current run:

1. Verify a `## Occurences` section exists (if it still doesn't, add an empty one).
2. Verify all lines under `## Occurences` are valid wikilinks (start with `[[` and end with `]]`). If a line is plain text or a malformed link, log it in the completion report as a warning — do not auto-fix plain text (it may be intentional prose).
3. Verify all lines under `## Parts` are valid wikilinks. Same rule as above.

Fixes are silent. Warnings are reported in the completion summary.

---

## Skill files to modify

### `.cowork/skills/update-kanji-list.md`

Add the following new steps (in order, after the existing occurrence-append/create logic):

- **Step 0 — Web fetch** (new, runs first per kanji): implements Step 0a–0d of this plan. Uses `WebFetch` to retrieve `https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html`. Extracts **Mnemonic** (section labelled "Mnemonic" / `id="idFeldErklar"`) and **Explanation** (section labelled "Explanation" / `id="idFeldErlaeter"`). On failure, skips Mnemonic and Parts for that kanji and logs a warning.
- **Step 3 — Component linking** (new): implements Steps 1a–1c of this plan. Sources components from the Explanation text fetched in Step 0, not from the lesson file.
- **Step 4 — Bare link migration** (new): implements Step 3 of this plan.
- **Step 5 — Consistency check** (new): implements Step 4 of this plan.

Also insert into Step 2 the rename rule (Step 2b/2c above) and the routing rule for new component files (Step 2a), clearly marked as additions that do not override existing behavior.

### `.cowork/skills/kanji-headers.md`

Two minor consistency updates (no behavior change):

1. The wikilink-lookup section already says `Kaligrafia/Kanji/` for file search. Add a note that the same recursive-glob pattern applies when `update-kanji-list` creates a new file — the wikilink must be re-derived after creation.
2. Add a cross-reference note: "Component files (primitives) referenced in `## Parts` blocks are handled by `update-kanji-list` Step 3 — `kanji-headers` does not need to touch them."

---

## Completion report format

`update-kanji-list` must emit a summary after each run:

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

---

## Edge cases

| Case | Handling |
|---|---|
| kanji-trainer.org fetch fails (network error, HTTP error, 404) | Skip Mnemonic and Parts for that kanji; log warning in completion report; continue run |
| kanji-trainer.org returns a page but Explanation text has no recognisable component pattern | Skip `### Parts` for that kanji; log warning; still write `### Mnemonic` if available |
| kanji-trainer.org rate-limits the skill (HTTP 429) | Treat as fetch failure; skip Mnemonic and Parts; log warning |
| Kanji file already has a `### Mnemonic` section | Overwrite it with the freshly fetched text |
| Explanation text names the same component character more than once (e.g. 土 appears twice in 坴) | De-duplicate; add the component file link only once under `### Parts` |
| Component character extracted from Explanation already has a file in the correct directory with the wrong name format | Do not rename pre-existing untouched file; use its actual filename for the wikilink |
| Kanji character appears in both `Kaligrafia/Kanji/` and `Kaligrafia/Primitives/` | Use the existing file found first; do not create a duplicate |
| Explanation text is absent (Step 0 succeeded but no Explanation section found) | Skip `### Parts`; write `### Mnemonic` only |
| Multiple kanji in a single lesson share the same component | Add occurrence link to the component file once per lesson (de-duplicate) |
| Existing kanji file H1 heading does not match the rename convention | Leave H1 as-is (do not normalize headings) |
