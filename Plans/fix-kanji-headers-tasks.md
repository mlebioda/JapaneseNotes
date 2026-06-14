# Fix kanji-headers — Tasks

## Pre-flight

- [ ] Read `.cowork/skills/kanji-headers.md` in full before making any edits
- [ ] Read `.cowork/skills/update-kanji-list.md` in full (reference for logic being absorbed)
- [ ] Check whether `.claude/commands/kanji-headers.md` already exists
- [ ] Check whether `.claude/commands/kanji-file.md` already exists

---

## Task 1 — Rewrite `.cowork/skills/kanji-headers.md`

- [x] Update frontmatter `description` — reflect new design: skill ensures kanji reference files
  exist, fixes `##` header formatting and wikilinks in the lesson file, and updates
  `KanjiList.md`. Remove any mention of `update-kanji-list` or writing a `# Summary` section.

- [x] Rewrite `## Workflow` section — five steps:
  1. Read the lesson file
  2. For each kanji in `##` headers: search `Caligraphy/Kanji/` and `Caligraphy/Primitives/`
     recursively; if found → call `kanji-file`; if not found → create file (using
     `kanji-meaning` naming, no spaces around hyphen) → call `kanji-file`
  3. Fix `##` header line formats in the lesson file in-place (template:
     `## Kanji - meaning・kun・on`). Do NOT touch block content, reading lines, `---`,
     `## Parts`, or anything at/below `# Summary`.
  4. Write verified wikilinks under each `##` header (files guaranteed to exist from Step 2).
  5. Update `KanjiList.md` — append new kanji characters (last step, one character per line,
     no duplicates).

- [x] Remove all references to `update-kanji-list` from the skill body and workflow.
- [x] Remove any remaining trace of the destructive "replace everything from `# Summary` onward"
  rule.
- [x] Verify `## Header format rules`, `## Content block rules`, `## Scope boundary`, and
  `## Example output` sections are retained (they are still valid reference material).
- [x] Add a one-line note to `## Example output`: "This shows the target format for correctly
  formatted blocks, not a from-scratch write."

---

## Task 2 — Create `.cowork/skills/kanji-file.md`

- [x] Create the file with frontmatter:
  - `name: kanji-file`
  - `description`: standalone skill for processing a single kanji reference file — fetches
    mnemonic and components from kanji-trainer.org, writes/updates `### Mnemonic` and
    `### Parts`, verifies all non-lesson wikilinks, migrates bare links to `## Occurences`.
    Runnable independently or called by `kanji-headers`.

- [x] Write `## Trigger` section — "User says: `kanji-file [character]`; or called by
  `kanji-headers` after ensuring a kanji file exists."

- [x] Write `## Input` section — single kanji character or full file path.

- [x] Write `## Step 1 — Web fetch` section:
  - URL: `https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html`
  - Extract `id="idFeldErklar"` → mnemonic phrase
  - Extract `id="idFeldErlaeter"` → component explanation (sole source for `### Parts`)
  - On failure: skip `### Mnemonic` and `### Parts`, log warning, do not abort

- [x] Write `## Step 2 — Write/update ### Mnemonic` section:
  - Write Explanation text first, then Mnemonic phrase on new line below
  - Overwrite existing section if present

- [x] Write `## Step 3 — Write/update ### Parts` section:
  - Parse component characters using positional keywords (`Left:`, `Right:`, `Top:`,
    `Bottom:`, `Below:`, `Above:`, `Inside:`, `Outside:`, `Center:`)
  - For each component: search `Caligraphy/Primitives/` → `Caligraphy/Kanji/` → if not found,
    create in `Caligraphy/Primitives/` (naming: `character-name.md`, no spaces around hyphen,
    English name from Explanation text) → recursively call `kanji-file` on it
  - Cycle guard: if a component character is already being processed in the current call stack,
    skip recursive call and log a warning
  - Write wikilinks under `### Parts` (exact filename, no path, de-duplicated)

- [x] Write `## Step 4 — Link verification` section:
  - Rule: links containing `#` → lesson occurrence links → NEVER TOUCH
  - Rule: links without `#` → verify against actual filename in `Caligraphy/Kanji/` and
    `Caligraphy/Primitives/`; fix if link text does not match actual filename
  - Scan applies to all wikilinks in the file regardless of section (legacy files may lack
    `### Parts`)

- [x] Write `## Step 5 — Bare link migration` section:
  - Collect wikilinks not under any named `##` section
  - Move under `## Occurences` (create if absent); preserve existing section contents

- [x] Write `## Step 6 — Consistency check` section:
  - Verify `## Occurences` exists; add empty one if missing
  - Verify all links under `## Occurences` and `### Parts` are valid wikilinks (`[[…]]`)
  - Log warnings for malformed lines; do not auto-fix plain text prose

- [x] Write `## Section placement order` block:
  ```
  [title line]
  ## Occurences
  ### Parts
  ### Mnemonic
  ```

- [x] Write `## Completion report` format (similar to `update-kanji-list` format but scoped to
  a single kanji file).

---

## Task 3 — Deprecate `.cowork/skills/update-kanji-list.md`

- [x] Insert deprecation notice at the very top of the file (before the `# Skill:` heading):
  ```
  > **DEPRECATED** — superseded by `kanji-headers` (Steps 2 & 5) and the new `kanji-file`
  > skill. Do not invoke directly. Retained for reference only until confirmed safe to delete.
  ```
- [ ] Do not alter any other content in the file.

---

## Task 4 — Slash command stubs

- [x] If `.claude/commands/kanji-headers.md` does not exist → create minimal stub invoking
  the `kanji-headers` skill.
- [x] Create `.claude/commands/kanji-file.md` — minimal stub invoking the `kanji-file` skill.

---

## Task 5 — Update `.cowork/instructions.md` skills table

- [ ] Add `kanji-file` row to the skills table with its trigger phrase and description.
- [ ] Mark `update-kanji-list` row as DEPRECATED (append note to description).

---

## Self-review checklist (implementer runs after all edits)

- [ ] Re-read `kanji-headers.md`: no mention of `update-kanji-list`; no destructive
  `# Summary` replacement rule anywhere in the file; Workflow has exactly five steps as designed.
- [ ] Re-read `kanji-file.md`: all six steps present; cycle guard documented in Step 3; lesson
  link guard (`#` check) documented in Step 4; section placement order present.
- [ ] Re-read `update-kanji-list.md`: deprecation notice is the first content in the file;
  no other content changed.
- [ ] Confirm slash command stubs exist for both `kanji-headers` and `kanji-file`.
- [ ] Confirm `.cowork/instructions.md` skills table has `kanji-file` row and deprecated note
  on `update-kanji-list`.
- [ ] Confirm no lesson files, `# Summary` sections, `<!--ID:-->` lines, or `TARGET DECK`
  lines were touched.
