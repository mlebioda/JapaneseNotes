# add-word-to-deck

## Goal
Let the user, mid-cowork-session (while reading a lesson, chatting, or reviewing
something), flag an unfamiliar word as worth remembering and have it added as a
fully-formed Anki flashcard to the correct file under `Vocabulary/JLPT-decks/`
— without leaving the current task to manually pick a level, a part-of-speech
file, write the tag line, and generate the card block by hand.

## Approach
A new flat-level skill, `add-word-to-deck`, triggered by a small set of natural
phrases ("add this word to a deck", "remember this word", "save this word", plus
an explicit-word form like "add <word> to deck"). If no word is typed explicitly
after the trigger, the skill infers it from the single most recent Japanese
word/phrase explicitly mentioned in the last user or assistant message (bounded
lookback — see Step 1 word-inference rule); if that message contains no
unambiguous candidate, the skill asks the user which word they mean rather than
searching further back.

The skill classifies the word into a tag (`#w`/`#wc`/`#wp`) per the conventions
already documented in `.cowork/instructions.md`, then guesses both the JLPT level
(N5–N1) and the target part-of-speech file (`Nouns.md`/`Verbs.md`/`Adjectives.md`/
`Others.md` — for `#w` words specifically, distinguishing concrete nouns →
`Nouns.md` from expressions/greetings/adverbs/grammatical words → `Others.md`).
This guess is always shown to the user for a quick confirm/override before
anything is written (per user decision: "guess + confirm").

Before writing, the skill fuzzy-scans all files under `Vocabulary/JLPT-decks/**`
(all 5 levels x 4 POS files = 20 files) for a possible existing entry — matching
not just exact text but also different readings, okurigana variants, or
conjugated forms of the same word (e.g. 見る vs 見ます) — and flags any hit to the
user for confirm-before-add rather than blocking silently (per user decision:
"fuzzy match, flag for confirm"). If the user chooses to fix the existing entry
instead of adding a new one, the skill performs a small inline edit itself on
the existing raw tag line's translation/definition text (see Step C below) —
it does not hand off to `templates-update` and abort.

Once confirmed (and after a git-safety check on the target file — see Step C2),
the skill does two writes to the target file:
1. Appends the raw `#w`/`#wc`/`#wp` tagged line to the top list, following the
   spacing and per-tag conventions actually used in the existing deck files
   (verified against `N4/Nouns.md`, `N4/Others.md`, `N4/Verbs.md`,
   `N4/Adjectives.md` — see Step D for the exact templates), not the differently
   -spaced example in `.cowork/instructions.md`'s "Image extraction format".
2. Generates the full Anki card block by hand — the same way `fill-templates`'
   final card content is authored ("Claude generates cards directly — no script
   execution needed", per `.cowork/instructions.md`'s "fill workflow" section)
   — reusing fill-templates' four reference files (`verb-conjugation.md`,
   `adj-forms.md`, `honorific-forms.md`, `kanji-links.md`) purely to fill in
   field *values*, and appends the finished block after the last existing card
   in the target file's `# Summary` section. **The `fill_extract.py` script
   itself is never invoked for this skill** — its insertion logic only matches
   an empty, freshly-appended `# Summary` block at end-of-file and would
   corrupt an already-populated deck file if run against one (see Step E for
   the full explanation). `Vocabulary/JLPT-decks/` files use a flatter card
   layout than lesson files (no `Rzeczowniki:`/`Czasowniki:`/`Przymiotniki:`
   section headers — see `N4/Others.md` for the actual shape).

This reuses existing, already-tested conjugation/adjective/honorific/kanji-link
*derivation logic* (not the script) rather than reinventing it, and keeps the
two vocab-file structural invariants (raw tag list above `# Summary`, generated
card block below it) consistent with every other file in `Vocabulary/JLPT-decks/`.

## Steps

