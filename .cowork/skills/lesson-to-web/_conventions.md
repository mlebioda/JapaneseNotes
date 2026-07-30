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
- `topic_slug` — slugs of the topic(s) this pattern belongs to (inline array, up to 3)
- `level` — JLPT level string (e.g. `N4`)
- `proofread` — boolean; starts as `false`; only see-also-grammar sets it to `true`
- `partial` — boolean; optional. Absent, or `false`-equivalent, when a file is fully extracted by extract-grammar. Set to `true` only when register-confusability-grammar's backfill mode creates a minimal stub for a grammar point that has not yet been through full extraction. No skill removes or clears `partial: true` automatically — only a future full `extract-grammar` pass on the source lesson completes the file and clears the flag.

Optional machine-readable fields (the ontology layer — frontmatter mirrors of human-readable content):

- `register` — bare scalar; one of `neutral | polite | tiered | unknown`. Normally owned by register-confusability-grammar Step 8, which writes it whenever it writes/overwrites the `## Register` section: `polite` mirrors the section value "polite-context typical"; `unknown` mirrors "unknown — insufficient source material". Overwritten (not appended) on every re-run, mirroring the section overwrite rule. **Seeding exception:** extract-grammar may also write `## Register` and `register:` at file-creation time, when the source lesson has its own `### Register` heading under a grammar point (see `_heading-roles.md` scaffolding special case) — the lesson author's own analysis, not hashtag-derived. register-confusability-grammar still has final authority: a later run overwrites the seeded value with its own hashtag-based analysis, same as any other file. No skill other than extract-grammar (seeding) and register-confusability-grammar (authoritative) writes this field.
- `confused_with` — YAML array of grammar slugs. Owned by register-confusability-grammar Step 9. Append-only and dedup-checked; must always mirror the link targets of the `## Often confused with` section (one array entry per section link). No other skill writes this field.
- `function` — YAML array of 0–2 values taken exclusively from the **`function` controlled vocabulary** section below. Created as `function: []` by extract-grammar's grammar point template (step 7) and populated by extract-grammar step 9d during the same run; immutable after that run completes (same protected status as `topic_slug`). Grammar point files only — container files and vocabulary files never carry `function`.

**Frontmatter immutability rule.** "After file creation" means **after the creating skill's run completes** — a skill may still patch fields it owns during the same run that created the file (extract-grammar step 9d patches `topic_slug`, created as `""` in step 7, and assigns `function` in the same step). Once the creating skill's run completes:

- `lesson`, `pattern`, `topic_slug`, `function`, and `level` are immutable — no skill modifies them.
- **Scoped carve-out:** `register` and `confused_with` may be written or updated after creation, but **only** by register-confusability-grammar Steps 8–9, and only as described above (`register`: overwrite by Step 8; `confused_with`: dedup-checked append by Step 9). No other skill, and no other field.

### Canonical YAML serialization

- Arrays are written in inline JSON-compatible style, matching `topic_slug`'s existing convention: `topic_slug: ["reasons-causes"]`, `confused_with: ["slug-a", "slug-b"]`, `function: ["purpose"]`. This is load-bearing: `.claude/scripts/grammar-audit.py` parses these values with `json.loads`. Never use YAML block-list style (indented `- item` lines) for these fields.
- `register` is a bare scalar: `register: neutral` (no quotes, no array).
- **Insertion position** when adding `register:` or `confused_with:` to an existing frontmatter block: insert after `level`, before `proofread`.
- **Creation-template field order:** `lesson`, `pattern`, `topic_slug`, `function`, `level`, `proofread` (, `partial`). Deterministic placement — different sessions must produce byte-identical frontmatter layouts.

---

## `function` controlled vocabulary

Single source of truth for the values allowed in the `function:` frontmatter field. The allowed values are exactly:

`purpose`, `cause-reason`, `permission`, `prohibition`, `obligation`, `desire`, `intention`, `hearsay-appearance`, `conditional`, `temporal`, `comparison`, `existence-location`, `means-method`, `direction-destination`, `quantity-counting`, `request`, `giving-receiving`, `potential`, `passive-causative`, `formality`

Rules:

- `function` is a YAML array with 0–2 values per file. An empty array (`function: []`) is allowed and correct when nothing on the list fits — do not force a value.
- **Hard stop — skills never invent values.** If a value not on this list seems needed, extending the list means editing this section **first**, with explicit user confirmation. The new value may not be used anywhere until this section has been updated.
- `function` joins the protected after-creation fields: set by extract-grammar during its own run (step 9d, same run-scoped pattern as `topic_slug`), immutable after that run completes.
- Grammar point files only — container files and vocabulary files never carry `function` (they do not participate in the confusability graph).

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
8. `## Register` (optional — populated by register-confusability-grammar)
9. `## Often confused with` (optional — may be absent on first pass; populated by register-confusability-grammar)
10. `## See also` (final section)

