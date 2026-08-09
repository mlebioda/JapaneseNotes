---
name: lesson-grammar-practice
description: >
  Interactive grammar practice session driven by a single lesson file, identified
  by an explicit lesson code (e.g. `UN5GL14`) or lesson filename. Extracts grammar
  points from the 文法 section, walks each one through Study Mode's per-topic
  explanation loop, collects a self-evaluation score per topic, and writes
  results to the spaced-repetition state file. Requires a lesson-code/filename shape in the
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
   effect on Study Mode's explanation content, which continues to read only
   the lesson body exactly as today. A point's extracted linkage may silently fall back
   to plain lesson-file linking if the container guard rejects it — this is
   expected and requires no user-facing message.
4. **Confirm topic list.** Print the full numbered list of grammar headers
   discovered in step 3 (see this skill's own **Session header and footer**
   below for the exact format) — the whole list, no subset selection. Ask
   the user to confirm before proceeding. On cancel, end the session with no
   writes (no `grammar-state.json` changes, no `.ics` file).
5. **Study Mode, every topic, in order.** On confirmation, load
   `.cowork/skills/practice-grammar/practice-grammar-study-mode.md` and
   enter directly at its **Step 2** (`2a` explanation → `2b` choice prompt →
   `2c` branch, including the optional `2d` Practice sub-loop exactly as it
   works today) for every topic from step 3, in lesson order, treated as
   already "selected." That file's own **Step 1** (topic-selection prompt)
   is never shown and never executed for this trigger — this skill supplies
   the full topic list directly instead. Pass the same context Study Mode
   already expects: `batch_topics` (the step-3 topic list), `user_answers:
   {}` (always empty for this trigger — Study Mode's existing
   answer-retrieval fallback in `2a` already handles an empty/missing answer
   with no change needed there), `vocab_pool` (the step-3 vocab pool).
   Before entering Study Mode, load `.cowork/progress/grammar-state.json`
   (create-as-empty if missing) to pick up prior `weak_points` per grammar
   point and pass those along too — this load was previously done by
   `scheduled-grammar-practice.md`'s Batch-loop mechanics, which this trigger
   no longer invokes at all, so this step performs it directly. If the user stops/ends
   mid-loop, end the session immediately — nothing is written, since no
   self-eval scores exist yet.
6. **Return control after the last topic; collect self-eval.** When Step 2's
   loop reaches "Continue" on the last topic (which
   `practice-grammar-study-mode.md`'s own `2c` text says would "proceed to
   Step 3"), control returns here instead — that file's own **Step 3**
   (batch/"Next batch/Finish" routing) is never entered for this trigger.
   Once control returns: print the topic list again (same numbered format as
   step 4). Ask for a self-eval score per topic (see this skill's own
   **Session header and footer** below for the exact prompt format), 1–4
   scale (1=fail, 2=hard, 3=good, 4=easy — same scale/meaning as the
   exercise self-scoring in `_practice-grammar-common.md`), reply as bare
   numbers in order (e.g. `3 4 2`), same batch-reply convention as that
   exercise self-scoring. No weak_points are collected in this step — always
   `[]` for this trigger's entries. Invalid or out-of-range reply →
   re-prompt once → if still invalid, cancel without writing.
7. **Persist.** Build `session_scores`: one entry per grammar point →
   `{min_score: <step-6 score>, weak_points: [], grammar_header,
   lesson_file}`, using the same `extracted_file_path` substitution rule
   already documented in `scheduled-grammar-practice.md`'s **Persistence and
   Calendar sync** section ("Per-point `lesson_file` source"). Call
   `.cowork/skills/practice-grammar/practice-grammar-srs.md` directly with
   `scope="lesson"`. Same SM-2 write, same direct `next_review` computation,
   same `.ics` export via `ics-export.py`.

Don't skip any step. Start practicing immediately after the user triggers
the skill.

---

## Session header and footer

**Topic-list-confirm format** (Workflow step 4 and, reprinted, step 6):

```
<lesson-code> — N grammar points:
  1. <grammar_header_1>
  2. <grammar_header_2>
  ...

Study all topics? (yes / cancel)
```

**Self-eval-scores prompt format** (Workflow step 6, after the reprinted
topic list above):

```
Score each 1–4 (1=fail, 2=hard, 3=good, 4=easy). Reply with the N scores in order, e.g. `3 4 2`.
```

**Session-complete footer** (Workflow step 7, after persistence):

```
Session complete — <lesson-code> (N grammar points)
```

This one-line footer fully replaces the old Solid/Needs-practice breakdown
for this trigger — no per-point classification is shown.

---

## Study Mode

This skill enters `.cowork/skills/practice-grammar/practice-grammar-study-mode.md`
directly at its **Step 2**, per Workflow step 5 above — bypassing that
file's Step 1 (topic-selection prompt) entirely and never reaching its
Step 3 (batch/"Next batch/Finish" routing). See Workflow step 5 for the
exact invocation contract (topics passed, context, mid-loop stop behavior).

---

## Persistence

Call `.cowork/skills/practice-grammar/scheduled-grammar-practice.md`'s **Persistence and
Calendar sync** directive with `scope="lesson"`. For this trigger, this is
invoked from Workflow step 7 — after Study Mode and the post-study
self-eval — not before Study Mode as in the old flow.

---

## Never touch

- Lesson files under `JPLessons/` (read-only — never write)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- Do not run `git push` or any remote git operation
- See `.cowork/skills/practice-grammar/_practice-grammar-common.md`'s own Never-touch list for
  the full shared rule set (this skill loads that file for everything else)
