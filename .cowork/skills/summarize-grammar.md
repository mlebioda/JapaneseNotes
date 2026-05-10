---
name: summarize-grammar
description: >
  Process a single lesson file and add its grammar points to the topic-grouped
  master index at /Gramatyka-Index/. Each grammar point is linked (not copied)
  to the source lesson and may appear in multiple topic files. Trigger:
  "summarize <lesson>", "index <lesson>", or "add <lesson> to grammar index".
---

# Summarize Grammar Skill

## Trigger

User says any of:

- "summarize <lesson>" — e.g. "summarize UN4GL5"
- "index <lesson>"
- "add <lesson> to grammar index"

If user references a lesson by code only, find the file under `JPLessons/Udemy/N<level>/Gramatyka/` — match by prefix, ignore trailing description in filename.

---

## Workflow

1. **Find the lesson file** — by code or filename. Determine its level (`N5`, `N4`, …) from the path segment.
2. **Extract everything before `# Summary`** — never read the whole lesson file:

   ```bash
   awk '/^# Summary$/{exit} {print}' "$LESSON"
   ```

3. **Parse `# 文法` and `# Vocabulary`** — collect every grammar point heading (see **Parsing**).
4. **List existing topic files** — `ls /Gramatyka-Index/*.md` (excluding `_index.md`). This is the current taxonomy the LLM must respect.
5. **Classify each grammar point** — pick which topic file(s) it belongs to. A point may go in multiple. Bias toward existing topic files; only create a new topic file when no existing one fits AND the new topic is specific and reusable across lessons.
6. **Update topic files** — for each target topic file:
   - **Exists**: append the new entry under `## Entries`, deduped (skip if the same `[[<lesson>#<header>]]` link is already present).
   - **New**: create from the topic file template below.
7. **Update `_index.md`** — only if a new topic file was created during this run. Regenerate it from the current state of `/Gramatyka-Index/`.

No confirmation needed at any step.

---

## Parsing grammar topics

Both `# 文法` and `# Vocabulary` contain grammar points. Parse them identically.

Inside each section, find every `^## ` heading. These are the grammar points to index. For each one:

- The heading text is the **point label** (preserve Japanese exactly — kanji, kana, spacing, punctuation).
- The wikilink target is `[[<lesson-code>#<exact heading text>]]`.

If a `##` has only `###` subpoints with no prose of its own, promote the `###` headings to be the indexed points instead. If the `##` has both prose and `###` children, index the `##` only.

---

## Entry format

Each entry in a topic file is one line:

```
- [[<lesson-code>#<exact Japanese heading>]] · <level>
```

Examples:

- `- [[UN5GL18#から]] · N5`
- `- [[UN4GL3#ので]] · N4`
- `- [[UN4GL7#ため]] · N4`

No copied lesson text. The wikilink IS the data. Level (N5/N4/etc.) comes from the lesson's path.

---

## Topic file template

```markdown
# <Topic Name>

> <One-line description of what this topic covers — your own words, do not copy lesson text>

## Entries

- [[<lesson-code>#<heading>]] · <level>

## See also

- [[<related-topic>]] — <short reason>
```

When creating a new topic file:

- Filename: kebab-case English, descriptive, reusable across future lessons. Good: `reasons-causes.md`, `verb-te-form.md`, `particles-wa-ga.md`. Bad: `kara.md`, `because-only.md`, `n5-particles.md`.
- Title: human-readable derivation of the filename (`reasons-causes` → `# Reasons / Causes`).
- Description: one sentence, your own words, explaining when to look here.
- First entry: the grammar point that triggered creation.
- "See also": 1–2 wikilinks to existing related topics if obvious; otherwise omit the section.

---

## Dedup rule

Before appending an entry to a topic file, search the file's existing `## Entries` list for the exact wikilink (case-sensitive, including the heading anchor). Skip if already present.

Two entries with the same Japanese heading but different lesson codes are NOT duplicates — keep both.

---

## `_index.md`

Lives at `/Gramatyka-Index/_index.md`. Groups topic files into a fixed high-level taxonomy:

- **Verbs** — `verb-*` topic files
- **Adjectives** — `adjectives-*` topic files
- **Particles** — `particles-*` topic files
- **Patterns** — sentence-level patterns: reasons, comparisons, suggestions, obligations, giving-receiving, conditionals, etc.
- **Forms & Counters** — counters, time expressions, numbers
- **Other** — anything that doesn't fit the above

Regenerate `_index.md` only when a new topic file was created during this run. Read each topic file's `> <description>` line to fill in the index.

Format:

```markdown
# Grammar Index

## Verbs

- [[verb-te-form]] — <description>
- [[verb-passive]] — <description>

## Particles

- [[particles-wa-ga]] — <description>

## Patterns

- [[reasons-causes]] — <description>
- [[comparisons]] — <description>

(etc., omit empty groups)
```

---

## Classification guidance

- **Bias toward existing topic files.** The list from step 4 is the current taxonomy.
- **Multiple topics OK** if a point genuinely fits more than one (e.g., `から` fits both `particles-direction` and `reasons-causes`).
- **Cap at 3 topics per point.** If more than 3 seem to fit, you're being too liberal — pick the strongest 3.
- **New topic file only when**: no existing topic fits AND the new name is broad enough to attract future lessons (not a one-off).

---

## Never touch

- Source lesson files (read-only — only path, level, and grammar headings matter).
- TARGET DECK lines.
- `<!--ID: -->` lines.
- Other skill files or the instructions file.
