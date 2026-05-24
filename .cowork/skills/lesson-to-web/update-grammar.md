---
name: update-grammar
description: >
  Post-process grammar files under grammar-index/grammar/. Applies 7 rules in
  order: remove tag prefixes, translate Polish to English, convert trailing furigana
  to inline format, fix typos, check substantive correctness, suggest missing info,
  enforce file structure. Then populates ## See also and sets proofread: true.
  Trigger: "update grammar <file>" or called automatically from extract-grammar.
---

# Update Grammar Skill

## Trigger

User says any of:
- "update grammar <slug>" — where `<slug>` is the filename without `.md` (e.g. `seeking-approval`)
- "update grammar grammar-index/grammar/<slug>.md" — full relative path
- (called automatically from extract-grammar step 10 with a list of file paths)

---

## Workflow

Process each target file in order. Apply all steps below to one file at a time before moving to the next.

Before starting any step on a file, read its frontmatter. If `proofread: true` is already set, pause and notify the user:

```
<slug>.md already has proofread: true. Re-process anyway? (yes / no)
```

If the user says no (or does not respond with yes), skip all steps for that file and note it as skipped in the completion report. If the user says yes, proceed with all steps as normal.

---

### Step 1 — Remove vocabulary tag prefixes

**Reusable script:** Run before starting LLM review:

```bash
python3 .claude/scripts/grammar-process.py <file> [<file> ...]
# Preview without writing:
python3 .claude/scripts/grammar-process.py --dry-run <file>
```

If the script is not available, scan every line manually. If a line starts with `#w `, `#wc `, or `#wp ` (tag followed by a space), strip the tag prefix and keep everything after the tag and space.

Examples:
- `#w 自分の意見 (じぶん, いけん) - one's own opinion` → `自分の意見 (じぶん, いけん) - one's own opinion`
- `#wc 出来る（でき）- to be built` → `出来る（でき）- to be built`
- `#wp 難しい (むずかしい) - difficult` → `難しい (むずかしい) - difficult`

Lines without a tag prefix are left unchanged. This step runs before furigana conversion on the same line.

---

### Step 2 — Language consistency (translate Polish to English)

Scan all prose sections: the gloss line (`> ...`), `## Structure`, `## Meaning`, `## Examples`, `## Notes`, `## Use Cases`, and any numbered use-case sections (`## 1. ...`, `## 2. ...`).

Detection: at least 2 of the following signals must be present before translation is triggered:
- Polish diacritics: ą ę ó ś ź ż ć ń ł (each distinct diacritic counts as one signal)
- Common Polish words: jest, są, się, nie, lub, oraz, przez, które, który, też, już, można, należy (each match counts as one signal)

A single isolated keyword or a single diacritic is not sufficient to trigger translation.

Action: translate detected Polish prose to English in-place.

Never translate:
- Japanese text (kana, kanji)
- Frontmatter field values

---

### Step 3 — Furigana format conversion

Convert trailing-reading format to inline furigana.

**Reusable script:** Prefer calling the saved CLI tool rather than implementing inline:

```bash
python3 .claude/scripts/furigana-convert.py <file> [<file> ...]
# Preview without writing:
python3 .claude/scripts/furigana-convert.py --dry-run <file>
```

The algorithm below documents what the script does.

**Trailing format (input):**
```
明日の仕事のしりょうですね（あした、しごと）
```

**Inline format (output):**
```
明日(あした)の仕事(しごと)のしりょうですね
```

**Algorithm:**
1. Detect lines with a trailing parenthesised reading list — either `（r1、r2）` (fullwidth parens, 、) or `(r1, r2)` (ASCII parens, comma).
2. Strip the trailing list; split into ordered readings.
3. Scan left-to-right for kanji-words: maximal runs of CJK Unified Ideographs (U+4E00–U+9FFF).
4. Match readings to kanji-words in order of left-to-right appearance; insert `kanji-word(reading)` inline using ASCII parentheses `()`.
5. Remove the trailing reading list from the line.
6. **Mismatch warning**: if the number of readings does not equal the number of kanji-words, log a warning and leave the line unchanged:
   ```
   [WARN] <file>: reading count mismatch on line: "<line>" — left unchanged
   ```
7. Lines already in inline format (no trailing list): skip.
8. Lines with no kanji (CJK characters): skip silently — no warning logged.
9. Lines inside a `## Structure` section (or a `### Structure` subsection): skip entirely. These use parentheses for grammatical notation, not readings.

