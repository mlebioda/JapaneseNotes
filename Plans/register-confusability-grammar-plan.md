# Register & Confusability Pipeline Step

## Goal

Fold the ad-hoc `prompt.md` workaround (adding Register and "Often confused with" notes to `grammar-index/grammar/` files) into the real lesson-to-web pipeline as a proper skill step, so the work is repeatable, consistent with pipeline conventions, and survives future full pipeline runs instead of being silently overwritten by them. `prompt.md` is deleted once the new skill exists.

Two structural gaps are closed at the same time:
- `_conventions.md` currently has no notion of `## Register`, `## Often confused with`, or the `partial: true` frontmatter flag that `prompt.md` introduced — any skill touching these files today would not know to preserve them.
- `prompt.md` already treated Register / See also / Often confused with as three separate concerns, but as a standalone ad-hoc document it was never bound by the pipeline's stricter `## See also` container-only rule (see `see-also-grammar` Step 8, which forbids point-to-point links there). Folding this work into the real pipeline means point-to-point confusable relationships need a home that doesn't collide with that established rule — hence the new `## Often confused with` section, leaving `## See also`'s container-only rule untouched. This is about pipeline integration and guarding against future drift (a full pipeline run silently overwriting ad-hoc content), not about fixing an internal defect in `prompt.md` itself.

## Approach

Add one new skill, `register-confusability-grammar`, as pipeline steps 8–9, running between `structure-grammar` (step 7) and `see-also-grammar` (renumbered 10–11, still the final step that sets `proofread: true`). It has two invocation modes: **pipeline mode** (called with a file list, like every other step in the chain) and **backfill mode** (triggered directly with a lesson file path, replacing `prompt.md`'s manual workflow one-for-one, including its minimal `partial: true` stub-creation behavior for grammar points that haven't been extracted yet, and reusing `extract-grammar`'s existing heading-classification logic so the two modes don't diverge).

Confusability matching reuses the `topic_slug` field that `extract-grammar` already computes (no new registry/index file to maintain) as a candidate-pool prefilter, falling back to a full directory scan only when `topic_slug` is empty. When a genuine match is found, the relationship is written bidirectionally: into the current file AND into the matched file's `## Often confused with` section (creating that section if it doesn't exist yet, via an anchor-based insert — see Step 2 below), even if that file already has `proofread: true` — documented as a narrow, scoped exception to the existing proofread guard.

Because this changes the chain's step count and order, every place in the vault that names the chain by skill or by step number needs a matching update: the three sibling skill files' "all mode" prose, the `.claude/commands/lesson-to-web/` stubs (which use their own independent Step 1–4 numbering), and `.cowork/instructions.md`'s "Available skills" list (the source-of-truth skill catalog). `.cowork/instructions.md` is not a skill file — it requires an explicit user permission ask before editing, per project rules, separate from skill-implementer's normal license to write to `.cowork/skills/`.

## Steps

1. **Update `.cowork/skills/lesson-to-web/_conventions.md`**
   - Add `## Register` and `## Often confused with` to the "File structure rules" list, positioned between `## Notes` (optional) and `## See also` (final section). Mark `## Register` as populated by `register-confusability-grammar`, `## Often confused with` as optional/may be absent on first pass.
   - Add `partial` to the frontmatter conventions section: boolean, defaults absent/`false`-equivalent when a file is fully extracted; `true` when created as a minimal backfill stub. Note that no skill removes `partial: true` automatically — a future full `extract-grammar` pass on that lesson is what completes/clears it.
   - Add a clarifying note under the "Never touch" / proofread-guard section: `## See also` keeps its existing container-only rule; point-to-point relationships (e.g. ように/のに/ために) belong exclusively in `## Often confused with`, never in `## See also`.
   - Add the scoped proofread-guard exception: writing to another (already-`proofread: true`) file's `## Often confused with` section during Step 9's bidirectional backlink write does not require the guard's "re-process anyway?" prompt, since it is not a re-process of that file — it is a single, dedup-checked, anchor-bounded insert limited to the `## Often confused with` section only (see the exact mechanics defined in Step 2 below). This exception applies only to Step 9's backlink target files, never to the file being primarily processed.

