---
name: add-word-to-deck
description: >
  Flag a word encountered mid-session (in a lesson, chat, or review) as worth
  remembering and add it as a fully-formed Anki flashcard to the correct file
  under Vocabulary/JLPT-decks/ — tag classification, JLPT level + POS file
  guess, duplicate scan, and full card generation, all with a confirm gate
  before writing. Trigger: "add this word to a deck", "remember this word",
  "save this word", "add <word> to deck".
---

# Add Word to Deck Skill

## Trigger

User says any of:

- "add this word to a deck"
- "add word to deck"
- "remember this word"
- "save this word"
- "add <word> to deck" (explicit word given)
- close variants of the above

### Word-inference rule (bounded lookback)

If no word is typed explicitly after the trigger phrase, infer it from the
**single most recent Japanese word/phrase explicitly mentioned in the last
user or assistant message only** (the message immediately before the trigger,
or the trigger message itself if it names a word). Do not search further back
in the conversation.

- If that message contains exactly one plausible Japanese word/phrase
  candidate, use it.
- If that message contains **no** Japanese word/phrase, or **more than one**
  plausible candidate, stop and ask the user which word they mean. Do not
  guess and do not look further back.

---

## Workflow

### Step A — Tag classification

Classify the word per the tag conventions in `.cowork/instructions.md`:

- Verb → `#wc`. Append `(transitive)` or `(intransitive)` after the English
  translation.
- Adjective → `#wp`.
- Everything else (noun, expression, sentence, adverb) → `#w`.
- Suru-noun (a noun that pairs with する, e.g. 安心する) → `#w`, with `(する)`
  appended directly after the reading parenthesis: `安心 (あんしん)(する)`.

### Step B — Placement guess

Guess, then show to the user for confirm/override before continuing:

- **JLPT level** (N5–N1) — Claude's best judgment based on word difficulty/frequency.
- **POS file**:
  - `#wc` → `Verbs.md`
  - `#wp` → `Adjectives.md`
  - `#w` → `Nouns.md` if it is a concrete noun; `Others.md` if it is an
    expression/greeting/adverb/grammatical word (matching the existing
    Nouns.md vs Others.md split visible in the current deck files).

Present the guess as `<level> / <file> / <tag>` and wait for the user to
confirm or override before proceeding to Step C. Do not write anything yet.

### Step C — Duplicate scan

Scope: read the confirmed target level's four POS files (`Nouns.md`,
`Verbs.md`, `Adjectives.md`, `Others.md`) plus the same four files in every
other level, restricted in every file to **the content above that file's
`# Summary` line only** (the raw `#w`/`#wc`/`#wp` tag list). The generated
card block below `# Summary` is not needed for this check — larger files can
have 1000+ lines there, so do not read past `# Summary`.

Check the confirmed word (and its component kanji/reading) against every
existing tag line for:
- an exact match,
- a different-reading match,
- an okurigana variant,
- a conjugated-form match of the same lemma (e.g. 見る vs 見ます).

**If no candidate is found**, proceed to Step C2.

**If a candidate is found**, present it (file path + the matching line) to
the user and ask them to choose one of:

- **(a) proceed anyway** — add the new entry alongside the existing one. Go
  to Step C2.
- **(b) skip** — abort the add entirely. Stop here, no write happens.
- **(c) edit the existing entry instead** — ask the user to dictate the
  corrected translation/definition, then replace only the existing raw tag
  line's translation/definition text (everything after the word/reading
  portion — the ` - <translation> | <short definition>` part, including any
  transitive/intransitive marker or adjective-type suffix) via a plain-text
  Edit on that single line. Never touch the word/reading portion of the
  line, and never touch anything below that file's `# Summary` line for this
  entry. If the existing card's *mechanics* (conjugation forms, kanji links,
  `<!--ID:-->` positioning) also need repair, tell the user that is out of
  scope for this skill — they should run `templates-update` on that file
  separately. After an inline edit under option (c), the add is complete —
  do not also append a new duplicate entry; do not proceed to Step D/E.

Wait for the user's decision before writing in all three cases.

### Step C2 — Git safety check

Before any write (the Step C option-(c) inline edit, or the Step D/E
append), run `git status` scoped to the target file. If it has pending
uncommitted changes, commit a "WIP" snapshot for that file first, per
`.cowork/instructions.md`'s rule: "Git is the rollback mechanism — no `.bak`
files. Before a destructive edit, ensure pending changes are committed...
then edit; commit the change separately." Then proceed with the edit. The
add-word-to-deck change itself is committed separately if the user has git
commits enabled for this workflow — otherwise leave it staged/unstaged per
normal session behavior. Never run `git push`.

### Step D — Compose and append the raw tag line

Use `word (reading)` — a **space** before the reading parenthesis (verified
against `N4/Nouns.md`, `N4/Others.md`, `N4/Verbs.md`, `N4/Adjectives.md`, all
of which consistently use this spacing). Do **not** copy the differently
spaced `word(reading)` example from `.cowork/instructions.md`'s "Image
extraction format" section — that spacing does not match the actual deck
files.

Exact templates per tag:

- `#w` (non-suru):
  `#w <word> (<reading>) - <translation> | <short definition>`
  e.g. `#w 間 (あいだ) - space, interval | The gap or period between two points...`
- `#w` (suru-noun):
  `#w <word> (<reading>)(する) - <translation> | <short definition>`
  e.g. `#w 安心 (あんしん)(する) - relief, peace of mind | A state of feeling reassured...`
- `#w` (kana-only, no reading):
  `#w <word> - <translation> | <short definition>`
  e.g. `#w つもり - intention, plan | What a person means or plans to do...`
