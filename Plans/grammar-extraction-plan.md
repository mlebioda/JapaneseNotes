# Grammar Extraction & Online Features — Plan v2

Supersedes `grammar-online-features-plan.md`. The corrected architecture: grammar content is extracted to standalone published files first; future practice skills read those small files rather than full lesson files.

Base URL for published grammar pages: `https://mlebioda.github.io/JapaneseNotes/Grammar/<slug>`

---

## Architecture Overview

### Current state

- Lesson files hold grammar explanations inside `# 文法` sections as `## Heading` subsections.
- `grammar-index/` holds group/topic files whose `## Entries` lists contain wikilinks: `[[LESSONCODE#anchor]]` pointing at local lesson files.
- `practice-grammar` (existing) reads one lesson file at a time — stays unchanged.

### Target state after WP1 + WP2

- Each grammar point lives in its own standalone file: `Grammar/<slug>.md`, published to GitHub Pages.
- `grammar-index/` group files link to published web URLs instead of local wikilinks.
- `Vocabulary/words-extracted.md` holds pre-extracted words from all lessons.
- Future practice skills (`practice-grammar-due`, `practice-grammar-group`) read small standalone files instead of full lesson files, keeping context bounded.

---

## Standalone Grammar File Format

**⚠️ Format must be agreed before WP1 Step 1.1 begins. The structure below is a proposal — confirm or adjust before implementation.**

```
---
lesson: UN5GL14
pattern: Vないでください
topic_slug: requests-commands
level: N5
proofread: false
---

# Vないでください

> [One-line English gloss of what the pattern expresses]

## Structure

[Formation rule — e.g. "Verb (ない-form) + でください"]

## Meaning

[Explanation from the lesson file — Polish or English]

## Examples

[Example sentences from the lesson file]

## Notes

[Populated during internet enrichment — additional context, nuance, common mistakes, related patterns]
```

**File naming:** `<lesson-code>-<anchor-slug>.md`
Example: `UN5GL14-v-nai-de-kudasai.md`

Slug normalisation rule: lowercase the anchor text, strip non-ASCII and punctuation except `-`, replace spaces with `-`.
Using lesson code in the filename avoids collisions if the same pattern appears in multiple lessons.

**Directory:** `Grammar/` at vault root.

---

## Work Package 1 — Grammar Extraction and Publication

### Goal

Extract every grammar point from lesson files to standalone published pages. Enrich with internet sources. Proofread. Update grammar index to point to published pages.

### Step 1.1 — Extract Grammar to Standalone Files

**New skill:** `extract-grammar`

Trigger phrases:
- "extract grammar from UN5GL14"
- "extract grammar from all N5 lessons"

Workflow:

1. Find the target lesson file(s). Accept a single lesson code or a JLPT level (e.g. "all N5") for batch mode.
2. Read the lesson file **up to `# Summary` only** — never past it.
3. Locate the `# 文法` section. Split by `## Heading` — each heading is one independent grammar point.
4. For each grammar point, construct the output filename: normalise the heading text to a slug, prepend the lesson code.
5. Create `Grammar/<lesson-code>-<slug>.md` using the agreed format. Populate front matter from known data; populate content sections from the extracted text.
6. **Idempotent:** if the file already exists, skip — do not overwrite.
7. **Batch mode:** process one lesson file at a time; do not load multiple lesson files into context simultaneously.
8. Never modify the lesson file. Never read past `# Summary`.

Risks:
- `## Heading` text may contain characters invalid in filenames (`〜`, `/`, `・`). The slug normalisation rule must be applied consistently and identically every time so the filename is reproducible.
- If a `# 文法` section is missing from a lesson file, skip that file and log a note.

### Step 1.2 — Internet Enrichment

Runs after extraction, one file at a time.

For each standalone grammar file in `Grammar/`:

1. Read the file. Check if `## Notes` is empty or missing.
2. Search authoritative sources for the grammar pattern: Jisho, Tae Kim's Guide, JLPT Sensei, NHK Web Easy grammar notes.
3. Populate `## Notes` with: alternative explanations, nuance differences from similar patterns, common learner mistakes, related patterns.
4. **Do not overwrite** `## Structure`, `## Meaning`, or `## Examples` — lesson content is authoritative for those sections. Append to `## Notes` only.
5. Run one file per invocation to keep context small.

### Step 1.3 — Proofreading

Runs after enrichment, one file at a time.

For each standalone grammar file:

1. Correct spelling, grammar mistakes, and typos in the explanation text (Polish and Japanese).
2. Correct kanji/kana errors in example sentences.
3. Do not change meaning or significantly rewrite style — fix errors only.
4. Set `proofread: true` in the file's front matter once done.

### Step 1.4 — Update Grammar Index Links

Runs after `Grammar/` files are pushed and GitHub Pages has deployed.

For each topic file in `grammar-index/`:

