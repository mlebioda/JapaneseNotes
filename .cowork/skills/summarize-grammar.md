---
name: summarize-grammar
description: >
  Process a single lesson file and add its grammar points to the topic-grouped
  master index at /grammar-index/. Each grammar point is linked (not copied)
  to the source lesson and may appear in multiple topic files. Trigger:
  "summarize <lesson>", "index <lesson>", or "add <lesson> to grammar index".
---

# Summarize Grammar Skill

## Trigger

User says any of:

- "summarize <lesson>" — e.g. "summarize UN4GL5"
- "index <lesson>"
- "add <lesson> to grammar index"

If user references a lesson by code only, find the file under `JPLessons/Udemy/N<level>/Grammar/` — match by prefix, ignore trailing description in filename.

---

## Workflow

1. **Find the lesson file** — by code or filename. Determine its level (`N5`, `N4`, …) from the path segment.
2. **Extract everything before `# Summary`** — never read the whole lesson file:

   ```bash
   awk '/^# Summary$/{exit} {print}' "$LESSON"
   ```

3. **Parse `# 文法` and `# Vocabulary`** — collect every grammar point heading (see **Parsing**).
4. **List existing topic files** — `ls /grammar-index/*.md` (excluding `index.md`). This is the current taxonomy the LLM must respect.
5. **Classify each grammar point** — pick which topic file(s) it belongs to. A point may go in multiple. Bias toward existing topic files; only create a new topic file when no existing one fits AND the new topic is specific and reusable across lessons.
6. **Update topic files** — classification is a judgment call made by Claude, not a script. Once the grouping is settled, use Python for the mechanical write. For each target topic file:
   - **Exists**: insert all new entries for that file as a single batch, immediately before the `## See also` line (or at the end of `## Entries` if there is no `## See also`). Never use `cat >>` — it appends to end-of-file and breaks files that have `## See also`. Use a Python snippet like:
     ```python
     with open(path) as f: content = f.read()
     block = "\n".join(new_entries)
     if "## See also" in content:
         content = content.replace("\n## See also", "\n" + block + "\n\n## See also", 1)
     else:
         content = content.rstrip() + "\n" + block + "\n"
     with open(path, "w") as f: f.write(content)
     ```
   - **New**: create from the topic file template below.
   - Always deduplicate: skip any entry whose exact wikilink is already present in the file.
7. **Update `index.md`** — only if a new topic file was created during this run. Regenerate it from the current state of `/grammar-index/`.
8. **Print coverage summary** — after all writes are done, output a markdown table listing every grammar point parsed from the lesson. See **Coverage summary** below.

No confirmation needed at any step.

---

## Parsing grammar topics

Both `# 文法` and `# Vocabulary` contain grammar points. Parse them identically.

Lesson files use inconsistent heading levels (some use `##`, some start at `###` or `####`). Apply the promotion rule recursively until you reach headings that have substantive content:

1. Start at `##`. If no `##` headings exist in the grammar section, drop to `###` as the primary level.
2. **Promotion rule** — if a heading has *only* sub-headings with no prose of its own, replace it with those sub-headings. Apply this rule at every level (`##`→`###`, `###`→`####`), stopping when the heading has actual content (prose, examples, or structure notes).
3. If a heading has both prose and sub-headings, index the heading itself (do not promote).
4. **Skip vocabulary items** — if a `###`/`####` heading in a grammar section is clearly a vocabulary gloss rather than a grammar pattern (e.g. a single word with a translation, no structural rule), skip it.

For each heading kept:

- The heading text is the **point label** (preserve exactly — kanji, kana, spacing, punctuation, including any Polish or English words in the heading).
- The wikilink target is `[[<lesson-code>#<exact heading text>]]`.

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

## `index.md`

Lives at `/grammar-index/index.md`. Groups topic files into a fixed high-level taxonomy:

- **Verbs** — `verb-*` topic files
- **Adjectives** — `adjectives-*` topic files
- **Particles** — `particles-*` topic files
- **Patterns** — sentence-level patterns: reasons, comparisons, suggestions, obligations, giving-receiving, conditionals, etc.
- **Forms & Counters** — counters, time expressions, numbers
- **Other** — anything that doesn't fit the above

Regenerate `index.md` only when a new topic file was created during this run. Read each topic file's `> <description>` line to fill in the index.

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

Classification is Claude's judgment — never automate it. Read each grammar point's content before deciding.

- **Bias toward existing topic files.** The list from step 4 is the current taxonomy.
- **Multiple topics OK** if a point genuinely fits more than one (e.g., `から` fits both `particles-direction` and `reasons-causes`).
- **Cap at 3 topics per point.** If more than 3 seem to fit, you're being too liberal — pick the strongest 3.
- **New topic file only when**: no existing topic fits AND the new name is broad enough to attract future lessons (not a one-off).
- **Present the classification plan to yourself first** — list every grammar point and its target file before writing anything. This catches misclassifications before they touch the index.

---

## Coverage summary

After completing all file writes, print a table to the chat. One row per grammar point parsed from the lesson.

Format:

```
| Topic | Topic file | Status |
|---|---|---|
| `### から` | reasons-causes | ✅ already indexed |
| `## て-form` | verb-te-form | 🆕 new topic |
| `### ので` | reasons-causes | ✅ added |
```

**Status values:**
- `✅ already indexed` — the exact wikilink was already present in the topic file (dedup skipped it)
- `✅ added` — entry was appended to an existing topic file
- `🆕 new topic` — a new topic file was created for this entry

If a grammar point was classified into multiple topic files, emit one row per topic file.

---

## Never touch

- Source lesson files (read-only — only path, level, and grammar headings matter).
- TARGET DECK lines.
- `<!--ID: -->` lines.
- Other skill files or the instructions file.
