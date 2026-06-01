---
name: _conventions
description: Shared output contract for all lesson-to-web skills. Load upfront.
---

# Lesson-to-Web Conventions

This file is the single source of truth for rules that must be consistent across all lesson-to-web skills. Every skill loads this file unconditionally before executing any step.

---

## Canonical furigana format

- Inline per word, ASCII parentheses: `明日(あした)の仕事(しごと)`
- Never use fullwidth parentheses for furigana output
- Never place readings after the whole word group

---

## File locations and naming

- Grammar point files: `grammar-index/grammar/<slug>.md`
- Container files: `grammar-index/grammar/<slug>.md` (identified by presence of `## Sub-topics`)
- Topic index files: `grammar-index/<topic>.md` (identified by presence of `## Entries`)
- Vocabulary subfiles: `grammar-index/grammar/vocabulary/<subdir>/<slug>.md`

---

## Frontmatter conventions

Required fields and expected values on file creation:

- `lesson` — source lesson identifier (e.g. `UN4GL7`)
- `pattern` — the grammar pattern string (e.g. `〜ている`)
- `topic_slug` — slug of the primary topic this pattern belongs to
- `level` — JLPT level string (e.g. `N4`)
- `proofread` — boolean; starts as `false`; only see-also-grammar sets it to `true`

No skill modifies `lesson`, `pattern`, `topic_slug`, or `level` after file creation.

---

## File structure rules (grammar point file)

Required sections in order:

1. Frontmatter (`---` block)
2. `# <pattern>` — heading matching the `pattern` frontmatter field
3. `> <gloss>` — one-line English gloss
4. `## Structure`
5. `## Examples`
6. `## Use Cases` (optional)
7. `## Notes` (optional)
8. `## See also` (final section)

Container files use `## Sub-topics` in place of the standard sections. Topic index files use `## Entries`.

---

## proofread: true guard

Before starting any step on a file, read its frontmatter. If `proofread: true` is already set, pause and ask:

```
<slug>.md already has proofread: true. Re-process anyway? (yes / no)
```

- **no** — skip all steps for that file and note it as skipped in the handoff summary.
- **yes** — proceed with all steps.

---

## Never touch

Applies to all lesson-to-web skills:

- `<!--ID: -->` lines — never add, remove, or shift
- `TARGET DECK` lines — never touch
- Japanese text — never translate kana or kanji
- Files outside `grammar-index/grammar/` (except: skills that explicitly read topic files from `grammar-index/` for context, and extract-grammar step 8 which inserts one wikilink into a lesson file)
- Lesson files under `JPLessons/` beyond the extract-grammar step 8 wikilink insertion
- Other skill files or `.cowork/instructions.md`
- Do not run `git push` or any remote git operation
- Frontmatter fields other than `proofread` — no skill modifies `lesson`, `pattern`, `topic_slug`, or `level` after file creation
