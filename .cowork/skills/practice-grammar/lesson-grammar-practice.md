---
name: lesson-grammar-practice
description: >
  Interactive grammar practice session driven by a single lesson file, identified
  by an explicit lesson code (e.g. `UN5GL14`) or lesson filename. Extracts grammar
  points from the 文法 section, generates exercises using vocabulary from the
  Summary section (plus N5-level fillers), grades answers, and writes results to
  the spaced-repetition state file. Requires a lesson-code/filename shape in the
  request — phrasing like "let's practice UN5GL14", "practice <lesson>", "exercise
  <lesson>", "drill grammar in <lesson>". Does NOT match date/scope phrasing
  ("today", "today's topics", "overdue", "due", "scheduled") — that shape belongs
  to scheduled-grammar-practice instead.
---

# Lesson Grammar Practice Skill

## Trigger

User says any of:
- "Let's practice UN5GL14" / "Let's practice <filename>"
- "practice <lesson>"
- "exercise <lesson>"
- "drill grammar in <lesson>"

If user references a lesson by code only (e.g. `UN5GL14`), find the file
under `JPLessons/Udemy/N<level>/Grammar/` — match by prefix, ignore trailing
description in filename.

This skill only matches when the request names a specific lesson (a code
like `UN5GL14` or an explicit filename). It does not match scope/date
phrasing such as "today's topics" or "overdue" — that shape belongs to
`scheduled-grammar-practice`.

---

## Workflow

1. **Resolve the lesson file** — by code or filename (see Trigger above).
2. Load `.cowork/skills/practice-grammar/_practice-grammar-common.md`. Call its **Loading a
   lesson file slice** routine on the resolved file path.
3. Parse fresh via the common file's **Parsing → Grammar topics**
   (heading-role classification, loads `_heading-roles.md`) and **Parsing →
   Vocab pool**. This trigger never has pre-selected entries — every grammar
   point in the lesson is discovered fresh via heading-role classification.
   There is no entry-lookup-by-search step and no Migration note here; both
   only apply to the scheduled trigger's pre-selected `grammar-state.json`
   entries. This fresh parse also captures `extracted_file_path` per point
   (via the common file's **Extracted-file linkage (fresh-discovery
   detection)** subsection, including its container-file guard) — used only
   when building `session_scores` for persistence in step 7 below; it has no
   effect on exercise generation, which continues to read only the lesson
   body exactly as today. A point's extracted linkage may silently fall back
   to plain lesson-file linking if the container guard rejects it — this is
   expected and requires no user-facing message.
4. `num_batches` is always `1` — no batch-split prompt, no batch headers, no
   between-batch `Batch B / num_batches` printouts. (The common file's
   Batch-loop mechanics still run their single pass for this one batch,
   including the MANDATORY between-batch-gate / `Study mode / Finish`
   prompt logic.)
5. Run the common file's **Batch-loop mechanics** — loads `weak_points`,
   generates exercises via **Exercise generation**, presents via
   **Interaction flow**, grades via **Grading**.
6. On completion, use this skill's own **Session header and footer** (below)
   plugged into the common file's generic Session summary / batch-prompt
   formats.
7. Persist via the common file's **Persistence and Calendar sync** directive
   with `scope="lesson"`.

Don't skip any step. Start practicing immediately after the user triggers
the skill.

---

## Session header and footer

**Session header** — plugs into the common file's generic batch-prompt
layout (`## Interaction flow` → Batch mode):

```
Session: <lesson-code> — N exercises across M grammar points. Reply with all answers in one message (numbered or in order).
```

Worked example:

```
Session: UN4GL7 — 14 exercises across 9 grammar points. Reply with all answers in one message (numbered or in order).

Exercise 1 / 14
Translate to Japanese: "The meeting is currently in progress."

Exercise 2 / 14
Translate to Japanese: "I travelled all around Japan."

Exercise 3 / 14
Translate to Japanese: "Please don't use a cellphone in the hospital."

…

Exercise 14 / 14
Fill the blank: ペンが ___ あります (3 pens).
```

**Session-summary footer** — plugs into the common file's `## Session
summary` `Session complete — <header> (...)` format:

```
Session complete — <lesson-code> (N exercises across M grammar points)
```

Worked example: `Session complete — UN4GL7 (14 exercises across 9 grammar points)`

---

## Study Mode

Handled entirely by `.cowork/skills/practice-grammar/_practice-grammar-common.md`'s
**Study Mode** section — see that file for the invocation hookup. No
duplicate content here.

---

## Persistence

Call `.cowork/skills/practice-grammar/_practice-grammar-common.md`'s **Persistence and
Calendar sync** directive with `scope="lesson"`.

---

## Never touch

- Lesson files under `JPLessons/` (read-only — never write)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- Do not run `git push` or any remote git operation
- See `.cowork/skills/practice-grammar/_practice-grammar-common.md`'s own Never-touch list for
  the full shared rule set (this skill loads that file for everything else)
