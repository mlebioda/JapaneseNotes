# Practice Grammar — Scope-Based Triggers

## Goal

Extend the `practice-grammar` skill with two new trigger modes that allow the user to
practice grammar points selected from `grammar-state.json` by date, without specifying a
single lesson file. "Today's topics" drills exactly what is scheduled for today.
"Overdue topics" drills what is past due. The two sets are mutually exclusive by design:
a point due today is never overdue, and a point that is overdue is never in today's set.

The existing single-lesson trigger path (`practice <lesson>`) is not changed at all.

---

## Approach

Add a new **Trigger** block and a new **Scope resolution** section to the skill, placed
before the existing `## Workflow` section. When a scope trigger is detected, the skill
runs scope resolution (which produces a list of grammar point entries), then falls through
to the existing session machinery (exercise generation, grading, SM-2 persistence,
calendar write) as if those entries had come from a single lesson — with the exception of
the session header line and the session summary footer, which use scope-specific labels.
No existing workflow steps are modified.

The two filter conditions are implemented with strict date comparisons against today's
date (ISO `YYYY-MM-DD`):

- **Today's topics:** `next_review == today` (exact match only)
- **Overdue topics:** `next_review < today` (strictly before today, never including today)

---

## Steps

1. **Add trigger phrases to `## Trigger` in `.cowork/skills/practice-grammar.md`**

   Append to the existing bullet list:

   ```
   - "practice today's topics" / "practice grammar due today" / "drill today's grammar"
     → scope = TODAY
   - "practice overdue topics" / "practice overdue grammar" / "drill overdue topics"
     → scope = OVERDUE
   ```

   Scope triggers are detected before checking for a lesson code. If neither scope phrase
   nor a lesson reference is found, fall through to existing ambiguity handling.

2. **Add `## Scope resolution` section** (inserted immediately before `## Workflow`)

   This section describes what happens when scope = TODAY or scope = OVERDUE. It does
   NOT replace the Workflow — it produces the `selected_entries` list that the session
   machinery consumes.

   ### TODAY flow

   a. Read `.cowork/progress/grammar-state.json`. If file missing, treat state as empty.
   b. Filter entries: keep only those where `next_review` is a valid ISO date AND
      `next_review == today` (string equality on YYYY-MM-DD; do not compare as < or ≤).
   c. Apply edge-case skips (see § Edge cases).
   d. If filtered list is empty: print exactly —
      `Nothing is scheduled for today.` and stop.
   e. Print: `N grammar points scheduled for today.` and proceed to session.

   ### OVERDUE flow

   a. Read `.cowork/progress/grammar-state.json`. If file missing, treat state as empty.
   b. Filter entries: keep only those where `next_review` is a valid ISO date AND
      `next_review < today` (strictly less than today; entries where `next_review == today`
      are excluded here).
   c. Apply edge-case skips (see § Edge cases).
   d. If filtered list is empty: print exactly —
      `No overdue grammar points — you're up to date.` and stop.
   e. Sort remaining entries by `next_review` ascending (oldest first).
   f. Print: `N grammar points are overdue. How many do you want to practice? (most overdue first, or 'all')`
      and wait for user reply.
   g. Parse user reply X:
      - If X is `'all'`: use all N entries.
      - If X is a positive integer > N: use all N entries, print `Only N overdue points found — using all N.`
      - If X is a positive integer == N: use all N entries.
      - If X is a positive integer < N: take the first X entries (already sorted oldest first).
      - If X is invalid (non-integer, negative, zero): ask once more with the same prompt.
        If still invalid: stop with message `Invalid selection — session cancelled.`
   h. Print: `Starting session with X grammar points.` and proceed to session.

3. **Specify multi-lesson loading in the scope session context** (in `## Scope resolution`)

   Once `selected_entries` is resolved:

   - Collect the set of unique `lesson_file` paths referenced by the selected entries.
   - For each lesson file, read the content up to `# Summary` using the awk cut (same as
     Workflow step 2). Load lazily: only read a lesson file when the first grammar point
     from that file is needed. Deduplicate: if multiple grammar points share a lesson file,
     read that file only once.
   - For each selected entry, locate its grammar point in the loaded lesson slice by
     matching `grammar_header` against `## Heading` lines in `# 文法` and `# Vocabulary`
     sections. Match strategy: exact first, then case-insensitive, then
     whitespace-normalised. If still not found (or ambiguous — more than one match): skip
     with warning `Warning: grammar header "<header>" not found in <lesson_file> — skipped.`
   - Build a merged vocab pool: union of all `# ごい` + `# ひょうげん` lines from all
     loaded lesson files. Deduplicate by Japanese form (full `日本語(よみ)` string). When
     the same form appears in multiple lessons, keep the first occurrence (session-list
     order = order entries appear in `selected_entries`).
   - If all lesson files fail to load (all skipped with warnings): stop with message
     `Error: no lesson files could be loaded — session cancelled.` and report all warnings.

4. **Specify session header and footer formats for scope sessions**

   In `## Interaction flow`, add a note that scope sessions use these header and footer
   formats instead of the single-lesson variants:

   Session header (Today):
   ```
   Session: today's topics — N exercises across M grammar points (K lessons). Reply with all answers in one message.
   ```

   Session header (Overdue):
   ```
   Session: overdue topics — N exercises across M grammar points (K lessons). Reply with all answers in one message.
   ```

   Session summary footer (Today):
   ```
   Session complete — today's topics (N exercises across M grammar points)
   ```

   Session summary footer (Overdue):
   ```
   Session complete — overdue topics (N exercises across M grammar points)
   ```

   `K lessons` = count of distinct lesson files successfully loaded for this session.

5. **Add `## Edge cases` subsection within `## Scope resolution`**

   Specify silently-skipped conditions (skip the entry, emit no output unless file
   missing):

   - `next_review` field missing, null, empty, or not a parseable YYYY-MM-DD date → skip
     silently.
   - `lesson_file` field missing or empty → skip with warning.
   - Lesson file path not found on disk → skip with warning, continue with remaining
     entries.
   - `grammar_header` not found in lesson file after all match strategies → skip with
     warning.
   - `grammar_header` matches more than one heading in the file (ambiguous) → skip with
     warning.

   N (the count shown to the user) is derived solely from `grammar-state.json` — it equals
   the number of entries that pass the date filter. Lesson-file load failures and
   warned-and-skipped entries do not reduce N; they are reported as warnings but do not
   change the announced count.

6. **Flag `instructions.md` trigger list for update (post-implementation, requires permission)**

   `.cowork/instructions.md` lists trigger phrases for the `practice-grammar` skill. After
   the skill is updated, the trigger list there must be extended with the two new scope
   phrases. This file must not be modified without user permission — flag it here as a
   post-implementation step requiring explicit user approval.

---

## Risks

- **Filter logic confusion** — The `== today` vs `< today` boundary is the critical
  invariant. The implementer must not use `<=` for overdue or `>=` for today. The task
  file spells out both conditions explicitly.
- **Read-only on lesson files** — scope sessions still read lesson files with the awk
  cut; no writes occur to any lesson file. The SM-2 write and the calendar write are the
  only file outputs, identical to single-lesson sessions.
- **grammar-state.json corruption** — the skill reads state but does not write it until
  after the session completes. A failed mid-session run leaves the state file unchanged.
  No risk of partial writes if the skill is interrupted before persistence step.
- **No changes to SM-2 algorithm, persistence format, exercise generation, or grading** —
  these sections of the skill are untouched. The only additions are the trigger block, the
  scope resolution section, and the session header/footer format notes.
- **instructions.md** — must not be modified during implementation. Flag for user review.
