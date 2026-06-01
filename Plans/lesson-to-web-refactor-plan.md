# lesson-to-web Refactor — Design Plan

## Overview

The six lesson-to-web skill files (preprocess-grammar, review-grammar, structure-grammar, see-also-grammar, extract-grammar, update-grammar) each carry a near-identical "Never touch" block and scattered copies of the furigana format rules, proofread guard, and file location constants. This duplication makes the skills fragile: a rule change must be applied in six places.

This plan introduces two shared files that absorb the duplicated content, then trims each skill to only its own step logic. Two known bugs are fixed in the same pass.

**Slug:** `lesson-to-web-refactor`

**Files touched:**
- Create: `.cowork/skills/lesson-to-web/_conventions.md`
- Create: `.cowork/skills/lesson-to-web/_patterns.md`
- Modify: `preprocess-grammar.md`, `review-grammar.md`, `structure-grammar.md`, `see-also-grammar.md`, `extract-grammar.md`, `update-grammar.md`
- Not touched: `extract-vocabulary.md`, `.cowork/instructions.md`

---

## New Shared Files

### _conventions.md — Output contract (loaded upfront by every skill)

This file is the single source of truth for everything that must be consistent across the pipeline. Every skill loads it unconditionally before executing any step.

Content to include:

**Canonical furigana format**
- Inline per word, ASCII parentheses: `明日(あした)の仕事(しごと)`
- Never use fullwidth parentheses for furigana output
- Never place readings after the whole word group

**File locations and naming**
- Grammar point files: `grammar-index/grammar/<slug>.md`
- Container files: `grammar-index/grammar/<slug>.md` (identified by presence of `## Sub-topics`)
- Topic index files: `grammar-index/<topic>.md` (identified by presence of `## Entries`)
- Vocabulary subfiles: `grammar-index/grammar/vocabulary/<subdir>/<slug>.md`

**Frontmatter conventions**
- `lesson`, `pattern`, `topic_slug`, `level`, `proofread` — exact field names and expected values on creation
- `proofread` starts as `false`; only see-also-grammar sets it to `true`

**File structure rules (grammar point file)**
Required sections in order: frontmatter, `# <pattern>`, `> <gloss>`, `## Structure`, `## Examples`, and optionally `## Use Cases` and `## Notes`. `## See also` is the final section. Container files use `## Sub-topics` instead.

**proofread: true guard**
Before starting any step on a file, read its frontmatter. If `proofread: true` is already set, pause and ask: `<slug>.md already has proofread: true. Re-process anyway? (yes / no)`. If no: skip all steps for that file and note it as skipped in the handoff summary. If yes: proceed.

**Never touch rules (applies to all lesson-to-web skills)**
- `<!--ID: -->` lines — never add, remove, or shift
- `TARGET DECK` lines — never touch
- Japanese text — never translate kana or kanji
- Files outside `grammar-index/grammar/` (except: skills that explicitly read topic files from `grammar-index/` for context, and extract-grammar step 8 which inserts one wikilink into a lesson file)
- Lesson files under `JPLessons/` beyond the extract-grammar step 8 wikilink insertion
- Other skill files or `.cowork/instructions.md`
- Do not run `git push` or any remote git operation
- Frontmatter fields other than `proofread` — no skill modifies `lesson`, `pattern`, `topic_slug`, or `level` after file creation

---

### _patterns.md — Input recognition registry (lazy-loaded)

This file records decisions about unexpected or ambiguous input formats. Skills load it only when they encounter input that does not match the canonical format defined in `_conventions.md`.

**Lazy-load rule:** A skill loads `_patterns.md` only when it encounters input it cannot classify on its own. If the pattern is found: apply the stored decision silently and continue. If the pattern is not found: ask the user, record the decision, then continue.

**Seed entry — trailing furigana after word group**

This is the known legacy format already described in preprocess-grammar Step 3. Seed the file with this pattern so skills can recognise it from the registry rather than from skill-embedded documentation.

- Pattern: one or more kanji-words followed by a parenthesised reading list at the end of the phrase, e.g. `明日の仕事（あした、しごと）` (fullwidth parens, 、-separated) or `明日の仕事 (あした, shigoto)` (ASCII parens, comma-separated).
- Decision: convert to inline per-word format using ASCII parentheses — `明日(あした)の仕事(しごと)`.
- Apply: silently (standard Step 3 rule in preprocess-grammar).

---

## Per-File Breakdown

### preprocess-grammar.md

**Remove:**
- The entire `## Never touch` section at the bottom — moves to `_conventions.md`
- The inline documentation of the furigana input format at the top of Step 3 (the Input/Output example block and the algorithm description reference) — the algorithm stays, but the "what counts as a known pattern" description moves to `_patterns.md`
- The proofread guard prose — moves to `_conventions.md` (the behavioral instruction stays as a one-line reference: "apply the proofread: true guard from _conventions.md")

**Add:**
- A `## Shared files` section at the top of the workflow: "Load `.cowork/skills/lesson-to-web/_conventions.md` before starting. Load `.cowork/skills/lesson-to-web/_patterns.md` only if Step 3 encounters an unrecognised input format."
- A one-line reference replacing the proofread guard prose: "Check the proofread: true guard (see _conventions.md) before processing each file."

**Keep unchanged:**
- Step 1 (tag removal): full algorithm and examples
- Step 2 (Polish detection): full detection logic, threshold, sub-topics special case
- Step 3 (furigana conversion): algorithm steps 1–9, mismatch warning, Structure section skip rule
- Step 4 (typos): rule and log instruction
- Handoff summary: format and yes / no / all prompt

