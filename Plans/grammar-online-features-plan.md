# Grammar Online Features — Implementation Plan

Base URL for all GitHub Pages links: `https://mlebioda.github.io/JapaneseNotes/grammar-index/<slug>`
where `<slug>` is the filename without `.md` (e.g. `verb-forms`, `ability-expressions`).

---

## Feature 1 — Grammar Index Enrichment

### Goal
Make topic file titles and descriptions precise enough that Claude can auto-match a grammar pattern found in a sentence to the correct topic file, and therefore produce a deterministic GitHub Pages URL for that topic.

### What exists
- 31 topic files in `grammar-index/`, each with:
  - A `# Title` heading
  - A `> blockquote` description (one sentence)
  - An `## Entries` list of wikilinks
  - Optional `## See also`
- `grammar-index/index.md` — the Jekyll navigation page

### What is missing
A canonical, machine-readable mapping: grammar pattern text → topic slug → GitHub Pages URL.
The blockquote descriptions exist but are prose and not keyed to pattern strings (e.g. `Vないで ください`, `〜たことがあります`).

### Steps

1. **Create `grammar-index/_grammar-patterns.md`** — a mapping file with one row per grammar pattern. Format:

   ```
   | Pattern | Topic slug | Description |
   |---------|-----------|-------------|
   | Vないでください | requests-commands | Request not to do |
   | 〜たことがあります | verb-forms | Have-ever experience |
   ```

   - "Pattern" is the canonical pattern string as it appears in lesson `## Heading` lines (pull from the wikilink anchors already in the topic files).
   - "Topic slug" is the filename without `.md` — directly usable in the GitHub Pages URL.
   - "Description" is a one-line English gloss of what the pattern expresses.
   - Populate by reading every entry wikilink across all 31 topic files, extracting the `#anchor` text, and assigning it to the topic. One pattern may appear under more than one topic — include a row for each topic it belongs to.
   - This file does NOT need front matter or Jekyll layout; it is only read by Claude.

2. **Update topic file blockquotes** (optional, low priority) — where a blockquote is too vague to distinguish a topic (e.g. "Verb forms" is used by three files), sharpen it to name the specific patterns covered. This is a quality improvement for GitHub Pages readers, not required for Claude matching.

3. **Exclude `_grammar-patterns.md` from Anki plugin scope** — it lives inside `grammar-index/` which is already excluded from the Anki plugin's TARGET DECK scanning, so no action needed there.

### Risks
- None to existing data. This is a new file.
- If a grammar pattern string contains special Markdown characters (`〜`, `・`, parentheses), ensure the table cells escape them or are tested in Jekyll (the file is Claude-only, so Jekyll rendering is irrelevant).
- Pattern strings must exactly match the `## Heading` text used in lesson files so `summarize-grammar` and `fill-templates` can do a reliable lookup.

---

## Feature 2 — Update `fill-templates` Skill (Grammar Link Appended to Anki Cards)

### Goal
After generating Anki `#w` sentence cards (not word cards — only sentences), Claude detects grammar patterns used in the sentence, looks up `_grammar-patterns.md`, and appends a GitHub Pages link to the card.

### What exists
- `.cowork/skills/fill-templates.md` — generates `# Summary` cards
- `grammar-index/_grammar-patterns.md` — to be created in Feature 1

### What is modified
**File:** `.cowork/skills/fill-templates.md`

Grammar link annotation is an **optional post-fill pass**, run after all card generation is complete. It must not be interleaved with card writing. The skill file should label this as **"Step 7 — Grammar link annotation (optional pass)"** and make clear that the user can skip this step if they only need the cards.

### New step — "Step 7 — Grammar link annotation (optional pass)"

1. After all `#wc` and `#wp` skeletons are filled and all cards are written, scan each `#w` card in `Rzeczowniki:` to detect sentence cards.
   - A sentence card is any `#w` line whose Japanese field contains a verb conjugation form or a recognizable grammar pattern string. A simple noun or expression with no predicate is not a sentence.
2. For each sentence card, read `grammar-index/_grammar-patterns.md` and attempt to match one or more pattern strings against the card's Japanese content.
3. For each match, append a link line below the card's translation line:

   ```
   > [Pattern name](https://mlebioda.github.io/JapaneseNotes/grammar-index/<slug>)
   ```

   Multiple matches → multiple `>` link lines, one per match.
4. If no pattern matches, leave the card unchanged — do not append a placeholder.

### Card format after annotation

