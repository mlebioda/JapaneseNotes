---
name: _patterns
description: Input recognition registry for unexpected source formats. Load lazily, only when encountering unrecognised input.
---

# Lesson-to-Web Input Patterns

This file records decisions about unexpected or ambiguous input formats encountered during processing. Skills load this file only when they encounter input that does not match the canonical format defined in `_conventions.md`.

---

## Lazy-load rule

A skill loads `_patterns.md` only when it encounters input it cannot classify on its own.

- If the pattern is found in this registry: apply the stored decision silently and continue.
- If the pattern is not found: ask the user, record the decision in this file, then continue.

---

## Pattern registry

### Trailing furigana after word group

**Format examples:**

- Fullwidth parens, 、-separated: `明日の仕事（あした、しごと）`
- ASCII parens, comma-separated: `明日の仕事 (あした, shigoto)`

One or more kanji-words are grouped together, followed by a parenthesised reading list at the end of the phrase rather than inline after each word.

**Decision:** Convert to inline per-word format using ASCII parentheses.

**Output:** `明日(あした)の仕事(しごと)`

**Apply:** Silently. This is the standard Step 3 rule in preprocess-grammar and requires no user confirmation.
