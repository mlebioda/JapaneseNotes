# Extract-Grammar Cross-Reference & Content-Gap Fixes

## Goal
The `extract-grammar.md` rewrite (flat 846-line file → table-driven format with 6a–6e/6c-ii sub-steps) renumbered its own steps but left 15 stale step-number references scattered across 8 other skill files that point at the old numbering. It also introduced 4 content gaps in the two files split out of the rewrite (`_grammar-templates.md` and `extract-grammar.md` itself). This plan fixes both classes of issue so every cross-reference in the pipeline points at a step that actually exists under that name, and no template/definition regressed relative to the pre-rewrite file.

## Approach
This is a verified, mechanical fix — every reference below was checked against the current `extract-grammar.md` content (not just the reviewer's line numbers, which had drifted slightly in a couple of files) before being included. All fixes are string replacements or small text insertions; no logic changes. A grep sweep (`grep -rniE "step [0-9]+[a-z]{0,2}"` across the affected files) was already run as part of planning and surfaced one additional stale reference beyond the reviewer's 14 — `register-confusability-grammar.md:69` — which is folded into the same file's task since it's adjacent to the already-flagged line 63. `documentation` and `scribe` are explicitly out of scope for this plan — do not call either.

## Steps

### Critical — stale step-number cross-references (verified against current extract-grammar.md numbering: Step 5 = Confirm classification, Step 6a = Compute slug, Step 6c = Create file, Step 6c-ii = Vocabulary leaf files, Step 6d = POS container append, Step 6e = Insert wikilink, Step 7 = Classify into topics, Step 8 = Patch topic_slug/function, Step 11 = Offer chain)

1. `.cowork/skills/_heading-roles.md:51` — "the step 4b table" → "the Step 5 table"
2. `.cowork/skills/practice-grammar/_practice-grammar-common.md:114` — "extract-grammar step 8 guarantees" → "extract-grammar step 6e guarantees"
3. `.cowork/skills/lesson-to-web/_conventions.md:44` — "extract-grammar's grammar point template (step 7)" → "(step 6c)"; "extract-grammar step 9d" → "extract-grammar step 8" (same line, two edits)
4. `.cowork/skills/lesson-to-web/_conventions.md:46` — "extract-grammar step 9d patches `topic_slug`, created as `""` in step 7" → "extract-grammar step 8 patches `topic_slug`, created as `""` in step 6c"
5. `.cowork/skills/lesson-to-web/_conventions.md:70` — "set by extract-grammar during its own run (step 9d, ...)" → "(step 8, ...)"
6. `.cowork/skills/lesson-to-web/_conventions.md:270` — "`extract-grammar.md` Step 7b" → "`extract-grammar.md` Step 6c-ii"
7. `.cowork/skills/lesson-to-web/_conventions.md:297` — "via the Step 7b flat/numbered" → "via the Step 6c-ii flat/numbered"
8. `.cowork/skills/lesson-to-web/_conventions.md:344` — "extract-grammar step 8 which inserts" → "extract-grammar step 6e which inserts"
9. `.cowork/skills/lesson-to-web/_conventions.md:345` — "beyond the extract-grammar step 8 wikilink insertion" → "beyond the extract-grammar step 6e wikilink insertion"
10. `.cowork/skills/lesson-to-web/see-also-grammar.md:43` — "re-run extract-grammar classification (step 9)" → "(step 7)"
11. `.cowork/skills/lesson-to-web/structure-grammar.md:107` — "`extract-grammar.md` Step 7b" → "`extract-grammar.md` Step 6c-ii"
12. `.cowork/skills/lesson-to-web/register-confusability-grammar.md:63` — "Reuse `extract-grammar` Step 4b's classification workflow" → "Step 5's classification workflow"
13. `.cowork/skills/lesson-to-web/register-confusability-grammar.md:69` — "compute the slug using `extract-grammar`'s Step 5 algorithm exactly" → "Step 6a algorithm exactly" (found during the grep-sweep task, not in the original reviewer list — slug computation is Step 6a, not Step 5, which is classification confirmation)
14. `.cowork/skills/lesson-to-web/update-grammar.md:16` — "called automatically from extract-grammar step 10" → "step 11"
15. `.cowork/skills/lesson-to-web/preprocess-grammar.md:16` — "called automatically from extract-grammar step 10" → "step 11"

Do NOT touch `register-confusability-grammar.md:58` ("step 2") or `:62` ("steps 3–4") — those are still correct under the new numbering (Step 2 = Read pre-Summary slice, Steps 3–4 = Locate sections / Collect headings).

16. Final grep sweep: run `grep -rniE "step [0-9]+[a-z]{0,2}" .cowork/skills/` (or scoped to the files above) after all edits land, to confirm no other stale `extract-grammar` + "step N" reference was missed and that every remaining "Step N" mention in these files is either (a) now correct against extract-grammar's new numbering, or (b) a skill's reference to its own internal step numbering (e.g. preprocess-grammar's own Step 1–4, structure-grammar's own Step 7, register-confusability-grammar's own Step 8–9, see-also-grammar's own Step 10/10b/11 — these are unrelated to extract-grammar's numbering and correct as-is per `update-grammar.md`'s pipeline table).

### Moderate — content gaps

17. `.cowork/skills/lesson-to-web/_grammar-templates.md` — grammar-point template's `## Examples` placeholder (currently `[One bullet per sentence — omit if section would stay empty per rules; otherwise leave empty]`) is self-contradictory. Rewrite to match `extract-grammar.md` Step 6c's Field rules table ("always present, empty if none"), e.g.: `[One bullet per sentence — section header is always present; leave the body empty if the lesson has no examples]`.

18. `.cowork/skills/lesson-to-web/extract-grammar.md` Step 6d — restore a literal example prompt block for the placement-proposal sub-step (item 3: "Propose placement per new entry..."), in the same literal style as Step 5's and Step 6c-ii's example blocks. Model:
    ```
    Vocabulary POS entry: <label> (<slug>)
    grammar-index/grammar/vocabulary-<pos>.md — existing themes: <theme list, or "none yet">
    Proposed placement: 1. Join theme "<theme>"  2. New theme "<name>"  3. Stay ungrouped
    Confirm or override (theme name / ungrouped):
    ```

19. `.cowork/skills/lesson-to-web/_grammar-templates.md` — "Topic file" template section dropped 3 authoring rules present in the pre-rewrite file. Add back near the Topic file template:
    - Title: human-readable derivation of the filename.
    - Description: one sentence explaining when to look here.
    - "See also": 1–2 full absolute URL links to existing related topics if obvious; otherwise omit.

20. `.cowork/skills/lesson-to-web/extract-grammar.md` Step 5 — add back the `skip` classification's prose definition (currently only appears as a routing-table destination row). Add alongside the routing table: "**skip** — do not extract. Used for pure vocabulary lists or headings that are not grammar patterns."

## Explicitly out of scope
- Step 5's dropped "indent each candidate under its parent" prose (cosmetic — survives implicitly via the example table's indentation).
- Step 6d's dropped maintainer anti-regression note ("do not 'fix' this into matching Step 9's gate").
- Step 6e's literal Python regex snippet → prose (functionally equivalent).
- Step 7's dropped "if more than 3 topics fit, pick the strongest 3" tie-break line.
- Calling `documentation` (vault diagram regen) — explicitly held off per user instruction.
- Calling `scribe` — not part of this plan; offered as a next-agent option only, per standard planner flow.

## Risks
- All edits are text replacements inside prose/instructions — no plugin export data, `TARGET DECK`, `# Summary`, or `<!--ID:-->` lines are touched; none of the 10 files are lesson files.
- `_conventions.md` line 44/46 each need two separate substring replacements on the same line — must apply both, not just one, or the line stays inconsistent.
- The Step 6d prompt-block restoration (#18) is a new addition, not a strict revert — word it to match Step 5/6c-ii's existing style so the three blocks stay visually consistent for future maintainers.
