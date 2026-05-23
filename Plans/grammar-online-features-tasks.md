# Grammar Online Features — Task Checklist

Derived from `grammar-online-features-plan.md`. Work top-to-bottom; items marked with a dependency note must wait for their prerequisite.

---

## Pre-implementation Discovery

- [ ] Fetch one live grammar-index topic page (e.g. `https://mlebioda.github.io/JapaneseNotes/grammar-index/ability-expressions`) and inspect HTML structure to confirm the CSS class wrapping content (needed for any future HTML parsing)
- [ ] Open one local `grammar-index/` topic file and confirm the wikilink format matches `[[LESSONCODE#anchor]]` before building the pattern extractor

---

## Feature 1 — Grammar Index Enrichment

- [ ] Read all 31 topic files in `grammar-index/` and collect every wikilink anchor text (the grammar pattern string after `#` in each `[[LESSONCODE#anchor]]` entry)
- [ ] Create `grammar-index/_grammar-patterns.md` with a Markdown table: columns Pattern | Topic slug | Description
- [ ] Populate the table — one row per pattern string, one row per topic it belongs to (patterns may repeat across multiple topic slugs)
- [ ] Verify every topic slug in the table matches an actual `.md` filename in `grammar-index/`
- [ ] Verify the GitHub Pages URL template works for at least two slugs: `https://mlebioda.github.io/JapaneseNotes/grammar-index/<slug>`

---

## Feature 2 — Update `fill-templates` Skill

_Depends on Feature 1 (`_grammar-patterns.md` must exist)._

- [ ] Read `.cowork/skills/fill-templates.md` in full
- [ ] Add "Step 7 — Grammar link annotation (optional pass)" after the current Step 6 in the skill file; make clear this is a separate pass run after all card generation is complete, not interleaved with card writing
- [ ] Specify the detection logic: scan only `#w` cards in `Rzeczowniki:`, identify sentence cards (contain a conjugated verb or grammar pattern), skip plain noun/adverb cards
- [ ] Specify the lookup logic: read `grammar-index/_grammar-patterns.md`, match pattern strings against the card's Japanese field
- [ ] Specify the output format for appended links: `> [Pattern name](https://mlebioda.github.io/JapaneseNotes/grammar-index/<slug>)` on a new line below the Japanese line
- [ ] Add a safety guard in the skill: only annotate cards that do NOT already have an `<!--ID: -->` line (i.e. newly generated cards only)
- [ ] Add a fallback: if `_grammar-patterns.md` does not exist, skip annotation silently
- [ ] Add a skip note: if the user does not request annotation, card generation output is complete after Step 6 with no annotation
- [ ] Test mentally: confirm the appended link line appears between the Japanese line and the next card separator (`---` or blank line), not inside an existing Anki block

---

## Feature 3 — New Skill: `practice-grammar-due`

_Depends on Feature 1 (`_grammar-patterns.md` must exist)._

- [ ] Create `.cowork/skills/practice-grammar-due.md`
- [ ] Define trigger phrases: "practice due grammar", "drill due", "what grammar is due"
- [ ] Add architecture note in skill file: GitHub Pages topic pages are index pages only and do not contain grammar explanation text; all grammar content is read from local lesson files; GitHub Pages URLs appear only in session output links
- [ ] Write the workflow: read `grammar-state.json`, collect all grammar points where `due_date` <= today
- [ ] Add early-exit: if no points are due, report this to the user and exit
- [ ] Write the local lesson file lookup step: resolve `lesson_file` field to a file path under `JPLessons/Udemy/`, read the `# 文法` section at the specific `grammar_header` anchor
- [ ] Write the vocab pool step: for each due point's lesson file, parse `# ごい` + `# ひょうげん`; merge pools across lessons, deduplicate by Japanese field
- [ ] Write the session output step: include a GitHub Pages link per grammar point using `topic_slug` field — for user navigation only, not fetched
- [ ] Add error handling: if a local lesson file is not found, skip that grammar point and log a warning in session output
- [ ] Copy exercise generation, grading, batch/interactive modes, session summary, and SM-2 persistence sections from `practice-grammar.md` — adapt references to content source
- [ ] Add shared-state warning in the skill file: `grammar-state.json` is shared with `practice-grammar` and `practice-grammar-group`
- [ ] Add "Never touch" section: TARGET DECK lines, `<!--ID: -->` lines, lesson files (read-only)

