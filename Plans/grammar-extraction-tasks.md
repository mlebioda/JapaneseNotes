# Grammar Extraction & Online Features — Task Checklist

Derived from `grammar-extraction-plan.md`. Work top-to-bottom within each work package. Items marked with a dependency note must wait for their prerequisite.

---

## Prerequisite — Agree Standalone Grammar File Format

- [x] Review the proposed format in `grammar-extraction-plan.md` (front matter fields, section headings, file naming convention)
- [x] Confirm or adjust the format — in particular: language of `## Meaning` section (Polish or English?), whether `## Structure` and `## Meaning` are separate or merged, whether any additional front matter fields are needed
- [x] Confirm file naming convention: `<lesson-code>-<anchor-slug>.md` — or alternative
- [x] Confirm directory: `Grammar/` at vault root — or alternative
- [x] Confirm the slug normalisation rule for special characters (`〜`, `・`, parentheses, spaces)
- [x] Confirm preferred grammar index link format: plain markdown link, or wikilink + web link side by side

**⚠️ Do not begin WP1 Step 1.1 until all items above are confirmed.**

---

## Work Package 1 — Grammar Extraction and Publication

### Step 1.1 — Extract Grammar to Standalone Files

_Depends on: format agreement above._

- [x] Create `.cowork/skills/extract-grammar.md` skill file
- [x] Define trigger phrases in the skill: "extract grammar from \<lesson>", "extract grammar from all N5 lessons"
- [x] Write file-finding step: accept single lesson code or JLPT level; resolve to file path(s) under `JPLessons/Udemy/`
- [x] Write extraction step: read lesson file up to `# Summary` only; locate `# 文法`; split by `## Heading`
- [x] Write slug normalisation rule into the skill: lowercase, strip non-ASCII and punctuation except `-`, replace spaces with `-`, prepend lesson code
- [x] Write file creation step: populate front matter and content sections from extracted text; use agreed format
- [x] Write idempotency check: skip if `Grammar/<slug>.md` already exists
- [x] Write batch mode rule: process one lesson file at a time — do not load multiple lesson files simultaneously
- [x] Add "Never touch" section to skill: TARGET DECK lines, `<!--ID: -->` lines, never read past `# Summary`, never modify lesson files
- [ ] Run on one lesson manually to verify the output format before batch use
- [x] Update `.cowork/instructions.md` skills table to list `extract-grammar` once the skill file is written

### Step 1.2 — Internet Enrichment

_Depends on: Step 1.1 (at least some `Grammar/` files must exist)._

- [ ] For each `Grammar/` file where `## Notes` is empty or absent: search for the grammar pattern on Jisho, Tae Kim, JLPT Sensei, or NHK Web Easy
- [ ] Populate `## Notes` with: alternative explanation, nuance vs. similar patterns, common mistakes, related patterns
- [ ] Do not overwrite `## Structure`, `## Meaning`, or `## Examples` — append to `## Notes` only
- [ ] Process one file per invocation — do not batch multiple files in a single context window
- [ ] After completing a file, verify the `## Notes` content is accurate and relevant before moving to the next

### Step 1.3 — Proofreading

_Depends on: Step 1.2 (enrich before proofread, so proofreading covers the full content)._

- [ ] For each `Grammar/` file: check Polish and Japanese explanation text for spelling errors, grammar mistakes, and typos
- [ ] Check kanji and kana in example sentences for errors
- [ ] Fix errors only — do not rewrite style or change meaning
- [ ] Set `proofread: true` in the file's front matter after completing each file
- [ ] Process one file at a time

### Step 1.4 — Update Grammar Index Links

_Depends on: Steps 1.1–1.3 complete AND `Grammar/` pages confirmed live on GitHub Pages._

- [ ] Commit and push all `Grammar/` files; wait for GitHub Actions to complete
- [ ] Manually verify at least two published URLs before proceeding (e.g. `https://mlebioda.github.io/JapaneseNotes/Grammar/<slug>`)
- [ ] Confirm preferred link format (plain markdown link vs. wikilink + web link) — see prerequisite checklist above
- [ ] For each file in `grammar-index/`: read `## Entries`, find `[[LESSONCODE#anchor]]` wikilinks
- [ ] For each wikilink: confirm the corresponding `Grammar/<slug>.md` exists locally before writing the URL
- [ ] Replace or supplement each wikilink with the published URL in the agreed format
- [ ] If a corresponding `Grammar/` file does not exist for a wikilink, skip that entry and log it — do not write a broken link
- [ ] Commit `grammar-index/` changes separately from `Grammar/` additions

---

## Work Package 2 — Vocabulary Extraction

_Independent — no dependency on WP1. Can be done in parallel._

- [x] Create `.cowork/skills/extract-vocabulary.md` skill file
- [x] Define trigger phrases: "extract vocabulary from \<lesson>", "extract vocab N5", "update vocabulary file"
- [x] Write file-finding step: accept single lesson code or JLPT level; resolve to file path(s)
- [x] Write `# ごい` extraction step:
  - All `#wc` lines → include
  - All `#wp` lines → include
  - `#w` lines → include only if Japanese field is a single word (1–3 tokens, no conjugated verb) — skip sentence-length lines
- [x] Write `# ひょうげん` extraction step: include all lines (`#w`, `#wc`, `#wp`) regardless of length — single words and full expressions alike
- [x] Write idempotency check: if `## <lesson-code>` block already exists in output file, skip that lesson
- [x] Write append step: add `## <lesson-code>` heading followed by extracted lines
- [x] Write create-if-missing step: if `Vocabulary/words-extracted.md` does not exist, create with `# Extracted Vocabulary` header before appending
- [x] Add "Never touch" section to skill: no TARGET DECK lines, never read past `# Summary`, do not run fill-templates during extraction
- [x] Add note: `fill-templates` is NOT triggered — lines are copied raw to save context
- [ ] Run on one lesson manually to verify correct section filtering before batch use
- [x] Update `.cowork/instructions.md` skills table to list `extract-vocabulary` once the skill file is written

---

## Cross-cutting

- [ ] Confirm `Grammar/` directory is rendered by Jekyll (no `exclude:` in `_config.yml` that would suppress it — unlike `_grammar-patterns.md` which uses an underscore prefix)
- [ ] After each batch of `Grammar/` files is pushed, spot-check one published URL to confirm Jekyll is rendering the front matter and content correctly
- [ ] Confirm git workflow: `Grammar/` additions committed separately from `grammar-index/` link updates