1. Read the file. Find the `## Entries` section.
2. For each `[[LESSONCODE#anchor]]` wikilink, locate the corresponding `Grammar/<slug>.md` file to confirm it exists.
3. Construct the published URL: `https://mlebioda.github.io/JapaneseNotes/Grammar/<slug>`
4. Replace the wikilink with a standard markdown link: `[pattern name](url)`

**Obsidian compatibility note:** replacing wikilinks removes Obsidian backlink tracking for those entries. If this is undesirable, keep the wikilink and append the web link on the same line: `[[LESSONCODE#anchor]] — [pattern name](url)`. Confirm preferred format before running this step.

Risks:
- If a `Grammar/` file does not yet exist for a wikilink, skip that entry and log it — do not write a broken URL.
- Run this step only after GitHub Actions confirms the pages are live (check at least one URL manually first).

---

## Work Package 2 — Vocabulary Extraction

### Goal

Extract words from lesson files into a standalone vocabulary file. Bounded scope: single words and all `ひょうげん` expressions. No template update pass — raw lines only, to keep context small.

**Independent — no dependency on WP1. Can start immediately.**

### What to extract

| Section | Tag | Rule |
|---------|-----|------|
| `# ごい` | `#wc` | All verbs |
| `# ごい` | `#wp` | All adjectives |
| `# ごい` | `#w` | Single words only (1–3 tokens, no conjugated verb form) — skip sentence-length lines |
| `# ひょうげん` | `#w` | All — single words AND expressions/sentences |
| `# ひょうげん` | `#wc` | All |
| `# ひょうげん` | `#wp` | All |

`fill-templates` is **not run** during extraction — lines are copied as-is. This avoids loading Polish translation state into context.

### Output file

`Vocabulary/words-extracted.md`

Grouped by lesson code:

```
## UN5GL14

#w 病院 (びょういん) - hospital
#wc 使う (つかう) - to use
#wp 難しい (むずかしい) - difficult
```

Preserve the original tag and the full text of the line. Do not strip or reformat.

### New skill: `extract-vocabulary`

Trigger phrases:
- "extract vocabulary from UN5GL14"
- "extract vocab N5"
- "update vocabulary file"

Workflow:

1. Find target lesson file(s). Accept a single lesson code or a JLPT level.
2. Read up to `# Summary` only.
3. Extract `# ごい` lines: all `#wc` and `#wp`; `#w` single words only (heuristic — Japanese field is 1–3 tokens with no verb form detected).
4. Extract all lines from `# ひょうげん` regardless of tag or length.
5. **Idempotent:** if a `## <lesson-code>` block already exists in the output file, skip that lesson.
6. Append new entries under `## <lesson-code>` heading.
7. If `Vocabulary/words-extracted.md` does not exist, create it with a `# Extracted Vocabulary` header before appending.

Risks:
- The `#w` single-word heuristic is Claude judgment — misclassifications are cosmetic and do not cause data loss.
- Never write a TARGET DECK line to this file.
- Never read past `# Summary` in lesson files.

---

## Implementation Order

1. **Agree standalone grammar file format** — prerequisite for WP1, no code. (⚠️ must happen first)
2. **WP2** (`extract-vocabulary`) — independent, can start immediately in parallel.
3. **WP1 Step 1.1** (`extract-grammar`) — one lesson at a time.
4. **WP1 Step 1.2** (internet enrichment) — per file, after extraction.
5. **WP1 Step 1.3** (proofreading) — per file, after enrichment.
6. **Commit and push** `Grammar/` — let GitHub Actions complete.
7. **WP1 Step 1.4** (grammar index link update) — after pages confirmed live.

---

## Deferred — Future Work Packages

These depend on WP1 and WP2 being complete and are not detailed here:

- `practice-grammar-due` — drills due grammar points from `grammar-state.json`; reads `Grammar/` files and `Vocabulary/words-extracted.md`; hard cap of 10 points per session; user-selectable difficulty (hard / easy).
- `practice-grammar-group` — drills all grammar points in a `grammar-index` group; reads `Grammar/` files and `Vocabulary/words-extracted.md`; natural limit = number of entries in the group file.
- `fill-templates` Step 7 — appends GitHub Pages grammar links to newly generated sentence cards.
- `_grammar-patterns.md` — can be auto-generated by scanning `Grammar/` front matter rather than manually curated; deferred until `Grammar/` is populated.

---

## Global Constraints

- Never read past `# Summary` in lesson files.
- Never modify `<!--ID: -->` lines.
- Never modify TARGET DECK lines.
- Git is the rollback mechanism — no `.bak` files. Commit before any batch edit that modifies existing files.
- Commit `Grammar/` additions and `grammar-index/` link updates in separate commits.
- Verify at least one published URL manually before running Step 1.4.
- `practice-grammar` (existing skill) is not modified — it continues to work on a single specified lesson file only.
