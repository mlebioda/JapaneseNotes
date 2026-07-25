# Grammar-index ontology upgrade (frontmatter mirrors, test: format, function tag)

Source: `Plans/lesson-to-web-idea.md` (Ideas 1, 2, 3). Ideas 4–6 are dropped/deferred — see "Out of scope / deferred" below.

## Goal

Make grammar-index files machine-readable at the relation level so future exercise generation (practice-grammar consumption work, planned separately in `Plans/practice-grammar-ideas.md`) can reason over confusability, register, and semantic function from frontmatter instead of re-deriving them from prose. The `grammar-index/` corpus was wiped by the user on 2026-07-25 (only the empty `grammar/vocabulary/` scaffold remains), so these format changes must land **now, before the N4 lesson backfill**: every file regenerated through the pipeline gets the structured form on first write, and no migration pass will ever be needed.

## Approach

Two phases, both pure skill/convention edits — no content pass exists anymore, because there is no content.

- **Phase A (Ideas 1+3):** `register-confusability-grammar` Steps 8–9 write machine-readable frontmatter mirrors (`register:`, `confused_with:`) alongside the human-readable sections, and the "Often confused with" line format gets a strict `— test:` prefix so the distinguishing question is extractable without NLP. `_conventions.md` gets a scoped carve-out of the "no skill modifies frontmatter after creation" rule for these two fields, owned by register-confusability-grammar, and the existing Step-9 proofread exception widens to cover the matched file's `confused_with` append.
- **Phase B (Idea 2):** a controlled-vocabulary `function:` tag (purpose, cause-reason, hearsay-appearance, …) assigned by extract-grammar at classification time, documented as a single source of truth in `_conventions.md`, and consumed immediately by register-confusability-grammar Step 9 as the primary confusability prefilter (function intersection beats topic_slug intersection).

Empty-index consequence, verified against `extract-grammar.md`: topic-file recreation works from zero — step 9c creates new topic files from its template when no existing topic fits, and step 9e regenerates `index.md` whenever a topic file is created. Only step 9a's `ls grammar-index/*.md` needs a one-line graceful-empty note (the glob errors on an empty directory). Step 9 of register-confusability-grammar will legitimately find zero confusability candidates for a while; the skill already treats an absent `## Often confused with` as expected, and this plan keeps both the function-intersection pool and the full-scan fallback explicitly zero-candidate-safe.

## Steps

### Phase A — frontmatter mirrors + strict test: format

1. **`.cowork/skills/lesson-to-web/_conventions.md` — frontmatter conventions section.** Document three new optional fields:
   - `register` — one of `neutral | polite | tiered | unknown`; owned by register-confusability-grammar Step 8; overwritten (not appended) on re-run, mirroring the section overwrite rule.
   - `confused_with` — YAML array of grammar slugs; owned by register-confusability-grammar Step 9; append-only, dedup-checked, always mirrors the `## Often confused with` section links.
   - `function` — documented here in Phase A for completeness but populated per Phase B (see step 6).
   Amend the "No skill modifies `lesson`, `pattern`, `topic_slug`, or `level` after file creation" rule with a scoped carve-out: `register` and `confused_with` may be written/updated after creation, but **only** by register-confusability-grammar Steps 8–9, and only in the ways described above. No other skill and no other field. Two precision requirements for the implementer:
   - The operative contradiction is the **opening clause of the "Never touch" bullet** — "Frontmatter fields other than `proofread`" (`_conventions.md` line 91) — which forbids *all* other fields, not just the enumerated four. That exact phrase must be amended, not just the enumerated-field sentence.
   - Redefine "after file creation" as **"after the creating skill's run completes"** — extract-grammar's own step 9d already patches `topic_slug` after creation (created as `""` in step 7, patched in 9d), and `function` inherits the same pattern. One run-scoped definition covers `topic_slug`/`function`/`register`/`confused_with` consistently instead of accumulating parentheticals.
   Also mandate canonical YAML serialization for the new fields:
   - Arrays use inline JSON-compatible style matching `topic_slug`'s existing convention: `confused_with: ["slug-a", "slug-b"]`, `function: ["purpose"]` (`.claude/scripts/grammar-audit.py` parses `topic_slug` via `json.loads`, so inline JSON-compatible style is load-bearing). `register` is a bare scalar.
   - Insertion position when creating `register:`/`confused_with:` in an existing frontmatter block: **insert after `level`, before `proofread`**. In creation templates the field order is `lesson`, `pattern`, `topic_slug`, `function`, `level`, `proofread` (, `partial`). Deterministic placement so different sessions produce identical layouts.
