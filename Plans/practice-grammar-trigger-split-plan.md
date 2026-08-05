# Split practice-grammar into lesson-file and scheduled-session skills

## Goal

`.cowork/skills/practice-grammar.md` (527 lines) currently dispatches on two
structurally different session types under one trigger set: a single-lesson-file
drill session, and a scheduled (TODAY/OVERDUE) multi-file SRS-driven session
sourced from `grammar-state.json`. The mixed trigger-dispatch makes the file
harder to reason about and to extend (e.g. the metadata-driven exercise
generation for extracted-file topics only ever applies to the scheduled path,
but currently sits inline next to logic the lesson path never uses). This
plan splits the file into three: a shared common file holding everything both
session types actually use, and two thin trigger-specific skills.

Design rule driving every boundary call below (user's own framing): **what is
currently a common behavior goes in the single shared file — everything else
stays local to whichever of the two new skills can actually produce it.**

Two already-externalized helper files keep their internal logic unchanged by
this plan — but their cross-references to the file being deleted must be
updated (see boundary decision 9 and Step 4 below):
- `.cowork/skills/practice-grammar-srs.md` — SM-2 persistence + `.ics` write. Already takes a `scope` param.
- `.cowork/skills/practice-grammar-study-mode.md` — Study Mode. Already file-agnostic re: session type.

## Approach

Three new files replace the one:

1. `.cowork/skills/_practice-grammar-common.md` — never directly triggered (underscore
   prefix, matching `_heading-roles.md` / `_conventions.md` convention). Carries
   its own frontmatter (`name` + `description`) even though it's loaded
   programmatically, same as `_heading-roles.md`. Holds the shared awk-slice
   loading step, grammar-topic and vocab-pool parsing (base rules), grammar
   point ID construction, the core exercise-generation rules (Types 1–6, the
   3 gates, furigana/vocab/weak-point/type-selection/variety rules, with the
   two extracted-file-only cross-references trimmed — see boundary decisions
   4 and 5), all interaction-flow *mechanics* (progress indicator, batch/interactive
   presentation and grading-display formatting — not session header/footer
   text), grading rules, session-summary mechanics (format description with a
   generic placeholder header, not a lesson- or scope-specific worked
   example), the Persistence/Calendar-sync load-directive (parameterized by
   `scope`, which the caller sets), the Study Mode invocation hookup, and the
   Never-touch list.
2. `.cowork/skills/lesson-grammar-practice.md` — the lesson-code/filename
   trigger path. Single file load via the shared awk-slice step plus its own
   fresh heading-role parsing (no pre-selected entries — see boundary decision
   7), `num_batches` fixed at 1 (no batch-split prompt), its own session
   header/footer text and worked example (`Session: UN4GL7 — ...` / `Session
   complete — UN4GL7 (...)`), calls into the common file for everything else,
   persists with `scope="lesson"`. Its frontmatter `description` is written
   to positively require a lesson-code/filename shape and explicitly exclude
   scope/date phrasing (boundary decision 8).
3. `.cowork/skills/scheduled-grammar-practice.md` — the TODAY/OVERDUE trigger
   path. Scope resolution (TODAY/OVERDUE filters, edge cases), multi-lesson
   file loading (extracted-file flow 2a in full, plus a loop over the shared
   awk-slice step for lesson-file entries 2b — including the entry-lookup-by-search
   and orphaned-entry Migration note, which only make sense against
   pre-selected `grammar-state.json` entries — see boundary decision 7), the
   `Vocabulary/*.md` fallback pool, the extracted-file use-case-extraction
   variant, the entire Metadata-driven exercise generation section
   (`confused_with`, `register`, weak_points↔confused_with synergy), the
   batch-split prompt, its own Today/Overdue session header/footer text and
   format strings, calls into the common file for everything else, persists
   with `scope="TODAY"`/`"OVERDUE"`. Its frontmatter `description` is written
   to positively require an explicit scope keyword and not fire on
   lesson-code-shaped input (boundary decision 8).

**Disposition changed during implementation (user instruction):** the old
`.cowork/skills/practice-grammar.md` is not deleted — it is moved to
`practice-grammar.md` at the vault root once the split is verified working,
kept as a reference copy. Since skills only load from `.cowork/skills/`,
this file no longer functions as an active skill once moved; this is an
explicit one-off exception to the "never create files in vault root" rule.
The old `.claude/commands/practice-grammar.md` stub is still deleted outright
and replaced with two new stubs (confirmed with user) — a command stub
pointing at a relocated reference file would be non-functional either way.
Stale references to the old filename in other vault files (agent catalog,
shared-rule descriptions, provenance notes) are also fixed — see Step 10.

## Content-boundary decisions (resolve ambiguous splits before implementation)

Do not re-derive these during implementation — they were resolved during
planning (items 1–5 with the user directly; items 6–9 added after a reviewer
audit of this plan found gaps):

1. **`## Session summary`** (source lines 474–499): mechanics/rules (lines
   476, 478, 496–499 — "summarize at grammar-point level," Solid/Needs-practice
   classification) go in the common file, described with a generic placeholder
   header (e.g. `Session complete — <header> (N exercises across M grammar points)`)
   instead of the source's concrete `UN4GL7` example. Each trigger skill supplies
   only its own footer-line text that plugs into this shared format:
   - lesson skill: `Session complete — <lesson-code> (N exercises across M grammar points)` (pattern from source line 481)
   - scheduled skill: `Session complete — today's topics (N exercises across M grammar points)` / `Session complete — overdue topics (N exercises across M grammar points)` (source lines 342, 347)
2. **`## Persistence and Calendar sync`** (source lines 503–517): identical
   load-directive and field list for both flows — only `scope` differs. Lives
   **once** in the common file, parameterized by `scope` (set by whichever
   trigger skill calls it: `"lesson"` vs `"TODAY"`/`"OVERDUE"`). Not duplicated.
3. **Batch-mode "Layout for the batch prompt" example** (source lines 352–370):
   conflates a generic exercise-numbering/no-hints layout mechanic (shared)
   with a concrete lesson-only header example (`Session: UN4GL7 — 14 exercises...`).
   Common file keeps the generic layout description with no lesson name in it;
   each trigger skill's own concrete header/example lives in its own file
   (lesson skill: the `UN4GL7` example verbatim; scheduled skill: source lines
   328–350, the Today/Overdue header and footer format blocks, plus the `K
   lessons = ...` / `M = ...` variable definitions on line 350).
4. **Weak-point bias paragraph** (source line 269): base rule is shared; its
   trailing sentence ("For extracted-file topics, if the weak_point names a
   pattern confusion... apply the weak_points ↔ confused_with synergy rule
   instead...") is scope-only and must be trimmed from the common file's
   version — that rule already lives in full in Metadata-driven exercise
   generation, which is scope-only content.
5. **Type-selection rule bullet** (source line 277, the "Extracted-file topic
   with a resolvable `confused_with` entry..." bullet under Type selection
   rule): same failure category as decision 4 — this bullet's
   `(see Metadata-driven exercise generation → confused_with / → register)`
   cross-reference points into scope-only content. Trim this bullet out of
   the common file's Type selection rule list entirely; the rest of the Type
   selection rule (source lines 271–276) is shared as-is.
6. **`## Never touch`** (source lines 521–526): copied into the common file
   as-is — every rule in it applies identically to both flows. The
   `.cowork/instructions.md` update note stays flagged as requiring explicit
   user permission (task-level flag, not duplicated per skill file).
7. **Single-lesson-file loading routine is split, not merged.** Source
   describes this in two places — Workflow steps 1–2 (lines 110–117, generic
   awk-slice extraction) and Scope resolution's "2b. Lesson-file flow" (lines
   79–84, which *also* includes "for each selected entry, locate
   `grammar_header` in the loaded slice by searching... skip with warning if
   no/ambiguous match"). That entry-lookup-by-search step only makes sense
   when entries are **pre-selected** from `grammar-state.json` (the scheduled
   flow's case) — the lesson trigger never has pre-selected entries; it
   discovers every grammar point fresh via heading-role classification
   (source lines 171–187) and never searches for a specific pre-given
   `grammar_header` string. Therefore:
   - **Common file** gets only the awk-slice extraction (source lines 81–83,
     the `awk '/^# Summary$/{exit}'` command and "pass only this slice to
     subsequent parsing" instruction) as a routine taking a resolved file
     path as input.
   - **Scheduled skill** gets the entry-lookup-by-search logic (source line
     84: exact → case-insensitive → whitespace-normalised match, skip with
     warning on no-match or ambiguous-match) as part of its own Multi-lesson
     file loading section, since only it ever has pre-selected entries to
     look up.
   - **Scheduled skill** also gets the "Migration note" (source line 187,
     currently sitting inside the Grammar-topics parsing subsection) — it
     describes the exact same failure mode (a stored `grammar_header` from
     `grammar-state.json` no longer matching any heading after a lesson is
     re-parsed) and only applies to the entry-lookup path. It must move out
     of the common file's Grammar-topics parsing content and into the
     scheduled skill, next to the entry-lookup logic it documents.
   - The fuzzy code/filename matching that produces a lesson trigger's
     resolved file path (source line 23) stays in the lesson skill's Trigger
     section — only the lesson trigger ever needs to resolve a
     user-typed code.
8. **Trigger disambiguation between the two new skills has no home in either
   skill's own Trigger section — it must be solved via frontmatter
   `description` wording.** Source line 31 ("Scope triggers are matched
   before lesson-code detection. If no scope phrase and no lesson reference
   are found, fall through to existing ambiguity handling.") was the single
   file's internal dispatch order — it assumed one skill doing both matches
   itself, in sequence, with the ability to try one pattern then fall back to
   the other. After the split, Claude Code's own skill-selection mechanism
   matches each of the two skills **independently** via its frontmatter
   `description` — neither skill can defer to or override its sibling from
   inside its own Trigger section, and copying line 31's wording verbatim
   into either file is meaningless (it references "lesson-code detection," a
   concept that would live entirely in the other file). Both phrase shapes
   collide (`"practice <X>"` / `"drill <X>"` for both lesson-code and
   scope-keyword X), so the descriptions must be written to be mutually
   exclusive by content, not by dispatch order:
   - `lesson-grammar-practice.md` frontmatter `description`: must positively
     require a lesson-code/filename shape (e.g. `UN5GL14`-style codes,
     explicit lesson filenames, or phrasing that names a specific lesson) and
     explicitly state it does **not** match date/scope phrasing ("today",
     "today's topics", "overdue", "due", "scheduled").
   - `scheduled-grammar-practice.md` frontmatter `description`: must
     positively require an explicit scope keyword ("today", "today's
     topics", "overdue", "due today") and explicitly state it does **not**
     match lesson-code/filename-shaped input.
   - Delete source line 31 rather than copying it into either file. Each
     skill's own Trigger section may keep a short one-line note on what
     shape of input it does *not* match (naming the sibling skill by name),
     but the actual disambiguation mechanism is the frontmatter wording, not
     in-body dispatch logic.
9. **`practice-grammar-srs.md` and `practice-grammar-study-mode.md` contain
   live references to the file being deleted.** Their internal logic is
   unchanged, but every reference to `practice-grammar.md` by filename, and
   the one reference to a specific numbered Workflow step (which no longer
   exists as a single numbered sequence spanning one file once the batch-loop
   mechanics move into the common file's own section structure), must be
   rewritten. See Step 4 for the exact line-by-line fixes.

## Steps

1. **Create `.cowork/skills/_practice-grammar-common.md`.**
   - Frontmatter (`name: _practice-grammar-common`, `description` explaining it's
     a shared sub-skill loaded by `lesson-grammar-practice.md` and
     `scheduled-grammar-practice.md`, never directly triggered).
   - Shared awk-slice loading step only (source lines 81–83) — per boundary
     decision 7, do **not** include the entry-lookup-by-search logic or the
     Migration note; both move to the scheduled skill.
   - Parsing → Grammar topics: heading-role classification via `_heading-roles.md`
     (source lines 171–186, stopping before the Migration note at line 187),
     use-case extraction for the lesson-file H3 format only (source lines
     189–196, 206 — drop the extracted-file H2 variant at 197–204 and its
     "unconfirmed against a second lesson" note, both scope-only).
   - Parsing → Vocab pool base rules (source lines 208–227). Do not include the
     cross-file dedup-by-Japanese-form rule from Scope resolution (source line 85)
     or the `Vocabulary/*.md` fallback (source lines 229–242) — both are scope-only.
   - Parsing → Grammar point ID construction (source lines 244–248).
   - Exercise generation (source lines 252–287), with the weak-point-bias
     trailing sentence (decision 4) and the extracted-file Type-selection
     bullet (decision 5) both trimmed.
   - Interaction flow mechanics: progress indicator rule (source lines 316–320,
     minus the confused_with-merge-affects-total clause — scope-only, already
     covered in Metadata-driven exercise generation), batch-mode generic layout
     description (no lesson name — per boundary decision 3), grading-reply layout
     and display rules (source lines 374–393, fully generic already), interactive
     mode (source lines 395–426, fully generic), both-modes rules (source lines 428–432).
   - Grading rules in full (source lines 451–470).
   - Session-summary mechanics with generic placeholder header (per boundary decision 1).
   - Persistence and Calendar sync load-directive, parameterized by `scope`
     (per boundary decision 2; source lines 503–517).
   - Study Mode invocation hookup, relocated unchanged (source lines 436–447).
   - Never-touch list (per boundary decision 6; source lines 521–526).
   - Batch-loop mechanics: the full batch loop (generate exercises for current
     batch → present → collect answers/scores → between-batch gate → advance),
     parameterized by `num_batches` (source Workflow step 7, lines 129–160,
     including the MANDATORY between-batch-gate callout and the early-exit
     "stop"/"end" handling) — same code path for both triggers; lesson skill
     always passes `num_batches=1`. Include the "load grammar-state.json for
     weak_points" step (source Workflow step 5, line 120) here too, since both
     triggers do this identically at session start (scheduled skill has
     already read the file during scope resolution but the weak_points
     lookup-and-apply step is the same mechanic). Give this batch-loop
     section a clear, stable heading name (e.g. `## Batch-loop mechanics`) —
     both `practice-grammar-srs.md`'s Step 4 fix and `practice-grammar-study-mode.md`'s
     Step 4 fix need to reference it by section name, not by a numbered
     Workflow step that no longer exists as a single sequence.

2. **Create `.cowork/skills/lesson-grammar-practice.md`.**
   - Frontmatter matching the old file's style (adapted `name`/`description`).
     Per boundary decision 8, the `description` must positively require a
     lesson-code/filename shape and explicitly state it excludes
     date/scope-keyword phrasing.
   - Trigger section: lesson-code/filename matching only (source lines 17–23),
     excluding scope triggers. Do not copy source line 31 — optionally add a
     one-line note that this skill does not match scope-keyword phrasing
     (naming `scheduled-grammar-practice` for that case).
   - Workflow: resolve file via Trigger's code/filename match → call common
     file's awk-slice loading step → parse fresh via common file's
     Grammar-topics/heading-role classification (no pre-selected entries,
     no entry-lookup-by-search — per boundary decision 7) → common file's
     exercise generation, batch-loop (with `num_batches=1` fixed, no
     batch-split prompt — source line 128) → common file's session-summary
     mechanics with this skill's own footer text → common file's
     Persistence/Calendar-sync directive with `scope="lesson"`.
   - This skill's own concrete session header/example (source lines 352–370,
     the `UN4GL7` worked example) and session-summary footer text (source
     line 481 pattern) — per boundary decisions 1 and 3.
   - Study Mode: reference the common file's invocation hookup (no duplicate content).

3. **Create `.cowork/skills/scheduled-grammar-practice.md`.**
   - Frontmatter matching the old file's style (adapted `name`/`description`).
     Per boundary decision 8, the `description` must positively require an
     explicit scope keyword and explicitly state it excludes
     lesson-code/filename-shaped input.
   - Trigger section: scope triggers only (source lines 25–29). Do not copy
     source line 31 — optionally add a one-line note that this skill does
     not match lesson-code-shaped phrasing (naming `lesson-grammar-practice`
     for that case).
   - Scope resolution in full: TODAY flow, OVERDUE flow, Multi-lesson file
     loading (extracted-file flow 2a in full — source lines 72–78; 2b's
     awk-slice step delegates to the common file's routine, called once per
     `lesson_file`, but the entry-lookup-by-search logic and skip/warning
     rules (source line 84) and the Migration note (source line 187) live
     here in full — per boundary decision 7), Edge cases (source lines 35–106).
   - Vocabulary base fallback (source lines 229–242) and the mixed-session pool
     merge / cross-file dedup rule (source line 85, source line 242).
   - Use-case extraction extracted-file variant (source lines 197–204).
   - Metadata-driven exercise generation section in full (source lines 291–312).
   - Workflow: batch-split prompt (source Workflow step 6, lines 121–127) →
     call common file's parsing/exercise-generation/batch-loop → common file's
     session-summary mechanics with this skill's own footer text → common
     file's Persistence/Calendar-sync directive with `scope="TODAY"`/`"OVERDUE"`.
   - This skill's own Today/Overdue session header/footer format strings and
     the `K lessons = ...` / `M = ...` variable definitions (source lines
     328–350) — per boundary decisions 1 and 3.

4. **Update `.cowork/skills/practice-grammar-srs.md` and
   `.cowork/skills/practice-grammar-study-mode.md` cross-references.** Logic
   in both files is unchanged — only wording that names the file being
   deleted or a Workflow step that no longer exists as a single sequence:
   - `practice-grammar-srs.md:11` — `## Context required (passed by
     practice-grammar.md)` → `## Context required (passed by
     lesson-grammar-practice.md or scheduled-grammar-practice.md via
     _practice-grammar-common.md)`.
   - `practice-grammar-study-mode.md:6` (frontmatter description) —
     "Loaded on demand by practice-grammar.md on first Study Mode
     invocation." → "Loaded on demand by lesson-grammar-practice.md or
     scheduled-grammar-practice.md (via `_practice-grammar-common.md`'s
     Study Mode invocation hookup) on first Study Mode invocation."
   - `practice-grammar-study-mode.md:12` — same `## Context required`
     rewrite as the srs file above.
   - `practice-grammar-study-mode.md:19` — "as loaded once at Workflow step 5
     (session start)" → rewrite to reference the common file's batch-loop
     mechanics section by name (e.g. "as loaded once at session start, in
     `_practice-grammar-common.md`'s Batch-loop mechanics section") — this
     line wasn't flagged by the reviewer audit but is the same category of
     staleness as line 25 below and must be fixed in the same pass.
   - `practice-grammar-study-mode.md:25` — "(see Workflow step 7e in
     practice-grammar.md)" → rewrite to name the actual new location of the
     between-batch gate (e.g. "(see the between-batch gate in
     `_practice-grammar-common.md`'s Batch-loop mechanics section)") — not
     just a filename swap, since "Workflow step 7e" as a numbered reference
     no longer exists once batch-loop mechanics move into the common file's
     own section structure.
   - `practice-grammar-study-mode.md:106` — "Types 1–6 as defined in `##
     Exercise generation` in practice-grammar.md" → "Types 1–6 as defined in
     `## Exercise generation` in `_practice-grammar-common.md`".

5. **Verify the split before deleting anything.** Read all three new files
   plus the two updated sub-skill files back and confirm: no content was
   silently dropped against the line-range map above; the MANDATORY
   between-batch-gate callout is present and intact in the common file; the
   `confused_with` minimal-pair merge logic and its `Exercise N / T`
   total-computed-after-merge note are present only in the scheduled skill,
   not duplicated in common; the Never-touch list is present in the common
   file; the entry-lookup-by-search logic and Migration note are present
   only in the scheduled skill, not in the common file; the two skills'
   frontmatter `description` fields are mutually exclusive per boundary
   decision 8 (one requires lesson-code shape and excludes scope keywords,
   the other requires a scope keyword and excludes lesson-code shape); all
   five reference fixes from Step 4 are applied correctly in
   `practice-grammar-srs.md` and `practice-grammar-study-mode.md`.

6. **Move `.cowork/skills/practice-grammar.md` to the vault root as
   `practice-grammar.md`, and delete `.claude/commands/practice-grammar.md`**
   — only after Step 5 passes. *(Changed during implementation, by user
   instruction: the skill file is moved/kept as a reference copy rather than
   deleted outright — see the disposition note in the Approach section
   above. The command stub is still deleted outright, since it would be
   non-functional pointing at a relocated reference file.)*

7. **Create `.claude/commands/lesson-grammar-practice.md`** — slash command
   stub, same style as the deleted `.claude/commands/practice-grammar.md`
   (`Read .cowork/skills/lesson-grammar-practice.md and follow its
   instructions... Lesson file or number: $ARGUMENTS`).

8. **Create `.claude/commands/scheduled-grammar-practice.md`** — slash command
   stub (`Read .cowork/skills/scheduled-grammar-practice.md and follow its
   instructions... Scope (today/overdue): $ARGUMENTS`).

9. **Update `.cowork/instructions.md`.** Replace the single `practice-grammar`
   line in "Available skills" with two entries reflecting the split trigger
   phrases (lesson-code triggers → `lesson-grammar-practice`; TODAY/OVERDUE
   triggers → `scheduled-grammar-practice`). **Requires explicit user
   permission before editing** — this file is outside `.cowork/skills/` and
   is covered by the project rule "Never modify files in `.cowork/` without
   permission." Ask before making this edit even though the plan authorizes
   the overall split.

10. **Fix stale `practice-grammar` references in other vault files.** These
    were found by grepping the vault for the old filename/skill name and are
    outside this plan's originally declared scope, but will go stale the
    moment Step 6 deletes the old file:
    - `.claude/agents/planner.md:52` — the skill-catalog table row for
      `practice-grammar` (`| practice-grammar | .cowork/skills/practice-grammar.md
      | Interactive SM-2 grammar drill from a lesson file... |`). Replace with
      two rows, one per new skill, describing each one's actual scope.
      Highest priority of this group — planner reads this table to know what
      skills exist for future plans.
    - `.cowork/skills/_heading-roles.md:3` (frontmatter description) and
      `:8` — "Loaded by lesson-to-web/extract-grammar and practice-grammar" /
      "Both lesson-to-web/extract-grammar (file extraction) and
      practice-grammar (drill-topic parsing) load this file" → update both to
      say `_practice-grammar-common.md` (the file that actually loads
      `_heading-roles.md` post-split) rather than `practice-grammar`. Lines
      37, 45, 49, 50, 51 of the same file use "practice-grammar" as a
      descriptive label for the drilling behavior (not a load reference) —
      leave those as-is unless they become confusing without renaming; if
      renamed for clarity, keep the meaning (drill-topic parsing behavior)
      intact.
    - `.cowork/skills/lesson-to-web/extract-grammar.md:27` — "shared with
      practice-grammar" → "shared with `_practice-grammar-common.md`".
    - `.cowork/progress/README.md:4` — "written by `practice-grammar` and
      read by `repeat-grammar` (future skill)" → update the provenance note
      to name both new skills as writers (`lesson-grammar-practice` and
      `scheduled-grammar-practice`), since both now write to
      `grammar-state.json` via the shared Persistence directive.
    - `.cowork/skills/lesson-to-web/register-confusability-grammar.md:157` —
      lower-priority "future work" pointer mentioning `practice-grammar`;
      update the name if this file is touched anyway during this task, not
      worth a dedicated pass on its own.

11. **Smoke-check.** Confirm: `_practice-grammar-common.md` has frontmatter;
    both trigger skills reference it for shared logic rather than repeating
    it; the old file and old command stub no longer exist; the two new
    command stubs exist and point at the correct skill files; no file
    anywhere in `.cowork/` or `.claude/` references the deleted
    `practice-grammar.md` by name (grep check, re-run after Step 10's fixes
    to confirm they landed).

## Risks

- **Content drop during the split** — this is a three-way split of
  interleaved content (not a clean top-to-bottom cut), so the highest risk is
  silently losing a rule that lives in a boundary zone (Session summary,
  Persistence call, batch-layout example, weak-point-bias sentence,
  entry-lookup-vs-fresh-parsing split). Step 5 exists specifically to catch
  this before the irreversible deletion in Step 6.
- **Between-batch gate regression** — the MANDATORY between-batch-gate callout
  (source Workflow step 7e) was added in a prior split specifically to fix a
  context-loss bug where Claude auto-advanced batches. It must land intact in
  the common file's batch-loop mechanics, not be paraphrased or shortened.
- **Trigger disambiguation depends entirely on frontmatter wording quality**
  — unlike the old single file's sequential dispatch (line 31), the two new
  skills have no shared runtime to negotiate precedence at. If both
  descriptions are written loosely, ambiguous input like "practice this
  week's grammar" could match neither or both. Step 5's verification must
  actually read both descriptions side by side and confirm they're
  mutually exclusive, not just present.
- **Transitional window during implementation** — between Step 2 (creating
  `lesson-grammar-practice.md`) and Step 6 (deleting the old unified
  `practice-grammar.md`), both files simultaneously match lesson-code trigger
  phrases. This is expected and harmless as long as Step 6 runs before the
  user's next real practice session — implementation should not be left
  paused in this window across a session boundary.
- **Deletion is irreversible in intent** — Step 6 is a user-confirmed
  destructive action. *(Updated during implementation: only
  `.claude/commands/practice-grammar.md` is actually deleted now; the old
  skill file is moved to the vault root as a kept reference copy instead of
  deleted.)* Do not perform the command-stub deletion until Step 5's
  verification passes; git is the rollback mechanism if something is wrong
  after the fact, but the plan should not rely on that as the primary safety
  net.
- **`.cowork/instructions.md` edit needs a fresh permission ask** — this plan
  documents the intended change (Step 9) but does not itself constitute the
  permission required by the project rule; skill-implementer must ask again
  at that step.
- **Sub-skill reference fixes are easy to under-scope** — Step 4 fixes five
  specific lines across two files; a implementer who only searches for the
  literal string `practice-grammar.md` will miss line 19 of
  `practice-grammar-study-mode.md` ("Workflow step 5"), which names a
  Workflow step, not a filename, but is equally stale post-split.
- **Stale references beyond the two sub-skill files** — Step 10's five files
  were found by a single grep pass during plan review; if any other file
  references `practice-grammar` by name, Step 11's re-run grep is the
  backstop, but it should not be treated as guaranteed exhaustive on the
  first pass.
