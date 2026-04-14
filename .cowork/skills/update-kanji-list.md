# Skill: update-kanji-list

## Purpose
Search files with calligraphy lessons to update the list of known kanji, then create or update individual kanji files used for cross-referencing.

## Trigger phrases
User says: "Update kanji list [file]"

## Input
- `[file]` — a calligraphy lesson file (e.g. UNK5L9-Basic-Nouns)
- `[KanjiList.md]` — file with all known kanji, in ObsidianJP root directory

## Step 1 — Update KanjiList.md

Extract all kanji characters from `##` headers in `[file]`.
For each kanji:
- If already in `KanjiList.md`, skip
- If not, add it

## Step 2 — Update individual kanji files

For each kanji in `[file]`, derive its header text (e.g. `電 - electricity・デン`).

### File name rule
`Kanji-meaning.md` — kanji character + hyphen + first English word of the meaning.

Examples:
- `電 - electricity・デン` → `電-electricity.md`
- `方 - direction, way・かた、-がた・ホウ` → `方-direction.md`
- `社 - company, shrine・シャ、-ジャ` → `社-company.md`

### File location
`Kaligrafia/Kanji/[filename].md` (flat, no subdirectories)

### Check if kanji file exists
Search `Kaligrafia/Kanji/` (including subdirectories) for any file whose **filename starts with the kanji character** — regardless of what follows. Do not require an exact title match.

Examples: `電` matches `電-electricity.md`, `電-electricity-old.md`, `雨/電-electricity.md` etc.

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

---

**If NO matching file EXISTS:**

Create `Kaligrafia/Kanji/[kanji]-[first-meaning-word].md` with this structure:

```
電 - electricity・デン

## Occurences
[[UNK5L9-Basic-Nouns#電 - electricity・デン]]
```

Note: the first line is the plain header text (no `##`), copied exactly from the source lesson header.

---

Process all kanji from the lesson file before finishing.
