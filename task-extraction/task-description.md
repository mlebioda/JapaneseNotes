# Task: Grammar-gap audit of JPLessons/Japoński_lekcje

## Goal
`grammar-index/` was built by extracting grammar topics from the **Udemy** course
directory (`JPLessons/Udemy/`). `JPLessons/Japoński_lekcje/` is an older, separate
course (mostly Polish-language notes, no consistent file structure — not the
TARGET DECK / ごい / 文法 / Summary format described in `.cowork/instructions.md`).

This task scans each in-scope file in `Japoński_lekcje/` and identifies grammar
topics/patterns that are **not yet covered** in `grammar-index/`. Phase 1
(below) was **identification-only** — it did not extract, restructure, or
modify any lesson file, and did not create new grammar-index entries. Phase 2
(see further down) is where findings turn into actual decisions and, where
warranted, new content.

**Status:** Phase 1 complete (`file-list.md` 100% checked, `findings.md` +
`findings2.md` written). Phase 2 is split into two passes: the 17-topic
`UNCERTAIN` pass is **complete** (2026-09-12, all 17 decided and executed —
plus C2, C5, M1, and F4, picked up opportunistically along the way). The
`GAP`-topic pass (29 topics still open, of the original 32 minus C2/C5/M1) is
next — see "Phase 2" section below.

## Phase 1 — Audit (complete)

### Scope — which files
In scope (listed in `file-list.md`):
- All `Gramatyka*.md` files (explicit grammar lesson notes)
- General lesson/summary `.md` files with no topic prefix (e.g. `L1.md`,
  `S6L11.md`, `S7L1-L2.md`, `Semestr1.md`, `Egzamin.md`, `toimport1.md`,
  `Sunstar-Deck.md`) — these often mix grammar with other content

Explicitly excluded:
- `Kaligrafia*.md` — calligraphy notes, not grammar
- `Slownictwo*.md` (and vocabulary-only files like `SlownictwoL4.md`) — vocabulary, not grammar
- `Podsumowanie Kanji.md` — kanji summary, not grammar
- `*.pdf` files — not text-scannable the same way; excluded from this pass
- `.DS_Store`

Two filenames are worth double-checking while processing (flagged, not resolved,
by this setup pass):
- `Semestr6/L02/GramatykaS6L2 1.md` alongside `Semestr6/L02/GramatykaS6L2.md` —
  possible duplicate/alternate version
- `Semestr4/L01/Untitled.md` — unclear content, confirm it's actually a lesson file

### Method — how to check "covered"
For each file:
1. Read the full file content.
2. Identify distinct grammar topics/patterns discussed (a topic = a specific
   grammar point, e.g. "〜ばよかった", not a whole lesson).
3. For each topic found, check whether an equivalent standalone file already
   exists under `grammar-index/grammar/*.md` (these are the per-pattern files
   created by `extract-grammar`, one per grammar point). Match on meaning/
   function, not just surface string — Polish and Udemy/English phrasing will
   differ for the same grammar point.
4. If no matching file exists → record it as a finding in `findings.md`.
5. If it matches an existing file → do not record it (already covered); no need
   to note "covered" items unless genuinely ambiguous (see below).
6. If genuinely unsure whether something counts as "already covered" (e.g. a
   near-miss, a variant form, a register difference) → record it anyway in
   findings.md, flagged as "uncertain — needs review", rather than silently
   skipping it.

### Output files in this directory
- **file-list.md** — checkbox list of in-scope files, one checkbox per file.
  Check a box only once that file has been fully read and any findings for it
  have been written to findings.md.
- **findings.md** — one `##` chapter per file that had at least one finding
  (files with nothing new found do not need a chapter, but see step 6 above).
  Each chapter should note: topic name/short description, and a line number or
  section reference in the source file so it's easy to look up later.

### Resuming Phase 1 (only relevant if new source files are ever added)
Point the agent at this `task-extraction/` directory. It should:
1. Read this file for context.
2. Read `file-list.md`, find the first unchecked file.
3. Process it per the Method above.
4. Append findings to `findings.md`, check the box in `file-list.md`.
5. Continue to the next unchecked file (ask the user how many files to process
   per session/batch, rather than assuming "all of them").

## Phase 2 — Deciding & remediating findings (started 2026-09-11)

`findings2.md` groups Phase 1's raw findings into ~66 distinct topics; 17 of
those turned out to already be covered by the Udemy course and were removed
(see the callout at the top of `findings2.md`). The remaining topics are each
`GAP` (32, nothing covers them) or `UNCERTAIN` (17 near-misses/variants).

For every remaining topic, add a `- **DECISION:**` line under its entry in
`findings2.md` recording what to do with it, plus a `- **STATUS:**` line once
that decision is actually executed (not just recorded).

**Progress:**
- All 17 `UNCERTAIN` topics: **decided and executed** (2026-09-12). Every one
  has both a `DECISION:` and a `STATUS:` line — verified with a grep pass,
  no gaps or duplicates.
- 3 `GAP` topics (C2, C5, M1) plus 1 topic outside the original 49 (F4,
  surfaced while reviewing F3) were also decided and executed opportunistically
  during the uncertain-topic pass — see their entries for detail.
- **29 `GAP` topics remain fully open** (no DECISION line yet) — this is the
  next pass, using the exact same process and rules documented below (decision
  types, master-list gate, Leftovers workflow, tracking requirements). Go
  through them the same way: one at a time, present the topic + relevant
  master-list check, let the user decide, execute via subagent only after an
  explicit go-ahead (never infer approval from a clarifying question), then
  record DECISION + STATUS.

A decision is one of:

