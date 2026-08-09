# Grammar-state extracted-file linking on fresh discovery

## Goal

When `lesson-grammar-practice` discovers a grammar point fresh out of a
lesson file (its normal discovery path — there is no pre-selected entry),
and that point has already been extracted to `grammar-index/grammar/`
(marked by the `→ [[grammar-index/grammar/<slug>]]` wikilink extract-grammar
inserts under the heading), the **brand-new** `grammar-state.json` entry
created for that point should store `lesson_file` pointing at the extracted
file instead of the lesson file. This lets later `scheduled-grammar-practice`
sessions pick up the richer extracted-file flow (frontmatter, `register`,
`confused_with`, enriched body) automatically, without lesson-grammar-practice
ever having to open or parse the extracted file itself.

## Approach

This is a **cheap, detection-only** change on the write side — not a
metadata-driven-exercise change. During `lesson-grammar-practice`'s existing
fresh heading-role parse, add a one-line regex check under each **point**
heading for the wikilink extract-grammar already inserts there. If found,
capture its target path; this becomes the point's `extracted_file_path`,
subject to a lightweight container-file guard (below). No frontmatter is
read and no body_text assembly happens for this — that heavier logic stays
exactly where it already earns its cost, in `scheduled-grammar-practice`'s
re-read path (which is being refactored into a shared common-file routine so
`scheduled-grammar-practice` doesn't duplicate it, per the confirmed reuse
decision).

**Hardened container-file guard (added on revision).** extract-grammar's
heading classification is user-gated (the user confirms/overrides every
candidate), while `lesson-grammar-practice`'s parse is deterministic and
never gated. If the two ever disagree on a heading's role — now or after
`_heading-roles.md`'s scaffolding-label list is extended later — a wikilink
under what this parse treats as a point heading could in principle target a
container file. Rather than relying on scheduled-grammar-practice's existing
downstream container guard to silently skip an orphaned entry later, this
plan adds an explicit guard at the point the link is about to be trusted:
before finalizing `extracted_file_path` for a point, open the target file
and check for the `## Sub-topics` heading — the exact container-file
signature scheduled-grammar-practice's extracted-file flow already checks.
If present, treat the point exactly as if no wikilink had been found at all
(`extracted_file_path = null`, ordinary lesson-file linking) — never leave
the point silently unlinked. This is a small, deliberate cost: one
lightweight file open (a heading-presence check, not a frontmatter parse or
body_text assembly) per point where a wikilink was actually detected — not
per point overall, and not the full "Loading an extracted grammar file"
routine.

At persistence time, `lesson_file` passed into `session_scores` for a given
point is the point's `extracted_file_path` if detected (and not
guard-rejected), otherwise the resolved lesson file path exactly as today.
`grammar_header` is always the lesson heading text already parsed — never
read from the extracted file's H1 (extract-grammar preserves the heading
verbatim, so they match by construction; no read needed to confirm it on
this hot path).

**"Leave existing entries alone" — enforced at both write sites (added on
revision).** The requirement is that `lesson_file` and `grammar_header`
become identity fields written only when a `grammar-state.json` entry is
created for the first time, preserved untouched on every later update. This
must hold at **both** places that actually write the state file, not just in
one skill's prose:

- The **lesson-scope direct-write path** (`practice-grammar-srs.md`'s
  generic Persistence section) — the path this feature's new entries are
  always created through, since `extracted_file_path` is only ever computed
  by `lesson-grammar-practice`.
