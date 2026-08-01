# Unify Structure Format Between Grammar Points and Vocabulary Files

## Goal

Eliminate the duplicated/divergent rule text between grammar-point files
(`grammar-index/grammar/*.md`) and vocabulary files
(`grammar-index/grammar/vocabulary/**/*.md`) for how their body content is structured. Today
`structure-grammar.md` owns a fully specified, enforced Structure 1 (flat) / Structure 2
(numbered use cases) template for grammar points, while `extract-grammar.md`'s "Vocabulary
file format" rules separately say to copy the lesson body "verbatim" and explicitly forbid
adding `## Structure` / `## Examples` sections — so vocabulary files with genuinely distinct
senses (e.g. `chikara-strength-effect-power-ability.md`, 3 senses) come out as whatever ad-hoc
shape the source lesson happened to use, while others accidentally hand-roll a Structure-2-like
shape (`au-match.md`, `yoru-stop-by.md`) without following a real template. This plan makes the
single/multi-part inference concept and template shapes one canonical, shared definition in
`_conventions.md`, referenced (not re-copied) by both `structure-grammar.md` (grammar points,
post-processing pass) and `extract-grammar.md` (vocabulary files, creation-time only).

## Approach

`_conventions.md` already states it is "the single source of truth for rules that must be
consistent across all lesson-to-web skills" — this plan holds it to that for Structure
formatting specifically, the same way it was already done for the Examples-bullet-format rule
earlier this session.

Resolved design decisions (from user interview this session):

1. **Vocabulary "multi-sense" shape reuses only the outer skeleton of Structure 2** — numbered
   `## N. Sense Name` sections, each with `### Structure` + `### Examples` — but the `Structure`
   content itself is free-form prose (part of speech, reading, transitivity, collocations, a
   short attachment note where relevant), never the grammar-point word-type conjugation table.
   That table's row scheme (Verb/い-adj/な-adj/Noun × Present/Negative/Past/Past-negative)
   assumes a *pattern* attaching to different word types, which breaks down for a standalone
   vocabulary word (a plain noun like 力 has no such rows to fill).
2. **Single-sense vocabulary files stay flat** — bare `## Structure` + `## Examples`, no forced
   numbering — mirroring the same single-vs-multi inference grammar points already use
   (Structure 1 vs Structure 2), rather than always numbering even trivial one-sense words.
3. **The inference + user confirmation happens once, at creation time, inside
   `extract-grammar.md` step 7b** — in the same interactive session where the vocabulary file
   is first written. `structure-grammar.md` is explicitly **not** extended to accept
   `vocabulary/` paths; vocabulary files continue to never enter a separate post-processing
   pass (register-confusability-grammar's explicit `vocabulary/` scope guard, and
   see-also-grammar's implicit exclusion — its algorithm only scans `## Sub-topics`/`## Entries`
   files, which vocabulary files never are — are both unaffected and unchanged by this plan).
4. **Migration of the 12 existing vocabulary files is out of scope for this plan** — see
   "Out of scope" below. This plan only changes the rules for future extractions.

The shared reference lives in `_conventions.md` as a new `## Structure format` section: it
states the general single-vs-multi inference concept once, then gives four templates under it
(grammar Structure 1, grammar Structure 2, vocabulary flat, vocabulary numbered), with an
explicit callout that section shape/nesting/inference is shared while `Structure` *content*
differs by file type. `structure-grammar.md` keeps its grammar-specific mechanics (ambiguity
prompt, section normalisation, the `→` vs bullet "Section distinction" note, handoff) but no
longer holds its own copy of the templates. `extract-grammar.md`'s vocabulary rules are
rewritten to run the same inference, propose it to the user, and populate whichever shared
template was confirmed — replacing "copy verbatim" with "reorganize into Structure/Examples
buckets."

## Steps

1. **Edit `.cowork/skills/lesson-to-web/_conventions.md`** — insert two new sections after the
   existing `## File structure rules (grammar point file)` section (which ends right before the
   `---` separator that currently precedes `## Examples content format`):

   a. **New `## File structure rules (vocabulary file)` section** — documents the two allowed
      section orders (flat: Frontmatter → `# <pattern>` → `## Structure` → `## Examples`;
      numbered: Frontmatter → `# <pattern>` → repeated `## N. <Sense Name>` blocks, each with
      `### Structure` + `### Examples`), and explicitly lists what vocabulary files never carry:
      `## Use Cases`, `## Notes`, `## Register`, `## Often confused with`, `## See also`, and the
      `function` / `register` / `confused_with` frontmatter fields — cross-referencing the
      grammar-point section and `register-confusability-grammar.md` / `see-also-grammar.md` for
      why (vocabulary files never enter the confusability graph).

   b. **New `## Structure format` section** — the canonical home for the inference concept and
      all four templates:
      - States the shared inference concept once: one unified thing → flat shape; two or more
        meaningfully distinct things → numbered `## N. <Name>` shape with per-section `Examples`
        that are never pooled across sections.
      - States the content-differs-by-type callout: grammar-point `Structure` content is a
        word-type conjugation table (full template below); vocabulary `Structure` content is
        free-form prose (part of speech, reading, transitivity, collocations, attachment note
        where relevant) — no forced conjugation table.
      - **Moves the existing Structure 1 template verbatim** from `structure-grammar.md` (its
        current `#### Structure 1 — Shared structure across word types` code block) into this
        section, labeled "Grammar point files — Structure 1."
      - **Moves the existing Structure 2 template verbatim** from `structure-grammar.md` (its
        current `#### Structure 2 — Distinct use cases` code block) into this section, labeled
        "Grammar point files — Structure 2."
      - **Adds a new "Vocabulary files — flat (single sense)" template**: `# <heading>` →
        `## Structure` (free-form) → `## Examples` (bulleted).
      - **Adds a new "Vocabulary files — numbered (2+ distinct senses)" template**: `# <heading>`
        → repeated `## N. <Sense Name>` → `### Structure` (free-form, sense-scoped) →
        `### Examples` (bulleted, sense-scoped, never pooled).
      - Closes with an "Applied by" note: `structure-grammar.md` Step 7 for grammar point files
        (post-processing pass, user-confirmed reformat), `extract-grammar.md` Step 7b for
        vocabulary files (creation-time only, user-confirmed before the file is written,
        never re-entered later by `structure-grammar.md`).

