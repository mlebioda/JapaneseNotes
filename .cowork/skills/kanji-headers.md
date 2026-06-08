---
name: kanji-headers
description: >
  Extract kanji from a file headers and write structured markdown headers directly into a target
  file. Use this skill whenever the user provides a filename — whether
  they say "kanji headers", or similar. Writes kanji headers plus
  a # Summary section at the end of the file.
---

# Kanji Headers Skill

## Workflow

User provides: a **filename** (target file in the vault).

1. Read the target file
2. Extract all kanji from the file Headers. For each kanji, search `Caligraphy/Kanji/**/漢*` and record the result in a per-run map:
   ```
   kanji-file-map[漢] = "漢-kanji,china"   # found — filename without .md
   kanji-file-map[電] = null               # not found
   ```
   Build this map as you perform the searches so no search is repeated.
3. Write the formatted kanji blocks to the file, followed by `# Summary`
4. Save the file
5. Run the `update-kanji-list` workflow on the same file, passing `kanji-file-map` as the `[kanji-file-map]` input (load `.cowork/skills/update-kanji-list.md` and follow its instructions)

## File output structure

```
[existing file content, if any]

## Kanji - meaning・kun・on
[[Kanji-meaning]]

**(reading 1)**

**(reading 2)**

---

## Kanji - meaning・kun・on
[[Kanji-meaning]]

...

---

# Summary
```

If the file already has a `# Summary` line, replace everything from that line onward with the new kanji blocks + `# Summary`. Never modify content above the existing `# Summary`.

### Link under each header

Immediately after each `## header` line, there must be a wikilink to the corresponding kanji file in `Caligraphy/Kanji/`. Always verify the link — whether adding a new one or correcting an existing one.

**File names in `Caligraphy/Kanji/` are not consistent and may be in subdirectories** — do not guess the name or path from a pattern. Instead, search recursively under `Caligraphy/Kanji/` for any file whose name **starts with the kanji character** and use the exact filename (without `.md`) as the wikilink.

If a wikilink already exists under the header, verify it matches the actual filename found by the search. If it does not match, correct it.

Use a recursive glob: `Caligraphy/Kanji/**/漢*` — this matches both `Caligraphy/Kanji/漢-china.md` and `Caligraphy/Kanji/艹/漢-kanji,china.md`.

The wikilink uses only the **filename** (no path): `[[漢-kanji,china]]`.

Example lookup for 漢: search `Caligraphy/Kanji/**/漢*` → result is `Caligraphy/Kanji/艹/漢-kanji,china.md` → use `[[漢-kanji,china]]`.

If no matching file exists, use `[[Kanji-firstMeaningWord]]` as a placeholder — it will be created by the `update-kanji-list` skill.

> **Note:** When `update-kanji-list` creates a new file for a kanji that had no existing file, the wikilink written by `kanji-headers` may not yet match the actual filename. After `update-kanji-list` completes, re-derive the wikilink from the actual filename that was created (post-creation), not from the placeholder.

## Header format rules

- Structure: `## Kanji - meaning・kun・on`
- Use `・` (middle dot, U+30FB) as separator between sections
- If the kanji has **no kun reading**, omit it: `## 電 - electricity・デン`
- If the kanji has **no on reading**, omit it: `## 何 - what・なに、なん`
- Multiple readings in the same category are comma-separated in the header: `## 家 - house・いえ、や・カ、ケ`

## Content block rules

- Each reading goes on its **own line**, wrapped in bold parentheses: `**(くるま)**`
- Kun readings come first, then on readings — matching the order in the header
- Separate each kanji block with `---`
- Keep hyphens on variant readings: `**(-がた)**`, `**(-ゴク)**`
- Keep verb inflection as-is: `**(あ（う）)**`

## Scope boundary

`kanji-headers` writes `## Kanji - …` headers and reading blocks only. It does **not** touch `## Parts` blocks or component (primitive) files. Those are handled exclusively by `update-kanji-list` Step 3 (component linking). If a kanji file already contains a `## Parts` section, leave it untouched.

## Extraction from images

Read each row carefully:
- Column 1: Kanji character
- Column 2: Kun-yomi (hiragana) — may be empty
- Column 3: On-yomi (katakana) — may be empty
- Column 4: Stroke count (ignore)
- Column 5: English meaning

Produce all kanji in the order they appear in the table.

## Example output (end of file)

```markdown
## 車 - car・くるま・シャ
[[車 - car]]          ← exact filename found in Caligraphy/Kanji/

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

# Summary
```

Note: the wikilink format varies per file — always use the actual filename.