- The **TODAY/OVERDUE two-step path** (`practice-grammar-srs.md` Step A +
  `load-control.py`'s `merge_and_write()`) — the path that later re-writes
  the *same* entries once `scheduled-grammar-practice` picks them up. This
  path already has a live case where the passed `grammar_header` can
  legitimately differ from the stored value (scheduled-grammar-practice's
  extracted-file flow: "if the H1 text differs ... continue using the H1")
  and, in the current code, `merge_and_write()`'s existing-entry branch
  unconditionally copies `lesson_file`/`grammar_header` from the session
  payload into the stored entry — the enforcement point is the *script*,
  not the prose describing it. This plan's scope therefore explicitly
  includes `.cowork/scripts/load-control.py`, not just files under
  `.cowork/skills/`.

## Steps

1. **`.cowork/skills/_practice-grammar-common.md` — "Grammar topics" parsing
   section (~lines 41-79):** add a new subsection, e.g. "Extracted-file
   linkage (fresh-discovery detection)":
   - For each **point**-role heading, check the line immediately after the
     heading line, before any other body content — extract-grammar step 8
     guarantees the wikilink is always inserted there, so this is a single,
     committed instruction, not a hedged "wherever it ends up" check — and
     test it against `^→ \[\[(grammar-index/grammar/[^\]]+)\]\]\s*$`.
   - Match → provisionally set `extracted_file_path = "<captured path>.md"`
     on that point's triple (append `.md`; the wikilink target omits the
     extension, the file on disk has it), **subject to the container-file
     guard in step 2 below.** This regex already covers both
     `grammar-index/grammar/<slug>.md` and
     `grammar-index/grammar/vocabulary/<subdir>/<slug>.md` (vocabulary
     extractions nest under the same prefix) — confirmed live against
     `JPLessons/Udemy/N4/Grammar/UN4GL15.md` →
     `grammar-index/grammar/vocabulary/Verbs/yoru-stop-by.md`.
   - No match → `extracted_file_path = null`, no further check needed.
   - Strip the matched wikilink line out of `body_text` (minor adjacent
     fix — it's a bare navigation link, not example content, and
     shouldn't be fed into exercise-generation prompts as if it were).
   - Note explicitly: this check never runs on container- or
     scaffolding-role headings, since those never become point triples in
     the first place (per `_heading-roles.md`).
   - **Scope note:** this subsection is only ever walked by
     `lesson-grammar-practice`'s full heading-role-classification pass over
     `# 文法`/`# Vocabulary`. `scheduled-grammar-practice`'s "2b. Lesson-file
     flow" does a separate, narrower single-heading-text search (locate
     `grammar_header` by exact/case-insensitive/whitespace-normalised match)
     and must never be wired into this detection subsection — it has no use
     for it, since 2b only re-reads pre-selected entries that already carry
     a `lesson_file`.
   - **Why the duplicate-heading-text carve-out doesn't apply here:**
     extract-grammar step 8's duplicate-heading-text handling exists because
     that step does a *global* regex substitution keyed on heading text
     across the whole pre-Summary slice, so an ambiguous match must be
     narrowed to a parent section's line range. This detection routine is a
     *positional* check (line immediately after a specific node) performed
     while walking an already-distinct per-node heading tree — each node is
     already unambiguous by construction, so no analogous scoping fix is
     needed.

2. **`.cowork/skills/_practice-grammar-common.md` — container-file guard
   (new; part of the same "Extracted-file linkage" subsection):** for any
   point where step 1 found a wikilink match, before finalizing
   `extracted_file_path`, open the target file and check whether it contains
   a `## Sub-topics` heading — the exact container-file signature already
   defined for scheduled-grammar-practice's extracted-file flow (reuse that
   check verbatim; do not invent a second one). If present: discard the
   match — set `extracted_file_path = null` and fall back to ordinary
   lesson-file linking for that point, exactly as if no wikilink had been
   detected. This is a lightweight read (open + heading-presence check
   only) — it does **not** parse frontmatter or assemble `body_text`; that
   remains exclusive to the "Loading an extracted grammar file" routine
   (step 3), used only when `scheduled-grammar-practice` actually drills the
   point later.

3. **`.cowork/skills/_practice-grammar-common.md` — new shared routine,
   "Loading an extracted grammar file"** (placed near "Loading a lesson file
   slice"): move `scheduled-grammar-practice.md`'s existing "2a.
   Extracted-file flow" logic here verbatim (whole-file read, frontmatter
   parse of `pattern`/`register`/`confused_with`/`function`/`topic_slug`/
   `level`, container-file guard on `## Sub-topics`, `grammar_header` =
   file's H1 with mismatch-warning-but-don't-skip, `body_text` assembly).
   This is the confirmed reuse target — a shared routine callable by any
   future consumer, even though today only `scheduled-grammar-practice`
   calls it. (This is a separate, heavier routine from step 2's lightweight
   guard — the two happen to check the same `## Sub-topics` signature but at
   different depths of file inspection; step 2 does not call into this
   routine.)

4. **`.cowork/skills/scheduled-grammar-practice.md` — "Multi-lesson file
   loading" section:** replace the inline "2a. Extracted-file flow" body with
   a short pointer to the common file's new "Loading an extracted grammar
   file" routine. Leave "2b. Lesson-file flow" untouched (genuinely
   scheduled-only — lesson-grammar-practice's fresh discovery never does
   entry-lookup-by-search). No behavioral change for scheduled-grammar-practice
   — this step is a pure refactor (move, not rewrite).

