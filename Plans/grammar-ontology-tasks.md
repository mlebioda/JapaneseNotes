# Grammar-index ontology upgrade — Tasks

Plan: `Plans/grammar-ontology-plan.md`

## Phase A — frontmatter mirrors + strict test: format

- [x] `_conventions.md`: document `register` and `confused_with` frontmatter fields (optional; owned by register-confusability-grammar; `register` overwrite-on-rerun, `confused_with` append-only dedup-checked array mirroring the section)
- [x] `_conventions.md`: add scoped carve-out to the "No skill modifies frontmatter after creation" rule — `register`/`confused_with` writable only by register-confusability-grammar Steps 8–9. Must amend the exact opening clause "Frontmatter fields other than `proofread`" in the Never-touch bullet (line 91), and redefine "after file creation" as "after the creating skill's run completes" (one run-scoped definition covering `topic_slug`/`function`/`register`/`confused_with`)
- [x] `_conventions.md`: mandate canonical YAML serialization — inline JSON-compatible arrays matching `topic_slug` style (`confused_with: ["slug-a", "slug-b"]`, `function: ["purpose"]`; grammar-audit.py parses via `json.loads`); `register` bare scalar; insertion position for new fields: after `level`, before `proofread`; template field order `lesson`, `pattern`, `topic_slug`, `function`, `level`, `proofread` (, `partial`)
- [x] `_conventions.md`: add canonical "Often confused with" line format with mandatory `— test:` prefix (single source of truth)
- [x] `_conventions.md`: widen the Step-9 proofread-guard scoped exception to also cover the matched file's `confused_with` frontmatter append (create-if-absent), still anchor-bounded, never a general bypass
- [x] `register-confusability-grammar.md` Step 8: mirror the Register section value into `register:` frontmatter (`neutral | polite | tiered | unknown`), overwrite on re-run
- [x] `register-confusability-grammar.md` Step 9: switch forward and reverse line templates to the strict `— test:` format, referencing `_conventions.md`
- [x] `register-confusability-grammar.md` Step 9: append matched slug to current file's `confused_with:` array and current slug to matched file's array (create field if absent; touch only that field; permitted under widened proofread exception)
- [x] `register-confusability-grammar.md` Step 9: dedup checks both representations (array + section links) with asymmetric repair — section-without-array: mechanically append slug to `confused_with` (current-run pairs only; covered by widened proofread exception); array-without-section: skip with `[MIRROR-GAP]` log, deferred to Idea 6 audit (would require composing a fresh test: question); both present: skip

## Phase B — controlled-vocabulary function tag

- [x] `_conventions.md`: add `function` controlled-vocabulary section — 20 starter values, array of 0–2 per file, empty allowed, hard rule: extend this list (with user confirmation) before using any new value; `function` joins protected after-creation fields
- [x] `extract-grammar.md` step 7: add `function: []` to the grammar point file frontmatter template only (not container, not vocabulary templates)
- [x] `extract-grammar.md` step 9d: assign `function` values from the `_conventions.md` list when patching `topic_slug`; propose new values to the user before using them
- [x] `extract-grammar.md` step 9a: graceful-empty note — empty `grammar-index/` (glob matches nothing) means empty taxonomy; proceed, creating topic files and regenerating index.md per existing 9b/9c/9e rules
- [x] `register-confusability-grammar.md` Step 9 candidate pool: **union** of `function` intersection and `topic_slug` intersection; full-scan fallback when both empty; state that zero candidates on a sparse index is expected (no section written, no error)
- [x] `register-confusability-grammar.md` backfill stub template: add `function: []`
- [x] `extract-grammar.md` step 6 Overwrite path: preserve existing `register:`/`confused_with:` frontmatter and `## Register`/`## Often confused with` sections when overwriting a file that has them (notably a `partial: true` stub being resolved by full extraction) — prevents dangling reverse links
- [x] `structure-grammar.md`: one-line note — preserve existing `## Register` and `## Often confused with` sections (in their `_conventions.md` position) when reformatting into Structure 1/2 on a re-run

## Wrap-up

- [x] `.cowork/instructions.md` lesson-to-web catalog: verify and fix staleness around register-confusability-grammar's entry and update-grammar's step count/labels — **ask the user for explicit permission before editing this file**
- [x] `.claude/commands/lesson-to-web/register-confusability-grammar.md` stub: fix "run Step 4 Register research" → reference Steps 8–9
- [x] Self-review: confirm carve-outs stayed field- and owner-scoped, no wording generalizes the frontmatter or proofread exceptions; YAML-validity spot-check of edited frontmatter templates/examples (`python3` yaml parse + `json.loads` on inline arrays)
- [x] No new `.claude/commands/` stubs needed (no new skills — edits only; the stub change above is a fix to an existing file)
