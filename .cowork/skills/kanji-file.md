---
name: kanji-file
description: >
  Standalone skill for processing a single kanji reference file. Fetches the mnemonic phrase and
  component explanation from kanji-trainer.org, writes or updates the ### Mnemonic and ### Parts
  sections, verifies all non-lesson wikilinks against actual filenames, and migrates bare links to
  ## Occurences. Runnable independently or called by kanji-headers after ensuring the kanji file
  exists.
---

# Kanji-File Skill

## Trigger

User says: `kanji-file [character]` or `kanji-file [file path]`

Also called by `kanji-headers` after a kanji reference file is confirmed or created (Step 2).

---

## Input

A **single kanji character** (e.g. `近`) or the **full path to an existing kanji file**
(e.g. `Caligraphy/Kanji/近-near.md`).

If a bare character is given, locate the file by searching `Caligraphy/Kanji/` and
`Caligraphy/Primitives/` recursively for a file whose name starts with that character.
If no file is found, report the error and stop — do not create the file (file creation is
`kanji-headers`'s responsibility when called through a lesson workflow; when called directly,
ask the user whether to create the file).

---

## Workflow

### Step 1 — Web fetch

Fetch the mnemonic page from:

```
https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html
```

where `X` is the Unicode code point of the kanji character in decimal (e.g. `è¿` → `36817`).

From the fetched HTML, extract:

- `id="idFeldErklar"` → **mnemonic phrase** (short memorable sentence)
- `id="idFeldErlaeter"` → **component explanation** (describes the visual components; the sole
  source for `### Parts` in Step 3)

Store both in a `fetch-result` map keyed by the kanji character:

```
fetch-result[近] = { mnemonic: "...", explanation: "..." }
```

**On fetch failure** (network error, 404, missing element IDs): skip `### Mnemonic` and
`### Parts` for this kanji; log a warning in the completion report; do not abort the run.

This step runs once per invocation. Results are used by Steps 2 and 3.

---

### Step 2 — Write/update `### Mnemonic`

Using the `fetch-result` for this kanji:

1. Write the **component explanation** text first (from `idFeldErlaeter`).
2. Write the **mnemonic phrase** text below it on a new line (from `idFeldErklar`).

If a `### Mnemonic` section already exists in the kanji file, **overwrite its content** with the
newly fetched data. Do not preserve the old content.

If the fetch failed (Step 1), skip this step entirely.

---

### Step 3 — Write/update `### Parts`

Parse **component characters** from the component explanation text (from `idFeldErlaeter`) using
positional keywords:

```
Left:, Right:, Top:, Bottom:, Below:, Above:, Inside:, Outside:, Center:
```

For each component character found:

1. **Search `Caligraphy/Primitives/`** recursively for a file whose name starts with that
   character. If found, record the filename (no `.md`, no path).
2. **If not found**, search `Caligraphy/Kanji/` recursively for the same character.
3. **If still not found**, create a new file in `Caligraphy/Primitives/` using naming convention
   `character-name.md` (no spaces around hyphen; English name taken from the word immediately
   following the character in the explanation text, lowercase). Then recursively call `kanji-file`
   on the new component file.

**Cycle guard:** before any recursive `kanji-file` call, check whether the target character is
already being processed in the current call stack. If yes, skip the recursive call and log a
warning: `CYCLE GUARD: skipped recursive call for [character] — already in progress`.

Write wikilinks to all resolved component files under `### Parts`:

```
### Parts
[[貝-shell]]
[[刀-sword]]
```

- Use exact filename, no path, no `.md`.
- De-duplicate: each wikilink appears at most once.
- If a `### Parts` section already exists, overwrite its content with the newly resolved links.

If the fetch failed (Step 1), skip this step entirely.

---

### Step 4 — Link verification

Scan **all wikilinks** in the kanji file, regardless of which section they appear in (legacy
files may lack `### Parts`).

Classification rule:

- Links **containing `#`** (e.g. `[[UN5KL5#生 - be born…]]`) → **lesson occurrence links →
  NEVER TOUCH**. Skip entirely.
- Links **without `#`** → component or kanji reference links → verify against actual filename:
  1. Search `Caligraphy/Kanji/` and `Caligraphy/Primitives/` recursively for a file whose name
     starts with the linked kanji character.
  2. If the link text does not match the actual filename (e.g. link is `[[貝 - muszla]]` but file
     is `貝-muszla.md`) → fix the link to match the actual filename.
  3. If no file is found for the linked character, log a warning; do not remove the link.

---

### Step 5 — Bare link migration

Collect all wikilinks that appear **outside any named `##` section** (i.e. links at the top of
the file before any `##` heading, or between `##` headings without a section of their own).

Move them under `## Occurences`:

- If `## Occurences` does not exist, create it.
- Append the collected wikilinks under `## Occurences`. Preserve all existing content already
  under that section.
- Do not duplicate links already present in `## Occurences`.

---

### Step 6 — Consistency check

After all writes are complete:

1. Verify `## Occurences` exists in the file. If it is still missing (e.g. Steps 1 and 5 both
   produced nothing), add an empty `## Occurences` section.
2. Scan all lines under `## Occurences` and `### Parts`. For each line that contains a link:
   - If it is a valid wikilink (`[[…]]`) → OK.
   - If it is plain text that looks like a link (e.g. a bare kanji or an unbracketed filename)
     → log a warning: `WARN: malformed link in [section]: [line]`. Do not auto-fix.
3. Report any warnings in the completion report.

---

## Section placement order

The final kanji file must follow this section order:

```
[title line — first line of file, e.g. # 近]
## Occurences
### Parts
### Mnemonic
```

When rewriting sections, preserve any content not managed by this skill (e.g. user-written notes
below a section heading). Do not reorder sections that already exist unless they violate this
order.

---

## Completion report

After all steps finish, output a summary:

```
kanji-file: 近
  Step 1 — fetch: OK (mnemonic and explanation retrieved)
  Step 2 — ### Mnemonic: written
  Step 3 — ### Parts: 2 components resolved ([[貝-shell]], [[刀-sword]])
  Step 4 — link verification: 3 links checked, 1 fixed ([[貝 - muszla]] → [[貝-muszla]])
  Step 5 — bare link migration: 2 links moved to ## Occurences
  Step 6 — consistency check: OK
  Warnings: none
```

If called by `kanji-headers` for multiple kanji, each kanji produces its own report block.

---

## Never touch

- Lesson files under `JPLessons/` — read-only, never write
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- Wikilinks containing `#` (lesson occurrence links — never modify)
- `# Summary` sections and everything below them in any file
- Do not run `git push` or any remote git operation