**Known limitation (Structure 2 files):** Once `### Structure` sets the in-structure flag within a numbered use case (`## 1. …`), all subsequent `### Verb`, `### Noun` etc. subsections inside that use case also have the flag set and are skipped. In practice this is harmless — formation rule rows use `→` for examples, not trailing `（）` parens, so the algorithm would not have converted them anyway.

---

### Step 4 — Typos and grammar mistakes

Review all English prose sections for spelling and grammar errors. Fix silently — no user approval needed for minor corrections. Log each fix in the completion report.

Note: Steps 1–4 are applied silently before any user gate. Steps 5 and 6 are the first points at which execution pauses for user input.

---

### Step 5 — Substantive correctness check

Verify the grammar explanation is accurate:
- Structure rules correct (e.g. correct conjugation forms listed)
- Example sentences grammatically valid Japanese
- English glosses match the Japanese

May use web search to verify. If something appears incorrect:
1. Present the issue and proposed correction to the user.
2. **Wait for user approval before applying any change.**
3. If the user declines or defers: skip this correction, leave the file unchanged for this issue, and continue to Step 6.

---

### Step 6 — Missing information suggestions

Check whether the file is missing important information:
- Common usage nuances not mentioned
- A major conjugation form not shown
- A frequent learner error not noted

If something is missing: suggest it to the user. **Do not add content without user approval.** Wait for user response before continuing.
If the user declines or defers: skip the suggestion and continue to Step 7.

---

### Step 7 — File structure enforcement

#### Section normalisation (before enforcing template)

Apply silently before proposing the structure to the user:

- `## Examples` absent → add an empty `## Examples` section between `## Structure` and `## Notes`.
- `## Notes` present but empty → remove the section entirely (optional; omit when empty).

#### Summary line

The gloss line (`> ...`) immediately under the main heading is the summary. It stays as a blockquote line — not a separate `## Summary` header.

#### Inferring which structure to use

**Structure 1** — use when the grammar point has a single unified pattern that applies across word types (verbs, adjectives, nouns) in the same way.

**Structure 2** — use when the grammar point has two or more meaningfully distinct use cases that each need separate explanation.

The skill infers the structure from the file content, proposes it to the user, and **waits for confirmation before reformatting**.

**If content is ambiguous** (mixed layout, cannot determine which structure fits), do not guess. Present:

```
Could not determine structure for: grammar-index/grammar/<slug>.md
Content summary: <brief description of what is in the file>

Options:
  1. Structure 1 — shared structure across word types
  2. Structure 2 — distinct numbered use cases
  3. Skip restructuring for this file

What should I do?
```

Wait for user input before making any changes to file structure.

#### Structure 1 — Shared structure across word types

```markdown
# Pattern Name

> One-line summary of what the pattern expresses.

## Use Cases

Short description of when/how to use the pattern (1–3 sentences). Omit if the summary line already covers it.

## Structure

### Verb
- Present:         V-plain + pattern        → example sentence
- Negative:        V-ない + pattern          → example sentence
- Past:            V-た + pattern            → example sentence
- Past-negative:   V-なかった + pattern      → example sentence

### い-adjective
- Present:         Adj + pattern             → example sentence
- Negative:        Adj-くない + pattern      → example sentence
- Past:            Adj-かった + pattern      → example sentence
- Past-negative:   Adj-くなかった + pattern  → example sentence

### な-adjective
- Present:         Adj + pattern             → example sentence
- Negative:        Adj + じゃない + pattern  → example sentence
- Past:            Adj + だった + pattern    → example sentence
- Past-negative:   Adj + じゃなかった + pattern → example sentence

### Noun
- Present:         N + pattern               → example sentence
- Negative:        N + じゃない + pattern    → example sentence
- Past:            N + だった + pattern      → example sentence
- Past-negative:   N + じゃなかった + pattern → example sentence

## Examples

[Full natural sentences showing real usage in context — required; leave empty if none available]

## Notes

[Optional — nuances, contrasts, or learner pitfalls. Omit the section entirely if empty.]

## See also

- [Pattern Name](/JapaneseNotes/grammar-index/grammar/slug) — short reason
```

Omit word-type sections that do not apply (e.g. a particle-only pattern may only have a Noun section). Omit tense rows that do not apply. Each remaining row must have at least one inline example (`→ example`).

**Section distinction:**
- `## Structure` rows use `→` for short inline examples showing the pattern mechanically.
- `## Examples` holds full natural sentences showing real usage in context.

