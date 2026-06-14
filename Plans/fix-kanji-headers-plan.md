# Fix kanji-headers: new architecture with `kanji-file` skill

## Goal

Redesign the `kanji-headers` skill and introduce a new `kanji-file` skill, splitting
responsibilities cleanly: `kanji-headers` owns the lesson file (header formatting, wikilinks,
KanjiList.md); `kanji-file` owns a single kanji reference file (mnemonic, parts, link
verification, bare link migration). `update-kanji-list` is deprecated — its logic is absorbed
into the two new skills.

The previous fix (non-destructive header correction) is already in place in `kanji-headers.md`.
This plan extends that foundation rather than replacing it.

## Approach

`kanji-headers` is trimmed to its core job: iterate `##` headers in the lesson file, guarantee
kanji reference files exist (creating them if needed), fix header format, write wikilinks, and
update `KanjiList.md`. All per-kanji-file work (web fetch, mnemonic, parts, link verification,
bare link migration) is delegated to the new `kanji-file` skill. `kanji-file` is independently
runnable so the user can invoke it on a single kanji without going through a lesson file.
`update-kanji-list.md` is not deleted but receives a deprecation notice at the top.

## Steps

1. **Rewrite `.cowork/skills/kanji-headers.md`** — new workflow:

   - **Step 1** — Read the lesson file.
   - **Step 2** — For each kanji found in existing `##` headers:
     - Search `Caligraphy/Kanji/` and `Caligraphy/Primitives/` recursively for a file whose name
       starts with the kanji character.
     - If found → record in `kanji-file-map`; call `kanji-file` skill on that file.
     - If not found → create the file using `kanji-meaning` naming convention (no spaces around
       hyphen: `漢-meaning.md`); then call `kanji-file` skill on it.
   - **Step 3** — Fix `##` header line formats in the lesson file in-place
     (`## Kanji - meaning・kun・on` template). Do NOT touch content inside blocks (reading lines,
     `---`, `## Parts`, etc.). `# Summary` and everything below strictly off-limits.
   - **Step 4** — Write verified wikilinks under each `##` header (files now guaranteed to exist
     from Step 2).
   - **Step 5** — Update `KanjiList.md` — append any new kanji characters (one per line, no
     duplicates). This is the last write operation.

   Remove or make no reference to `update-kanji-list` in the revised file. Remove the
   destructive "replace everything from `# Summary` onward" rule if any trace remains.
   Update frontmatter `description` to reflect the new design.

2. **Create `.cowork/skills/kanji-file.md`** — new standalone skill:

   **Trigger:** user says "kanji-file [character]" or it is called by `kanji-headers`.

   **Input:** a single kanji character (e.g. `近`) or the full path to an existing kanji file.

   **Steps inside the skill:**

   - **Step 1 — Web fetch** from `kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html`.
     Extract `id="idFeldErklar"` (mnemonic phrase) and `id="idFeldErlaeter"` (component
     explanation). Cache both in a `fetch-result` map for this run.
     On fetch failure: skip `### Mnemonic` and `### Parts` for this kanji; log a warning; do
     not abort.

   - **Step 2 — Write/update `### Mnemonic` section** in the kanji file.
     Write the Explanation text first, then the Mnemonic phrase below it on a new line.
     If the section already exists, overwrite it.

   - **Step 3 — Write/update `### Parts` section.**
     Parse component characters from the Explanation text using positional keywords
     (`Left:`, `Right:`, `Top:`, `Bottom:`, etc.). For each component character:
     1. Search `Caligraphy/Primitives/` recursively for a file whose name starts with that
        character. If found, use it.
     2. If not found, search `Caligraphy/Kanji/` recursively.
     3. If still not found, create a new file in `Caligraphy/Primitives/` using
        `character-name.md` naming (no spaces around hyphen; English name taken from the word
        immediately following the character in the Explanation text). Then recursively call
        `kanji-file` on the new component file.
     Write wikilinks to resolved component files under `### Parts` (exact filename, no path,
     de-duplicated).

   - **Step 4 — Link verification.** Scan ALL wikilinks in the file:
     - Links containing `#` (e.g. `[[UN5KL5#生 - be born…]]`) → lesson occurrence links →
       NEVER TOUCH.
     - Links without `#` → component or kanji reference links → verify against actual filename:
       Search `Caligraphy/Kanji/` and `Caligraphy/Primitives/` for a file starting with the
       linked kanji character. If the link text does not match the actual filename (e.g. link is
       `[[貝 - muszla]]` but file is `貝-muszla.md`) → fix the link to match the actual filename.
     Note: `### Parts` may not exist in legacy files — scan all wikilinks regardless of section.

   - **Step 5 — Bare link migration.** Collect wikilinks not under any named `##` section. Move
     them under `## Occurences` (create the section if absent). Preserve all existing section
     contents.

   - **Step 6 — Consistency check.** Verify `## Occurences` exists; verify all links under
     `## Occurences` and `### Parts` are valid wikilinks. Log warnings for malformed lines; do
     not auto-fix plain text prose.

   Section placement order in the kanji file:
   ```
   [title line]
   ## Occurences
   ### Parts
   ### Mnemonic
   ```

   **Slash command:** create `.claude/commands/kanji-file.md` stub.

3. **Add deprecation notice to `.cowork/skills/update-kanji-list.md`** — insert at the very top
   of the file (before the `# Skill:` heading):

   ```
   > **DEPRECATED** — superseded by `kanji-headers` (Steps 2 & 5) and the new `kanji-file`
   > skill. Do not invoke directly. Retained for reference only until confirmed safe to delete.
   ```

   Do not delete the file or alter any other content.

4. **Create `.claude/commands/kanji-headers.md`** — slash command stub (only if it does not
   already exist).

5. **Update `CLAUDE.md` / `.cowork/instructions.md` skills table** — add `kanji-file` row;
   mark `update-kanji-list` as deprecated.

## Risks

- `kanji-headers` currently delegates to `update-kanji-list` for KanjiList.md and kanji file
  creation. After this change, both responsibilities live in `kanji-headers` and `kanji-file`
  respectively. Any existing prompt history that calls `update-kanji-list` directly will still
  work (the file is retained), but the skill is no longer the authoritative path.
- Recursive `kanji-file` calls for component creation could produce deep chains on kanji with
  many nested primitives. The skill must detect cycles (a component referencing itself or an
  already-in-progress character) to avoid infinite recursion.
- Lesson links (`[[UN5KL5#…]]`) must never be modified — the `#` check in Step 4 is the guard.
  Make this rule explicit and tested in the self-review checklist.
- `Caligraphy/Kanji/` contains subdirectories (e.g. `木/`) — all searches must use recursive
  glob (`**/漢*`), not flat lookup.
- No lesson files, `# Summary` sections, `<!--ID:-->` lines, or `TARGET DECK` lines are touched
  by either skill.
