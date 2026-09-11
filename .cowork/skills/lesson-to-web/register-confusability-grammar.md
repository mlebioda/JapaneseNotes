---
name: register-confusability-grammar
description: >
  Research and add Register (politeness/formality usage) and Often confused with
  (point-to-point confusable-pattern backlinks) sections to grammar files under
  grammar-index/grammar/. Steps 8–9 in the grammar post-processing pipeline, running
  between structure-grammar and see-also-grammar. Also supports a standalone backfill
  mode that mirrors the retired prompt.md workaround, creating minimal partial: true
  stubs for grammar points not yet extracted. Trigger: "register-confusability grammar
  <file>" or called from structure-grammar.
---

# Register & Confusability Grammar Skill

## Trigger

- "register-confusability grammar `<slug>`" — filename without `.md` → pipeline/direct mode, target is `grammar-index/grammar/<slug>.md`
- "register-confusability grammar grammar-index/grammar/`<slug>`.md" — full relative path → pipeline/direct mode
- "register-confusability grammar `<lesson-file-path>`" — path prefix `JPLessons/` → **backfill mode**, mirrors the retired `prompt.md` workaround
- (called automatically from structure-grammar with a list of file paths — always pipeline mode)

**Disambiguation rule:** if the argument path starts with `JPLessons/`, treat as backfill mode. If it starts with `grammar-index/grammar/`, or has no path separator (a bare slug), treat as pipeline/direct mode. This mirrors the unambiguous trigger forms already used by every other skill in this pipeline.

---

## Workflow

Process each file in order. Apply both steps to one file before moving to the next.

If called with **all** mode (from structure-grammar "all" answer): skip the handoff prompt at the end and automatically continue to see-also-grammar in all mode.

---

## Shared files

Load `.cowork/skills/lesson-to-web/_conventions.md` before starting.

---

Check the proofread: true guard (see `_conventions.md`) before processing each file — except when writing the reverse half of a bidirectional backlink into a matched file during Step 9, which is exempt per the scoped exception documented in `_conventions.md`.

---

## Container / vocabulary scope guard

Mirrors structure-grammar's container detection. Before applying Step 8 or Step 9 to any file:

- If the file has a `## Sub-topics` section (a container file): skip Steps 8–9 for it and log `Register/Confused-with: container file — skipped`.
- Files under `grammar-index/grammar/vocabulary/` are out of scope entirely — never processed by this skill, in either mode.
- Files matching `grammar-index/grammar/vocabulary-*.md` are also out of scope entirely — never processed by this skill, in either mode. This is a sibling exclusion by top-level filename pattern, in addition to (not a replacement for) the `vocabulary/` subdirectory rule above.

---

## Backfill mode

Only active when triggered directly with a `JPLessons/` lesson file path (not when called from structure-grammar).

1. **Read the lesson up to `# Summary` only** — same `awk` boundary as `extract-grammar` step 2:
   ```bash
   awk '/^# Summary$/{exit} {print}' "$LESSON_FILE"
   ```
2. **Locate `# 文法` and `# Vocabulary`** grammar-construction sections using the same section rules as `extract-grammar` steps 3–4.
3. **Reuse `extract-grammar` Step 5's classification workflow exactly** — present every heading found in both sections in the same table format, and wait for the user to classify each as grammar / container / skip, before computing any slugs. This is required, not optional: it is what prevents backfill mode from creating spurious `partial: true` stubs for headings that are actually containers or pure vocabulary lists with no grammar content.
4. **Vocabulary-sourced "grammar" headings are out of scope.** `extract-grammar` routes a `# Vocabulary` heading classified `grammar` to `grammar-index/grammar/vocabulary/<subdir>/<slug>.md`, which falls under this skill's own vocabulary/ scope guard above. To stay consistent with that guard rather than diverge from `extract-grammar`'s own routing, backfill mode **skips** any `# Vocabulary` heading classified `grammar` — no stub is created, no Register/Confused-with processing happens. Log it as:
   ```
   [SKIP] <heading>: Vocabulary-sourced, out of scope for register-confusability-grammar (see extract-grammar for full extraction)
   ```
   Only `# 文法`-sourced headings classified `grammar` proceed to slug computation and stub creation below.
5. **For each `文法`-sourced heading classified grammar:** compute the slug using `extract-grammar`'s Step 6a (Compute slug) algorithm exactly (reuse, don't reimplement).
   - If `grammar-index/grammar/<slug>.md` already exists: add it to the working file list and continue to Step 8 below.
   - If it does not exist: create the minimal stub:
     ```
     ---
     lesson: <lesson-code>
     pattern: <exact heading text>
     topic_slug: ""
     function: []
     level: <N5 | N4 | N3 | N2 | N1>
     proofread: false
     partial: true
     ---

     # <exact heading text>

     [Short Structure summary derived from the lesson body, OR a pointer back to the lesson: "See JPLessons/... for full explanation." — do not duplicate lesson content at length.]
     ```
     Then add it to the working file list and continue to Step 8 below.
6. **For headings classified container or skip:** no stub is created, no slug is computed. Log as skipped with the classification reason (matches the container/vocabulary scope guard above — containers are out of scope for Register/Confused-with regardless of mode).
7. **Never modify the lesson file itself** — read-only, per the retired `prompt.md`'s original rule 5.

---

## Step 8 — Register

For each file in the working list, research the pattern's register/politeness usage. Web search is allowed — same allowance as `review-grammar` Step 5's "may use web search to verify."

**Format — exactly:**
```
## Register
Register: neutral | polite-context typical | tiered (name the tiers)
[1–3 sentences: who you'd say this to / in what setting, when the register isn't neutral]
```