2. **Edit `_conventions.md` `## Examples content format` section** — extend the bullet list of
   "every shape an Examples section takes" to include the two new vocabulary shapes: `##
   Examples` (flat vocabulary files) and `### Examples` under `## N. <Sense Name>` (numbered
   vocabulary files) — replacing the current single vocabulary bullet, whose exact live wording
   is: "`### Examples` — inside vocabulary files (`grammar-index/grammar/vocabulary/**`). Applies
   only to the Examples section itself; other copied content (e.g. a `### Use cases` section)
   keeps whatever list/heading structure it already has in the source lesson." Remove the "other
   copied content ... keeps whatever list/heading structure it already has" caveat entirely — it
   becomes obsolete once step 4 below lands, since vocabulary bodies are reorganized into
   Structure/Examples buckets rather than copied verbatim going forward, and must not be left
   stale. Also update the closing "Applies whenever this section is written or rewritten ..."
   paragraph (which currently ends "... extract-grammar on file creation (both grammar point
   files and vocabulary files), and structure-grammar on any reformat into Structure 1 or
   Structure 2") to describe the vocabulary half as governed by the new Step 7b flat/numbered
   inference, cross-referencing the new `## Structure format` section, instead of implying a
   flat "copy on creation" treatment.

3. **Edit `.cowork/skills/lesson-to-web/structure-grammar.md`** — replace the current `####
   Structure 1 — Shared structure across word types` and `#### Structure 2 — Distinct use cases`
   code blocks (and their template markdown) with a short reference to `_conventions.md`'s new
   `## Structure format` section, retaining every piece of grammar-specific process guidance that
   is not itself a copy of the template:
   - Keep the "Inferring which structure to use" one-liners and the ambiguity prompt as-is.
   - Keep "Section order follows `_conventions.md`..." paragraph.
   - Keep "Omit word-type sections and tense rows..." paragraph.
   - Keep the "Section distinction" paragraph (`→` inline examples vs bulleted `## Examples`).
   - Keep the Structure-2-specific paragraph about numbered `##` headers, per-use-case
     `### Examples` scoping, and repeating shared `### Structure` content per use case rather than
     hoisting it out.
   - Add one clarifying line: vocabulary files are out of scope for this skill — they are
     structured at creation time by `extract-grammar.md` Step 7b using the same shared inference
     concept from `_conventions.md`, and never enter this post-processing pass. This is a
     documentation cross-reference only — `structure-grammar.md`'s container-file-detection logic
     and file-path handling are unchanged; it is not being extended to accept `vocabulary/` paths.

