# Skill: update-kanji-list

## Purpose
Search files with calligraphy lessons to update list of known kanjis that will be used to add #k tags to #w, #wc, #wp templates by other skills.

## Trigger phrases
User says: "Update kanji list [file]"

## Input
- `[file]` — a calligraphy lesson file (e.g. UNK5L9-Basic-Nouns)
- `[KanjiList.md]` — file with all known kanjis, in ObsidianJP root directory

## Step 1 — Update KanjiList.md

Extract all kanji characters from headers in `[file]` (every `##` header contains one kanji).
For each kanji:
- If it is already in `KanjiList.md`, skip it
- If not, add it to `KanjiList.md`

## Step 2 — Update individual kanji files

For each kanji found in `[file]`, determine its full header text (e.g. `電 - electricity・デン`).

### Kanji file name rule
Derive the filename from the header by removing `・`: e.g. `電 - electricity デン.md`

### Check if kanji file exists
Look under `Kaligrafia/Kanji/` (including subdirectories).

---

**If the file EXISTS:**

1. Add a new section at the end of the kanji file with this structure:
   ```
   ## Kaligrafia[LessonID] > [full header text]
   [[lesson-filename]]
   ```
   Where:
   - `[LessonID]` = the lesson identifier from the source file name (e.g. `UNK5L9`)
   - `[full header text]` = the full kanji header, e.g. `電 - electricity・デン`
   - `[[lesson-filename]]` = Obsidian wikilink to the source lesson file

   Example:
   ```
   ## KaligrafiaUNK5L9 > 電 - electricity・デン
   [[UNK5L9-Basic-Nouns]]
   ```

---

**If the file DOES NOT EXIST:**

1. Create a new file at `Kaligrafia/Kanji/[filename].md`
2. First line: `# [full header text]` — e.g. `# 電 - electricity・デン`
3. Then add the same section as in the EXISTS case (steps above)

   Full new file example:
   ```
   # 電 - electricity・デン

   ## KaligrafiaUNK5L9 > 電 - electricity・デン
   [[UNK5L9-Basic-Nouns]]
   ```

---

Process all kanji from the lesson file before finishing.
