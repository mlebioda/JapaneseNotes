# Consolidate Per-Lesson Vocabulary Containers Into Shared POS Files — Tasks

- [x] Read `extract-grammar.md`, `structure-grammar.md`, `register-confusability-grammar.md`, and
      `see-also-grammar.md` in full immediately before editing (confirm exact current text/line
      positions haven't shifted since planning).
- [x] Confirm no existing `grammar-index/grammar/*.md` slug already starts with `vocabulary-`
      (checked during planning: none do — re-confirm at implementation time).

## extract-grammar.md

- [x] Rewrite the container-routing rule using the **literal** text in the plan's "Routing
      change → Literal replacement text / Literal insertion text" section (not a paraphrase):
  - [x] Replace the single `container` bullet in Step 4b's "Carry the classification forward"
        list with the two-bullet replacement given verbatim in the plan.
  - [x] Insert the "Not used for a routed Vocabulary POS container" paragraph verbatim into Step
        7's "Container file format" section, immediately after its existing two trailing
        sentences ("List only the sub-headings..." / "As with grammar point files...").
  - [x] Confirm a `# 文法`-sourced container (e.g. `kenjougo-verbs.md`'s case) is never affected
        by this rule, regardless of heading text.
- [x] Add new **Step 7c — Vocabulary POS container (consolidated)**:
  - [x] Read-or-create `grammar-index/grammar/vocabulary-<pos>.md` in the new format (frontmatter:
        `pattern`, `topic_slug: ""`, `proofread: false` — no `lesson:`, no `level:`; `# <POS>`
        heading; one-line gloss; `## Sub-topics`).
  - [x] State explicitly that Step 7c runs for every Vocabulary-sourced leaf under a routed
        container heading regardless of whether Step 6 produced Created or Skip for that leaf —
        unlike Step 8/Step 9's "Created only" gate — because its own per-entry dedup (link-target
        check, next bullet) is sufficient on its own. Call out that this is deliberate, not an
        inconsistency to "fix" toward matching Step 8/9.
  - [x] Per-entry dedup: before adding a bullet, check whether a bullet already links to this
        exact `grammar-index/grammar/vocabulary/<subdir>/<slug>` path anywhere in the file (any
        theme or ungrouped) — skip if found.
  - [x] Theming-gate user prompt: for entries being appended, propose join-existing-theme /
        start-new-theme / stay-ungrouped per entry, considering both existing file content and
        other entries from the same run. Use the prompt format from the plan. Wait for
        confirmation; a user override is used verbatim. Never force a theme with no genuine shared
        topic — default to ungrouped.
  - [x] Write logic: themed bullets go under their `### <Theme Name>` heading (created on first
        use, placed after `## Sub-topics` or after the last existing themed group); ungrouped
        bullets are flat, appended after all themed groups.
- [x] Update Step 6 (Idempotency check): note that the consolidated-file path does not use the
      `pattern:` grep (useless — `pattern:` is always the fixed POS name) and instead relies
      entirely on Step 7c's per-entry link-target check.
- [x] Update Step 8 (lesson wikilink): for the consolidated-file routing case, the inserted link
      has no anchor and points at the bare `[[grammar-index/grammar/vocabulary-<pos>]]` — no
      per-lesson deep link exists anymore.
- [x] Update Step 9's vocabulary-file exclusion line using the literal replacement sentence in
      the plan: do **not** reuse "their subdir path is their classification" for the new flat
      files (they have no subdir) — use "POS-consolidated vocabulary files, never individually
      topic-classified" instead.
- [x] Update Step 10's carve-out (the `N`-count text feeding the preprocess-grammar
      yes/no/all prompt) to also name `vocabulary-<pos>.md` files as excluded from the post-
      processing offer, and update the completion-report example to show a consolidated-file
      append line (e.g. `Appended: grammar-index/grammar/vocabulary-verbs.md ← <slugs> (theme /
      ungrouped notes)`).

## structure-grammar.md

- [x] Add filename guard to "Container file detection": a file matching
      `grammar-index/grammar/vocabulary-*.md` is a vocabulary consolidation file, never a
      container — skip this skill entirely for it (not even the container-skip log line),
      checked before the `## Sub-topics` check.

## register-confusability-grammar.md

- [x] Add the same `vocabulary-*.md` filename guard to "Container / vocabulary scope guard",
      alongside (not replacing) the existing `vocabulary/` subdirectory guard.

