---
name: extract-vocabulary
description: >
  Extract vocabulary lines from lesson files into a single shared file at
  Vocabulary/words-extracted.md. Covers single words from # ごい and all lines
  from # ひょうげん. Idempotent: skips a lesson if its block already exists in the
  output file. Does NOT run fill-templates — lines are copied raw.
  Trigger: "extract vocabulary from <lesson>", "extract vocab N5", "update vocabulary file".
---

# Extract Vocabulary Skill

## Trigger

User says any of:

- "extract vocabulary from UN5GL14"
- "extract vocabulary from <lesson code>"
- "extract vocab N5" (or any JLPT level)
- "extract vocab from all N4 lessons"
- "update vocabulary file"

If user references a lesson by code only (e.g. `UN5GL14`), find the file under
`JPLessons/Udemy/N<level>/Gramatyka/` — match by prefix, ignore trailing description
in filename.

---

## Workflow

### 1. Find the target lesson file(s)

- **Single lesson** — resolve the lesson code to its full path under
  `JPLessons/Udemy/N<level>/Gramatyka/`. The level is the digit in the code
  (e.g. `UN5GL14` → `N5`). Match by filename prefix; ignore trailing words.
- **Batch level** — list all files matching `JPLessons/Udemy/N<level>/Gramatyka/UN<level>GL*.md`.
  Process **one file at a time** — do not load multiple lesson files into context
  simultaneously.
- **"update vocabulary file"** — scan all levels; process files that do not yet have a
  block in `Vocabulary/words-extracted.md`.

### 2. Idempotency check (per lesson)

Before reading a lesson file, check whether `Vocabulary/words-extracted.md` already
contains a line `## <lesson-code>` (exact match). If yes, skip this lesson entirely and log:

```
[SKIP] <lesson-code>: block already present in words-extracted.md
```

### 3. Read up to `# Summary` only

Never read past the `# Summary` line. Use:

```bash
awk '/^# Summary$/{exit} {print}' "$LESSON_FILE"
```

Pass only this slice to all subsequent parsing steps.

### 4. Extract from `# ごい`

Find the `^# ごい` heading. Collect lines until the next `^# ` heading of the same level.

Extraction rules for `# ごい`:

| Tag | Rule |
|-----|------|
| `#wc` | Include ALL verb lines — no filtering |
| `#wp` | Include ALL adjective lines — no filtering |
| `#w`  | Include only **single-word** entries — see heuristic below |

**Single-word heuristic for `#w` in `# ごい`:**

A line is a single word if the Japanese field (before the first ` - `) contains 1–3 tokens
and shows no sign of being a full sentence or conjugated phrase. Indicators that a line
should be **skipped** (it is a sentence or expression, not a single word):

- Contains a verb in て-form, た-form, ない-form, ます-form, or similar conjugation
- Contains two or more independent words separated by a particle (e.g. `を`, `に`, `で`,
  `が`, `は`, `も`, `と`, `で`)
- Contains a full sentence-ending element (`です`, `ます`, `だ`, `か`, `ね`, `よ`)
- Contains more than approximately 6–8 characters in the Japanese field

When in doubt (borderline case), include the line — misclassifications are cosmetic and
do not cause data loss.

### 5. Extract from `# ひょうげん`

Find the `^# ひょうげん` heading. Collect lines until the next `^# ` heading of the same
level (or end of the pre-Summary slice).

Extraction rules for `# ひょうげん`:

Include **all** `#w`, `#wc`, and `#wp` lines regardless of length or whether the entry
is a single word or a full expression. Expressions and sentences from this section are
always included.

### 6. Preserve lines exactly as written

Do not reformat, reorder, or translate any extracted lines. Copy the full raw line
including the tag (`#w`, `#wc`, `#wp`), Japanese text, reading, and translation.

### 7. Ensure the output file exists

Output file: `Vocabulary/words-extracted.md`

Full path:
```
/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/Vocabulary/words-extracted.md
```

If the file does not exist, create it with this header before appending:

```markdown
# Extracted Vocabulary

Lines extracted raw from lesson files. Not formatted by fill-templates.
Each lesson block is idempotent — a lesson is processed only once.
```

### 8. Append the lesson block

Append the following block to the end of `Vocabulary/words-extracted.md`:

```markdown
## <lesson-code>

<extracted lines, one per line>
```

Example:

```markdown
## UN5GL14

#w 病院 (びょういん) - hospital
#wc 使う (つかう) - to use
#wp 難しい (むずかしい) - difficult
#w 入院(する) (にゅういん) - hospitalization / to be hospitalized
```

Leave a blank line between the `## <lesson-code>` heading and the first entry, and a
blank line after the last entry before the next block (or end of file).

### 9. Per-lesson completion report

After processing each lesson file, print a compact report:

```
UN5GL14 — extracted 12 lines (8 from ごい, 4 from ひょうげん)

  Appended to: Vocabulary/words-extracted.md
```

Or if skipped:

```
UN5GL14 — [SKIP] block already present in words-extracted.md
```

### 10. Batch mode rule

When processing multiple files (e.g. "extract vocab N5"):
- Process one lesson file at a time.
- Report per lesson after each.
- Do not load two lesson files into context simultaneously.

---

## What is NOT done during extraction

- Do not run `fill-templates` — lines are copied raw to keep context small.
- Do not translate vocabulary lines.
- Do not reformat tags or readings.
- Do not generate Anki cards.
- Do not write a `TARGET DECK` line to the output file.

---

## Never touch

- Lesson files under `JPLessons/` — read-only; never write to them
- Never read past `# Summary` in any lesson file
- `<!--ID: -->` lines — do not add, remove, or shift them anywhere
- `TARGET DECK` lines — do not write this to any file
- Other skill files or `.cowork/instructions.md` — do not modify
- Do not run `git push` or any remote git operation
- Do not trigger or load the `fill-templates` skill during extraction
