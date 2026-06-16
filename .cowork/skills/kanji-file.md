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

### Step A — Check `### Mnemonic` before fetching

Read the kanji file and check whether a `### Mnemonic` section exists and contains non-empty
content (ignoring blank lines).

- **Non-empty** → skip Steps B and C entirely; proceed to Step D using the existing mnemonic text.
- **Empty or absent** → proceed to Step B (web fetch).

---

### Step B — Web fetch (conditional)

Only runs when Step A determined the mnemonic is absent or empty.

Fetch the mnemonic page from:

```
https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html
```

where `X` is the Unicode code point of the kanji character in decimal (e.g. `近` → `36817`).

**Rate-limit rule**: Fetches to kanji-trainer.org must be done sequentially — one at a time.
Never issue parallel or concurrent requests to the site, even when `kanji-file` is called
for multiple kanji in a single run. Wait for the current fetch (and any resulting writes) to
complete before starting the next kanji.

From the fetched HTML, extract:

- `id="idFeldErklar"` → **mnemonic phrase** (short memorable sentence)
- `id="idFeldErlaeter"` → **component explanation** (describes the visual components)

**On fetch failure** (network error, 404, missing element IDs): log a warning in the completion
report; skip Steps C and D for this kanji; do not abort the run.

---

### Step C — Write `### Mnemonic` from web data (conditional)

Only runs after a successful Step B.

Write to `### Mnemonic`:

1. Component explanation text (from `idFeldErlaeter`) on the first line.
2. Mnemonic phrase text (from `idFeldErklar`) on the next line.

This overwrites any previously empty `### Mnemonic` section.

After writing, the settled mnemonic text is the content just written, and Step D will use it.

---

### Step D — Scan mnemonic for CJK characters → write `### Parts`

Scan the settled `### Mnemonic` text (either the existing text from Step A, or the text just
written in Step C) for CJK characters in the following Unicode ranges:

- CJK Unified Ideographs: U+4E00–U+9FFF
- CJK Unified Ideographs Extension A: U+3400–U+4DBF
- CJK Radicals Supplement / Kangxi Radicals: U+2E80–U+2FFF

Skip hiragana and katakana — they are not components.
Skip the kanji being processed itself (do not add a self-reference to `### Parts`).

For each CJK character found:

1. **Already linked in `### Parts`** → skip (no duplicate).
2. **Not yet in `### Parts`**:
   a. Search `Caligraphy/Primitives/` recursively for a file whose name starts with that
      character. If found, add wikilink to `### Parts`.
   b. If not found, search `Caligraphy/Kanji/` recursively. If found, add wikilink to
      `### Parts`.
   c. If not found in either location:
      - Extract the English name from the word **immediately adjacent** to the CJK character in
        the mnemonic text (prefer the word that follows; fall back to the word before).
        Example: `"axe 斤"` → name = `axe`; `"斤 axe"` → name = `axe`.
      - If no adjacent English word is found, use the hex code point as the name: `u<XXXX>`.
        Log a warning: `WARN: no adjacent English word for [char]`.
      - If two CJK characters appear adjacent with no separating Latin word, skip name extraction
        for both and log the warning above — do not create primitive files for them.
      - Create `Caligraphy/Primitives/<character>-<name>.md` with minimal content:
        ```
        # <character>
        ## Occurences
        [[<current-kanji-filename>]]
        ```
        If `Caligraphy/Primitives/` does not exist, create it first.
        If the file already exists (e.g. created concurrently), do not overwrite it.
      - Add wikilink `[[<character>-<name>]]` to `### Parts` of the current kanji file.

**Cycle guard**: before creating or processing any new primitive file, verify the target character
is not already in the current call stack. If it is, skip it and log:
`CYCLE GUARD: skipped [character] — already in progress`.

Write the final `### Parts` section:

```
### Parts
[[貝-shell]]
[[刀-sword]]
```

- Use exact filename, no path, no `.md`.
- De-duplicate: each wikilink appears at most once.
- Preserve links already present in `### Parts` that were not derived from this scan
  (e.g. manually added links).
- If a `### Parts` section already exists, overwrite its generated content but preserve any
  manually added links.

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
  3. If no file is found for the linked character, **remove the link from the file** and record it
     in the completion report as `REMOVED: [[<link>]] — no file found`.

---

### Step 5 — Bare link migration and classification

Collect all wikilinks that appear **outside any named `##` section** (i.e. links at the top of
the file before any `##` heading, or between `##` headings without a section of their own).

By the time Step 5 runs, Step 4 has already removed all broken links; every remaining bare link
is verified to have a corresponding file in `Caligraphy/`.

Classify and move each bare link to the correct destination:

- Bare links **without `#`** (component or kanji references — verified by Step 4) → move to
  `### Parts`:
  - If `### Parts` does not exist, create it.
  - Append the link under `### Parts`. Preserve all existing content already under that section.
  - Do not duplicate links already present in `### Parts`.
- Bare links **containing `#`** (lesson occurrence links) → move to `## Occurences`:
  - These should already be skipped by the "never touch `#` links" rule in Step 4; this branch
    is a safety catch only.
  - If `## Occurences` does not exist, create it.
  - Append the link under `## Occurences`. Preserve all existing content already under that
    section.
  - Do not duplicate links already present in `## Occurences`.

---

### Step 6 — Consistency check

After all writes are complete:

1. Verify `## Occurences` exists in the file. If it is still missing (e.g. Steps A–D and Step 5
   produced no links to migrate), add an empty `## Occurences` section.
2. Verify **no bare links remain outside any named `##` section**. Steps 4–5 must have classified
   and moved every bare link; if any remain, log a warning:
   `WARN: unsectioned bare link remains after Steps 4–5: [link]`.
3. Scan all lines under `## Occurences` and `### Parts`. For each line that contains a link:
   - If it is a valid wikilink (`[[…]]`) → OK.
   - If it is plain text that looks like a link (e.g. a bare kanji or an unbracketed filename)
     → log a warning: `WARN: malformed link in [section]: [line]`. Do not auto-fix.
4. Report any warnings and any `REMOVED` entries in the completion report.

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

After all steps finish, output a summary. Two examples — one where the mnemonic was already
present (skipping web fetch), one where it was absent (fetch required):

```
kanji-file: 斤
  Step A — mnemonic check: non-empty (skipping web fetch)
  Step D — ### Parts: 2 components found in mnemonic ([[木-tree]], [[口-mouth]])
  Step 4 — link verification: 3 links checked, 0 fixed, 0 removed
  Step 5 — bare link migration: 0 links moved to ### Parts, 0 links moved to ## Occurences
  Step 6 — consistency check: OK
  Warnings: none
```

```
kanji-file: 近
  Step A — mnemonic check: empty
  Step B — web fetch: OK
  Step C — ### Mnemonic: written
  Step D — ### Parts: 1 component found ([[斤-axe]]), 1 primitive created (Caligraphy/Primitives/斤-axe.md)
  Step 4 — link verification: 2 links checked, 0 fixed, 0 removed
  Step 5 — bare link migration: 0 links moved to ### Parts, 0 links moved to ## Occurences
  Step 6 — consistency check: OK
  Warnings: none
```

```
kanji-file: 千
  Step A — mnemonic check: non-empty (skipping web fetch)
  Step D — ### Parts: 1 component found in mnemonic ([[十-ten,10]])
  Step 4 — link verification: 3 links checked, 0 fixed, 1 removed
    REMOVED: [[丿 - component]] — no file found
  Step 5 — bare link migration: 1 link moved to ### Parts ([[十-ten,10]]), 0 links moved to ## Occurences
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