2. **`_conventions.md` — canonical "Often confused with" line format.** Add the strict format as the single source of truth:
   ```
   - [Label](/JapaneseNotes/grammar-index/grammar/<slug>) — test: <one-line question that picks between the two patterns>
   ```
   The `test:` prefix is mandatory; the question must be answerable to choose between exactly these two patterns (it is the future wrong-answer feedback line for discrimination exercises).
3. **`_conventions.md` — proofread guard scoped exception.** Extend the existing Step-9 exception paragraph: the bounded write into a matched `proofread: true` file now covers both the `## Often confused with` section line **and** the corresponding append to that file's `confused_with` frontmatter array (creating the field if absent). Still never a general bypass; still limited to Step 9 backlink targets.
4. **`.cowork/skills/lesson-to-web/register-confusability-grammar.md` — Step 8.** After writing/overwriting the `## Register` section, mirror the register value into `register:` frontmatter (`neutral`, `polite` for "polite-context typical", `tiered`, `unknown` for the insufficient-source case). Overwrite on re-run.
5. **`register-confusability-grammar.md` — Step 9.** Three edits:
   - Replace both line templates (forward line in the current file, reverse line in the matched file) with the strict `— test:` format from step 2, referencing `_conventions.md` as the source of truth.
   - After adding a forward line, append the matched slug to the current file's `confused_with:` array (create the field if absent). After the reverse-line insert into the matched file, append the current file's slug to **that** file's `confused_with:` array — permitted under the widened proofread exception (step 3). Frontmatter edit mechanics: touch only the `confused_with` line/array, never reorder or rewrite any other frontmatter field.
   - Dedup rule now checks both representations, with a deliberately asymmetric repair (decision: option (b), the safe cut):
     - Section link present, array entry missing → **repair mechanically** (append the slug to `confused_with`). This is a pure copy, no content generation. Applies only to pairs matched in the current run — this is not a global audit. A repair write into a `proofread: true` matched file is covered by the widened Step-9 exception (step 3 above).
     - Array entry present, section link missing → **skip with log** (`[MIRROR-GAP] <slug>: confused_with entry has no section line — left for consistency audit`). Repairing this direction would require composing a fresh `— test:` question (content generation, potentially inside a proofread file) — explicitly deferred to the parked Idea 6 audit.
     - Both present → skip as fully linked (current behavior).

### Phase B — controlled-vocabulary function tag

6. **`_conventions.md` — `function` controlled vocabulary.** New section holding the single-source-of-truth value list. Starter vocabulary (from the idea file): purpose, cause-reason, permission, prohibition, obligation, desire, intention, hearsay-appearance, conditional, temporal, comparison, existence-location, means-method, direction-destination, quantity-counting, request, giving-receiving, potential, passive-causative, formality. Rules: `function` is a YAML array, 0–2 values per file, empty allowed when nothing fits; skills never invent values — extending the list means editing this section first, with user confirmation. `function` joins the protected after-creation fields (same status as `topic_slug`: set by extract-grammar during its own run, immutable afterwards).
7. **`.cowork/skills/lesson-to-web/extract-grammar.md` — step 7 templates.** Add `function: []` to the grammar point file frontmatter template only (not container files, not vocabulary files — function describes a pattern's semantic role; containers and vocab files don't participate in the confusability graph).
8. **`extract-grammar.md` — step 9d.** When patching `topic_slug`, also assign `function` values from the `_conventions.md` controlled list (0–2 values, empty allowed). If a genuinely new function value seems needed, propose adding it to `_conventions.md` and wait for user confirmation before using it.
9. **`extract-grammar.md` — step 9a graceful-empty.** One-line adjustment: if `grammar-index/` contains no topic files (fresh/wiped index — the `ls` glob matches nothing), treat the taxonomy as empty and proceed; every classification then creates new topic files per the existing 9b/9c rules, and 9e regenerates `index.md` from scratch.
10. **`register-confusability-grammar.md` — Step 9 candidate pool.** Redefine the prefilter as a **union** (decision per review: better recall at negligible cost on an index this size): pool = pattern files whose `function` array intersects the current file's `function` array **∪** files whose `topic_slug` array intersects the current file's `topic_slug` array. If both arrays on the current file are empty (or the union pool is empty), keep the existing full-scan fallback. State explicitly that zero candidates after all tiers is the expected outcome on a sparse/freshly-rebuilt index — leave `## Often confused with` absent, no error.
11. **`register-confusability-grammar.md` — backfill-mode stub template.** Add `function: []` to the minimal `partial: true` stub frontmatter so stubs match the extract-grammar template shape.
12. **`extract-grammar.md` — step 6 Overwrite path preservation.** When the Overwrite option is chosen for an existing file that carries `register:`/`confused_with:` frontmatter or `## Register`/`## Often confused with` sections (the typical case: a later full extraction pass resolving a `partial: true` stub), preserve those fields and sections when recreating the file from the step-7 template. Without this, overwriting a stub silently wipes the mirror while other files still hold reverse links to its slug — a dangling half-relation.
13. **`.cowork/skills/lesson-to-web/structure-grammar.md` — re-run section preservation.** One-line note: when reformatting a file into Structure 1/2, preserve existing `## Register` and `## Often confused with` sections in their `_conventions.md` position (the current templates end at `## See also` and predate these sections — a re-run on a completed file would otherwise drop both). Same drift class as step 12.