- `#wc`:
  `#wc <word> (<reading>) - <translation> (transitive|intransitive) | <short definition>`
  e.g. `#wc 合う (あう) - to match, to fit (intransitive) | Describes two things...`
  Additional parenthetical markers such as `(honorific)` or `(humble)` may
  appear immediately before the transitive/intransitive marker when
  applicable, e.g.
  `いらっしゃる - to be, to come, to go (honorific) (intransitive) | ...`
- `#wp`:
  `#wp <word> (<reading>) - <translation> | <short definition>; i-adjective.`
  or `; na-adjective.` — the adjective-type suffix is appended directly after
  the short definition, ending the line, e.g.
  `#wp 浅い (あさい) - shallow | Describes a small distance from top to bottom... the opposite of 深い; i-adjective.`
  This convention is not documented in `.cowork/instructions.md` but is
  consistently used in `N4/Adjectives.md` and must be followed.

Append the composed line to the end of the target file's top tag list (the
block of `#w`/`#wc`/`#wp` lines directly above `# Summary`), as its own new
last line.

### Step E — Generate and append the full card block

**Do not run `fill_extract.py` or any script for this step.** That script
builds skeleton cards by regex-matching an *empty* `# Summary` block at
end-of-file — it only matches when `# Summary` has nothing after it. Run
against an already-populated file like `Vocabulary/JLPT-decks/N4/Nouns.md`
(thousands of lines, hundreds of existing cards with `<!--ID:-->` lines), the
regex would not match the existing non-empty `# Summary`, so the script would
append a *second* `# Summary` block and regenerate skeletons for every
existing tag line in the file — duplicating the entire deck. Instead, compose
the one new card directly as plain text — the same "Claude generates cards
directly — no script execution needed" approach used by the `fill-templates`
skill's fill workflow.

`Vocabulary/JLPT-decks/` files use a flat card layout — no
`Rzeczowniki:`/`Czasowniki:`/`Przymiotniki:` section headers (see
`N4/Others.md`). Do not add one.

The Japanese field in the card body (the `ほんやく:` line for `#wc`/`#wp`, or
the bare line for `#w`) uses the exact same `word (reading)` text — same
spacing — composed for the raw tag line in Step D. Copy it as-is.

Field values are derived by reusing the four reference files' derivation
logic (never the script, never its skeleton-insertion regex):

- `#wc`: determine godan/ichidan/suru/kuru type, fill all conjugation rows
  per `.cowork/skills/references/verb-conjugation.md`. Suru verbs skip
  conjugation rows entirely (header + `ほんやく:` line only).
- `#wp`: determine い/な type, fill 過去形/否定形/副詞形/そう(looks) per
  `.cowork/skills/references/adj-forms.md`.
- `#w`/`#wp`: evaluate honorific eligibility per
  `.cowork/skills/references/honorific-forms.md` and insert the
  `お/ご (honorific):` row (immediately after the Japanese field line for
  `#w`, or as the last form row before kanji links for `#wp`) only if a
  natural form exists. Omit the row entirely otherwise — no placeholder.
  `#wc` is never eligible for this row (per `honorific-forms.md`) — its own
  honorific-flavored fields (`お〜になる/special verb (honorific):` and
  `謙譲語 (humble):`) are separate conjugation-row fields already covered by
  the `#wc` bullet above, derived from `verb-conjugation.md`, not from
  `honorific-forms.md`.
- All types: append one kanji trainer link
  `<a href="https://kanji-trainer.org/Mnemonic_phrase/Mnemonic_X.html">X</a>`
  per unique CJK kanji character (furigana stripped, ordered by first
  occurrence), per `.cowork/skills/references/kanji-links.md`.

#### `#k` tag rule

Part of composing the card header line (`<translation> [#k] #card`): check
the word's kanji (furigana stripped) against `KanjiList.md` at the vault root
(~262 entries, one kanji character per line — the curated list). If **any**
single kanji character in the word matches a line in `KanjiList.md`, include
`#k` in the header (`<translation> #k #card`); otherwise omit it
(`<translation> #card`).

This is a **different, narrower** test than the kanji-links.md CJK-range test
used for the mnemonic `<a>` links above — a word can have kanji mnemonic
links without qualifying for the `#k` tag, if none of its kanji are in the
curated `KanjiList.md`. Never substitute "contains any CJK character" for
this check. `KanjiList.md` is a dependency of this skill.

#### Card header

`<translation> | <short definition> [#k] #card` — i.e. everything after the
` - ` separator in the Step D raw tag line, plus the `#k`/no-`#k` tag from
above, plus `#card`.

#### Placement

Append the finished card block directly after the last existing card block
in the target file's `# Summary` section.

**Empty-file handling**: if the target file currently has no cards yet (e.g.
current N1–N3 files, which are just `TARGET DECK` + `# Summary` + ` ---`),
append the new card block directly after the ` ---` separator line instead —
do not produce a stray blank card block or an extra separator.

---

## Never touch

- Lesson files under `JPLessons/` (read-only — never write; this skill never
  reads them either, it operates only on `Vocabulary/JLPT-decks/`).
- The `TARGET DECK` line at the top of the target file.
- The `# Summary` heading itself.
- Any existing `<!--ID:-->` line, anywhere. New cards have no `<!--ID:-->`
  line until the Anki plugin later syncs them — this is expected, not an
  error.
- Do not run `git push` or any remote git operation.
- Never invoke `fill_extract.py` for this skill (see Step E).

---

## Final report

After the write (or after an inline edit under Step C option (c)), report a
one-line confirmation to the user: word, tag, level, target file, whether a
full card block was generated, and whether `#k` was applied.
