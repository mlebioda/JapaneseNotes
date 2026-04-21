---
name: kanji-headers
description: >
  Extract kanji from a table image and write structured markdown headers directly into a target
  file. Use this skill whenever the user provides a kanji table image and a filename — whether
  they say "extract", "format", "fill", "add headers", or similar. Writes kanji headers plus
  a # Summary section at the end of the file.
---

# Kanji Headers Skill

## Workflow

User provides: an **image** of a kanji table and a **filename** (target file in the vault).

1. Read the target file
2. Create a `.bak` backup (automatic, no confirmation needed)
3. Extract all kanji from the image
4. Write the formatted kanji blocks to the file, followed by `# Summary`
5. Save the file
6. Run the `update-kanji-list` workflow on the same file (load `.cowork/skills/update-kanji-list.md` and follow its instructions)

## File output structure

```
[existing file content, if any]

## Kanji - meaning・kun・on
[[Kanji-meaning]]

(reading 1)

(reading 2)

---

## Kanji - meaning・kun・on
[[Kanji-meaning]]

...

---

# Summary
```

If the file already has a `# Summary` line, replace everything from that line onward with the new kanji blocks + `# Summary`. Never modify content above the existing `# Summary`.

### Link under each header

Immediately after each `## header` line, add a wikilink to the corresponding kanji file in `Kaligrafia/Kanji/`. Use the same naming rule as `update-kanji-list`: `[[Kanji-firstMeaningWord]]`.

Examples:
- `## 電 - electricity・デン` → `[[電-electricity]]`
- `## 方 - direction, way・かた、-がた・ホウ` → `[[方-direction]]`
- `## 社 - company, shrine・シャ、-ジャ` → `[[社-company]]`

Add the link even if the file doesn't exist yet — it will be created by the `update-kanji-list` skill.

## Header format rules

- Structure: `## Kanji - meaning・kun・on`
- Use `・` (middle dot, U+30FB) as separator between sections
- If the kanji has **no kun reading**, omit it: `## 電 - electricity・デン`
- If the kanji has **no on reading**, omit it: `## 何 - what・なに、なん`
- Multiple readings in the same category are comma-separated in the header: `## 家 - house・いえ、や・カ、ケ`

## Content block rules

- Each reading goes on its **own line**, wrapped in parentheses: `(くるま)`
- Kun readings come first, then on readings — matching the order in the header
- Separate each kanji block with `---`
- Keep hyphens on variant readings: `(-がた)`, `(-ゴク)`
- Keep verb inflection as-is: `(あ（う）)`

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
[[車-car]]

(くるま)

(シャ)

---

## 電 - electricity・デン
[[電-electricity]]

(デン)

---

## 何 - what・なに、なん
[[何-what]]

(なに)

(なん)

---

# Summary
```