5. **`.cowork/skills/_practice-grammar-common.md` — "Persistence and
   Calendar sync" directive (~lines 411-422):** document the new per-point
   `lesson_file` source rule: default to the session's resolved lesson file
   path; if the point's parsed triple carries `extracted_file_path` (set only
   by steps 1–2, i.e. only ever populated during `lesson-grammar-practice`'s
   fresh-discovery parse, and only when the container guard passed), use
   that instead. Cross-reference the creation-only identity-field rule now
   enforced at both write sites (steps 6–8 below) so it's clear why passing
   a different `lesson_file` here is safe for already-existing entries.

6. **`.cowork/skills/practice-grammar-srs.md` — generic Persistence section
   (~lines 41–59, and the example around ~line 100 — the lesson-scope
   direct-write path, which is the only path this feature's new entries
   actually go through):** add an explicit sentence next to "If no prior
   entry: create one with defaults" stating that `lesson_file` and
   `grammar_header` are written **only** at this creation step; when an
   entry already exists for the `grammar_point_id`, its stored `lesson_file`
   and `grammar_header` are left untouched, regardless of what value
   `session_scores` supplies for that point this session. Today this
   section only shows the rule inferable from a JSON example — make it an
   explicit stated rule.

7. **`.cowork/skills/practice-grammar-srs.md` — Step A wording (TODAY/OVERDUE
   two-step write, ~line 85 "Always include `lesson_file` and
   `grammar_header` ... harmless for existing entries, required safety net
   for any edge case"):** correct this line — it is no longer accurate once
   step 8's script fix lands. Still always include both fields in the Step B
   payload (harmless to send), but clarify: they are only ever *applied* by
   `load-control.py` when the entry is being created for the first time; for
   an already-existing entry, the script now ignores these two fields
   entirely and keeps the stored values. Reference step 8 for the actual
   enforcement.

8. **`.cowork/scripts/load-control.py` — `merge_and_write()` (lines
   ~356–370), CRITICAL fix:** this is the actual enforcement point for "never
   rewrite an existing entry's identity fields" on the TODAY/OVERDUE path —
   prose changes alone (steps 6–7) don't change the script's behavior. Change
   the existing `is_new` branch split so identity fields are copied **only**
   in the `is_new` branch:
   - `is_new` branch: keep copying `lesson_file` and `grammar_header` (along
     with the SM-2/last-reviewed fields already copied there) — unchanged.
   - `else` branch (existing entry): remove `lesson_file` and
     `grammar_header` from the fields copied here. The entry already starts
     as `grammar_points[key].copy()`, so simply not copying these two
     fields leaves the stored values untouched (mirrors the existing
     "never SM-2 fields" comment's intent, extended to identity fields too;
     update that comment to say "never SM-2 fields, never identity fields").
   - Add a new test to `.cowork/scripts/test_load_control.py` (there is
     currently no test asserting identity-field preservation — only
     `TestExistingJSONPreserved` checks an untouched *other* entry, and
     `TestMergeWriteOnlyChangesDate` only checks SM-2 fields) mirroring
     `test_interval_days_not_overwritten_by_input`'s pattern: an existing
     entry with `lesson_file: "old/path.md"`, a session topic for the same
     key carrying a different `lesson_file`/`grammar_header`, assert the
     written entry still has the original values after `merge_and_write()`.

9. **`.cowork/skills/lesson-grammar-practice.md` — Workflow step 3:** add a
   sentence noting that fresh parsing now also captures `extracted_file_path`
   per point (via the common file's updated "Grammar topics" section,
   including its container-file guard), used only when building
   `session_scores` for persistence in step 7 — it has no effect on exercise
   generation, which continues to read only the lesson body exactly as
   today. Note that a point's extracted linkage may silently fall back to
   plain lesson-file linking if the container guard rejects it — this is
   expected and requires no user-facing message.

## Risks

- **Scope now includes `.cowork/scripts/load-control.py`**, not just
  `.cowork/skills/` — this is a behavior change to a script with an existing
  test suite (`test_load_control.py`). Step 8 adds a regression test for the
  new behavior; skill-implementer should run the full existing suite
  afterward to confirm nothing else asserts the old (overwrite-on-existing)
  identity-field behavior — confirmed by review of the current test file
  that no such assertion exists today.
- **Container-file guard (step 2) adds a real file read** to fresh discovery
  for every point where a wikilink is found — previously framed as a
  zero-file-read change. This is a deliberate, user-requested hardening
  trade-off (correctness over pure cheapness); the read is a single
  heading-presence check, not a full parse.
- **`body_text` wikilink stripping (step 1)** touches parsing behavior that
  is already live for every lesson with extracted headings — low risk
  (removes a bare markdown link, not example content) but flag for review
  since it's a change to existing, not just new, parsing output.
- **Regex false negatives**: if extract-grammar's wikilink format ever
  changes (e.g. adds a display alias `[[path|text]]`), the detection regex in
  step 1 needs to track it — no shared constant exists today, so both
  `extract-grammar.md`'s insertion format and this detection regex must be
  kept in sync manually.
- Everything else in this plan stays within `.cowork/skills/` — no lesson
  files, `<!--ID:-->` lines, or `TARGET DECK` are touched.

---

## Follow-up fix (post-implementation review)

**Status: step 7 above was reported complete but a post-implementation
review of the actual landed diff found it was never applied.** `git diff`
on `.cowork/skills/practice-grammar-srs.md` shows zero edits to the Step A
block (lines ~71-73). This is a real, live bug, not a documentation gap:

Step A is the manual, prose-driven write `lesson-grammar-practice`/
`scheduled-grammar-practice` execute directly against `grammar-state.json`
for every TODAY/OVERDUE session, *before* `load-control.py` (Step B) ever
runs. Step B's `merge_and_write()` fix (step 8 above, confirmed correctly
landed) only protects the existing-entry branch by starting from a copy of
what's already on disk when *it* runs — it has no way to undo damage Step A
already did earlier in the same session. So today, for TODAY/OVERDUE-scope
sessions, Step A silently overwrites `lesson_file`/`grammar_header` on an
already-existing entry whenever `session_scores` carries different values
for that grammar point — exactly the extracted-file-vs-old-plain-linkage
case this whole feature exists to handle. This reproduces the original bug
one write-site earlier than the site the first post-plan review round
caught.