1. Create `.cowork/skills/add-word-to-deck.md` — the new skill file. Contents:
   - Trigger phrases: "add this word to a deck", "add word to deck", "remember
     this word", "save this word", "add <word> to deck" (and close variants).
     Word-inference rule (bounded lookback): if no word is given explicitly,
     look only at the single most recent Japanese word/phrase explicitly
     mentioned in the last user or assistant message. If that message contains
     no Japanese word/phrase, or contains more than one plausible candidate, do
     not search further back in the conversation — ask the user which word
     they mean.
   - Step A — Tag classification: verb → `#wc` (append transitive/intransitive
     per convention), adjective → `#wp`, everything else (noun/expression/
     sentence/adverb) → `#w`; suru-noun → `#w` with `(する)` appended directly
     after the reading parenthesis, per `.cowork/instructions.md` conventions.
   - Step B — Placement guess: JLPT level (N5–N1) by Claude's best judgment;
     POS file — `Verbs.md` for `#wc`, `Adjectives.md` for `#wp`; for `#w`,
     `Nouns.md` if it's a concrete noun, `Others.md` if it's an
     expression/greeting/adverb/grammatical word (matching the existing
     Nouns.md vs Others.md split visible in the current files). Show the guess
     (level + file + tag) to the user; wait for confirm/override before
     continuing.
   - Step C — Duplicate scan: read the confirmed target level's four POS files
     plus a scan of all other `Vocabulary/JLPT-decks/**` files, restricted to
     each file's content **above its `# Summary` line only** (the raw tag list
     — see the "narrowed scan" note below; the generated card block below
     `# Summary` is not needed for this check and can be 1000+ lines in the
     larger files). Check the confirmed word (and its component kanji/reading)
     against every existing `#w`/`#wc`/`#wp` line for an exact match, a
     different-reading match, an okurigana variant, or a conjugated-form match
     of the same lemma. If any candidate is found, present it (file path +
     line) to the user and ask whether to:
     (a) proceed anyway (add the new entry alongside the existing one),
     (b) skip (abort the add), or
     (c) edit the existing entry instead.
     If (c): ask the user to dictate the corrected translation/definition, then
     replace the existing raw tag line's translation/definition text (i.e.
     everything after the word/reading, including the `| short definition`,
     transitive/intransitive marker, or adjective-type suffix as applicable)
     via a plain text Edit on that line only — never touch the word/reading
     portion of the line, and never touch anything below `# Summary` for that
     entry. This inline edit covers raw tag-line text only. If the existing
     card's *mechanics* (conjugation forms, kanji links, `<!--ID:-->`
     positioning) also need repair, tell the user that's out of scope for this
     skill and they should separately run `templates-update` on that file.
     After an inline edit (c), the add is complete — do not also append a new
     duplicate entry. Wait for the user's decision before writing in all three
     cases.
   - Step C2 — Git safety check: before any write (Step C's inline edit, or
     Step D/E's append), run `git status` on the target file. If it has pending
     uncommitted changes, commit a "WIP" snapshot first (per
     `.cowork/instructions.md`'s general rule: "Git is the rollback mechanism —
     no `.bak` files. Before a destructive edit, ensure pending changes are
     committed... then edit; commit the change separately"). Then proceed with
     the edit; the add-word-to-deck change itself is committed separately, if
     the user has git commits enabled for this workflow — otherwise left
     staged/unstaged per normal session behavior.
   - Step D — Compose and append the raw tag line. Use a space before the
     reading parenthesis (verified against `N4/Nouns.md`, `N4/Others.md`,
     `N4/Verbs.md`, `N4/Adjectives.md` — all consistently use `word (reading)`,
     not `word(reading)` as shown in `.cowork/instructions.md`'s "Image
     extraction format" example; that example's spacing does not match the
     actual deck files and must not be copied literally here). Exact templates
     per tag, matching real entries in the sampled files:
     - `#w` (non-suru): `#w <word> (<reading>) - <translation> | <short definition>`
       e.g. `#w 間 (あいだ) - space, interval | The gap or period between two points...`
     - `#w` (suru-noun): `#w <word> (<reading>)(する) - <translation> | <short definition>`
       e.g. `#w 安心 (あんしん)(する) - relief, peace of mind | A state of feeling reassured...`
     - `#w` (kana-only, no reading): `#w <word> - <translation> | <short definition>`
       e.g. `#w つもり - intention, plan | What a person means or plans to do...`
     - `#wc`: `#wc <word> (<reading>) - <translation> (transitive|intransitive) | <short definition>`
       e.g. `#wc 合う (あう) - to match, to fit (intransitive) | Describes two things...`
       (additional parenthetical markers such as `(honorific)` or `(humble)`
       may appear immediately before the transitive/intransitive marker when
       applicable, matching existing entries like
       `いらっしゃる - to be, to come, to go (honorific) (intransitive) | ...`)
     - `#wp`: `#wp <word> (<reading>) - <translation> | <short definition>; i-adjective.`
       or `; na-adjective.` — the adjective-type suffix is appended directly
       after the short definition, ending the line, e.g.
       `#wp 浅い (あさい) - shallow | Describes a small distance from top to
       bottom... the opposite of 深い; i-adjective.` This convention is not
       currently documented in `.cowork/instructions.md` but is consistently
       used in `N4/Adjectives.md` and must be followed for consistency with
       existing entries.
     Append the composed line to the end of the target file's top tag list (the
     block of `#w`/`#wc`/`#wp` lines above `# Summary`).
   - Step E — Generate and append the full card block by hand. **Do not run
     `fill_extract.py` or any script for this step.** That script (see
     `.cowork/skills/fill_extract.py`) builds skeleton cards by regex-matching
     an *empty* `# Summary` block at end-of-file
     (`re.sub(r"\n# Summary\s*$", "", content.rstrip())` — only matches when
     `# Summary` has nothing after it) and re-generates a skeleton for *every*
     `#w`/`#wc`/`#wp` line currently in the file. Run against an
     already-populated file like `Vocabulary/JLPT-decks/N4/Nouns.md`
     (thousands of lines, hundreds of existing cards with `<!--ID:-->` lines),
     the empty-`# Summary` regex would not match the existing non-empty
     `# Summary`, so the script would append a *second* `# Summary` + ` --- `
     block and regenerate skeletons for every existing tag line — duplicating
     the entire deck. Instead, Claude composes the one new card directly as
     plain text (the same "Claude generates cards directly — no script
     execution needed" approach documented in `.cowork/instructions.md`'s
     "fill workflow" section) and appends it via a plain text Edit immediately
     after the last existing card block in the target file's `# Summary`
     section — or directly after the ` --- ` separator line if the file is
     currently empty (e.g. current N1–N3 files, which are just
     `TARGET DECK` + `# Summary` + ` ---`).
     Only the reference files are reused, and only for filling in field
     *values* — never the script, never its skeleton-insertion regex:
     - `#wc`: determine godan/ichidan/suru/kuru type, fill conjugation rows per
       `.cowork/skills/references/verb-conjugation.md`; suru verbs skip
       conjugation rows (header + `ほんやく:` line only).
     - `#wp`: determine い/な type, fill 過去形/否定形/副詞形/そう(looks) per
       `.cowork/skills/references/adj-forms.md`.
     - `#w`/`#wc`/`#wp`: evaluate honorific eligibility per
       `.cowork/skills/references/honorific-forms.md` and insert the
       `お/ご (honorific):` row if a natural form exists.
     - All types: append kanji mnemonic `<a href="https://kanji-trainer.org/...">`
       links per `.cowork/skills/references/kanji-links.md` (its own broader
       "any CJK character U+4E00–U+9FFF" test — see the `#k` rule below for how
       this differs from the `#k` tag test).
     - `#k` tag determination (part of composing the card header line, e.g.
       `<translation> #k #card`): check the word's kanji (furigana stripped)
       against `KanjiList.md` at the vault root (~262 entries, one kanji
       character per line, the curated list — not simply "any CJK character").
       If any single kanji character in the word matches an entry in
       `KanjiList.md`, include `#k` in the header line
       (`<translation> #k #card`); otherwise omit it (`<translation> #card`).
       This is a different, narrower test than `kanji-links.md`'s CJK-range
       test used for the mnemonic `<a>` links above — a word can have kanji
       mnemonic links without qualifying for the `#k` tag if none of its kanji
       are in the curated `KanjiList.md`. `KanjiList.md` is a dependency of
       this skill.
     Append the finished card block directly after the last existing card block
     in the target file's `# Summary` section (or directly after the ` --- `
     separator line if the file is currently empty). Do not add a
     `Rzeczowniki:`/`Czasowniki:`/`Przymiotniki:` header — these vocab files do
     not use that grouping.
   - Never touch: the `TARGET DECK` line, `# Summary` heading itself, or any
     existing `<!--ID:-->` line. New cards simply have no `<!--ID:-->` line
     until the Anki plugin later syncs them — this is expected, not an error.
   - Final step: report a one-line confirmation to the user (word, tag, level,
     file, whether a card block was generated, whether `#k` was applied).
