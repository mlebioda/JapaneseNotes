# Practice-grammar: metadata-driven exercise generation from extracted grammar files

## Goal
Make scheduled practice-grammar sessions (TODAY / OVERDUE) work with grammar-state.json entries whose `lesson_file` points at extracted grammar point files under `grammar-index/grammar/` (produced by the lesson-to-web pipeline), and use those files' rich metadata (`confused_with` + pre-authored "— test:" lines, `register`, `function`, `topic_slug`) to generate better-targeted exercises. Currently such entries are skipped with a warning because the loader assumes lesson-file structure (`# Summary`, `# 文法`). Both source types (lesson files and extracted files) must work in one mixed session. Lesson-triggered sessions ("practice UN4GL14") keep working exactly as now.

## Approach
Single-file update to `.cowork/skills/practice-grammar.md` — the user explicitly decided NOT to split the skill. Add a source-type branch to the multi-lesson loading step (path prefix `grammar-index/grammar/` → whole-file read; otherwise → existing awk lesson flow, unchanged). Add a supplementary vocabulary base drawn from `Vocabulary/*.md` for extracted-file topics (their lesson ごい/ひょうげん pool is unavailable). Add a new "Metadata-driven exercise generation" section covering the mandatory `confused_with` and `register` rules. Helper modules `.cowork/skills/practice-grammar-srs.md` and `practice-grammar-study-mode.md` were verified and need no changes: the SRS module treats `lesson_file` as an opaque identity field, and study mode consumes `body_text` / `vocab_pool` passed in by the caller.

Decisions baked in (user-confirmed):
- **Minimal-pair contrast exercise = REPLACE, same-batch only.** When both halves of a confused pair are due in the same session AND land in the same generation batch, the pair exercise fills one exercise slot for each of the two topics. Session N stays stable — never added on top. If the pair spans two batches, Phase 1 does not attempt a cross-batch merge (known limitation, resolved by Phase 2 topic_slug batching).
- **Register-transformation = ALTERNATIVE FORM, `register: polite` only.** For `register: polite` patterns, one of the topic's existing use-case exercises may take the plain↔keigo transformation form. No extra exercises, no change to session length. `register: tiered` patterns (confirmed present in current data) use register-selection-logic situations instead — see step 5.
- **Use Cases/Structure variant rule = semantic, not syntactic.** Distinct structural sub-groups within `## Structure`/`## Use Cases` become separate use cases regardless of the markdown formatting (heading level, bullets, bold labels) used to express them. In current single-lesson data this is a rare case (one file); the common case is one point = one use case.
- **Broken confused_with references = silent skip.** Unresolvable `confused_with` slugs are a data-quality issue in the extract-grammar pipeline's output, outside this skill's control — skip the pairing silently, never warn or block.
- **Task C = PHASE 2 (deferred).** Steps 10–11 below are documented but clearly marked — the implementer skips them unless explicitly told otherwise.

## Steps

### Phase 1 — Task A: dual-source topic resolution (prerequisite)

1. **`.cowork/skills/practice-grammar.md` — "Multi-lesson file loading"**: add a source-type branch keyed on the `lesson_file` path.
   - If the path starts with `grammar-index/grammar/` → **extracted-file flow**: read the whole file directly (no awk slice — these files have no `# Summary`).
     - `grammar_header` = the file's H1 (`# <pattern>`). If H1 ≠ the stored `grammar_header`, print a warning but continue using the H1 (do not skip).
     - `body_text` = gloss blockquote + `## Structure` + `## Examples` + `## Use Cases` (if present) + `## Notes` (if present) + `## Register` (if present) + `## Often confused with` (if present). Exclude YAML frontmatter and `## See also`.
     - **Container files** (those with `## Sub-topics`) must never be drilled — skip the entry with a warning naming the file.
     - Also parse frontmatter fields for later use: `pattern`, `register`, `confused_with`, `function`, `topic_slug`, `level`.
   - Else → **existing lesson-file flow, byte-for-byte unchanged** (awk `# Summary` slice, `# 文法`/`# Vocabulary` heading search, `_heading-roles.md` rules).
   - Update the **Edge cases** warning list: remove the implicit "grammar_header not found" failure mode for extracted files (H1 is authoritative there); add the container-file skip warning.

