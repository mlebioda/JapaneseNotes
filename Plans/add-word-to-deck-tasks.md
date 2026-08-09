# add-word-to-deck — Tasks

- [x] Create `.cowork/skills/add-word-to-deck.md` with:
  - [x] Trigger phrases + bounded word-inference rule (single most recent
        Japanese word/phrase in the last user or assistant message only; ask
        the user if that message has no unambiguous candidate — never search
        further back)
  - [x] Step A: tag classification (#w/#wc/#wp, transitive/intransitive,
        suru-noun `(する)` suffix) per `.cowork/instructions.md` conventions
  - [x] Step B: JLPT level + POS file guess (Nouns.md vs Others.md split for
        #w), shown to user for confirm/override
  - [x] Step C: fuzzy duplicate scan, restricted to each candidate file's
        content above its `# Summary` line only (exact match, reading variant,
        okurigana variant, conjugated form), flagged to user with three
        options: (a) proceed anyway, (b) skip, (c) inline-edit the existing
        raw tag line's translation/definition text (word/reading and
        everything below `# Summary` left untouched; card-mechanics repairs
        are out of scope — tell the user to run `templates-update` separately
        for those)
  - [x] Step C2: git-safety check — `git status` the target file before any
        write; commit a WIP snapshot first if there are pending uncommitted
        changes to it, per `.cowork/instructions.md`'s destructive-edit rule
  - [x] Step D: compose + append the raw tag line using the actual deck-file
        spacing convention (`word (reading)`, space before the parenthesis —
        verified against N4/Nouns.md, N4/Others.md, N4/Verbs.md,
        N4/Adjectives.md, not the instructions.md example's spacing), with
        exact per-tag templates:
        - `#w`: `#w <word> (<reading>) - <translation> | <short definition>`
        - `#w` suru-noun: `#w <word> (<reading>)(する) - <translation> | <short definition>`
        - `#wc`: `#wc <word> (<reading>) - <translation> (transitive|intransitive) | <short definition>`
        - `#wp`: `#wp <word> (<reading>) - <translation> | <short definition>; i-adjective.` (or `; na-adjective.`)
  - [x] Step E: generate + append the full card block **by hand, without
        invoking `fill_extract.py`** (that script's skeleton-insertion regex
        only matches an empty `# Summary` block and would duplicate an
        already-populated deck file if run against one — see plan Step E for
        the full explanation); reuse only the four reference files'
        derivation logic (verb-conjugation.md, adj-forms.md,
        honorific-forms.md, kanji-links.md) for field values, matching the
        flat card format (no Rzeczowniki:/Czasowniki:/Przymiotniki: headers)
        used in `Vocabulary/JLPT-decks/` files
  - [x] `#k` tag rule: gate on the word's kanji (furigana stripped) appearing
        in `KanjiList.md` (~262 curated entries, one kanji per line) — not on
        "contains any CJK character" (that broader test is kanji-links.md's,
        for the mnemonic `<a href>` links only, a separate step)
  - [x] Explicit "never touch TARGET DECK / <!--ID:--> / # Summary heading"
        note
  - [x] Empty-file handling (insert directly after ` --- ` when no cards exist
        yet, e.g. current N1–N3 files)
  - [x] Final confirmation report to user (word, tag, level, file, whether a
        card block was generated, whether `#k` was applied)
- [x] Create `.claude/commands/add-word-to-deck.md` slash command stub,
      following the existing one-line stub pattern (e.g.
      `.claude/commands/summarize-grammar.md`)
- [x] Ask user for explicit permission, then update `## Available skills` in
      `.cowork/instructions.md` to register `add-word-to-deck` with its
      trigger phrases
- [x] (Addendum, optional) Update the "used by" description of
      `.cowork/skills/references/verb-conjugation.md`, `adj-forms.md`,
      `honorific-forms.md`, `kanji-links.md` to mention `add-word-to-deck`
      alongside `fill-templates`/`templates-update`