Compounding issue: `_practice-grammar-common.md` (~lines 535-540) already
asserts the rule is "enforced at both write sites (see
practice-grammar-srs.md's generic Persistence section and Step A wording,
and load-control.py's merge_and_write())" — that claim about Step A wording
is currently false as shipped and must not be corrected by editing the
claim; it must be corrected by actually fixing Step A to match it.

**Scope of this follow-up: two spots in one file, `.cowork/skills/practice-grammar-srs.md`. No other file needs to change** — `load-control.py`, `_practice-grammar-common.md`'s own wording, and everything else the first two review rounds checked are already confirmed correct and must not be touched again.

10. **`.cowork/skills/practice-grammar-srs.md` — Step A wording (~lines
    71-73):** current text reads: *"For each practiced grammar point,
    update its entry with the computed SM-2 fields... Also write identity
    fields `lesson_file` and `grammar_header`."* Add the same creation-only
    qualifier already correctly stated a few lines above in the generic
    Persistence section (line ~46: *"`lesson_file` and `grammar_header` are
    written only at this creation step..."*): Step A must state that it
    writes `lesson_file`/`grammar_header` **only when creating a new entry**
    for that `grammar_point_id`; when an entry already exists, Step A leaves
    its stored `lesson_file`/`grammar_header` untouched and only updates the
    computed SM-2 fields (`interval_days`, `ease`, `streak`,
    `total_reviews`, `weak_points`, `last_reviewed`, `last_score`, `score`),
    regardless of what value `session_scores` supplies for that point this
    session. Do not just cross-reference the generic section — Step A must
    state the rule inline, since it is executed as its own self-contained
    instruction block.

11. **`.cowork/skills/practice-grammar-srs.md` — stale parenthetical (~line
    108):** current text: *"The script reads the updated state (SM-2 fields
    from Step A), computes `next_review` via `place_topics()`, and writes
    only `next_review` (plus identity fields) via `merge_and_write()`."* The
    "(plus identity fields)" parenthetical is no longer accurate now that
    `merge_and_write()` only sets identity fields in the `is_new` branch
    (step 8, confirmed correctly landed). Correct to something like: "...and
    writes `next_review` (plus identity fields, but only for newly created
    entries — see `merge_and_write()`) via `merge_and_write()`."

No changes to `_practice-grammar-common.md`, `load-control.py`,
`test_load_control.py`, `scheduled-grammar-practice.md`, or
`lesson-grammar-practice.md` — all confirmed correct as landed.