## see-also-grammar.md

- [x] Exclude `grammar-index/grammar/vocabulary-*.md` from the "scan all files with `##
      Sub-topics`" candidate-container pool used when computing other files' backlinks.

## grammar-audit.py

- [x] Apply the literal line-62 change from the plan's "Interaction with
      `.claude/scripts/grammar-audit.py`" section — exclude filenames starting with
      `vocabulary-` from the `grammar_files` dict comprehension, so `vocabulary-verbs.md` is
      never scanned (matching the script's existing blind spot toward nested `vocabulary/**`
      leaf files, rather than fixing `parse_topic_slug`'s empty-string handling).

## Migration (requires explicit user confirmation before any deletion)

- [x] Present the migration clustering proposal to the user (theme "と思います／と言います — reporting
      thoughts and speech": 思う + 言う; theme "渡す／渡る — transitivity pair": 渡す + 渡る; できる /
      出来る flagged as a duplicate-lemma question for explicit decision, not silently resolved;
      付き合う and 知らせる ungrouped) and wait for confirmation before writing any file.
- [x] Create `grammar-index/grammar/vocabulary-verbs.md` in the new format, populated per the
      confirmed clustering (8 entries from the 5 old containers).
- [x] Update the 5 lesson-file wikilinks to point at the bare `[[grammar-index/grammar/
      vocabulary-verbs]]`:
  - [x] `JPLessons/Udemy/N4/Grammar/UN4GL1.md` (was `[[grammar-index/grammar/dekiru-verbs]]`)
  - [x] `JPLessons/Udemy/N4/Grammar/UN4GL13.md` (was `[[grammar-index/grammar/verbs-informing-un4gl13]]`)
  - [x] `JPLessons/Udemy/N5/Grammar/UN5GL13.md` (was `[[grammar-index/grammar/un5gl13-verbs]]`)
  - [x] `JPLessons/Udemy/N4/Grammar/UN4GL6.md` (was `[[grammar-index/grammar/verbs-tsukiau]]`)
  - [x] `JPLessons/Udemy/N5/Grammar/UN5GL15.md` (was `[[grammar-index/grammar/un5gl15-verbs]]`)
- [x] Remove the stale entry from `grammar-index/verb-potential-form.md`
      (`- [Verbs](.../dekiru-verbs) · N4`) — keep the rest of the file intact.
- [x] Remove the stale entry from `grammar-index/communication-verbs.md`
      (`- [Verbs](.../verbs-informing-un4gl13) · N4`) — keep the rest of the file intact.
- [x] Remove the stale entry from `grammar-index/relationships.md`
      (`- [Verbs](.../verbs-tsukiau) · N4`) — this leaves an empty `## Entries` section; leave the
      file in place (do not delete) unless the user separately asks to prune it.
- [x] Confirm `un5gl13-verbs.md` and `un5gl15-verbs.md` have no topic-file entries to remove
      (both carry `topic_slug: []` — verified during planning).
- [x] Ask explicit, separate permission before deleting the 5 old container files
      (`dekiru-verbs.md`, `un5gl13-verbs.md`, `un5gl15-verbs.md`, `verbs-tsukiau.md`,
      `verbs-informing-un4gl13.md`) — never delete as a side effect of an earlier confirmation.
- [x] Confirm `kenjougo-verbs.md` is untouched (not part of migration).
- [x] Check whether `grammar-index/index.md` needs regeneration (expected: no, since no topic
      file is created or deleted by this migration — confirm at implementation time).

## Self-review

- [x] Grep all four edited skill files for leftover "one container per lesson" framing describing
      the retired per-lesson-container behavior as current.
- [x] Grep the vault for remaining references to the 5 old container slugs
      (`dekiru-verbs`, `un5gl13-verbs`, `un5gl15-verbs`, `verbs-tsukiau`,
      `verbs-informing-un4gl13`) after migration — should be zero outside git history.
- [x] Confirm `kenjougo-verbs.md` frontmatter, body, and all 5 files that link to it are
      unmodified.
- [x] Confirm no `<!--ID: -->` line or `TARGET DECK` line was touched in any lesson file edited
      for the wikilink update.
- [x] Run `python3 .claude/scripts/grammar-audit.py --verbose` from the vault root and confirm
      `vocabulary-verbs.md` does not appear in the output at all (excluded/clean) — not as a
      surprise orphan or `topic_slug` mismatch entry.