### Wrap-up

14. **Catalog and stub consistency.**
    - `.cowork/instructions.md` lesson-to-web catalog: verify current state and fix any staleness around register-confusability-grammar's entry and update-grammar's step count/labels. **Requires explicit user permission before editing that file** — ask first, per project rules.
    - `.claude/commands/lesson-to-web/register-confusability-grammar.md` stub currently says "run Step 4 Register research" — fix to reference Steps 8–9.
15. **Self-review.** Besides the scope check (carve-outs stayed field- and owner-scoped), spot-check YAML validity of every edited frontmatter template/example by parsing with `python3` + `yaml` (and `json.loads` compatibility of the inline arrays).

No new skills are created — only edits to existing skill files — so no new `.claude/commands/` stubs are needed (only the one-line fix to the existing stub in step 14).

## Out of scope / deferred

- **Idea 4 (Notes→Often-confused-with content backfill)** — moot: the ~45 existing grammar-index files were removed by the user on 2026-07-25; all content regenerates fresh through the pipeline with the new format.
- **Idea 5 (`builds_on` prerequisite relation)** — parked; belongs to the future practice-grammar consumption session (`Plans/practice-grammar-ideas.md`, its Idea 6).
- **Idea 6 (dual-representation consistency audit)** — parked; fold into the same consumption session, when the `confused_with` mirror has data worth auditing.
- **All of `Plans/practice-grammar-ideas.md`** — explicitly deferred to a later planner → skill-implementer session.

## Risks

- **Frontmatter-immutability carve-out** — the "no skill modifies frontmatter after creation" rule is a real safety rail. The carve-out must stay field-scoped (`register`, `confused_with`) and owner-scoped (register-confusability-grammar only); implementer must not generalize the wording.
- **YAML edits inside `proofread: true` files** — the Step 9 reverse write now touches frontmatter, not just a section. Corrupted YAML breaks the published site's frontmatter parsing. Mitigation is in the plan: append/create the `confused_with` field only, never rewrite the block; keep edits anchor-bounded exactly like the existing section insert.
- **Controlled-vocabulary drift** — if function values get invented ad hoc during extraction, the intersection prefilter degrades into noise. The "extend `_conventions.md` first, with user confirmation" rule is the guard; implementer should word it as a hard stop, not a suggestion.
- **Sparse-index period** — until a meaningful number of files are re-extracted, Step 9 finds no candidates and `confused_with` arrays stay empty. This is correct behavior, not a bug; both skills must say so to prevent future "fixes" that force matches.
- **Re-run/overwrite drift** — skills that recreate file content from templates predating the new sections (extract-grammar step 6 Overwrite, structure-grammar reformatting) would silently wipe `register`/`confused_with` data and dangle reverse links. Closed by steps 12–13; the mirror-gap direction that cannot be repaired mechanically is logged and deferred to the Idea 6 audit rather than papered over.
- **No plugin-data exposure** — grammar-index files contain no `<!--ID: -->` or `TARGET DECK` lines, and this plan changes nothing about extract-grammar step 8 (the only lesson-file write in the pipeline). No `# Summary` interaction anywhere.
