---
name: extract-grammar
description: >
  Extract grammar points from a lesson file's 文法 section into standalone
  published files under grammar-index/grammar/. Each grammar point becomes one file named
  <anchor-slug>.md, then each new file is classified into
  grammar-index/ topic files (creating new topic files when needed).
  Idempotent: skips grammar-index/grammar files that already exist.
  Trigger: "extract grammar from <lesson>" or "extract grammar from all N5 lessons".
---

# Extract Grammar Skill

## Trigger

User says any of:

- "extract grammar from UN5GL14"
- "extract grammar from <lesson code>"
- "extract grammar from all N5 lessons"
- "extract grammar from all N4 lessons" (or any JLPT level)

If user references a lesson by code only (e.g. `UN5GL14`), find the file under
`JPLessons/Udemy/N<level>/Gramatyka/` — match by prefix, ignore trailing description
in filename.

---

## Workflow

### 1. Find the target lesson file(s)

- **Single lesson** — resolve the lesson code to its full path under
  `JPLessons/Udemy/N<level>/Gramatyka/`. The level is the digit in the code
  (e.g. `UN5GL14` → `N5`). Match by filename prefix; ignore any trailing words.
- **Batch level** — list all files matching `JPLessons/Udemy/N<level>/Gramatyka/UN<level>GL*.md`.
  Process **one file at a time** — do not load multiple lesson files into context
  simultaneously.

### 2. Read up to `# Summary` only

Never read past the `# Summary` line. Use:

```bash
awk '/^# Summary$/{exit} {print}' "$LESSON_FILE"
```

Pass only this slice to all subsequent parsing steps.

### 3. Locate the `# 文法` section

Find the `^# 文法` heading. Collect everything from that heading until the next `^# `
heading of the same level (or end of the pre-Summary slice).

If no `# 文法` section exists in the file, skip this file and log:
`[SKIP] <lesson-code>: no # 文法 section found`

### 4. Split into individual grammar points

Split the 文法 section on `## ` headings. Each `## Heading` is one independent grammar
point. Apply the same promotion rule used by `summarize-grammar`:

- If a `##` heading has only `###` subheadings with no prose of its own, treat each
  `###` as a top-level grammar point instead.
- If a `##` has both prose and `###` children, use the `##` as the grammar point
  (do not promote).
- Skip any heading that is clearly a vocabulary gloss rather than a grammar pattern
  (e.g. a single word with a translation, no structural rule).

For each grammar point, collect:
- `heading` — the exact heading text (preserve kanji, kana, punctuation, spaces)
- `body` — everything below the heading until the next same-level heading

### 5. Normalise the slug

Apply this rule to the heading text to produce the anchor slug:

1. Lowercase the text.
2. Strip all non-ASCII characters (removes kanji, kana, `〜`, `・`, `（`, `）`, etc.).
3. Strip punctuation except `-` (removes `.`, `,`, `!`, `?`, `(`, `)`, etc.).
4. Replace one or more spaces with a single `-`.
5. Strip leading and trailing `-`.
6. If the result is empty (heading was entirely non-ASCII), use the heading's
   position index: `point-1`, `point-2`, etc.

Examples:
- `Vないでください` → strip non-ASCII → `` → empty → use `point-1`
- `V + て-form (request)` → lowercase → strip non-ASCII → `+ -form (request)` →
  strip punctuation except `-` → `+ -form request` → collapse spaces → `-form-request`
  → strip leading `-` → `form-request`
- `がんばって！Let's do our best` → `lets-do-our-best`
- `Particle が vs は` → `particle-ga-vs-ha` (non-ASCII stripped, spaces → `-`)
  Note: Latin letters in the heading (e.g. `V`, `N`, `Adj`) are kept as-is through
  the lowercasing step.

The full output filename is: `grammar-index/grammar/<anchor-slug>.md`

Example: lesson `UN5GL14`, heading `Vないでください`, slug `point-1` →
`grammar-index/grammar/point-1.md`