Before:
```
translation #card
japanese expression (furigana)
```

After (if a pattern matched):
```
translation #card
japanese expression (furigana)
> [Vないでください](https://mlebioda.github.io/JapaneseNotes/grammar-index/requests-commands)
```

### Risks
- **Never modify `<!--ID: -->` lines** — the appended link must go on a new line after the Japanese line, before the next card separator (`---` or blank line). Inserting text between an existing `<!--ID:-->` line and its card body would break Anki sync. Rule: only annotate cards that do NOT yet have an `<!--ID:-->` line (i.e. newly generated cards in this session).
- Pattern matching is fuzzy (Claude semantic match against pattern strings) — false positives are possible. The worst outcome is an incorrect link; it does not corrupt data. The user can remove stray links manually.
- This step reads `_grammar-patterns.md` once per fill-templates run; if the file does not exist yet (Feature 1 not complete), skip the annotation step silently.
- Because annotation is a separate optional pass (Step 7), skipping it leaves all card content intact and clean.

---

## Feature 3 — New Skill: `practice-grammar-due`

### Goal
Run a drill across all grammar points that are due for review according to the SM-2 schedule in `grammar-state.json`, regardless of which lesson they belong to. Reads grammar explanation text from local lesson files. Uses GitHub Pages URLs only in session output links so the user can navigate to the topic page.

### New file
`.cowork/skills/practice-grammar-due.md`

### Trigger phrases
- "practice due grammar"
- "drill due"
- "what grammar is due"

### Architecture note
GitHub Pages only publishes `grammar-index/` topic files. These are index pages: they contain a heading, a blockquote description, and a list of wikilinks to lessons. They do NOT contain grammar explanation text. Grammar explanation text (`# 文法` sections) lives only in local lesson files. This skill therefore reads all grammar content from local files and uses GitHub Pages URLs only for navigation links in session output.

### How it differs from `practice-grammar`

| Aspect | practice-grammar | practice-grammar-due |
|--------|-----------------|----------------------|
| Scope | one lesson at a time | all due grammar points across all lessons |
| Grammar content source | local lesson file | local lesson file (same) |
| Point selection | all points in the lesson | only points with `due_date` <= today in `grammar-state.json` |
| Vocab pool | local `# ごい` + `# ひょうげん` | local lesson file for each due point's lesson |
| State file | `.cowork/progress/grammar-state.json` | same file — shared state |
| GitHub Pages URL | n/a | included in session output links per topic, not used as content source |

### Workflow steps (new file content)

1. Read `.cowork/progress/grammar-state.json`. Collect all grammar point entries where `due_date` <= today's date.
   - If no points are due, report this to the user and exit.
2. For each due grammar point, resolve the local lesson file path from the `lesson_file` field (e.g. `UN5GL14` → `JPLessons/Udemy/N5/Gramatyka/UN5GL14-*.md`). Read the `# 文法` section of that file to get the grammar explanation text for the specific `grammar_header` anchor.
3. Build the vocab pool: for each due point's lesson file, parse `# ごい` + `# ひょうげん`. Merge pools across lessons; deduplicate by Japanese field.
4. Generate exercises using the same algorithm as `practice-grammar` (same exercise types, same grading, same batch/interactive modes).
5. In session output, include a GitHub Pages link per grammar point using the `topic_slug` field: `https://mlebioda.github.io/JapaneseNotes/grammar-index/<topic_slug>`. This is for user navigation only — do not fetch from this URL.
6. Persist results to `.cowork/progress/grammar-state.json` using the same SM-2 logic.

### Risks
- If a lesson file is not found locally (file moved or renamed), skip that grammar point for this session and log a warning in session output.
- Grammar points in `grammar-state.json` may reference a `topic_slug` that is not yet published on GitHub Pages. This is harmless — the URL is only shown, never fetched.
- `grammar-state.json` is shared with `practice-grammar` and `practice-grammar-group`. Concurrent sessions (unlikely but possible) could cause write conflicts. Acceptable risk; document it in the skill file.

---

## Feature 4 — New Skill: `practice-grammar-group`

### Goal
Run a drill scoped to a single grammar-index topic file (e.g. all entries in `ability-expressions.md`), instead of a single lesson. Reads grammar explanation text from local lesson files. The local topic file provides the entry list; GitHub Pages URL for the topic is included in session output and Anki links, but not used as a content source.