2. **Create `.cowork/skills/lesson-to-web/register-confusability-grammar.md`** — new skill file, following the structure of the existing pipeline skills (frontmatter with `name`/`description`, Trigger section, Shared files section loading `_conventions.md`, proofread-guard check line, numbered steps, handoff summary).

   **Trigger — explicit disambiguation between the two modes:**
   - "register-confusability grammar `<slug>`" — filename without `.md` → pipeline/direct mode, target is `grammar-index/grammar/<slug>.md`
   - "register-confusability grammar grammar-index/grammar/`<slug>`.md" — full relative path, path prefix `grammar-index/grammar/` → pipeline/direct mode
   - "register-confusability grammar `<lesson-file-path>`" — path prefix `JPLessons/` → **backfill mode**, mirrors `prompt.md`'s original usage
   - (called automatically from `structure-grammar` with a list of file paths — always pipeline mode)
   - Disambiguation rule: if the argument path starts with `JPLessons/`, treat as backfill mode; if it starts with `grammar-index/grammar/` or has no path separator (bare slug), treat as pipeline/direct mode. This mirrors the unambiguous trigger forms already used by every other skill in this pipeline.

   **Container/vocabulary scope guard** (mirrors `structure-grammar`'s container detection): if the file has a `## Sub-topics` section, skip Steps 8–9 and log `Register/Confused-with: container file — skipped`. Files under `grammar-index/grammar/vocabulary/` are out of scope entirely — never processed by this skill.

   **Backfill mode (only when triggered with a `JPLessons/` lesson file path):**
   - Read the lesson up to `# Summary` only (same `awk` boundary as `extract-grammar` step 2).
   - Locate `# 文法` and `# Vocabulary` grammar-construction points using the same section rules as `extract-grammar` steps 3–4.
   - **Reuse `extract-grammar` Step 4b's classification workflow exactly** (present each heading in the same table format, classify grammar / container / skip, wait for user input) before computing any slugs. This is required, not optional — it is what prevents backfill mode from creating spurious `partial: true` stubs for headings that are actually containers or pure vocabulary lists with no grammar content.
   - **Vocabulary-sourced "grammar" headings are explicitly out of scope.** `extract-grammar` routes a `# Vocabulary` heading classified `grammar` to `grammar-index/grammar/vocabulary/<subdir>/<slug>.md`, which falls under this skill's own vocabulary/ scope guard above ("out of scope entirely — never processed by this skill"). To stay consistent with that guard rather than diverge from `extract-grammar`'s own routing, backfill mode **skips** any `# Vocabulary` heading classified `grammar` — no stub is created, no Register/Confused-with processing happens, log it as `[SKIP] <heading>: Vocabulary-sourced, out of scope for register-confusability-grammar (see extract-grammar for full extraction)`. Only `# 文法`-sourced headings classified `grammar` proceed to slug computation and stub creation below.
   - For each `文法`-sourced heading classified **grammar**: compute the slug using `extract-grammar`'s Step 5 algorithm exactly (reuse, don't reimplement).
     - If `grammar-index/grammar/<slug>.md` exists: add it to the working file list and continue to Step 8 below.
     - If it does not exist: create the minimal stub —
       ```
       ---
       lesson: <lesson-code>
       pattern: <exact heading text>
       topic_slug: ""
       level: <N5 | N4 | N3 | N2 | N1>
       proofread: false
       partial: true
       ---

       # <exact heading text>

       [Short Structure summary derived from the lesson body, OR a pointer back to the lesson: "See JPLessons/... for full explanation." — do not duplicate lesson content at length.]
       ```
       Then add it to the working file list and continue to Step 8 below.
   - For headings classified **container** or **skip**: no stub is created, no slug is computed. Log as skipped with the classification reason (matches the container/vocabulary scope guard above — containers are out of scope for Register/Confused-with regardless of mode).
   - Never modify the lesson file itself — read-only, per `prompt.md`'s original rule 5.

   **Step 8 — Register**
   - For each file in the working list, research the pattern's register/politeness usage (web search allowed — same allowance as `review-grammar` Step 5's "may use web search to verify").
   - Format exactly:
     ```
     ## Register
     Register: neutral | polite-context typical | tiered (name the tiers)
     [1–3 sentences: who you'd say this to / in what setting, when the register isn't neutral]
     ```
   - Insert immediately after `## Notes` if present, otherwise immediately after `## Examples` (or `## Use Cases` if that's the last section present), and always before `## Often confused with` / `## See also`.
   - If the section already exists (re-run), overwrite its content rather than duplicating.

   **Step 9 — Often confused with**
   - Build the candidate pool: all `grammar-index/grammar/*.md` files (excluding container files, excluding vocabulary/, excluding the current file) whose `topic_slug` array intersects the current file's `topic_slug` array.
   - If the current file's `topic_slug` is empty (e.g. a fresh `partial: true` stub with no classification yet), fall back to a full scan of all pattern files' `# heading` + `> gloss` lines instead of the prefiltered pool.
   - Within the pool, judge genuine confusability: similar surface gloss/translation but different underlying usage rule (e.g. ように / のに / ために all gloss near "in order to / because / for the sake of" but differ in agency and hypothetical-ness). Do not force a match if none is genuine — an empty section on first pass is expected, not an error.
   - For each genuine match not already linked (dedup by slug presence in both directions):
     - Add to the current file: `- [Label](/JapaneseNotes/grammar-index/grammar/<slug>) — <distinguishing test>`
     - Also update the matched file with the reverse line (own label + a distinguishing test phrased from the matched file's perspective). **Insertion mechanics for the matched file (this is an edit to an arbitrary already-published file, not in-context section building, so the target location must be located explicitly):**
       - If the matched file already has a `## Often confused with` section: append the new line inside it (dedup-checked).
       - If it does not: locate the `## See also` heading in that file and insert a new `## Often confused with` section (header + the one line) immediately before it — this is the only valid anchor, since `## See also` is guaranteed to be the final section per `_conventions.md`. If the matched file also lacks `## Register`, do not add one as a side effect — only `## Often confused with` is inserted.
       - This insert proceeds even if the matched file has `proofread: true` (per the `_conventions.md` exception from Step 1) — it is bounded to locating one anchor and inserting one section/line, never touching any other part of that file.
   - If no candidates found: leave `## Often confused with` absent (do not write an empty header).

   **Forward pointer (informational only, not in scope for this plan):** `prompt.md`'s "Usage" note said that once backfilling is done, the follow-up is wiring `practice-grammar` to consume the new `Register` + `See also` fields in its SRS drills. Carry this forward as a one-line note at the end of this skill file: "Future work (separate planning session): update `practice-grammar` to read `## Register` and `## Often confused with` when selecting/explaining drill items." Do not act on it here.

   **Handoff summary** (same shape as other pipeline skills):
   ```
   register-confusability-grammar — N files processed

     grammar-index/grammar/<slug>.md
       Register: added (tiered — 3 tiers)
       Often confused with: 2 backlinks added (ni-tame, node) — 1 new file touched for reverse link

     grammar-index/grammar/<slug>.md
       Register: container file — skipped
   ```
   Then ask (skip if running in **all** mode):
   ```
   Run see-also-grammar on these files? (yes / no / all)
   ```
   - **yes** — load `.cowork/skills/lesson-to-web/see-also-grammar.md` and pass the file list.
   - **no** — end the skill.
   - **all** — load `see-also-grammar` in all mode (no further handoff prompt).

3. **Update `.cowork/skills/lesson-to-web/structure-grammar.md`** — two separate references need updating, not just the bottom handoff section:
   - **Line 24** (top of file, "Workflow" section): `If called with **all** mode (from review-grammar "all" answer): skip the handoff prompt at the end and automatically continue to see-also-grammar.` → change the continuation target from `see-also-grammar` to `register-confusability-grammar`.
   - **Bottom handoff section**: change the end-of-file handoff prompt from "Run see-also-grammar on these files?" to "Run register-confusability-grammar on these files?", pointing to the new skill file, and update the **all** mode branch to load `register-confusability-grammar` in all mode (which itself continues to `see-also-grammar` in all mode) instead of loading `see-also-grammar` directly.

4. **Update `.cowork/skills/lesson-to-web/see-also-grammar.md`**
   - Renumber "Step 8 — Populate ## See also" → **Step 10**, and "Step 9 — Set proofread: true" → **Step 11**.
   - Update the frontmatter `description` and Trigger comment ("called from structure-grammar") to say "called from register-confusability-grammar".
   - No behavioral change to the See-also population logic itself (container-only rule stays as-is).

5. **Update `.cowork/skills/lesson-to-web/update-grammar.md`**
   - Add a new row to the pipeline table: `register-confusability-grammar | 8–9 | Register research, often-confused-with backlinks — web search + cross-file writes`.
   - Update the `see-also-grammar` row's step numbers from `8–9` to `10–11`.
   - Update the prose describing the chain order to list all five skills: preprocess → review → structure → register-confusability → see-also.
   - **Explicitly included:** the frontmatter `description:` field at the top of this file ("Chains: preprocess-grammar → review-grammar → structure-grammar → see-also-grammar") must also be updated to insert `register-confusability-grammar` in the correct position. This is not just the body prose — the frontmatter description line is in scope for this step too.

6. **Update chain-description prose in three sibling skill files not otherwise touched by this plan** — each currently names the chain by skill and will be stale once `register-confusability-grammar` is inserted:
   - `.cowork/skills/lesson-to-web/extract-grammar.md` (around line 443) — "load preprocess-grammar in **all** mode, which chains through review-grammar → structure-grammar → see-also-grammar without prompting at handoffs" → insert `register-confusability-grammar` between `structure-grammar` and `see-also-grammar`.
   - `.cowork/skills/lesson-to-web/preprocess-grammar.md` (around line 131) — "load review-grammar, instructing it to continue through structure-grammar and see-also-grammar without prompting at each handoff" → same insertion.
   - `.cowork/skills/lesson-to-web/review-grammar.md` (around line 87) — "load structure-grammar, instructing it to continue through see-also-grammar without prompting at the next handoff" → update to continue through `register-confusability-grammar` then `see-also-grammar`.

7. **Update `.claude/commands/lesson-to-web/` stubs** — these use their own independent Step 1–4 numbering (preprocess=Step 1, review=Step 2, structure=Step 3, see-also=Step 4), separate from the skill files' internal step numbers:
   - Create `.claude/commands/lesson-to-web/register-confusability-grammar.md`, following the existing stub pattern (one sentence pointing to the skill file + `File: $ARGUMENTS`), explicitly labeled **Step 4** ("run Step 4 Register research and Often-confused-with backlinks").
   - Update `.claude/commands/lesson-to-web/see-also-grammar.md`: change "Step 4" to "Step 5" in its instruction sentence.
   - Update `.claude/commands/lesson-to-web/update-grammar.md`: change the chain prose "preprocess → review → structure → see-also" to "preprocess → review → structure → register-confusability → see-also".

8. **Update `.cowork/instructions.md`'s "Available skills" list** — this is the source-of-truth skill catalog and currently ends at `lesson-to-web/see-also-grammar — Step 4: ...`, with `update-grammar` describing "chains all four steps below."
   - **This file requires explicit user permission before modification, per project rules ("Never modify files in .cowork/ without permission. Always ask and explain what do you want to modify.").** This is distinct from `.cowork/skills/`, which skill-implementer has standing license to write to as part of implementing this plan. Skill-implementer must ask the user before editing this specific file and explain exactly what will change, even though the rest of this plan is otherwise approved.
   - Once permission is granted: add a new bullet `lesson-to-web/register-confusability-grammar — Step 4: Register research (web search) + Often confused with backlinks (user-gated where noted). Trigger: "register-confusability grammar <file>"`, positioned after `structure-grammar` and before `see-also-grammar`.
   - Renumber the existing `see-also-grammar` bullet from "Step 4" to "Step 5".
   - Update the `update-grammar` bullet from "chains all four steps below" to "chains all five steps below".

9. **Delete `prompt.md`** (vault root) — its functionality is fully superseded by the new skill's backfill mode, and its forward-pointer note has been preserved in Step 2 above. Skill-implementer executes this deletion as part of implementing this plan (planner cannot touch files outside `Plans/`).

## Risks

- **Proofread-guard exception scope** — Step 9's bidirectional backlink write is the only place in the entire pipeline that intentionally bypasses the `proofread: true` guard. The exception is now defined precisely (single anchor-bounded insert/append to `## Often confused with` only — see Step 2). If the exception wording in `_conventions.md` is loosened during implementation, it must not be widened into a general bypass.
- **Renumbering and chain-name churn** — steps 8–9 in `see-also-grammar.md` become 10–11, and the chain now has five named skills instead of four in multiple independent places (skill files' internal step numbers, the three sibling skills' "all mode" prose, the `.claude/commands/lesson-to-web/` stubs' own Step 1–4 numbering, and `.cowork/instructions.md`'s catalog). Mitigation: grep `.cowork/skills/lesson-to-web/` and `.cowork/instructions.md` for both the literal strings `Step 8` / `Step 9` **and** the chain-name strings `structure-grammar` / `see-also-grammar`; additionally grep `.claude/commands/lesson-to-web/` for the **short forms** `structure` and `see-also` as well — that directory's prose (e.g. `update-grammar.md`'s stub: "preprocess → review → structure → see-also") uses the unhyphenated short names, not the full compound skill names, so the hyphenated-name grep alone would silently miss it there. The step-number grep alone would not have caught the command-stub or instructions.md gaps found in review, and the compound-name grep alone would not catch the short-form stub prose either.
- **`.cowork/instructions.md` permission gate** — Step 8 is blocked on an explicit user ask; if skipped or edited without asking, it violates project rules directly. Skill-implementer must treat this as a hard stop, not a formality.
- **`grammar-audit.py`** (referenced by `see-also-grammar` for orphan detection) is a script under `.claude/scripts/` — out of scope for this plan, but note that it does not know about `## Often confused with` or `partial: true`; a future pass could extend it, not required here.
- **Web search dependency in Step 8** — Register research quality depends on web search availability/results; if search is unavailable or inconclusive, the skill should state `Register: unknown — insufficient source material` rather than guessing, to avoid inserting unverified claims into published grammar files.
- **Backfill mode touching many files at once** — a lesson can have many grammar points; running backfill mode on an old lesson could create several `partial: true` stubs plus many cross-file backlink writes in one session, and now also runs the interactive extract-grammar Step 4b classification table for every heading. No explicit batching/confirmation step beyond the per-file handoff summary and the 4b classification gate itself — flag to the user during implementation if a further "confirm before processing N points" gate is wanted.
- **Pre-existing, out-of-scope cleanups noted but not required**: `_conventions.md` documents `topic_slug` inconsistently with its actual array usage elsewhere, and its canonical section order doesn't exactly match `structure-grammar.md`'s template order. Left as-is per reviewer sign-off; may be folded in opportunistically during Step 1 if trivial, but not a blocking requirement of this plan.
