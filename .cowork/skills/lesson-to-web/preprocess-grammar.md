---
name: preprocess-grammar
description: >
  Mechanically post-process grammar files under grammar-index/grammar/: remove
  #w/#wc/#wp tag prefixes, detect and translate Polish prose, convert trailing
  furigana to inline format, fix typos. Runs scripts where available; no user
  gates. Trigger: "preprocess grammar <file>" or called from extract-grammar.
---

# Preprocess Grammar Skill

## Trigger

- "preprocess grammar `<slug>`" — filename without `.md`
- "preprocess grammar grammar-index/grammar/`<slug>`.md" — full relative path
- (called automatically from extract-grammar step 10 with a list of file paths)

---

## Workflow

Process each file in order. Apply all steps to one file before moving to the next.

Before starting any step, read the file's frontmatter. If `proofread: true` is already set, pause:

```
<slug>.md already has proofread: true. Re-process anyway? (yes / no)
```

If no: skip all steps for that file and note it as skipped in the handoff summary.
If yes: proceed with all steps, including running the script in Step 1.

---

### Step 1 — Remove vocabulary tag prefixes

```bash
python3 .claude/scripts/grammar-process.py <file> [<file> ...]
# Preview without writing:
python3 .claude/scripts/grammar-process.py --dry-run <file>
```

If the script is unavailable, scan every line manually. Strip `#w `, `#wc `, or `#wp ` prefix from lines that start with one; keep everything after the tag and space.

Examples:
- `#w 自分の意見 (じぶん, いけん) - one's own opinion` → `自分の意見 (じぶん, いけん) - one's own opinion`
- `#wc 出来る（でき）- to be built` → `出来る（でき）- to be built`
- `#wp 難しい (むずかしい) - difficult` → `難しい (むずかしい) - difficult`

---

### Step 2 — Language consistency (Polish detection)

Scan all prose sections: gloss line (`> ...`), `## Structure`, `## Meaning`, `## Examples`, `## Notes`, `## Use Cases`, numbered use-case sections, and link labels inside `## Sub-topics`.

Detection threshold: at least 2 signals must be present.
- Polish diacritics: ą ę ó ś ź ż ć ń ł (each distinct diacritic = 1 signal)
- Common Polish words: jest, są, się, nie, lub, oraz, przez, które, który, też, już, można, należy (each match = 1 signal)

#### Prose sections

If Polish detected in any section other than `## Sub-topics`: translate to English in-place.

Never translate:
- Japanese text (kana, kanji)
- Frontmatter field values

#### Sub-topics link labels

For each Polish-looking link label:
1. Do NOT translate automatically.
2. Ask: `This link label appears to be Polish: '<label>'. What should the English name be?` — wait for answer.
3. Present: `Rename the linked file from '<current-slug>.md' to '<suggested-english-slug>.md'. This must be done manually — renaming affects all files that link to it.`
4. Continue without blocking on the rename.

---

### Step 3 — Furigana format conversion

```bash
python3 .claude/scripts/furigana-convert.py <file> [<file> ...]
# Preview:
python3 .claude/scripts/furigana-convert.py --dry-run <file>
```

Converts trailing-reading format to inline furigana.

**Input:** `明日の仕事のしりょうですね（あした、しごと）`
**Output:** `明日(あした)の仕事(しごと)のしりょうですね`

Algorithm:
1. Detect lines with a trailing parenthesised reading list — `（r1、r2）` (fullwidth) or `(r1, r2)` (ASCII).
2. Strip the trailing list; split into ordered readings.
3. Scan left-to-right for kanji-words: maximal runs of CJK Unified Ideographs (U+4E00–U+9FFF).
4. Match readings to kanji-words in order; insert `kanji-word(reading)` inline using ASCII parentheses.
5. Remove the trailing reading list.
6. **Mismatch warning**: if reading count ≠ kanji-word count, log and leave line unchanged:
   `[WARN] <file>: reading count mismatch on line: "<line>" — left unchanged`
7. Lines already in inline format: skip.
8. Lines with no kanji: skip silently.
9. Lines inside `## Structure` or `### Structure`: skip — parentheses are grammatical notation there.

---

### Step 4 — Typos and grammar mistakes

Review all English prose for spelling and grammar errors. Fix silently — no user approval needed. Log each fix.

---

## Handoff summary

After processing all files, print:

```
preprocess-grammar — N files processed

  grammar-index/grammar/<slug>.md
    Tags removed: 0
    Furigana: 3 lines converted
    Furigana warnings: 0
    Language: no Polish found
    Typos: 1 fixed ("listenner" → "listener")
```

Then ask:

```
Run review-grammar on these files? (yes / no / all)
```

- **yes** — load `.cowork/skills/lesson-to-web/review-grammar.md` and pass the file list.
- **no** — end the skill.
- **all** — load review-grammar, instructing it to continue through structure-grammar and see-also-grammar without prompting at each handoff.

---

## Never touch

- `<!--ID: -->` lines
- `TARGET DECK` lines
- Japanese text — never translate kana or kanji
- Files outside `grammar-index/grammar/`
- Lesson files under `JPLessons/`
- Other skill files or `.cowork/instructions.md`
- Do not run `git push` or any remote git operation