2. **`.cowork/skills/practice-grammar.md` — "Use case extraction"**: extend the extraction rules to the extracted-file section names, keyed on semantic content rather than markdown structure:
   - When `## Structure` (or `## Use Cases`) contains multiple distinct structural sub-groups — e.g. different verb-group conjugation patterns, different grammatical contexts, different registers of the same pattern — each distinct sub-group becomes its own use case, **regardless of whether the markdown expresses them as subheadings, bold labels, bullets, or plain prose, and regardless of heading level.** Do not key this rule on any specific markdown heading depth (H3, numbered list, etc.) — those are incidental formatting choices that vary file to file.
   - When `## Structure`/`## Use Cases` describes a single unified pattern with no distinct sub-groups, the whole point is one use case. **This is the common case in current data** — verified against all 8 non-container files extracted so far (all from UN4GL14), none of which have numbered Use Cases lists; only `o-go-v-masukudasai-respectful-request-form.md` has genuinely distinct sub-groups (Group 1/2 verbs vs. Group 3 vs. Exceptions, currently marked with H3 headings — but the rule above applies to the semantic grouping, not the H3 markup itself).
   - Same labels-stay-internal rule as before.
   - **Unconfirmed against a second lesson**: this rule set is derived from a single-lesson sample (all 8 extracted files come from UN4GL14). Re-validate against a second lesson's extracted files, which may use different formatting conventions, once one is available.

