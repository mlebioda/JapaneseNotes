---
name: kanji-headers
description: >
  Processes a calligraphy lesson file: ensures a kanji reference file exists in Caligraphy/Kanji/
  or Caligraphy/Primitives/ for each kanji found in ## headers (creating files when missing, then
  calling kanji-file on each), fixes ## header formatting in-place, writes verified wikilinks
  under each ## header, and appends new kanji characters to KanjiList.md. Does not write a
  # Summary section or delegate to update-kanji-list.
---

# Kanji Headers Skill

## Trigger

User provides a **filename** (calligraphy lesson file in the vault). User may say "kanji headers
[file]", or similar.

---

## Workflow

User provides: a **filename** (target lesson file in the vault).

**Step 1 — Read the lesson file.**

Read the target lesson file in full. Identify all `##` header lines that contain a kanji character
(format: `## Kanji - meaning・kun・on`). Collect the list of distinct kanji characters found.

**Step 2 — Ensure kanji reference files exist.**

For each kanji character found in `##` headers:

1. Search `Caligraphy/Kanji/` and `Caligraphy/Primitives/` recursively for any file whose name
   **starts with that kanji character**. Use glob: `Caligraphy/Kanji/**/漢*` and
   `Caligraphy/Primitives/漢*`.
2. Record the result in a `kanji-file-map` (built as searches complete — no search is repeated):
   ```
   kanji-file-map[漢] = "漢-kanji,china"   # found — filename without .md
   kanji-file-map[電] = null               # not found
   ```
3. **If found** → note the exact filename (no `.md`, no path). Then load `.cowork/skills/kanji-file.md`
   and call the `kanji-file` skill on that file.
4. **If not found** → create a new file in `Caligraphy/Kanji/` using the naming convention
   `kanji-meaning.md` (no spaces around hyphen; first English meaning word, lowercase). Example:
   `電-electricity.md`. Then update `kanji-file-map` with the new filename. Then call `kanji-file`
   on the newly created file.

Cycle guard: if a component character is already being processed in the current call stack, skip
the recursive `kanji-file` call and log a warning.

**Step 3 — Fix `##` header line formats in the lesson file in-place.**

For each `##` header line identified in Step 1, verify and correct the format to:

```
## Kanji - meaning・kun・on
```

Rules:
- Use `・` (middle dot, U+30FB) as separator between sections.
- If the kanji has no kun reading, omit it: `## 電 - electricity・デン`
- If the kanji has no on reading, omit it: `## 何 - what・なに、なん`
- Multiple readings in the same category are comma-separated: `## 家 - house・いえ、や・カ、ケ`
- Do NOT touch content inside blocks: reading lines, `---`, `## Parts`, or any other line.
- `# Summary` and everything below it is strictly off-limits — do not read or modify.

**Step 4 — Write verified wikilinks under each `##` header.**

Immediately after each `## header` line, ensure a wikilink exists to the corresponding kanji file.
All files are now guaranteed to exist (from Step 2).

- Use the filename recorded in `kanji-file-map` (exact filename, no path, no `.md`): `[[漢-kanji,china]]`
- If a wikilink already exists under the header, verify it matches the `kanji-file-map` entry. If
  it does not match, correct it.
- Place the wikilink on the line immediately following the `##` header, before any reading lines.

**Step 5 — Update `KanjiList.md`.**

This is the last write operation.

- Read `KanjiList.md` (vault root) in full.
- Collect all kanji characters processed in this run.
- Append any character not already present in `KanjiList.md`, one character per line.
- Never add duplicates.

---

## Header format rules

- Structure: `## Kanji - meaning・kun・on`
- Use `・` (middle dot, U+30FB) as separator between sections
- If the kanji has **no kun reading**, omit it: `## 電 - electricity・デン`
- If the kanji has **no on reading**, omit it: `## 何 - what・なに、なん`
- Multiple readings in the same category are comma-separated in the header: `## 家 - house・いえ、や・カ、ケ`

---

## Content block rules

- Each reading goes on its **own line**, wrapped in bold parentheses: `**(くるま)**`
- Kun readings come first, then on readings — matching the order in the header
- Separate each kanji block with `---`
- Keep hyphens on variant readings: `**(-がた)**`, `**(-ゴク)**`
- Keep verb inflection as-is: `**(あ（う）)**`

---

## Scope boundary

`kanji-headers` writes `## Kanji - …` headers and wikilinks in the lesson file, and updates
`KanjiList.md`. It does **not** touch `## Parts` blocks, `### Mnemonic`, `### Parts`, or
component (primitive) files directly — those are handled exclusively by the `kanji-file` skill.
If a kanji file already contains a `## Parts` section, leave it untouched.

`# Summary` and everything below it in any lesson file is strictly off-limits.

---

## Example output

This shows the target format for correctly formatted blocks, not a from-scratch write.

```markdown
## 車 - car・くるま・シャ
[[車-car]]          ← exact filename found in Caligraphy/Kanji/

**(くるま)**

**(シャ)**

---

## 電 - electricity・デン
[[電-electricity]]    ← exact filename found in Caligraphy/Kanji/

**(デン)**

---

## 何 - what・なに、なん
[[何-what]]           ← exact filename found in Caligraphy/Kanji/

**(なに)**

**(なん)**

---
```

Note: the wikilink format varies per file — always use the actual filename found or created.

---

## Never touch

- Lesson files' `# Summary` sections and everything below (strictly off-limits)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- `## Parts`, `### Parts`, `### Mnemonic` content in kanji files (handled by `kanji-file`)
- Do not run `git push` or any remote git operation