#### Structure 2 — Distinct use cases

```markdown
# Pattern Name

> One-line summary of what the pattern expresses.

## 1. Use Case Name

### Structure

### Verb
- Present: ...  → example
- ...

### い-adjective
- ...

(etc. — only applicable word types and tenses)

## 2. Use Case Name

### Structure

(same format)

## Examples

[Full natural sentences — required; leave empty if none available]

## Notes

[Optional — omit if empty]

## See also

- [Pattern Name](/JapaneseNotes/grammar-index/grammar/slug) — short reason
```

Each use case is a numbered `##` header. Structure subsections follow the same word-type / tense pattern as Structure 1, limited to what applies.

---

### Step 8 — Populate ## See also

Run after structure is finalised.

**Orphan warning:** While reading topic files, check whether the current file's slug appears in at least one topic's `## Entries`. If not, warn before continuing:

```
[WARN] <slug>.md has no entry in any grammar-index topic file.
Add it manually or re-run extract-grammar classification (step 9).
```

To check all grammar files at once: `python3 .claude/scripts/grammar-audit.py --verbose`

**Algorithm:**
1. List all files in `grammar-index/` non-recursively (do not descend into `grammar/` or any subdirectory). Exclude `index.md`. Use:
   ```bash
   find grammar-index -maxdepth 1 -name "*.md" ! -name "index.md"
   ```
2. For each topic file, scan its `## Entries` section for lines in the format:
   `- [Pattern Name](/JapaneseNotes/grammar-index/grammar/<slug>) · <level>`
   Extract the slug from each entry line by taking the final path segment of the URL (the part after the last `/`).
   Check whether any extracted slug matches the current file's slug.
3. For each matching topic file, collect all other slugs from its `## Entries` section (co-entries), using the same extraction rule. Exclude the current file's own slug.
4. De-duplicate the collected slugs across all matching topic files.
5. For each co-entry slug, read `grammar-index/grammar/<slug>.md` and extract the pattern name from the `# heading` line (first line starting with `# `).
6. Format each as an absolute URL link:
   `- [Pattern Name](/JapaneseNotes/grammar-index/grammar/<slug>) — <short phrase describing the relationship>`
   The reason phrase must be written by Claude based on the actual relationship between the two patterns (e.g. "also expresses purpose", "similar but formal register", "contrast: reason vs. cause"). Do not copy the topic filename verbatim.
7. Replace the entire content of `## See also` with the formatted list.
8. If no related files are found, write:
   ```
   ## See also

   *(none)*
   ```

---

### Step 9 — Set proofread: true

**Reusable script:** Run after all review steps are complete:

```bash
python3 .claude/scripts/grammar-process.py --set-proofread <file> [<file> ...]
```

If the script is not available, replace `proofread: false` with `proofread: true` in the frontmatter manually. Do not modify any other frontmatter field.

---

## Completion report

After processing all requested files, print a report in this format:

```
update-grammar — 2 files processed

  grammar-index/grammar/seeking-approval.md
    Tags removed: 0
    Furigana: 3 lines converted
    Language: no Polish found
    Typos: 1 fixed ("listenner" → "listener")
    Substantive: OK
    Missing info: suggested adding negative form examples (user approved)
    Structure: Structure 1 (shared) — confirmed by user
    See also: 1 link added (sentence-final-particles group)
    → proofread: true

  grammar-index/grammar/point-4.md
    Tags removed: 2
    Furigana: 0 lines (no trailing format found)
    Language: 1 section translated
    Typos: none
    Substantive: 1 issue raised, user approved correction
    Missing info: none suggested
    Structure: Structure 2 (use cases) — 2 use cases confirmed by user
    See also: 2 links added (demonstratives group)
    → proofread: true
```

---

## Never touch

- `<!--ID: -->` lines — do not add, remove, or shift them anywhere
- `TARGET DECK` lines — do not touch
- Frontmatter fields — the only field this skill may write is `proofread`. Never modify `lesson`, `pattern`, `topic_slug`, `level`, or any other frontmatter field
- Japanese text — never translate Japanese (kana, kanji) to English
- Files outside `grammar-index/grammar/` — only read topic files in `grammar-index/` for the See also step; do not write to them
- Lesson files under `JPLessons/` — read-only; never write to them
- Other skill files or `.cowork/instructions.md` — do not modify during skill execution
- Do not run `git push` or any remote git operation