4. **Edit `.cowork/skills/lesson-to-web/extract-grammar.md`** — rewrite the "Vocabulary file
   format" subsection (currently under step 7, referenced elsewhere in the file as "step 7b"):
   - Remove the line "Do not add `## Structure`, `## Meaning`, `## Examples`, or `## Notes`
     sections — only reformat an `### Examples` section the source lesson already has."
   - Add **Step 7b-i — infer single sense vs 2+ distinct senses**: read the heading's collected
     body (from step 4) and judge whether it describes one unified sense, or two-plus genuinely
     different senses (not just different grammatical forms of the same meaning — the same test
     `structure-grammar.md` applies to grammar use cases, scoped here to a vocabulary word's
     senses). Existing source structure (a `### Use cases` or `### Meaning` list with 2+ distinct
     entries) is a strong signal but not authoritative. Propose the shape to the user and wait for
     confirmation before writing the file, using a prompt in the same style as
     `structure-grammar.md`'s ambiguity prompt:
     ```
     Vocabulary word: <heading text> (<slug>)
     Content summary: <brief description of what senses/uses appear in the source body>

     Options:
       1. Single sense — flat ## Structure / ## Examples
       2. <N> distinct senses — numbered ## 1..<N> sections: <proposed sense names>
       3. Skip structuring — write flat shape anyway (fallback for genuinely unclear content)

     Which should I use?
     ```
     A user override of sense count or names is used verbatim in 7b-ii.
   - Add **Step 7b-ii — populate the file** per the flat or numbered vocabulary template in
     `_conventions.md`'s `## Structure format` section, chosen per the Step 7b-i inference —
     reference the template by name only, do **not** restate its markdown inline. This matches
     Step 3's treatment of `structure-grammar.md`: the templates live in exactly one place
     (`_conventions.md`), and both consuming skills point to them rather than each holding a copy.
     The only markdown extract-grammar.md keeps inline for vocabulary files is the frontmatter
     block (`lesson`/`pattern`/`topic_slug`/`level`/`proofread`), since that part is unique to
     this skill's file-creation step and isn't part of the shared Structure format templates.
   - Rewrite "Rules for vocabulary file body" to reflect reorganization instead of verbatim copy:
     - Keep unchanged: strip `#w `/`#wc `/`#wp ` tag prefixes.
     - New: body content is sorted into the `Structure` (free-form prose: part of speech,
       reading, transitivity, collocations, attachment note, any source `### Structure` line) and
       `Examples` (bulleted, one sentence per bullet, per `_conventions.md` "## Examples content
       format") buckets per confirmed sense — it is no longer copied as one verbatim block.
     - Keep unchanged: do not add `## Use Cases`, `## Notes`, `## Register`, or `## Often confused
       with` (cross-reference `_conventions.md` "File structure rules (vocabulary file)").
     - Keep unchanged: no topic-index entry (step 9) for vocabulary files; target path and subdir
       creation rules unchanged.

5. **No changes to `.cowork/skills/_heading-roles.md`** — heading-role classification
   (scaffolding/container/point) is unaffected; this plan changes how a classified "point" body
   is reorganized into vocabulary-file sections, a step downstream of role classification.

6. **No changes to `register-confusability-grammar.md` or `see-also-grammar.md`** — both already
   exclude vocabulary files, but for different reasons, and this plan doesn't change either:
   - `register-confusability-grammar.md` has an explicit "Container / vocabulary scope guard"
     section that skips `vocabulary/` paths outright.
   - `see-also-grammar.md` has no explicit vocabulary guard; it excludes vocabulary files only
     implicitly, because its algorithm only scans files that contain a `## Sub-topics` section
     (container files) or that appear in a topic file's `## Entries` list — vocabulary files
     never have either, so they're never visited. This is confirmed correct behavior, just not
     an explicit guard the way register-confusability-grammar.md has one.
   No edit to either file is expected; confirm during implementation review that this remains
   true after the Step 4 rewrite of extract-grammar.md's vocabulary handling.

7. **No new skill and no `.claude/commands/` stub** — this plan only edits three existing skill
   files. The existing "extract grammar from `<lesson>`" and "structure grammar `<slug>`"
   triggers are unchanged.

## Out of scope

- **Migration of the 12 existing vocabulary files** (`grammar-index/grammar/vocabulary/**/*.md`)
  to the new flat/numbered shape is deliberately **not** part of this plan. The rule changes
  above apply to future extractions only. Existing files (including the ones with accidental
  Structure-2-like shapes, `au-match.md` and `yoru-stop-by.md`, and the ones needing a full
  reshape, e.g. `chikara-strength-effect-power-ability.md`, `hakkiri.md`,
  `bun-portion-range.md`) are left as-is. Migration is a separate follow-up the user will
  trigger later (e.g. re-running extract-grammar's vocabulary path, or a dedicated migration
  pass) — not scheduled or stubbed here.

## Risks

- **Stale existing files vs. new rule.** Once this plan lands, newly created vocabulary files
  will look structurally different from all 12 existing ones until a future migration. Anything
  that assumes uniform vocabulary-file structure (none currently known, but worth checking during
  implementation) must tolerate both shapes until migration happens.
- **Re-introducing duplication.** `structure-grammar.md` and `extract-grammar.md` must actually
  reference `_conventions.md`'s templates rather than re-copy them — the whole point of this plan
  is to avoid recreating the same divergence. This applies equally to Step 3
  (`structure-grammar.md`'s Structure 1/2 references) and Step 4
  (`extract-grammar.md`'s Step 7b-ii vocabulary flat/numbered references) — neither file should
  contain literal Structure-format template markdown after this plan lands, only pointers to
  `_conventions.md`'s `## Structure format` section. Implementation should grep both files for
  leftover template markdown (e.g. stray `### Verb` / `Present:` / `Negative:` rows, or a second
  copy of the vocabulary flat/numbered skeletons) after the edit and confirm none remains.
- **Scope discipline.** `structure-grammar.md` must not be extended to accept `vocabulary/` paths
  (explicit user decision) — this is deliberate, not an oversight; a reviewer pass should confirm
  this constraint held.
- **Never touch:** `<!--ID: -->` lines, `TARGET DECK` lines, and any file under
  `grammar-index/grammar/vocabulary/` or `JPLessons/` — this plan's steps only touch
  `_conventions.md`, `structure-grammar.md`, and `extract-grammar.md` under `.cowork/skills/`.
