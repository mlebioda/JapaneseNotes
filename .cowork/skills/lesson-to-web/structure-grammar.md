---
name: structure-grammar
description: >
  Enforce file structure on grammar files under grammar-index/grammar/. Detects
  container files (skips them), normalises sections, infers Structure 1 vs Structure 2,
  and reformats with user confirmation. Trigger: "structure grammar <file>" or called
  from review-grammar.
---

# Structure Grammar Skill

## Trigger

- "structure grammar `<slug>`" — filename without `.md`
- "structure grammar grammar-index/grammar/`<slug>`.md" — full relative path
- (called automatically from review-grammar with a list of file paths)

---

## Workflow

Process each file in order. Apply all steps to one file before moving to the next.

If called with **all** mode (from review-grammar "all" answer): skip the handoff prompt at the end and automatically continue to see-also-grammar.

---

## Shared files

Load `.cowork/skills/lesson-to-web/_conventions.md` before starting.

---

Check the proofread: true guard (see _conventions.md) before processing each file.

---

### Step 7 — File structure enforcement

#### Container file detection

Before applying any normalisation, check whether the file is a container file:
- A `## Sub-topics` section is present.

If the file is a container file:
- Skip all normalisation and structure inference.
- Log: `Structure: container file — Step 7 skipped`.
- Continue to handoff.

#### Section normalisation (silent, before proposing structure)

- `## Examples` absent → add an empty `## Examples` section between `## Structure` and `## Notes`.
- `## Notes` present but empty → remove the section entirely.

#### Summary line

The gloss line (`> ...`) immediately under the main heading is the summary. It stays as a blockquote — not a separate `## Summary` header.

#### Inferring which structure to use

**Structure 1** — use when the grammar point has a single unified pattern that applies across word types in the same way.

**Structure 2** — use when the grammar point has two or more meaningfully distinct use cases that each need separate explanation.

Infer the structure from file content, propose it to the user, and **wait for confirmation before reformatting**.

If content is ambiguous, do not guess. Present:

```
Could not determine structure for: grammar-index/grammar/<slug>.md
Content summary: <brief description>

Options:
  1. Structure 1 — shared structure across word types
  2. Structure 2 — distinct numbered use cases
  3. Skip restructuring for this file

What should I do?
```

#### Structure 1 — Shared structure across word types

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

## Examples

[Full natural sentences showing real usage in context — required; leave empty if none available]

## Notes

[Optional — nuances, contrasts, or learner pitfalls. Omit the section entirely if empty.]

## See also

- [Container Name](/JapaneseNotes/grammar-index/<slug>) — short reason
```

Omit word-type sections and tense rows that do not apply. Each remaining row must have at least one inline example (`→ example`).

**Section distinction:**
- `## Structure` rows use `→` for short inline examples showing the pattern mechanically.
- `## Examples` holds full natural sentences showing real usage in context.

#### Structure 2 — Distinct use cases

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

## Examples

[Full natural sentences — required; leave empty if none available]

## Notes

[Optional — omit if empty]

## See also

- [Container Name](/JapaneseNotes/grammar-index/<slug>) — short reason
```

Each use case is a numbered `##` header. Structure subsections follow the same word-type / tense pattern as Structure 1, limited to what applies.

---

## Handoff summary

After processing all files, print:

```
structure-grammar — N files processed

  grammar-index/grammar/<slug>.md
    Structure: Structure 1 (shared) — confirmed by user

  grammar-index/grammar/<slug>.md
    Structure: container file — Step 7 skipped

  grammar-index/grammar/<slug>.md
    Structure: Structure 2 (use cases) — 2 use cases confirmed by user
```

Then ask (skip if running in **all** mode):

```
Run see-also-grammar on these files? (yes / no / all)
```

- **yes** — load `.cowork/skills/lesson-to-web/see-also-grammar.md` and pass the file list.
- **no** — end the skill.
- **all** — load see-also-grammar, instructing it to continue in all mode (no further handoff prompts after processing).