### Architecture note
GitHub Pages topic pages are index pages only — they do not contain grammar explanation text. The local `grammar-index/<slug>.md` file contains the same entry list and is read directly. Grammar explanations come from local lesson files.

### New file
`.cowork/skills/practice-grammar-group.md`

### Trigger phrases
- "practice group ability-expressions"
- "drill group <slug>"
- "practice topic <topic name>"

### Workflow steps

1. Accept a group identifier — either a slug (`ability-expressions`) or a plain English name (`ability expressions`). If a plain name is given, fuzzy-match against topic file names in `grammar-index/`.
2. Read the local topic file `grammar-index/<slug>.md` to get the `## Entries` list. No GitHub Pages fetch needed — the local file is the authoritative source.
3. For each entry wikilink, extract the lesson code and anchor (e.g. `UN5GL10`, `Be good/poor at 上手・下手`).
4. For each grammar point, read the local lesson file (`JPLessons/Udemy/N<level>/Gramatyka/<code>.md`) and extract the grammar explanation text from the `# 文法` section at the specific anchor.
5. Build the vocab pool: for each grammar point, parse `# ごい` + `# ひょうげん` from the same local lesson file. Merge pools across lessons if the topic spans multiple lessons; deduplicate by Japanese field.
6. Build the exercise set: one exercise per grammar point entry in the topic file. Apply the same exercise generation rules as `practice-grammar`.
7. Run the batch/interactive drill loop (identical to `practice-grammar`).
8. In session output, include the GitHub Pages URL for the topic: `https://mlebioda.github.io/JapaneseNotes/grammar-index/<slug>`. This is for user navigation and Anki links only — do not fetch from this URL.
9. Persist to `.cowork/progress/grammar-state.json` using the same SM-2 logic. Grammar point IDs follow the same `<lesson-code>::<anchor-slug>` convention.

### Grammar point ID for cross-lesson topics
Use `<lesson-code>::<anchor-slug>` (same convention as existing skill). The group file is not part of the ID — the same grammar point may be drilled via its lesson or via any group it belongs to, and state merges correctly.

### Risks
- A topic file may have many entries (e.g. `verb-forms.md` currently has 14 entries). A session with 14 exercises is long but manageable. No truncation needed — user can stop early.
- Vocab pool merging across lessons: duplicates (same Japanese word in two lessons) must be deduplicated by the Japanese field before building the exercise pool.
- If a lesson file is not found locally (future lessons not yet downloaded), skip its vocab and grammar explanation; log a warning in session output.

---

## Feature 5 — Vocabulary Extraction to Standalone Files

### Goal
Extract vocabulary out of lesson files into two dedicated files — one for single words (nouns, verbs, adjectives) and one for expressions/sentences — so practice skills can access vocabulary without loading full lesson files.

### New files

- `Vocabulary/words-extracted.md` — single words: nouns (`#w` without sentence structure), verbs (`#wc`), adjectives (`#wp`)
- `Vocabulary/expressions-extracted.md` — expressions and sentences (`#w` lines where the Japanese field is a full phrase or sentence, not a single lexeme)

Both files are standalone vocabulary files, following the existing convention in `Vocabulary/` (e.g. `Bank-vocabulary.md`). They are NOT lesson files and have no TARGET DECK line.

### Distinction: word vs expression/sentence

A `#w` line is classified as a word if the Japanese field is a single lexeme (one noun, one adverb, one particle-headed expression of 1–3 tokens with no verb). It is classified as an expression/sentence if it contains a conjugated verb form, a te-form chain, or is longer than approximately 5 tokens.

Exception: `#w` lines where the Japanese field ends with `(する)` (suru nouns, e.g. `入院(する)`) are always classified as **words**, not expressions, regardless of token count. They go to `words-extracted.md`.

Verbs (`#wc`) and adjectives (`#wp`) always go to `words-extracted.md`.

### Source
All lesson files under `JPLessons/Udemy/` — recursively, all `.md` files. For each file, extract only the section before `# Summary`.

### Extraction format

In both output files, group entries by lesson code:

```
## UN5GL14

#w 病院 (びょういん) - hospital
#wc 使う (つかう) - to use
#wp 難しい (むずかしい) - difficult
```

Preserve the original `#w`/`#wc`/`#wp` tag and the full text of the line (Japanese field + reading + translation). Do not strip or reformat.

### New skill file
`.cowork/skills/extract-vocabulary.md`

#### Trigger phrases
- "extract vocabulary from UN5GL14"
- "extract vocab <lesson>"
- "update vocabulary files"