Better example: lesson `UN5GL14`, heading `V (plain form) + N (noun modifier)` →
slug `v-plain-form-n-noun-modifier` → `grammar-index/grammar/v-plain-form-n-noun-modifier.md`

### 6. Idempotency check

Before creating each file:

```
if grammar-index/grammar/<slug>.md already exists → skip, log:
  [SKIP] grammar-index/grammar/<slug>.md already exists
```

Do not overwrite existing files.

### 7. Create the standalone grammar file

Populate the file with the agreed format:

```
---
lesson: <lesson-code>
pattern: <exact heading text>
topic_slug: ""
level: <N5 | N4 | N3 | N2 | N1>
proofread: false
---

# <exact heading text>

> [One-line English gloss of what the pattern expresses — derive from body text]

## Structure

[Formation rule — extract or derive from body text; e.g. "Verb (ない-form) + でください"]

## Meaning

[Explanation extracted from the lesson file body — in English]

## Examples

[Example sentences extracted from the lesson file body]

## Notes

[Leave empty — populated during internet enrichment step (Step 1.2)]
```

Rules for populating each section:
- `lesson` — the lesson code (e.g. `UN5GL14`)
- `pattern` — the exact heading text, unchanged
- `topic_slug` — leave as empty string `""` for now; filled in step 8
- `level` — from the lesson path (`N5`, `N4`, etc.)
- `proofread` — always `false` on creation
- One-line gloss after `# <heading>` — derive from the body text; keep it to one line
- `## Structure` — the formation rule. If the body has a clear structural description or
  bullet, use it. If not, derive from examples.
- `## Meaning` — the explanation text from the body, in English. If the body is in Polish,
  translate to English.
- `## Examples` — all example sentences found in the body. Preserve Japanese + any
  translation present.
- `## Notes` — always leave empty on creation.

### 8. Classify into grammar-index topics

Run this step after all grammar-index/grammar/ files for the lesson are written. Only process files
that were **Created** in step 7 — skip files that were already skipped in step 6.

**8a. Read existing topic file list**

```bash
ls grammar-index/*.md | grep -v '_index.md' | grep -v '^index.md$'
```

Read each file's `> <description>` line to understand what each topic covers.
This is the current taxonomy — respect it.

**8b. Plan all classifications before writing**

For each newly created grammar point, decide which topic file(s) it belongs to.
Write out the full plan (grammar point → topic file(s)) before touching any file.
This catches misclassifications before they land.

Apply these rules (same as `summarize-grammar`):
- Bias toward existing topic files.
- A point may appear in up to 3 topic files if it genuinely fits more than one.
- Create a new topic file only when no existing topic fits AND the new name is broad
  enough to attract future lessons (not a one-off).
- Cap at 3 topics per point. If more than 3 seem to fit, pick the strongest 3.

**8c. Update topic files**

For each (grammar point, topic file) pair:

- **Dedup**: skip if `grammar-index/grammar/<slug>)` already appears in the file.
- **Entry format**: `- [<pattern>](https://mlebioda.github.io/JapaneseNotes/grammar-index/grammar/<slug>) · <level>`
  where `<pattern>` is the exact heading text from the grammar point. Use full absolute
  URLs — NOT wikilinks or relative paths. This ensures the link works on GitHub Pages.
- **Exists**: insert immediately before `## See also` (or append to end of `## Entries`
  if no `## See also`). Use Python:

  ```python
  with open(path) as f: content = f.read()
  entry = "- [同じ - same](https://mlebioda.github.io/JapaneseNotes/grammar-index/grammar/same) · N5"
  if "## See also" in content:
      content = content.replace("\n## See also", "\n" + entry + "\n\n## See also", 1)
  else:
      content = content.rstrip() + "\n" + entry + "\n"
  with open(path, "w") as f: f.write(content)
  ```

- **New topic file**: create from the template in **Topic file template** below.

**8d. Fill `topic_slug` in each grammar-index/grammar/ file**