2. Create `.claude/commands/add-word-to-deck.md` — slash command stub pointing
   to the new skill (flat file, no subdirectory, matching the skill's own flat
   location). Follow the existing one-line stub pattern used by other flat
   skills, e.g. `.claude/commands/summarize-grammar.md`:
   ```
   Read `.cowork/skills/add-word-to-deck.md` and follow its instructions
   exactly to add a word to the appropriate Vocabulary/JLPT-decks/ file.

   Word (or leave blank to infer from context): $ARGUMENTS
   ```
3. Update the skills list in `.cowork/instructions.md` (the `## Available
   skills` section) to register `add-word-to-deck` with its trigger phrases —
   **ask the user for explicit permission before editing this file**, per the
   project rule "Never modify files in .cowork/ without permission."
4. (Addendum, optional/small) Once the skill exists and is confirmed working,
   update the "used by" wording in the descriptions of the four reference files
   it consults — `.cowork/skills/references/verb-conjugation.md`,
   `adj-forms.md`, `honorific-forms.md`, `kanji-links.md` — to include
   `add-word-to-deck` alongside `fill-templates`/`templates-update`, so they
   don't go stale as documenting only the two older skills. `card-templates.md`
   is not consulted by this skill (it's a `templates-update`-specific canonical
   structure reference) and does not need updating.

