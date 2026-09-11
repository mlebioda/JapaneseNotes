# Grammar Container Drift Fix — Tasks

- [x] `.claude/scripts/grammar-audit.py`: add a `subtopics_in_container()` helper (mirrors
      `entries_in_topic()`) to extract `## Sub-topics` link targets from a container file
- [x] `.claude/scripts/grammar-audit.py`: identify container files (`SUBTOPICS_RE` match) and
      build a `container_slug -> set(sub-topic slugs)` map
- [x] `.claude/scripts/grammar-audit.py`: for each topic file, for each co-entry container, flag
      other topic entries missing from that container's Sub-topics as `container_drift` tuples —
      first excluding any entry slug not present in `grammar_files` (already covered by the
      existing `broken_links` check; must not be read as a file or double-reported here)
- [x] `.claude/scripts/grammar-audit.py`: add "Container drift (topic entry missing from
      container Sub-topics)" as a new report section, counted into the existing `errors` total
- [x] `.claude/scripts/grammar-audit.py`: update the module docstring's numbered "Checks" list
      (currently 5 items) to add "6. Container drift" and update the `--verbose` usage note if it
      references the check list, so the docstring matches the new behavior
- [x] Run `python3 .claude/scripts/grammar-audit.py --verbose` after the change and confirm the
      known `counters-numbers` / `counters` drift (11 items, including
      `mai-counter-for-flat-thin-objects`) is now reported — read-only verification, no file edits
- [x] `.cowork/skills/lesson-to-web/extract-grammar.md`: add the new gated container-membership
      sync sub-step to Step 7, after the existing bidirectional `## See also` item, including the
      explicit "runs once after all of Step 7 items 1-4 finish for the whole run" timing note
- [x] `.cowork/skills/lesson-to-web/extract-grammar.md`: state explicitly that the new sub-step's
      `<pattern>`/`<level>` bullet values are read from the target point file's own frontmatter
      (`pattern:` / `level:`), matching how Step 6d states its bullet field sources
- [x] `.cowork/skills/lesson-to-web/extract-grammar.md`: verify the Step 7 prompt format, dedup
      rule, and bullet format match the plan and the existing Step 6c container template exactly
- [x] Confirm no changes are made to `.cowork/skills/lesson-to-web/see-also-grammar.md` (out of
      scope per user decision)
