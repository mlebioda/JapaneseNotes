# Extract-Grammar Cross-Reference & Content-Gap Fixes — Tasks

## Critical — stale step-number cross-references
- [x] `.cowork/skills/_heading-roles.md:51` — "step 4b table" → "Step 5 table"
- [x] `.cowork/skills/practice-grammar/_practice-grammar-common.md:114` — "extract-grammar step 8" → "extract-grammar step 6e"
- [x] `.cowork/skills/lesson-to-web/_conventions.md:44` — "(step 7)" → "(step 6c)" AND "step 9d" → "step 8" (both on this line)
- [x] `.cowork/skills/lesson-to-web/_conventions.md:46` — "step 9d" → "step 8" AND "in step 7)" → "in step 6c)" (both on this line)
- [x] `.cowork/skills/lesson-to-web/_conventions.md:70` — "step 9d" → "step 8"
- [x] `.cowork/skills/lesson-to-web/_conventions.md:270` — "Step 7b" → "Step 6c-ii"
- [x] `.cowork/skills/lesson-to-web/_conventions.md:297` — "Step 7b" → "Step 6c-ii"
- [x] `.cowork/skills/lesson-to-web/_conventions.md:344` — "extract-grammar step 8" → "extract-grammar step 6e"
- [x] `.cowork/skills/lesson-to-web/_conventions.md:345` — "extract-grammar step 8" → "extract-grammar step 6e"
- [x] `.cowork/skills/lesson-to-web/see-also-grammar.md:43` — "(step 9)" → "(step 7)"
- [x] `.cowork/skills/lesson-to-web/structure-grammar.md:107` — "Step 7b" → "Step 6c-ii"
- [x] `.cowork/skills/lesson-to-web/register-confusability-grammar.md:63` — "Step 4b's" → "Step 5's"
- [x] `.cowork/skills/lesson-to-web/register-confusability-grammar.md:69` — "Step 5 algorithm" → "Step 6a algorithm" (grep-sweep finding, not in original reviewer list)
- [x] `.cowork/skills/lesson-to-web/update-grammar.md:16` — "step 10" → "step 11"
- [x] `.cowork/skills/lesson-to-web/preprocess-grammar.md:16` — "step 10" → "step 11"
- [x] Do NOT touch `register-confusability-grammar.md:58` (step 2) or `:62` (steps 3–4) — unchanged and correct
- [x] Run final grep sweep: `grep -rniE "step [0-9]+[a-z]{0,2}" .cowork/skills/` — confirm no other stale `extract-grammar` step reference remains, and that remaining hits are each skill's own internal step numbering (unrelated to extract-grammar)

## Moderate — content gaps
- [x] `.cowork/skills/lesson-to-web/_grammar-templates.md` — rewrite `## Examples` placeholder in the grammar-point template so it isn't self-contradictory (header always present; body empty only if no examples)
- [x] `.cowork/skills/lesson-to-web/extract-grammar.md` Step 6d — restore a literal example prompt block for the placement-proposal sub-step, matching Step 5's/6c-ii's style
- [x] `.cowork/skills/lesson-to-web/_grammar-templates.md` — add back the 3 dropped Topic file authoring rules (Title derivation, Description sentence, "See also" link rule)
- [x] `.cowork/skills/lesson-to-web/extract-grammar.md` Step 5 — add back the `skip` classification's prose definition alongside the routing table

## Out of scope (do not do)
- [x] Do not restore Step 5's "indent each candidate" prose
- [x] Do not restore Step 6d's maintainer anti-regression note
- [x] Do not restore Step 6e's literal Python regex snippet
- [x] Do not restore Step 7's ">3 topics, pick strongest 3" tie-break line
- [x] Do not call `documentation` (vault diagram regen)
- [x] Do not call `scribe` as part of this plan's execution