3. **`.cowork/skills/practice-grammar.md` — vocab pool**: add a "Vocabulary base" for sessions containing extracted-file topics.
   - Source: `Vocabulary/*.md` — **top level only**; skip the `Vocabulary/JLPT-decks/` subdirectory entirely.
   - Collect only plain lines tagged `#w` / `#wc` / `#wp` — never lines inside Anki card-format blocks.
   - **Block-boundary rule (explicit, mechanical)**, needed because real files mix formats: `Interview.md`/`Car.md` separate card blocks with `---`; `Bank-vocabulary.md`/`Post-vocabulary.md`/`Slownictwo-kolejowe.md` interleave plain tag lines directly between card blocks with no separator; `Interview.md` is 100% cards (yields zero usable lines — that's fine, just move to the next file).
     - A **card block** starts at a tag line (`#w`/`#wc`/`#wp`) that is immediately followed by card-field lines (e.g. `ほんやく:`, `Przykład:`, or similar labeled-field lines) and ends at the next `<!--ID:-->` line, **inclusive**, or at the next `---` separator — whichever comes first.
     - A **plain usable line** is a `#w`/`#wc`/`#wp` tag line that is NOT immediately followed by card-field lines (i.e. the next non-blank line is either another tag line, a `---`, or end of file). Collect these into the pool.
     - Never read past the `<!--ID:-->` line of a card block back into plain-line collection — treat it strictly as the block's closing boundary.
   - Prefer topically relevant words when drawing from the base (best-effort judgment; the deterministic topic_slug matching is Phase 2).
   - Mixed sessions: merged pool = lesson ごい/ひょうげん pools (from lesson-file entries) + Vocabulary base. Existing dedup-by-Japanese-form rule applies.
   - **Tag-position-agnostic parsing**: the pool-merging step must not assume one fixed tag position. `practice-grammar.md`'s documented lesson pool format is tag-last (`日本語（よみ）- translation #w`), but real `Vocabulary/*.md` plain lines are tag-first (`#w 銀行（ぎんこう）- bank`). The parsing/merging logic must accept both orders rather than relying on the existing lesson-pool regex as-is.
   - The existing outside-vocab rule (strict N5) remains the final fallback when the pool cannot express the grammar point.

### Phase 1 — Task B: mandatory metadata rules (extracted-file topics)

4. **`.cowork/skills/practice-grammar.md` — new section "Metadata-driven exercise generation (extracted-file topics)"** covering `confused_with`:
   - Type 2 distractors may come from `confused_with`-linked files **even when those patterns are not in the session** — load the linked file (`grammar-index/grammar/<slug>.md`) on demand, read-only, just to get its pattern name (H1 / frontmatter `pattern`). This relaxes, for extracted-file topics only, the current Type 2 constraint that confusable forms must come from the lesson itself.
   - The pre-authored `— test: <question>` line in `## Often confused with` seeds Type 2 / Type 6 prompts.
   - Wrong-answer feedback quotes or derives from the test line.
   - **Broken `confused_with` reference fallback**: if a `confused_with` slug doesn't resolve to an existing file under `grammar-index/grammar/` (confirmed live example: `o-go-v-masushimasu.md` lists `o-go-v-masukudasai`, but the real file is `o-go-v-masukudasai-respectful-request-form.md`), silently skip that specific pairing and fall back to ordinary Type 2 distractor selection for that topic. No warning — this is a data-quality issue in the extract-grammar pipeline's output, outside this skill's control, and must never block or interrupt a session.
   - **Minimal-pair contrast exercise**: when both halves of a confused pair are due in the same session **and land in the same generation batch** (see batching constraint below), generate one contrast exercise that REPLACES one exercise slot for each of the two topics (fills one slot per topic; session N stays stable). The score from the pair exercise counts toward both topics.
   - **Phase-1 batching constraint (known limitation)**: exercise generation happens per-batch (step 6, unchanged), and batches are currently formed by even-count split with no confused_with-awareness. If both halves of a confused pair land in the **same** batch, apply the minimal-pair replacement above. If they land in **different** batches, do NOT attempt a cross-batch pair exercise — treat each topic independently with ordinary Type 2 distractors (using the on-demand confused_with lookup above, which is unaffected by batching). This gap is fully resolved by Task C's `topic_slug`-based batching (Phase 2, step 11), which groups confused/related topics into the same batch by design; Phase 1 explicitly does not attempt to fix it.

5. **Same new section — `register` rules**, plus a matching update to the **Grading** section:
   - Exercise situations must match the pattern's `register` frontmatter + `## Register` section content.
   - **`register: polite`**: business/service/customer scenarios, plain↔keigo transformation flavor.
   - **`register: tiered`** (confirmed live examples due day one: `teineigo-polite-expressions.md`, `uchi-soto-in-group-out-group.md`): do NOT apply the polite-mode transformation above. Instead, situations must exercise the register-**selection** logic itself — e.g. the uchi/soto (in-group/out-group) boundary, or tier-escalation across a formality scale — rather than a fixed formality bracket. Read the pattern's own `## Register` section prose for the specific selection rule to drill (which parties, which contexts trigger which tier) rather than inferring a generic transformation.
   - Grading gains a register dimension: grammatically correct but wrong register = mistake, with register-specific feedback (name the register mismatch, cite the `## Register` guidance — for `tiered` patterns, cite the specific selection rule that was violated, not a generic politeness note).
   - **Register-transformation flavor** (plain sentence → keigo form, or vice versa) for `register: polite` patterns only — implemented as an alternative form of one of the topic's existing use-case exercises. No extra exercises; session length unchanged. `register: tiered` patterns use the selection-logic situations above instead of this transformation flavor.

6. **Same new section — weak_points ↔ confused_with synergy**: when a stored `weak_point` string names a pattern confusion (e.g. "だけ vs しか"), look up the topic's `confused_with` list to load the counterpart file and build the targeted discrimination drill from it (test line + pattern names).

7. **Update the "Type selection rule" and "Weak-point bias" paragraphs** to reference the new metadata sources (confused_with-sourced Type 2 availability, register-transformation flavor) without changing behavior for lesson-file topics.

### Phase 1 — verification and bookkeeping

8. **Verify no changes needed** in `.cowork/skills/practice-grammar-srs.md` and `.cowork/skills/practice-grammar-study-mode.md` (pre-checked: srs passes `lesson_file` through opaquely; study mode consumes `body_text`/`vocab_pool` from the caller). If the implementer finds a hidden lesson-path assumption, stop and report rather than editing helpers.
9. **Flag (do not silently do): `.cowork/instructions.md`** — the practice-grammar skill description should gain one line noting extracted-file support. Requires explicit user permission per project rules; the implementer must ask before touching it.

### Phase 2 — Task C: preferences (DEFERRED — implementer skips unless explicitly told otherwise)

10. **[PHASE 2] `function`-based grouping**: same-`function` due topics can serve as each other's Type 2 distractors; function-based type-selection heuristics (request/permission/prohibition → Types 1/3; conditional/temporal → Type 4; hearsay-appearance → Type 5). Controlled vocabulary lives in `.cowork/skills/lesson-to-web/_conventions.md`.
11. **[PHASE 2] `topic_slug`-based batching**: in scheduled sessions, order/split batches so same-topic_slug entries land together (coherent batches); deterministic topical vocab preference when drawing from `Vocabulary/` (match file topic vs topic_slug/function).

## Risks
- All sources are **read-only**: lesson files, extracted grammar files, `Vocabulary/` files, `confused_with`-linked files. Never touch `TARGET DECK` lines or `<!--ID: -->` lines; `Vocabulary/` files in Anki card format contain `<!--ID: -->` blocks that must be skipped during parsing, never edited.
- The lesson-triggered flow and the lesson-file branch of scheduled sessions must remain byte-for-byte behaviorally identical — 239 of 247 grammar-state.json entries still point at `JPLessons/` lesson files.
- Grammar-state.json itself is written only via the unchanged `practice-grammar-srs.md` flow — no schema changes; `lesson_file` values pointing at `grammar-index/grammar/` are already valid identity strings.
- Container files under `grammar-index/grammar/` must never generate exercises — the `## Sub-topics` guard is the only safeguard; keep it explicit.
- Minimal-pair replacement must not break the `Exercise N / T` progress indicator: T is computed after pair-merging, at session start.
- Known Phase-1 limitation: minimal-pair merging only works within a single batch; batches are formed with no confused_with-awareness, so a pair split across two batches gets no merge (each topic drills independently instead). Accepted for Phase 1; Task C's topic_slug batching is the proper fix.
- Use Cases/Structure semantic-grouping rule and the block-boundary vocabulary parsing rule are both verified only against the current single-lesson sample (UN4GL14, 8 extracted files). Re-check both once a second lesson's extracted files exist, since formatting conventions may differ.