Container files use `## Sub-topics` in place of the standard sections. Topic index files use `## Entries`.

`## See also` keeps its existing container-only rule (links only to files with `## Sub-topics`). Point-to-point relationships between individual grammar points (e.g. ように / のに / ために) belong exclusively in `## Often confused with`, never in `## See also`.

---

## Examples content format

Every example sentence inside an Examples section is one Markdown bullet (`- `), never a
blank-line-separated paragraph. One sentence per bullet, in source order. Applies to both
shapes an Examples section takes:
- `## Examples` — the single shared section in Structure 1.
- `### Examples` — nested under each `## N. Use Case Name` heading in Structure 2. Each
  use case's examples stay scoped to that use case only — never pooled into one shared
  list across use cases.

```
## Examples

- これから夕飯(ゆうはん)を食(た)べるところで - Just as I'm about to eat dinner now, ...
- 家(いえ)に帰(かえ)ると、妻(つま)が晩(ばん)ご飯(はん)を作(つく)るところだった。 - When I got home, my wife was just about to make dinner.
```

Applies whenever this section is written or rewritten — extract-grammar on file creation,
and structure-grammar on any reformat into Structure 1 or Structure 2. Dialogue examples
(A: ... B: ...) stay on one bullet per exchange, not split across two bullets.

---

## "Often confused with" line format

Canonical format for every line inside a `## Often confused with` section. This is the single source of truth — register-confusability-grammar Step 9 uses it for both the forward line (current file) and the reverse line (matched file):

```
- [Label](/JapaneseNotes/grammar-index/grammar/<slug>) — test: <one-line question that picks between the two patterns>
```

The `— test:` prefix is mandatory. The question must be answerable in a way that chooses between exactly these two patterns — it is the future wrong-answer feedback line for discrimination exercises, so it must be extractable without NLP.

---

## proofread: true guard

Before starting any step on a file, read its frontmatter. If `proofread: true` is already set, pause and ask:

```
<slug>.md already has proofread: true. Re-process anyway? (yes / no)
```

- **no** — skip all steps for that file and note it as skipped in the handoff summary.
- **yes** — proceed with all steps.

**Scoped exception — register-confusability-grammar Step 9 backlink writes only:** when Step 9 writes the reverse half of a bidirectional "Often confused with" relationship into a *matched* file (not the file being primarily processed), this guard's "re-process anyway?" prompt does not apply, even if that matched file already has `proofread: true`. The write is not a re-process of that file — it is a bounded, dedup-checked edit limited to exactly two locations in the matched file:

1. The `## Often confused with` section line — append inside the section if it exists, or insert a new section immediately before `## See also` if it doesn't (see register-confusability-grammar Step 9 for exact mechanics).
2. The corresponding append to that file's `confused_with` frontmatter array — creating the field if absent (inserted after `level`, before `proofread`, per **Canonical YAML serialization**), touching only that one frontmatter line, never rewriting or reordering any other field.

This exception applies only to Step 9's backlink target files (including Step 9's mechanical section-without-array mirror repair on pairs matched in the current run); it never applies to the file being primarily processed by any skill, and never widens into a general bypass of this guard.

---

## Never touch

Applies to all lesson-to-web skills:

- `<!--ID: -->` lines — never add, remove, or shift
- `TARGET DECK` lines — never touch
- Register hashtags (`#sonkeigo` / `#kenjougo` / `#teineigo`) on example lines — source evidence for register-confusability-grammar Step 8; only see-also-grammar Step 10b removes them (final step). No other skill strips or rewrites them
- Japanese text — never translate kana or kanji
- Files outside `grammar-index/grammar/` (except: skills that explicitly read topic files from `grammar-index/` for context, and extract-grammar step 8 which inserts one wikilink into a lesson file)
- Lesson files under `JPLessons/` beyond the extract-grammar step 8 wikilink insertion
- Other skill files or `.cowork/instructions.md`
- Do not run `git push` or any remote git operation
- Frontmatter fields other than `proofread` — with one scoped carve-out: `register` and `confused_with` are writable, but solely by register-confusability-grammar Steps 8–9 (see **Frontmatter immutability rule** above). No skill modifies `lesson`, `pattern`, `topic_slug`, `function`, or `level` after the creating skill's run completes (the `partial` field is set once at stub-creation time by register-confusability-grammar's backfill mode and never modified afterward by any skill)