#### Workflow steps

1. Find the target lesson file(s). If a specific lesson code is given, process only that lesson. If the trigger is "update vocabulary files" (no lesson specified), process all lessons under `JPLessons/Udemy/` that are not yet present in the extracted files.
2. For each lesson, run `awk '/^# Summary$/{exit} {print}'` to get the pre-summary slice.
3. Extract all `#w`, `#wc`, `#wp` lines from `# ごい` and `# ひょうげん` sections.
4. Classify each `#w` line as word or expression (see distinction above, including the suru noun rule).
5. Append new entries to `Vocabulary/words-extracted.md` and `Vocabulary/expressions-extracted.md` under a `## <lesson-code>` heading. If a `## <lesson-code>` block already exists in the file, skip that lesson (idempotent).
6. Do not modify any existing entries in the output files.

### Risks
- These files are in `Vocabulary/`, not `JPLessons/`, so the Anki plugin will not scan them for TARGET DECK export. No risk to Anki data.
- `<!--ID: -->` lines are only present in the `# Summary` section of lesson files, which the skill never reads (awk exits at `# Summary`). No risk.
- The word/expression classification is heuristic (Claude judgment). Misclassifications are cosmetic — a word appearing in the wrong file does not cause data loss.
- If `Vocabulary/words-extracted.md` or `Vocabulary/expressions-extracted.md` do not exist yet, the skill must create them with a minimal header (`# Extracted Words` / `# Extracted Expressions`) before appending.

---

## Implementation Order (Dependencies)

1. Feature 1 (grammar-patterns mapping) — must be done first; Features 2, 3, 4 all depend on it.
2. Feature 5 (vocabulary extraction) — independent; can be done in parallel with Feature 1.
3. Feature 2 (fill-templates update) — depends on Feature 1.
4. Feature 3 (practice-grammar-due) — depends on Feature 1; benefits from Feature 5 but not blocked by it.
5. Feature 4 (practice-grammar-group) — depends on Feature 1; benefits from Feature 5 but not blocked by it.
6. Update `.cowork/instructions.md` skills table to list `practice-grammar-due`, `practice-grammar-group`, and `extract-vocabulary` once their skill files are written.

---

## Global Risks

- **Never modify `<!--ID: -->` lines** — all new skill files and the fill-templates update must explicitly state this constraint and check that any write targets only newly generated content (no existing Anki IDs present).
- **Never modify TARGET DECK lines** — extraction and fill-templates skills already enforce this; the new skills must also state it.
- **`_grammar-patterns.md` naming** — the underscore prefix is used to signal a non-Jekyll-published support file (Jekyll excludes underscore files by default). Confirm the `_config.yml` exclude list does not need updating; by default Jekyll already skips `_*` files.
- **Grammar-state.json is shared** — `practice-grammar-due` and `practice-grammar-group` write to the same file as `practice-grammar`. Concurrent sessions (unlikely but possible) could cause write conflicts. Acceptable risk; document it in the skill files.
- **GitHub Pages deployment lag** — changes committed to `grammar-index/` only appear on GitHub Pages after the Actions workflow completes (typically 1–2 minutes). Skills that include GitHub Pages links in output should note this: if a lesson was just summarized, the page may not be live yet.

---

## Appendix — `grammar-state.json` Schema

All skills that read or write `grammar-state.json` must agree on the following field names and structure. The file lives at `.cowork/progress/grammar-state.json`.

```json
{
  "grammar_points": {
    "<lesson-code>::<anchor-slug>": {
      "lesson_file": "UN5GL14",
      "grammar_header": "Vないでください",
      "topic_slug": "requests-commands",
      "interval": 1,
      "repetitions": 0,
      "ease_factor": 2.5,
      "due_date": "2026-05-22"
    }
  }
}
```

Field definitions:
- `lesson_file` — lesson code without path or extension (e.g. `UN5GL14`). Used to locate the local lesson file.
- `grammar_header` — the exact `## Heading` text from the lesson file. Used for display and pattern matching against `_grammar-patterns.md`.
- `topic_slug` — the `grammar-index/` filename without `.md`. Used to construct GitHub Pages URLs for session output and Anki links.
- `interval` — SM-2 interval in days.
- `repetitions` — number of successful repetitions in a row.
- `ease_factor` — SM-2 ease factor (default 2.5).
- `due_date` — ISO 8601 date string (YYYY-MM-DD). The next date this point should be reviewed.