---

### review-grammar.md

**Remove:**
- The entire `## Never touch` section — moves to `_conventions.md`

**Add:**
- A `## Shared files` section: "Load `.cowork/skills/lesson-to-web/_conventions.md` before starting."
- One-line reference: "Check the proofread: true guard (see _conventions.md) before processing each file."

**Keep unchanged:**
- Step 5 (substantive correctness): full rule including web search, user-gated correction flow
- Step 6 (missing information): full suggestion flow
- Handoff summary: format and yes / no / all prompt
- all-mode skip behavior at top of workflow

---

### structure-grammar.md

**Remove:**
- The entire `## Never touch` section — moves to `_conventions.md`

**Add:**
- A `## Shared files` section: "Load `.cowork/skills/lesson-to-web/_conventions.md` before starting."
- One-line reference to proofread guard.

**Fix (Bug 1):** Change the handoff prompt from `(yes / no)` to `(yes / no / all)` and add the `all` bullet: "all — load see-also-grammar, instructing it to continue in all mode (no further handoff prompts)." The current prompt (lines 188–194 in the file) offers only yes/no, silently dropping the all flag. This must match the pattern used in preprocess-grammar and review-grammar handoffs.

**Keep unchanged:**
- Step 7: container file detection, section normalisation, summary line rule, structure inference, structure 1 and structure 2 templates
- Handoff summary format
- all-mode skip behavior at top of workflow

---

### see-also-grammar.md

**Remove:**
- The entire `## Never touch` section — moves to `_conventions.md`

**Add:**
- A `## Shared files` section: "Load `.cowork/skills/lesson-to-web/_conventions.md` before starting."

**Fix (Bug 2):** In Step 8, Algorithm for grammar point files, step 1 currently reads: "Scan all files in `grammar-index/` non-recursively (do not descend into `grammar/`; exclude `index.md`) that contain a `## Sub-topics` section." This is wrong — container files (those with `## Sub-topics`) live under `grammar-index/grammar/`, not in `grammar-index/` directly. The topic index files in `grammar-index/` have `## Entries` sections, not `## Sub-topics`. Change the scan path to `grammar-index/grammar/` and update the prose accordingly.

The same path correction applies to the container file algorithm (step 1 of that section), which currently also uses `grammar-index/` non-recursively for listing topic files — that reference is correct (topic files are in `grammar-index/` non-recursively), so only the grammar-point algorithm's scan path needs the fix.

**Keep unchanged:**
- Step 8 overall structure: orphan warning, two algorithm branches (grammar point files vs container files), link format
- Step 9 (set proofread: true): script and manual fallback
- Completion report format

---

### extract-grammar.md

**Remove:**
- The entire `## Never touch` section at the bottom — moves to `_conventions.md`
- The `## File placement` section at the bottom — moves to `_conventions.md` (file locations)

**Add:**
- A `## Shared files` section: "Load `.cowork/skills/lesson-to-web/_conventions.md` before starting."

**Keep unchanged:**
- Steps 1–10: all workflow logic, classification table, slug normalisation algorithm and kana table, idempotency check, file templates (grammar, container, vocabulary), wikilink insertion, topic classification, index.md update, completion report
- `## Topic file template`
- `## index.md format`
- `## Slug normalisation — quick reference` table

---

### update-grammar.md

**Remove:**
- Nothing substantial; the file is already minimal (it just delegates to preprocess-grammar in all mode).

**Add:**
- A one-liner: "Load `.cowork/skills/lesson-to-web/_conventions.md` before starting."

**Keep unchanged:**
- Workflow table and all-mode delegation instruction

---

## Bug Fixes

### Bug 1 — all mode dropped at structure-grammar → see-also-grammar boundary

**Location:** `structure-grammar.md`, handoff summary section, the `Run see-also-grammar` prompt.

**Current behavior:** The prompt offers only `(yes / no)`. When structure-grammar is called directly by a user who wants to cascade through see-also-grammar, there is no way to request it. When it is called in all mode from review-grammar, it correctly skips the prompt — but a user invoking structure-grammar standalone cannot choose all.

**Fix:** Change the prompt to `(yes / no / all)` and add a bullet: "all — load see-also-grammar, instructing it to continue in all mode (no further handoff prompts after processing)."

---

### Bug 2 — Broken see-also-grammar scan path

**Location:** `see-also-grammar.md`, Step 8, "Algorithm — grammar point files (no `## Sub-topics`)", bullet 1.

**Current text:** "Scan all files in `grammar-index/` non-recursively (do not descend into `grammar/`; exclude `index.md`) that contain a `## Sub-topics` section."

**Why it is wrong:** Container files — those with `## Sub-topics` — are grammar point files that happen to group sub-points. They are created by extract-grammar and live in `grammar-index/grammar/`. The files that live directly in `grammar-index/` (non-recursively) are topic index files, which have `## Entries`, not `## Sub-topics`. Scanning `grammar-index/` non-recursively for `## Sub-topics` will find nothing useful.

**Fix:** Change the scan path to `grammar-index/grammar/` (non-recursively or with a depth-1 glob). Update the descriptive prose to match: "Scan all files in `grammar-index/grammar/` (exclude `index.md` if present) that contain a `## Sub-topics` section."

---

## Dependencies and Ordering

The shared files must exist before any skill file references them. The correct creation order is:

1. Create `_conventions.md`
2. Create `_patterns.md`
3. Modify skill files (any order; suggested: preprocess, review, structure, see-also, extract, update)

The two bug fixes are independent of the shared-file refactor and can be applied in the same editing pass as the skill file changes.
