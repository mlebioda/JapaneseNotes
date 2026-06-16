# Practice Grammar — Scope-Based Triggers — Tasks

## File to modify
`.cowork/skills/practice-grammar.md`

---

- [ ] **Task 1 — Extend `## Trigger` block with scope trigger phrases**

  Append to the existing `## Trigger` bullet list in `.cowork/skills/practice-grammar.md`:

  ```
  Scope triggers (no lesson file needed — select from grammar-state.json):
  - "practice today's topics" / "practice grammar due today" / "drill today's grammar"
    → scope = TODAY
  - "practice overdue topics" / "practice overdue grammar" / "drill overdue topics"
    → scope = OVERDUE

  Scope triggers are matched before lesson-code detection. If no scope phrase and no
  lesson reference are found, fall through to existing ambiguity handling.
  ```

- [ ] **Task 2 — Insert `## Scope resolution` section before `## Workflow`**

  Insert a new top-level section `## Scope resolution` immediately before the existing
  `## Workflow` section. It must contain the following subsections:

  ### 2a — TODAY filter rule (must be exact match, no range)

  ```
  When scope = TODAY:
  1. Read `.cowork/progress/grammar-state.json`. Missing file → treat as empty state.
  2. Filter: keep entries where `next_review` is a valid ISO date (YYYY-MM-DD)
     AND `next_review == today` (exact string equality — NOT <= or >=).
     Entries where next_review < today are NOT included.
     Entries where next_review > today are NOT included.
  3. Apply edge-case skips (see § Edge cases below).
  4. If 0 entries remain after filtering:
     - Print: "Nothing is scheduled for today." and stop.
  5. Print: "N grammar points scheduled for today." and proceed to session.
  ```

  ### 2b — OVERDUE filter rule (must be strictly less than today, today excluded)

  ```
  When scope = OVERDUE:
  1. Read `.cowork/progress/grammar-state.json`. Missing file → treat as empty state.
  2. Filter: keep entries where `next_review` is a valid ISO date (YYYY-MM-DD)
     AND `next_review < today` (strictly less than — NOT <= and NOT ==).
     Entries where next_review == today are NOT included.
     Entries where next_review > today are NOT included.
  3. Apply edge-case skips (see § Edge cases below).
  4. If 0 entries remain: print "No overdue grammar points — you're up to date." and stop.
  5. Sort remaining entries by `next_review` ascending (oldest next_review first).
  6. Print: "N grammar points are overdue. How many do you want to practice?
     (most overdue first, or 'all')" and wait for user reply.
  7. Parse user reply X — evaluated in this exact order:
     - X is "all" → use all N entries (no extra message).
     - X is a positive integer > N → use all N entries, print "Only N overdue points found — using all N."
     - X is a positive integer == N → use all N entries (no extra message).
     - X is a positive integer < N → use the first X entries (already sorted oldest first).
     - X is invalid (non-integer, negative, zero) → ask once more with identical prompt.
       If still invalid: print "Invalid selection — session cancelled." and stop.
  8. Print: "Starting session with X grammar points." and proceed to session.
  ```

  ### 2c — Multi-lesson file loading

  ```
  After selected_entries is resolved (from TODAY or OVERDUE):
  1. Collect unique `lesson_file` values from selected_entries.
  2. For each lesson file, read content up to `# Summary` using:
       awk '/^# Summary$/{exit} {print}' "$LESSON_FILE"
     Load lazily — only read a file on first demand. Deduplicate: read each path once.
  3. For each selected entry, locate `grammar_header` in the loaded lesson slice:
     - Search in `# 文法` and `# Vocabulary` sections for a `## Heading` line.
     - Match order: exact → case-insensitive → whitespace-normalised.
     - If no match found: skip with warning.
     - If more than one match found (ambiguous): skip with warning.
  4. Build merged vocab pool: union of all `# ごい` + `# ひょうげん` tagged lines
     from all loaded lesson files. Deduplicate by Japanese form (full kanji+reading string).
     When the same form appears in multiple lesson files, keep the first occurrence
     (session-list order = the order entries appear in selected_entries).
  5. If all lesson files fail to load (all skipped with warnings):
     print "Error: no lesson files could be loaded — session cancelled." and report all
     warnings. Stop.
  ```

  ### 2d — Edge cases

  ```
  The following conditions cause an entry to be skipped silently (no output):
  - `next_review` missing, null, empty, or not a parseable YYYY-MM-DD date.

  The following conditions cause an entry to be skipped with a warning line:
  - `lesson_file` missing or empty.
  - Lesson file path not found on disk.
  - `grammar_header` not found in lesson file after all match strategies.
  - `grammar_header` matches more than one heading in the lesson file (ambiguous).

  N (the count shown to the user) is derived solely from `grammar-state.json` — it equals
  the number of entries passing the date filter. Lesson-file load failures and
  warned-and-skipped entries do NOT reduce N; they are reported as warnings only.
  ```

- [ ] **Task 3 — Add scope session header and footer formats to `## Interaction flow`**

  In the `## Interaction flow` section, under the existing session-header layout block,
  add a note:

  ```
  For scope sessions (TODAY / OVERDUE), use these header and footer formats instead:

  Session header — Today:
    Session: today's topics — N exercises across M grammar points (K lessons). Reply with all answers in one message.

  Session header — Overdue:
    Session: overdue topics — N exercises across M grammar points (K lessons). Reply with all answers in one message.

  Session summary footer — Today:
    Session complete — today's topics (N exercises across M grammar points)

  Session summary footer — Overdue:
    Session complete — overdue topics (N exercises across M grammar points)

  K lessons = count of distinct lesson files successfully loaded for this session.
  ```

- [ ] **Task 4 — Flag `instructions.md` trigger list update (do NOT modify the file)**

  Do not modify `.cowork/instructions.md`. After implementation is confirmed working,
  the user must explicitly approve adding these trigger phrases to the `practice-grammar`
  entry in that file:
  - "practice today's topics" / "practice grammar due today" / "drill today's grammar"
  - "practice overdue topics" / "practice overdue grammar" / "drill overdue topics"

  Note this as a pending follow-up that requires user permission before touching
  `.cowork/instructions.md`.

- [ ] **Task 5 — Self-review: verify filter boundary invariant**

  After editing the skill file, re-read the new `## Scope resolution` section and
  confirm:
  - TODAY filter uses `==` (exact match) only — not `<=`, not `>=`.
  - OVERDUE filter uses `<` (strictly less than) only — not `<=`, not `==`.
  - The two sets are stated as mutually exclusive in the text.
  - No step in OVERDUE can return an entry where `next_review == today`.
  - No step in TODAY can return an entry where `next_review < today`.
