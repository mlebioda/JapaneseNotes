# Practice Grammar — Gate 4: Prompt language complexity

## Goal
The exercise-generation rules shared by `lesson-grammar-practice` and
`scheduled-grammar-practice` (both loaded via
`.cowork/skills/_practice-grammar-common.md`) currently check three gates
before an exercise can be shown to the student — all three are about whether
the target grammar/answer leaks or is trivial. None of them check whether
the English/Polish *prompt wording itself* is disproportionately
sophisticated for the grammar point's JLPT level. A real N5 case surfaced
this: the target Japanese answer was appropriately simple, but the prompt
used native-level phrasing ("point out," "nature," "good qualities"),
mismatching student expectations. This plan adds a fourth gate that anchors
prompt complexity to the grammar point's level.

## Approach
Add **Gate 4** to the existing "Non-trivial exercise checklist — mandatory"
in `_practice-grammar-common.md`'s Exercise generation section, immediately
after Gate 3 (currently ends at line 316) and before the extracted-file
footnote (currently lines 318-322, which stays as the section's closing
note). Gates 1-3 are untouched — Gate 1 was just carefully reworded in a
prior session to fix an answer-leak bug and must not regress. The new gate
is a compact per-level complexity table plus one before/after example
(mirroring Gate 1's "banned template" anchoring technique), not a long
explanation. Level derivation is free: the lesson-code prefix already in
hand during exercise generation (e.g. `UN5GL9` → `N5`) is the same value
`extract-grammar` uses to set its `level:` frontmatter field for extracted
files (per `.cowork/skills/lesson-to-web/_conventions.md` and
`extract-grammar.md` step 7) — so no new file read, frontmatter parse, or
lookup is introduced. The gate is explicitly framed as a judgment call
(unlike Gate 1's mechanical string-presence test), since there is no
mechanical test for prompt sophistication.

## Steps

1. Edit `.cowork/skills/_practice-grammar-common.md`, frontmatter
   `description` (line 5): change "the 3 gates" → "the 4 gates".

2. Edit `.cowork/skills/_practice-grammar-common.md`, the checklist intro
   (lines 282-284): change "verify all three gates pass" → "verify all four
   gates pass" and "until it passes all three" → "until it passes all four".

3. Insert new Gate 4 in `.cowork/skills/_practice-grammar-common.md`,
   immediately after Gate 3 ends (after line 316) and before the
   extracted-file-topics footnote (currently starting line 318). Insert
   exactly this block (blank line before and after, matching the spacing
   convention already used between Gates 1/2/3):

   ```
   **Gate 4 — Prompt language complexity matches the grammar point's JLPT
   level.** Derive the level from the lesson-code prefix already in hand
   (e.g. `UN5GL9` → `N5`, `UN4GL7` → `N4`) — no extra file read needed, even
   for extracted-file topics (their `level` frontmatter is itself derived
   from the same lesson-code digit, never independently researched).

   | Level | Prompt complexity |
   |---|---|
   | N5 | Short, everyday-vocabulary sentences. No idioms, no abstract phrasing. |
   | N4 | Slightly richer but still plain, concrete language. |
   | N3 | Moderate complexity — some abstract phrasing okay. |
   | N2/N1 | Natural native-level prompts are fine. |

   Example (N5): ✗ "You're complimenting a coworker. Point out that his
   serious, hardworking nature is one of his good qualities." → ✓ "Tell your
   coworker: 'You're always serious about work — that's a good thing.'"

   Unlike Gate 1's mechanical string check, there's no mechanical test for
   prompt sophistication — this is a judgment call the table and example
   anchor but can't guarantee against.
   ```

4. Verify the extracted-file-topics footnote (the paragraph beginning
   "(Extracted-file topics unlock additional exercise-generation options...")
   still immediately follows Gate 4 and precedes the `---` section break, and
   that no other line numbers or cross-references elsewhere in the file
   (e.g. the "Non-trivial exercise checklist" self-reference) were left
   inconsistent.

## Risks
- Low risk — single file, single section, additive change (no gate logic
  removed or reworded). Gates 1-3 text must remain byte-for-byte unchanged.
- Must not introduce a new file read/frontmatter parse for level lookup —
  the whole point of the design is that it's a zero-cost string operation on
  data already parsed elsewhere in the pipeline.
- Does not touch `lesson-grammar-practice.md` or `scheduled-grammar-practice.md`
  — both already delegate exercise generation to the shared file.