After classifying, patch the `topic_slug: ""` field in the frontmatter of each newly
created grammar-index/grammar/ file:
- Single topic: `topic_slug: "reasons-causes"`
- Multiple topics (YAML list): `topic_slug: ["reasons-causes", "particles-de"]`

**8e. Update `_index.md`**

Only if at least one new topic file was created in step 8c. Regenerate
`grammar-index/_index.md` from the current state of `grammar-index/`, following the
format in **`_index.md` format** below.

---

### 9. Batch mode rule

When processing multiple files (e.g. "all N5 lessons"):
- Process one lesson file at a time.
- After finishing all grammar points from one lesson (steps 7 and 8), report a summary
  for that lesson, then move to the next.
- Do not load two lesson files into context simultaneously.

### 10. Per-lesson completion report

After processing each lesson file, print a compact report:

```
UN5GL14 — 6 grammar points processed

  Created:  grammar-index/grammar/point-1.md  → requests-commands
  Created:  grammar-index/grammar/v-plain-form-n-noun-modifier.md  → sentence-structure, verb-forms
  Created:  grammar-index/grammar/te-form-request.md  → 🆕 verb-te-form (new topic file)
  Skipped:  grammar-index/grammar/point-3.md (already exists — not re-classified)
```

---

## Topic file template

Use when creating a new grammar-index topic file (step 8c):

```markdown
# <Topic Name>

> <One-line description of what this topic covers — your own words>

## Entries

- [[grammar-index/grammar/<slug>]] · <level>

## See also

- [[<related-topic>]] — <short reason>
```

- Filename: kebab-case English, descriptive, reusable across future lessons.
  Good: `reasons-causes.md`, `verb-te-form.md`, `particles-wa-ga.md`.
  Bad: `kara.md`, `because-only.md`, `n5-particles.md`.
- Title: human-readable derivation of the filename.
- Description: one sentence explaining when to look here.
- "See also": 1–2 wikilinks to existing related topics if obvious; otherwise omit.

---

## `_index.md` format

Lives at `grammar-index/_index.md`. Groups topic files into a fixed high-level taxonomy:

- **Verbs** — `verb-*` topic files
- **Adjectives** — `adjectives-*` topic files
- **Particles** — `particles-*` topic files
- **Patterns** — sentence-level patterns: reasons, comparisons, suggestions, conditionals, etc.
- **Forms & Counters** — counters, time expressions, numbers
- **Other** — anything that doesn't fit the above

```markdown
# Grammar Index

## Verbs

- [[verb-te-form]] — <description from file's > line>

## Particles

- [[particles-wa-ga]] — <description>

## Patterns

- [[reasons-causes]] — <description>

(etc. — omit empty groups)
```

---

## Slug normalisation — quick reference

| Input character type | Action |
|---|---|
| Latin letters (A–Z, a–z) | Lowercase and keep |
| Digits (0–9) | Keep |
| Space | Replace with `-` |
| Non-ASCII (kanji, kana, `〜`, `・`, `（`, `）`) | Strip |
| Punctuation (`.`, `,`, `!`, `?`, `(`, `)`, `/`) | Strip |
| Hyphen `-` | Keep |
| Multiple consecutive `-` | Collapse to one `-` |
| Leading or trailing `-` | Strip |
| Empty result | Use positional fallback: `point-1`, `point-2`, etc. |

---

## File placement

All grammar-index/grammar/ output files go in:

```
/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/grammar-index/grammar/
```

All grammar-index topic files go in:

```
/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/grammar-index/
```

If the `grammar-index/grammar/` directory does not exist, create it before writing the first file.

---

## Never touch

- Lesson files under `JPLessons/` — read-only; never write anything to them
- Never read past `# Summary` in any lesson file
- `<!--ID: -->` lines — do not add, remove, or shift them anywhere
- `TARGET DECK` lines — do not touch
- Other skill files or `.cowork/instructions.md` — do not modify
- Do not run `git push` or any remote git operation
- Do not run the `fill-templates` workflow during extraction