If web search is unavailable or the results are inconclusive, do not guess:
```
## Register
Register: unknown — insufficient source material
```

**Insertion position:** immediately after `## Notes` if present, otherwise immediately after the last content section present — `## Examples` or `## Use Cases` for Structure 1, or the last numbered `## N. Use Case Name` section (including its nested `### Examples`) for Structure 2. Always before `## Often confused with` and before `## See also`.

**Frontmatter mirror:** after writing/overwriting the `## Register` section, mirror its value into the `register:` frontmatter field (bare scalar, per `_conventions.md` Canonical YAML serialization). Value mapping:

- section `Register: neutral` → `register: neutral`
- section `Register: polite-context typical` → `register: polite`
- section `Register: tiered (...)` → `register: tiered`
- section `Register: unknown — insufficient source material` → `register: unknown`

If the field is absent, create it (insert after `level`, before `proofread`, per `_conventions.md`). Touch only the `register` line — never rewrite or reorder any other frontmatter field. This write is permitted by the scoped carve-out in `_conventions.md`'s Frontmatter immutability rule.

**Re-run behavior:** if `## Register` already exists, overwrite its content rather than duplicating the section, and overwrite the `register:` frontmatter value to match (never append a second field).

---

## Step 9 — Often confused with

1. **Build the candidate pool** from all `grammar-index/grammar/*.md` files, excluding container files, excluding files under `vocabulary/`, and excluding the current file. The pool is the **union** of two intersections:
   - files whose `function` array intersects the current file's `function` array (primary prefilter — semantic role beats topic grouping), **∪**
   - files whose `topic_slug` array intersects the current file's `topic_slug` array.
2. **Fallback:** if both the current file's `function` and `topic_slug` arrays are empty (e.g. a fresh `partial: true` stub with no classification yet), or the union pool comes out empty, fall back to a full scan of all pattern files' `# heading` + `> gloss` lines instead of the prefiltered pool. **Zero candidates after all tiers is the expected outcome on a sparse or freshly-rebuilt index** — leave `## Often confused with` absent, log no error, and do not force matches to fill the gap.
3. **Judge genuine confusability** within the pool: similar surface gloss/translation but different underlying usage rule (e.g. ように / のに / ために all gloss near "in order to / because / for the sake of" but differ in agency and hypothetical-ness). Do not force a match if none is genuine — an empty section on first pass is expected, not an error.
4. **For each genuine match, run the dual-representation dedup check first.** For each direction (current file → matched slug, and matched file → current slug), check both representations: the section link (`grammar-index/grammar/<slug>)` inside `## Often confused with`) and the frontmatter array entry (the slug inside `confused_with:`). Then act asymmetrically:
   - **Both present** → that direction is fully linked; skip it (current behavior).
   - **Section link present, array entry missing** → repair mechanically: append the slug to that file's `confused_with:` array. This is a pure copy of an existing link target — no content generation. Applies only to pairs matched in the current run; this is not a global audit. A repair write into a `proofread: true` matched file is covered by the widened Step-9 exception in `_conventions.md`.
   - **Array entry present, section link missing** → skip that direction and log:
     ```
     [MIRROR-GAP] <slug>: confused_with entry has no section line — left for consistency audit
     ```
     Never repair this direction — it would require composing a fresh `— test:` question (content generation, potentially inside a proofread file). Deferred to the parked consistency audit.
   - **Neither present** → a new link; write both representations per the mechanics below.

   For each direction that needs the new link:
   - Add to the current file, using the canonical "Often confused with" line format from `_conventions.md` (single source of truth — the `— test:` prefix is mandatory):
     ```
     - [Label](/JapaneseNotes/grammar-index/grammar/<slug>) — test: <one-line question that picks between the two patterns>
     ```
   - Also update the matched file with the reverse line in the same canonical `— test:` format (own label + a one-line question phrased from the matched file's perspective). **Insertion mechanics for the matched file** — this is an edit to an arbitrary already-published file, not in-context section building, so the target location must be located explicitly:
     - If the matched file already has a `## Often confused with` section: append the new line inside it (dedup-checked).
     - If it does not: locate the `## See also` heading in that file and insert a new `## Often confused with` section (header + the one line) immediately before it — this is the only valid anchor, since `## See also` is guaranteed to be the final section per `_conventions.md`. If the matched file also lacks `## Register`, do not add one as a side effect — only `## Often confused with` is inserted.
     - This insert proceeds even if the matched file has `proofread: true` (per the `_conventions.md` scoped exception) — it is bounded to locating one anchor and inserting one section/line, plus the matched file's `confused_with` frontmatter append below, never touching any other part of that file.
   - **Frontmatter mirror (both directions):** after adding the forward line, append the matched file's slug to the **current** file's `confused_with:` array. After inserting the reverse line, append the current file's slug to the **matched** file's `confused_with:` array — permitted under the widened proofread exception in `_conventions.md`. In both cases: create the field if absent (inline JSON-compatible array per `_conventions.md` Canonical YAML serialization, inserted after `level`, before `proofread`); if present, append the slug to the existing inline array. Touch only the `confused_with` line — never rewrite or reorder any other frontmatter field.
5. **If no candidates found:** leave `## Often confused with` absent — do not write an empty header.

---

## Future work

Not in scope for this skill. The retired `prompt.md`'s "Usage" note said that once backfilling is done, the follow-up is wiring `scheduled-grammar-practice` to consume the new `Register` + `Often confused with` fields in its SRS drills. Carried forward as a pointer only: **Future work (separate planning session): update `scheduled-grammar-practice` to read `## Register` and `## Often confused with` when selecting/explaining drill items.**

---

## Handoff summary

After processing all files, print:

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
