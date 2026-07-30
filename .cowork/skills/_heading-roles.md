---
name: _heading-roles
description: Shared heading-role recognition rules for lesson 文法/Vocabulary sections. Loaded by lesson-to-web/extract-grammar and practice-grammar so a heading means the same thing in both pipelines.
---

# Heading Roles

Single source of truth for classifying headings found in a lesson file's `# 文法` and `# Vocabulary` sections. Both `lesson-to-web/extract-grammar` (file extraction) and `practice-grammar` (drill-topic parsing) load this file and apply the same rules.

Roles are decided by **content and tree position, not by heading level** — real patterns appear at `##`, `###`, and `####` depending on the lesson (e.g. in UN4GL14: `## V「て形」おります`, `### Verbs`, `#### お・ご V「ます形」します`).

## The three roles

Evaluate in this order; the first rule that matches wins.

### 1. Part-of-topic (scaffolding)

The heading's text is a bare structural label from the **scaffolding label list** below (match case-insensitively, ignoring trailing punctuation), at any level.

- Its body belongs to the nearest non-scaffolding ancestor heading.
- Never becomes a file, never becomes a drill point, never appears in classification tables.

**Scaffolding label list:**

`Examples`, `Example`, `Structure`, `Structures`, `Form`, `Forms`, `Conjugation`, `Use Cases`, `Use cases`, `Note`, `Notes`, `Function`, `Exception`, `Exceptions`, `Core rule`, `Connecting sentences`, `Meaning`, `Register`

**Extending the list:** if a lesson uses a new structural label not listed here, add it to this list **first** (with explicit user confirmation), then proceed. Skills never treat an unlisted label as scaffolding silently, and never extend this list on their own.

**Special case — `Register`:** unlike other scaffolding labels, a `### Register` heading's body is not folded into the parent's general prose. extract-grammar routes it directly into the parent grammar point file's `## Register` section (and, when the text states a scalar value like "Register: neutral", also seeds the `register:` frontmatter field at creation time). See `_conventions.md` for the frontmatter ownership note this implies.

### 2. Container

A non-scaffolding heading with **no explanatory content of its own** — at most a one-line gloss/description — whose child headings include other containers or points.

- Examples: `## 謙譲語（けんじょうご) - Humble expressions` (gloss line only, sub-patterns below); `### Verbs` (pure grouping, no body).
- extract-grammar: becomes a container file (`## Sub-topics` links).
- practice-grammar: **excluded from drilling** — its descendant points are drilled individually.

### 3. Point

Any other non-scaffolding heading — it has its own explanation, structure, or examples, either directly in its body or via scaffolding children.

- Examples: `#### お・ご V「ます形」します` (Structure + Examples scaffolding children); `## ウチ・ソト (Uchi-Soto)` — whose children (`### ウチ`, `### ソト`, `### Core rule`) explain the concept rather than defining separate patterns.
- extract-grammar: becomes a standalone grammar point file.
- practice-grammar: becomes one drill point; scaffolding children fold into its body.

## Edge rules

- **Explanation-part children:** a child heading that carries no pattern of its own (no formation rule, no distinct grammatical construction — e.g. the `### ウチ` / `### ソト` lists under ウチ・ソト) is part of its parent point's explanation, even when its text is not on the scaffolding label list. When in doubt, extract-grammar surfaces it in the classification table for the user to decide; practice-grammar folds it into the parent.
- **Mixed heading** (own explanation AND real sub-patterns): it is a point *and* its sub-patterns are points too — extract-grammar lists both in the classification table; practice-grammar drills each separately.
- **Ambiguity is user-gated only in extract-grammar** — suggested roles are proposals; the user confirms every candidate in the step 4b table. practice-grammar has no gate and applies these rules deterministically.