---

## Feature 4 — New Skill: `practice-grammar-group`

_Depends on Feature 1 (`_grammar-patterns.md` must exist)._

- [ ] Create `.cowork/skills/practice-grammar-group.md`
- [ ] Define trigger phrases: "practice group <slug>", "drill group <slug>", "practice topic <topic name>"
- [ ] Add architecture note in skill file: GitHub Pages topic pages are index pages only; the local `grammar-index/<slug>.md` file is read for the entry list; grammar explanations come from local lesson files; GitHub Pages URL is included in output and Anki links but not fetched
- [ ] Write the input normalization step: accept slug or plain English name; fuzzy-match plain names against `grammar-index/` filenames
- [ ] Write the topic file read step: read local `grammar-index/<slug>.md`, extract `## Entries` wikilinks — no GitHub Pages fetch needed
- [ ] Write the wikilink parse step: extract lesson code and anchor from each `[[LESSONCODE#anchor]]` entry
- [ ] Write the local grammar explanation step: for each entry, read the local lesson file and extract the `# 文法` section body at the specific anchor
- [ ] Write the vocab pool step: for each grammar point, load `JPLessons/Udemy/N<level>/Gramatyka/<code>.md`, parse `# ごい` + `# ひょうげん`; merge pools, deduplicate by Japanese field
- [ ] Write the exercise generation step: one exercise per entry in the topic file; apply same rules as `practice-grammar`
- [ ] Write the session output step: include the GitHub Pages URL for the topic (`https://mlebioda.github.io/JapaneseNotes/grammar-index/<slug>`) for user navigation and Anki links — not fetched
- [ ] Clarify the grammar point ID convention: `<lesson-code>::<anchor-slug>` — same as existing skills, group file not part of the ID
- [ ] Copy batch/interactive modes, grading, session summary, and SM-2 persistence from `practice-grammar.md` — adapt
- [ ] Add note: large topic files (e.g. `verb-forms.md` has 14+ entries) produce long sessions; user can stop early
- [ ] Add error handling: if a lesson file is not found locally, skip its vocab and grammar explanation; log a warning in session output
- [ ] Add "Never touch" section: TARGET DECK lines, `<!--ID: -->` lines, lesson files (read-only)

---

## Feature 5 — Vocabulary Extraction Skill

_Independent — no prerequisite._

- [ ] Create `.cowork/skills/extract-vocabulary.md`
- [ ] Define trigger phrases: "extract vocabulary from <lesson>", "extract vocab <lesson>", "update vocabulary files"
- [ ] Write the file-finding step: single lesson by code, or all lessons under `JPLessons/Udemy/` for the bulk "update" trigger
- [ ] Write the pre-summary extraction step: `awk '/^# Summary$/{exit} {print}'` on the lesson file
- [ ] Write the vocab line extraction step: collect all `#w`, `#wc`, `#wp` lines from `# ごい` and `# ひょうげん` sections
- [ ] Write the classification step: `#wc` and `#wp` always go to words; `#w` where Japanese field ends with `(する)` always goes to words (suru noun rule, regardless of token count); remaining `#w` classified as word if single lexeme (1–3 tokens, no conjugated verb), as expression if sentence-length or contains a verb form
- [ ] Write the idempotency check: if `## <lesson-code>` block already exists in the target file, skip that lesson
- [ ] Write the append step: add `## <lesson-code>` heading followed by the extracted lines to the appropriate file
- [ ] Write the create-if-missing step: if `Vocabulary/words-extracted.md` or `Vocabulary/expressions-extracted.md` does not exist, create it with a header line (`# Extracted Words` or `# Extracted Expressions`) before appending
- [ ] Confirm output files are in `Vocabulary/`, not `JPLessons/`, so Anki plugin does not scan them
- [ ] Add "Never touch" section: no TARGET DECK lines should ever be written to these files; the skill must never read past `# Summary` in lesson files

---

## Cross-cutting

- [ ] Update `.cowork/instructions.md` skills table to list the three new skills (`practice-grammar-due`, `practice-grammar-group`, `extract-vocabulary`) once their skill files are written
- [ ] Confirm `_grammar-patterns.md` is not rendered by Jekyll (underscore prefix is excluded by default — verify `_config.yml` has no `include:` override that would pull it in)
- [ ] After deploying any new `grammar-index/` content, wait for GitHub Actions to complete before testing GitHub Pages links in session output