## Risks
- Fuzzy duplicate matching can false-positive (unrelated word that happens to
  share kanji) or false-negative (genuinely different reading of a rare kanji
  compound); the confirm gate in Step C is the safety net — never auto-skip or
  auto-block silently.
- JLPT-level and Nouns-vs-Others guesses can be wrong; the confirm gate in
  Step B is the safety net.
- Card block insertion must always land after the last existing card and never
  between/inside existing card blocks, or it risks disturbing an existing
  `<!--ID:-->` line's association with its card text.
- Empty target files (current N1–N3 files, which are just `TARGET DECK` +
  `# Summary` + ` --- `) need the insertion logic to handle "no existing cards
  yet" without producing a stray blank card block.
- Running `fill_extract.py` against an already-populated deck file would
  duplicate the entire deck (see Step E) — this skill must never invoke that
  script; this is now explicit in Step E precisely to prevent an implementer
  from "reusing" it by mistake.
- The `#k` tag must be gated on `KanjiList.md` membership, not "contains any
  CJK character" — conflating the two tests (as an earlier draft implied) would
  over-tag `#k` on words whose kanji aren't in the curated list.
- Step C's inline-edit path (option c) only rewrites the raw tag line's
  translation/definition text; it must never touch the word/reading, and never
  touch anything below `# Summary` for that entry — mechanics repairs stay out
  of scope and are deferred to `templates-update`.
- `.cowork/instructions.md` is a protected file — Step 3 requires explicit user
  sign-off before editing, separate from the rest of the implementation.
