# Practice Grammar — Trim Common File & Reinforce Gate 1

## Goal
During live grammar-drill sessions, the shared sub-skill
`.cowork/skills/practice-grammar/_practice-grammar-common.md` (648 lines) is
long enough that the model executing it skips gates — specifically Gate 1
(the answer-leak gate), which currently gets no visual emphasis unlike the
Between-batch gate, causing quiz answers to leak into the same turn as the
question. This plan (a) gives Gate 1 the same bold/MANDATORY treatment as
the Between-batch gate and puts a short reminder right where exercises are
emitted, (b) relocates ~115 lines of scheduled-only content (Batch-loop
mechanics, Session summary, Persistence and Calendar sync) out of the shared
common file into `scheduled-grammar-practice.md` — its only real caller —
and (c) cuts rationale-only/redundant prose. No drill flow or behavior
changes anywhere; this is wording, formatting, and file-location only.

## Approach
Reformat Gate 1 in place (bold blockquote, same style as the existing
Between-batch gate) and add one reinforcing line at the point exercises are
generated — no new paragraphs of explanation. Move the three scheduled-only
sections verbatim into `scheduled-grammar-practice.md` (inlined directly,
not a new standalone file — it has a single caller, so a separate file would
be pure indirection). Update every cross-reference across all four files so
nothing points at a section name/location that no longer exists there. Cut
pure-rationale passages that state no operative rule. Locate all edits by
heading text, not line number, since line numbers will shift as edits land.

## Steps

1. **`_practice-grammar-common.md` — reformat Gate 1.** Wrap the "Gate 1 —
   Prompt does not leak the answer" heading/lead sentence in a bold-blockquote
   MANDATORY callout, matching the Between-batch gate's existing format
   (currently under "Batch-loop mechanics", the `> **BETWEEN-BATCH GATE —
   MANDATORY...**` block). The two numbered sub-rules under Gate 1 keep their
   exact current wording — formatting only, no rule changes.

2. **`_practice-grammar-common.md` — add a reinforcing line at `## Interaction
   flow`.** One short sentence pointing back to Gate 1, placed right before
   `### Batch mode` (where exercises are actually emitted), so the reader
   doesn't have to recall the gate from ~60 lines earlier. No new paragraph.

3. **`_practice-grammar-common.md` — cut rationale-only passages** (keep any
   operative rule sentence, drop the essay around it):
   - The "This is a separate, heavier routine from..." paragraph under
     "Loading an extracted grammar file".
   - The caller-bookkeeping sentences under "Loading a lesson file slice"
     ("Both trigger skills call this routine once per resolved lesson file
     path...") and under "Loading an extracted grammar file" ("Today's only
     caller is scheduled-grammar-practice.md's...") — already stated from the
     other side in the respective trigger files.
   - The "This subsection is only ever walked by..." paragraph under
     "Extracted-file linkage (fresh-discovery detection)" — trim to one short
     sentence stating scope (runs only during lesson-grammar-practice's fresh
     discovery pass, not scheduled-grammar-practice's lesson-file flow).
   - The "Why the duplicate-heading-text carve-out doesn't apply here"
     paragraph — delete entirely (pure rationale, no instruction).

4. **`_practice-grammar-common.md` — remove three sections in full:**
   `## Session summary`, `## Persistence and Calendar sync`, `## Batch-loop
   mechanics`. Content relocates to `scheduled-grammar-practice.md` (step 5).
   While relocating Batch-loop mechanics, dedup the repeated
   "never auto-advance" / "re-present on off-topic question" restatements
   (currently repeated across the non-last-batch bullet, the last-batch
   bullet, and trailing point (f)) down to the single existing MANDATORY
   blockquote statement — keep the rule once, drop the echoes.

5. **`scheduled-grammar-practice.md` — add the three relocated sections**
   (`## Batch-loop mechanics`, `## Session summary`, `## Persistence and
   Calendar sync`), post-dedup, as new sections placed after `## Metadata-driven
   exercise generation` and before `## Workflow`.

6. **`scheduled-grammar-practice.md` — update Workflow steps 4–6** to
   reference this file's own (now-local) sections instead of "the common
   file's...": step 4's "Run its Batch-loop mechanics", step 5's "the common
   file's generic Session summary", step 6's "the common file's Persistence
   and Calendar sync directive".

7. **`scheduled-grammar-practice.md` — verify/repoint** the `## Study Mode`
   stub section and `## Never touch` footer if either still names the old
   (now-removed) locations in `_practice-grammar-common.md`.

8. **`_practice-grammar-common.md` — repoint the `## Study Mode` section's
   `weak_points` bullet** ("as loaded once at session start (see
   **Batch-loop mechanics** below)...") to `scheduled-grammar-practice.md`,
   since that heading no longer exists locally.

9. **`_practice-grammar-common.md` — trim the YAML frontmatter
   `description:`** to drop mentions of "the batch-loop mechanics" and adjust
   "session-summary formatting" / "Persistence/Calendar-sync load-directive"
   wording, since those sections no longer live in this file.

10. **`lesson-grammar-practice.md` — repoint cross-references:**
    - Workflow step 5's "...this trigger no longer invokes at all" mention of
      "the common file's Batch-loop mechanics" — repoint the file pointer to
      `scheduled-grammar-practice.md`; the explanatory content (that this
      trigger does NOT invoke it) stays word-for-word.
    - Workflow step 7's "the same extracted_file_path substitution rule
      already documented in the common file's Persistence and Calendar sync
      section" — repoint to `scheduled-grammar-practice.md`.
    - The `## Persistence` section's "Call `_practice-grammar-common.md`'s
      Persistence and Calendar sync directive..." — repoint to
      `scheduled-grammar-practice.md`.

11. **`practice-grammar-study-mode.md` — repoint cross-references:**
    - "Context required" bullet for `weak_points` ("as loaded once at session
      start (in `_practice-grammar-common.md`'s Batch-loop mechanics
      section)...") — repoint to `scheduled-grammar-practice.md`.
    - "Trigger" section's "the between-batch gate in
      `_practice-grammar-common.md`'s Batch-loop mechanics section" —
      repoint to `scheduled-grammar-practice.md`.

12. **Final consistency pass.** Grep all four files for remaining occurrences
    of "Batch-loop mechanics", "Session summary", "Persistence and Calendar
    sync" that still point at `_practice-grammar-common.md`, and confirm each
    now resolves to `scheduled-grammar-practice.md` (except references inside
    `scheduled-grammar-practice.md` itself, which resolve locally).

## Risks
- None of the four files are lesson files or contain plugin export data
  (`<!--ID:-->` lines, `TARGET DECK`) — no risk to plugin/Anki state.
- Missed cross-reference after relocation — mitigated by step 12's grep pass.
- Must not alter Gate 1's actual sub-rules while reformatting — wrap existing
  text only, don't rewrite the two numbered rules.
- Must not change the batch loop's actual call order or parameters while
  moving it — verify after edits that `scheduled-grammar-practice.md`'s
  Workflow still invokes Batch-loop mechanics with the same inputs, in the
  same order, as before the move.
- Net size: `_practice-grammar-common.md` ~648 → ~533 lines;
  `scheduled-grammar-practice.md` ~260 → ~375 lines; `lesson-grammar-practice.md`
  and `practice-grammar-study-mode.md` unchanged in length (pointer updates only).
