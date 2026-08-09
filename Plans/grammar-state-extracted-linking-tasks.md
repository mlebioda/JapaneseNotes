# Grammar-state extracted-file linking — Tasks

- [x] `_practice-grammar-common.md` — add "Extracted-file linkage
      (fresh-discovery detection)" subsection under "Grammar topics":
      regex-detect the `→ [[grammar-index/grammar/...]]` wikilink on the
      line immediately after a point heading (committed positional rule, no
      hedging), provisionally set `extracted_file_path` (with `.md`
      appended) on the point triple when found, `null` otherwise. Strip the
      matched wikilink line from `body_text`. Note containers/scaffolding
      are excluded by construction (never become point triples). State the
      scope note (only walked by lesson-grammar-practice's full
      heading-role pass, never 2b) and the duplicate-heading-text
      non-applicability note (positional per-node check vs. global regex
      substitution).
- [x] `_practice-grammar-common.md` — add the container-file guard to the
      same subsection: for any point where a wikilink was found, open the
      target file and check for `## Sub-topics` (reuse the exact check from
      the extracted-file flow, don't invent a second one); if present,
      discard the match (`extracted_file_path = null`, fall back to plain
      lesson-file linking — never leave the point unlinked). Document this
      as a lightweight heading-presence read, distinct from and cheaper
      than the full "Loading an extracted grammar file" routine.
- [x] `_practice-grammar-common.md` — add new "Loading an extracted grammar
      file" routine (move `scheduled-grammar-practice.md`'s "2a.
      Extracted-file flow" content here verbatim: whole-file read,
      frontmatter parse, container-file guard, `grammar_header` = file H1
      with mismatch warning, `body_text` assembly).
- [x] `scheduled-grammar-practice.md` — replace inline "2a. Extracted-file
      flow" body with a pointer to the common file's new routine. Leave "2b.
      Lesson-file flow" untouched.
- [x] `_practice-grammar-common.md` — update "Persistence and Calendar sync"
      directive to document the per-point `lesson_file` source rule (default
      to resolved lesson path; use `extracted_file_path` when set and not
      container-guard-rejected) and cross-reference the creation-only
      identity-field rule enforced at both write sites.
- [x] `practice-grammar-srs.md` — generic Persistence section (lesson-scope
      direct-write path, ~lines 41-59/100): add explicit sentence that
      `lesson_file`/`grammar_header` are written only at entry creation and
      preserved untouched on update — this is the only path this feature's
      new entries go through.
- [x] `practice-grammar-srs.md` — Step A **payload note** (~line 91, "Always
      include lesson_file and grammar_header ... harmless to send"): correct
      wording about the Step B JSON payload sent to load-control.py —
      confirmed correctly landed.
- [x] **REOPENED (post-implementation review found this was never actually
      applied — self-report was inaccurate).** `practice-grammar-srs.md` —
      **Step A instruction block itself** (~lines 71-73, "For each practiced
      grammar point, update its entry with the computed SM-2 fields... Also
      write identity fields `lesson_file` and `grammar_header`."): add the
      creation-only qualifier inline (mirror the generic Persistence
      section's wording at ~line 46) — Step A writes `lesson_file`/
      `grammar_header` only when creating a new entry; on an existing entry
      it updates only the computed SM-2 fields and leaves stored identity
      fields untouched, regardless of what `session_scores` supplies this
      session. See plan's "Follow-up fix" section, step 10.
- [x] `practice-grammar-srs.md` — stale parenthetical (~line 108, "...writes
      only `next_review` (plus identity fields) via `merge_and_write()`."):
      correct to reflect that identity fields are now only written by
      `merge_and_write()` for newly created entries, not unconditionally.
      See plan's "Follow-up fix" section, step 11.
- [x] `.cowork/scripts/load-control.py` — `merge_and_write()` CRITICAL fix:
      remove `lesson_file`/`grammar_header` from the `else` (existing-entry)
      branch's copied fields so they're only ever set in the `is_new`
      branch. Update the branch's comment accordingly ("never SM-2 fields,
      never identity fields").
- [x] `.cowork/scripts/test_load_control.py` — add a regression test
      mirroring `test_interval_days_not_overwritten_by_input`: existing
      entry with a stored `lesson_file`/`grammar_header`, session topic for
      the same key carrying different values, assert `merge_and_write()`
      leaves the stored identity fields unchanged.
- [x] Run the full `test_load_control.py` suite after the script change to
      confirm no other test depends on the old overwrite-on-existing
      identity-field behavior. (46/46 passed.)
- [x] `lesson-grammar-practice.md` — add a sentence to Workflow step 3
      noting `extracted_file_path` is captured during fresh parsing
      (including the container-file guard) and used only for persistence
      (step 7), not exercise generation; note the silent fallback case
      requires no user-facing message.
- [x] Self-review: grep `.cowork/skills/` and `.cowork/scripts/` for any
      other reader/writer of `lesson_file`/`grammar_header` in
      `grammar-state.json` that might assume these fields refresh on every
      write, per the Risks note in the plan. (No issues found —
      `ics-export.py` is read-only display; `manage-holidays.md` only
      re-passes existing stored values, never new ones;
      `practice-grammar-study-mode.md` uses in-memory labels, not the state
      file.)