- **Resolved** — turns out to already be covered somewhere in grammar-index
  (found during this closer analysis pass); no action needed.
- **Skip** — too narrow, compositional, vocab-level, or fixed-phrase to
  justify either of the options below.
- **Fold in** — the topic is a near-miss/missing detail of an *existing*
  `grammar-index/grammar/*.md` file; update that file directly with the
  missing structure/examples/section.
- **New file** — the topic needs a standalone new grammar point with no
  existing home. See "Creating a new-file topic" below for how these get
  written.
- **Vocab** — not actually a grammar point (a fixed phrase, interjection, or
  discourse marker with no structure of its own), often a topic that also
  fails New file's master-list gate (Step 0 below) — gets a `#w`/`#wc`/`#wp`
  card in a `Leftovers-<N>.md`'s `# Vocabulary` chapter instead of a `# 文法`
  entry. Counts toward the same 6-topic cap as New file.

### Creating a new-file topic
Grammar-index files are meant to be *generated* from a lesson file via
`lesson-to-web/extract-grammar`, not authored directly. So a "new file"
decision doesn't create a `grammar-index/grammar/*.md` file straight away —
it first creates (or adds to) a **lesson file**, structured like the `# 文法`
section of a normal Udemy grammar lesson, which can later be run through
`extract-grammar` like any other lesson:

0. **Master-list gate:** a topic only qualifies for "New file" if it maps to
   an actual bullet in `JLPT-N5-Grammar-List.md`, `JLPT-N4-Grammar-List.md`,
   or `JLPT-N3-Grammar-List.md` (checked as 🔴, i.e. flagged there as a real,
   currently-uncovered gap — at whichever level it's actually tagged, even N3).
   If it doesn't map to any of the three, it can't become a new-file topic by
   default — reconsider as Skip or Fold-in instead. A topic can still be
   made an exception to this gate, but only with explicit justification
   (e.g. a grep-confirmed vault-wide gap plus a clear teaching rationale) —
   flag the exception explicitly rather than treating the gate as optional.
   (B11 — と + mimetic word — was drafted before this gate existed and is
   grandfathered in as a one-off exception, not a precedent. F3/F4 — 欲しがる／
   を and たがる — are later exceptions, approved explicitly by the user after
   being flagged.)
1. **Where:** `JPLessons/Udemy/N5/Grammar/`, `JPLessons/Udemy/N4/Grammar/`, or
   `JPLessons/Udemy/N3/Grammar/` — whichever level the topic belongs to,
   decided by which master list it maps to. The N3 folder didn't exist until
   C2/C5 needed it (2026-09-12) — it's now established, same rules apply.
2. **Filename:** `Leftovers-<N>.md`, where `<N>` increments per level folder
   independently (N5, N4, and N3 each have their own numbering — currently
   all three are on `Leftovers-1.md`). A `Leftovers-<N>.md` file can hold two chapters — `# 文法`
   for grammar topics (New file decisions) and `# Vocabulary` for vocab
   topics (Vocab decisions, e.g. a discourse marker/interjection that fails
   the grammar master-list gate — see Step 0 — and gets a `#w`/`#wc`/`#wp`
   card instead). **Maximum 6 topics total per `Leftovers-<N>.md` file,
   counting `# 文法` and `# Vocabulary` entries together** (e.g. 4 grammar +
   2 vocab = 6, not 6 of each) — once a file has 6 combined, the next
   new-file topic starts `Leftovers-<N+1>.md`.
3. **Content sourcing:** translate/export the relevant content from the old
   `Japoński_lekcje` source file(s) findings2.md cites for that topic (Polish
   → a proper 文法-style structure/examples entry), then review the draft
   together before finalizing it in the `Leftovers-<N>.md` file.
4. **Structure:** each topic entry inside a `Leftovers-<N>.md` file follows
   the same shape as a `# 文法` entry in a real Udemy lesson (pattern header,
   structure, examples, etc.) — not the `findings2.md` analysis format.
5. **After drafting, two tracking updates are required (not optional):**
   - In the relevant master list (`JLPT-N5-Grammar-List.md` /
     `JLPT-N4-Grammar-List.md`), change the topic's marker from 🔴 to 🟡 and
     append " — drafted in Leftovers-<N>, pending extract-grammar". Never
     jump straight to 🟢 — the content isn't in `grammar-index/` yet, it's
     only a draft lesson stub.
   - In `findings2.md`, add both a `- **DECISION:** New file...` line and a
     `- **STATUS:**` line under the topic's entry, with the STATUS line
     naming the exact `Leftovers-<N>.md` file the topic was drafted into and
     the date.

## Open questions — resolved
- ~~What happens to a finding once recorded...~~ Resolved above: findings get
  a `DECISION:` line (resolved / skip / fold-in / new-file / vocab), a
  `STATUS:` line once executed, and new-file/vocab topics get written into
  `Leftovers-<N>.md` lesson files (N5, N4, or N3) for later `extract-grammar`
  processing.
- ~~Should new-file topics be gated by the master lists?~~ Yes — Step 0's
  master-list gate (added after B11), extended to cover N3 as well as N5/N4.
- ~~Can a Leftovers file mix grammar and vocab?~~ Yes — `# 文法` and
  `# Vocabulary` chapters share one combined 6-topic cap per file.

## Next: the GAP-topic pass
Same process as the just-finished `UNCERTAIN` pass, applied to the 29 open
`GAP` topics (see "Progress" above for the current list). Go through them one
at a time — present the topic and its master-list status, wait for an
explicit decision from the user, execute only after an explicit go-ahead
(never infer approval from a clarifying question — this was a real mistake
made and corrected during the `UNCERTAIN` pass), then record both `DECISION:`
and `STATUS:`.
