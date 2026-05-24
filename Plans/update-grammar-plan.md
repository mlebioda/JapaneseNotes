# update-grammar Skill — Design Plan

## Purpose

Post-process grammar files created by `extract-grammar`. Each file is reviewed and updated according to 7 rules before being marked `proofread: true`.

## Input

One or more file paths to `grammar-index/grammar/*.md` files. Passed either:
- Directly by the user ("update grammar seeking-approval")
- Automatically from `extract-grammar` step 10

---

## Rule 1 — Language consistency

All prose in the file must be in English.

- Sections to check: gloss line (`>`), `## Structure`, `## Meaning`, `## Examples`, `## Notes`, and any new structured sections.
- Detection: Polish diacritics (ą ę ó ś ź ż ć ń ł) or common Polish words (jest, są, się, nie, lub, oraz, przez, które, który, też, już, można, należy).
- Action: translate Polish prose to English in-place.
- Never translate: Japanese text, frontmatter field values.

---

## Rule 2 — Furigana format conversion

Convert trailing-reading format to inline furigana.

**Trailing format** (input):
```
明日の仕事のしりょうですね（あした、しごと）
```

**Inline format** (output):
```
明日(あした)の仕事(しごと)のしりょうですね
```

**Algorithm:**
1. Detect lines with a trailing parenthesised reading list — either `（r1、r2）` or `(r1, r2)`.
2. Strip the trailing list; split into ordered readings.
3. Scan left-to-right for kanji-words (maximal runs of CJK Unified Ideograph characters).
4. Match readings to kanji-words in order; insert `kanji-word(reading)` inline.
5. Remove the trailing list from the line.
6. Use ASCII `()` for all inserted furigana.
7. If reading count ≠ kanji-word count: log a warning and leave the line unchanged.
8. Lines already in inline format: skip.
9. Lines with no kanji: skip.

---

## Rule 3 — Remove vocabulary tags

If any line in the file starts with `#w `, `#wc `, or `#wp `, strip the tag prefix (keep everything after the tag and space).

```
#w 自分の意見 (じぶん, いけん) - one's own opinion
→ 自分(じぶん)の意見(いけん) - one's own opinion
```

Note: tag removal happens before furigana conversion on the same line.

---

## Rule 4 — Typos and grammar mistakes

Review all prose sections for spelling and grammar errors in English text. Fix silently — no need to ask the user for minor corrections. Log what was changed in the completion report.

---

## Rule 5 — Substantive correctness check

Verify that the grammar explanation is accurate:
- Structure rules correct (e.g. correct conjugation forms listed)
- Example sentences grammatically valid
- English glosses match the Japanese

May use web search to verify. If something appears incorrect:
1. Present the issue and proposed correction to the user.
2. Wait for user approval before changing.

---

## Rule 6 — Missing information

Check whether the file is missing important information for the grammar point:
- Common usage nuances not mentioned
- A major conjugation form not shown
- A frequent error learners make not noted

If something is missing: suggest it to the user. Do not add content without user approval.

---

## Rule 7 — File structure enforcement

### Summary line

The gloss line (`> ...`) immediately under the main heading is the summary. It remains a blockquote line — not a separate `## Summary` header.

### Choosing a structure

The skill infers which structure fits from the file's content:

**Use Structure 1** when the grammar point has a single unified pattern that applies across word types (verbs, adjectives, nouns) in the same way.

**Use Structure 2** when the grammar point has two or more meaningfully distinct use cases that each need separate explanation.

The skill proposes the inferred structure and asks the user to confirm before reformatting.

If the content does not clearly match either structure (ambiguous, mixed, or unusual layout), the skill must not guess. Instead, present the issue to the user and ask how to proceed:

```
Could not determine structure for: grammar-index/grammar/<slug>.md
Content summary: <brief description of what's in the file>

Options:
  1. Structure 1 — shared structure across word types
  2. Structure 2 — distinct numbered use cases
  3. Skip restructuring for this file

What should I do?
```

Wait for user input before making any changes to the file structure.

---

### Structure 1 — Shared structure across word types

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

## See also

- [Pattern Name](/JapaneseNotes/grammar-index/grammar/slug) — short reason
```

**Omit word-type sections that do not apply** (e.g. a particle-only pattern may only have a Noun section). Omit tense rows that do not apply for the pattern. Each row must have at least one example.

---

### Structure 2 — Distinct use cases

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

## See also

- [Pattern Name](/JapaneseNotes/grammar-index/grammar/slug) — short reason
```

Each use case is a numbered `##` header. Structure subsections follow the same word-type / tense pattern as Structure 1, limited to what applies.

---

## See also population algorithm

After structure is finalised:

1. Search all files in `grammar-index/` (non-recursive, excluding `grammar/` subdir and `index.md`) for any that mention the current file's slug in their `## Entries` section.
2. For each matching topic file, collect all other slugs listed in `## Entries`.
3. De-duplicate across all matching topic files.
4. Format each as an absolute URL link:
   `- [Pattern Name](/JapaneseNotes/grammar-index/grammar/<slug>) — <topic file name or short reason>`
5. Populate the `## See also` section (replace existing content if any).
6. If no related files are found, write `## See also` with a single line: `*(none)*`.

---

## Processing order per file

1. Remove vocabulary tags (#w / #wc / #wp)
2. Language consistency (translate Polish)
3. Furigana conversion
4. Typo/grammar fix
5. Substantive check (ask user if issues found)
6. Missing info suggestions (ask user)
7. Structure enforcement (propose + confirm with user)
8. See also population
9. Set `proofread: true` in frontmatter

---

## Completion report

```
update-grammar — 2 files processed

  grammar-index/grammar/seeking-approval.md
    Tags removed: 0
    Furigana: 3 lines converted
    Language: no Polish found
    Typos: 1 fixed ("listenner" → "listener")
    Substantive: OK
    Missing info: suggested adding negative form examples (user approved)
    Structure: Structure 1 applied
    See also: 1 link added (sentence-final-particles group)
    → proofread: true

  grammar-index/grammar/point-4.md
    Tags removed: 2
    Furigana: 0 lines (no trailing format found)
    Language: 1 section translated
    Typos: none
    Substantive: 1 issue raised, user approved correction
    Missing info: none suggested
    Structure: Structure 2 applied (2 use cases confirmed by user)
    See also: 2 links added (demonstratives group)
    → proofread: true
```
