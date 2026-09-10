# Vocabulary-container child wikilinks (extract-grammar Step 8)

## Goal
When `extract-grammar` routes a `# Vocabulary` POS container (`## Verbs` / `## Nouns` /
`## Adjectives`) to Step 7c because its children are exclusively Vocabulary-sourced `grammar`
headings consolidated into a shared file (e.g. `grammar-index/grammar/vocabulary-verbs.md`),
Step 8 currently inserts a wikilink **only** at the container heading. Each child heading
(e.g. `### 勉強 - learn`) has its own standalone leaf file under
`grammar-index/grammar/vocabulary/<subdir>/<slug>.md`, but today gets no lesson-file link to
it — confirmed missing on `JPLessons/Udemy/N5/Grammar/UN5GL7.md`, where the four child
headings under `## Verbs` had no `→ [[...]]` line even though
`grammar-index/grammar/vocabulary/Verbs/{benkyou-learn,kenkyuu-research,sumu-to-live,matsu-to-wait}.md`
all exist and are populated. A manual one-off fix (adding a per-child `→ [[...]]` line under
each of the four `###` headings in UN5GL7.md) was already applied and confirmed by the user;
this plan makes that behavior permanent in the skill so future extractions do it automatically.

**Revision note (this version):** a reviewer agent re-checked the first draft of this plan
against the live `.cowork/skills/lesson-to-web/extract-grammar.md` and found a critical gap:
the draft reused Step 8's existing "Only for files Created in step 7" gate for the new
per-child links. That gate is wrong for vocabulary leaves — vocabulary words recur constantly
across lessons (できる, 待つ, ある, etc.), so Step 6's idempotency check very often resolves to
Skip/Overwrite/Rename for a word already extracted from an earlier lesson. Under the original
draft, "Skip" would mean the current lesson's own heading gets **no link at all**, silently,
forever, even though the leaf file exists and is perfectly linkable. The user has confirmed the
fix direction below; this revision rewrites the plan around it.

## Approach
Edit only Step 8 of `.cowork/skills/lesson-to-web/extract-grammar.md` (the "Consolidated-file
routing case" subsection, its Format block example, and its adjoining Rules bullets — currently
lines ~530–594), plus two small cross-reference touch-ups outside Step 8: Step 7c's
self-referential "one place in the pipeline" claim (~lines 444–454) and Step 4b's carry-forward
bullet for Vocabulary-sourced `grammar` headings (~line 146).

The corrected behavior has two independently gated tiers:

- **Container-level link** (unchanged from today): bare, anchor-less wikilink to
  `[[grammar-index/grammar/vocabulary-<pos>]]`, still gated by the existing "Only for files
  whose leaf(s) were processed by Step 7c" rule. Container link logic itself is not being
  changed — only the framing sentence around it (see below).
- **Per-child link** (new): each Vocabulary-sourced `grammar` sub-heading under a routed
  container additionally gets its own wikilink to its leaf file,
  `[[grammar-index/grammar/vocabulary/<subdir>/<slug>]]`, inserted immediately after that
  sub-heading's own heading line, using the identical insertion mechanic already specified for
  the normal case (line-immediately-after-heading insertion, `re.subn`-with-verification,
  `# Summary` slice guard, duplicate-heading-text narrowing via the Step 4 heading tree). Its
  gate is **dedup only** — "is this exact link already present under this heading" — never
  Step 6's Created/Skip/Rename outcome. Step 6's Skip/Overwrite/Rename prompt already is the
  "inform the user, ask what to do" mechanism the user wants for a recurring word; nothing new
  is added there. What changes is what happens *after* that choice: regardless of which of
  Skip/Overwrite/Rename was picked, Step 8 still links the current lesson's heading to the
  resulting leaf file's path (existing, overwritten, or renamed).

This exactly mirrors the reasoning Step 7c already documents for its own append logic ("this is
the one place in the pipeline that deliberately does not inherit the Created-only gate"). Once
the per-child link is added to Step 8, Step 7c is no longer the *only* such place, so that
self-referential sentence in Step 7c needs a one-line correction to stay accurate (it does not
need any logic change).

The "deliberate, accepted regression" framing sentence in Step 8's consolidated-routing
paragraph stays, but narrowed in scope: it is true only of the **container-level** link (a
lesson's vocabulary entries can scatter across shared-file themes, so the container link
genuinely cannot be a precise per-item anchor) — it must not be read as implying no per-word
link exists at all, now that the per-child link covers that.

Step 4b's carry-forward bullet for `grammar` headings sourced from `Vocabulary` already says
"step 8 applies normally," which is the likely source of the original ambiguity — Step 8's own
vocabulary-specific behavior (container vs. per-child gating) was never spelled out there. Add
a one-line cross-reference so a reader of Step 4b isn't misled into thinking only the container
gets a link.

## Steps

1. **Edit `.cowork/skills/lesson-to-web/extract-grammar.md`, Step 8 "Format" block
   (~lines 535–542).**
   Add a second worked example directly after the existing single-heading example, showing both
   tiers together in one block:
   ```
   ## Verbs
   → [[grammar-index/grammar/vocabulary-verbs]]

   ### 勉強 - learn
   → [[grammar-index/grammar/vocabulary/Verbs/benkyou-learn]]

   雰囲気の勉強をしています...
   ```
   Caption it clearly as "for a routed Vocabulary POS container, both the container heading and
   each child heading receive their own link" so the two-tier behavior is visible as a concrete
   example, not just prose.

2. **Edit the Step 8 "Consolidated-file routing case" paragraph (~lines 544–550).**
   - Keep the existing description of the container-level bare link
     (`[[grammar-index/grammar/vocabulary-<pos>]]`) and its rationale (no per-lesson anchor
     exists inside the thematically-grouped shared file).
   - **Narrow** the "deliberate, accepted regression" sentence to state explicitly it describes
     the **container link only** — do not delete it outright (the reviewer confirmed it's still
     accurate for that link specifically), but add a clause pointing to the new "Per-child link"
     description so it isn't misread as "no per-word link exists."
   - **Add a new "Per-child link (routed containers only)" subsection** directly after it,
     stating:
     - Target: `[[grammar-index/grammar/vocabulary/<subdir>/<slug>]]`, inserted immediately
       after that child heading's own line, same mechanic as the normal case.
     - This link is inserted **regardless of whether Step 6 resulted in Created, Skip, or
       Rename** for that child's leaf file — explicitly call out that Skip is the *common* case
       for vocabulary (recurring words like できる, 待つ, ある), not an edge case, so this is not
       optional robustness but the primary path.
     - The **only** gate is the dedup check (link already present under that heading) — it does
       **not** inherit the "Only for files Created in step 7" gate that governs the container
       link and normal grammar/container links elsewhere in Step 8.
     - Cross-reference Step 7c's identical reasoning for not inheriting that gate.

3. **Edit the Step 8 "Rules" bullet list (~lines 552–556)** to split the gate explicitly by
   link tier instead of one shared bullet:
   - **Container-level link and normal (non-routed) links:** keep the existing gate —
     only for files Created in step 7 (or, for the container link specifically, for headings
     whose leaf(s) were processed by Step 7c) — skip if the leaf was skipped in step 6.
   - **Per-child link (routed containers only), new bullet:** insert regardless of Step 6's
     Created/Skip/Rename outcome for that child's leaf — gated **only** by the dedup rule below.
     State plainly this bullet intentionally does not reference "Created" at all.
   - **Dedup bullet, extended to three cases:**
     - normal case: skip if `[[grammar-index/grammar/<slug>]]` already present under that
       heading
     - container link: skip if `[[grammar-index/grammar/vocabulary-<pos>]]` already present
       under that heading
     - per-child link: skip if `[[grammar-index/grammar/vocabulary/<subdir>/<slug>]]` already
       present under **that child's own heading** — checked independently of the container's
       dedup check, not shared with it
   - **Duplicate heading texts bullet:** add one clause confirming this rule (narrow by the
     Step 4 heading tree's parent-section line range) applies identically to child headings —
     a vocabulary word heading that repeats verbatim across the lesson must not get its link
     misattributed to the wrong occurrence.
   - Leave the remaining bullets (Python locate-and-insert mechanics, `# Summary` slice-first
     requirement, never touch `<!--ID:-->` lines, never read/write past `# Summary`) unchanged —
     confirm during self-review (step 6 below) that they already read generically enough to
     cover both tiers without wording changes.

4. **Edit Step 7c's gate-reasoning paragraph (~lines 444–454)** — one-line correction only, no
   logic change. The current text claims: "This is the one place in the pipeline that
   deliberately does not inherit the 'Created only' gate used everywhere else (Step 8, Step 9)
   — do not 'fix' it into matching Step 8/9's gate." Once Step 8's per-child link also bypasses
   the Created-only gate (step 2/3 above), this is no longer accurate. Replace it with wording
   that: (a) points to Step 8's new per-child link rule as the other place that shares this
   reasoning, and (b) keeps Step 9 (and Step 8's *container*-level link) as still using the
   Created-only gate — so the "do not fix it to match" caution still applies, just against the
   correct remaining targets.

5. **Edit Step 4b's carry-forward bullet for Vocabulary-sourced `grammar` headings (~line 146)**
   — currently: "`grammar` from `Vocabulary` → `grammar-index/grammar/vocabulary/<subdir>/<slug>.md`
   (vocabulary file format, step 7b; step 8 applies normally)". Add a clause cross-referencing
   that under a routed POS container, "step 8 applies normally" specifically means this heading
   also gets its own per-child link (in addition to the container's bare link) — pointing to
   Step 8's new "Per-child link" subsection so a reader doesn't stop at "applies normally" and
   assume only the container link exists.

6. **No change to Step 6** (`.cowork/skills/lesson-to-web/extract-grammar.md` ~lines 230–262).
   Confirmed (read-only) that the existing Skip/Overwrite/Rename prompt already is the
   "inform the user, ask what to do" mechanism the user asked for — no new confirmation step is
   being added. This plan only changes what Step 8 does *after* that choice is made.

7. **No change to Step 10's completion report format** (~lines 694–724) — the existing
   `[Vocabulary]` example (`Created:` / `Appended:` lines) does not call out lesson-file
   wikilink insertions for the normal `文法` case either, so adding per-child link mentions here
   would be an inconsistent special case. The existing `[WARN]` collection mechanism (Step 8's
   insertion-verification rule) already generalizes to cover insertion failures for both link
   tiers without any report-template change.

8. **No `.claude/commands/` change needed** — this edits behavior within the existing
   `lesson-to-web/extract-grammar` skill; the trigger and command stub are unchanged.

9. **Self-review after edit** — re-read the fully edited Step 8 section end-to-end to confirm:
   - the container-link behavior and its gate are unchanged from today
   - the per-child link is fully specified (target path pattern, insertion point, dedup-only
     gate, duplicate-heading narrowing) and its gate is explicitly **not** tied to Step 6's
     Created/Skip/Rename outcome anywhere in the wording
   - the "deliberate, accepted regression" sentence reads as scoped to the container link only
   - Step 7c's corrected sentence and Step 4b's added cross-reference both point at the right
     subsection and don't contradict the rest of Step 8
   - grep `extract-grammar.md` for "accepted regression" and "deliberately does not inherit" to
     confirm no orphaned/contradictory copy remains after the edits

## Risks
- This is a `.cowork/skills/` prose/logic edit only — no lesson files, no `<!--ID:-->` lines,
  no `TARGET DECK` lines, and no `# Summary` sections are touched by this plan itself.
- **Behavior change to flag explicitly:** before this fix, "Skip" at Step 6 for a vocabulary
  leaf meant the current lesson's heading got no link, ever. After this fix, "Skip" (the common
  case for recurring vocabulary) will still produce a `→ [[...]]` line under the current
  lesson's heading, linking to the pre-existing leaf file. This means future extraction runs
  will write more `→ [[...]]` lines into lesson files above their `# Summary` line than before
  — this is the intended effect (already manually validated on UN5GL7.md) and is bounded by the
  same `# Summary` slice guard and `<!--ID:-->` protection already in place for every other
  Step 8 insertion, but call it out to the user before running skill-implementer since it
  changes observable output on every future vocabulary-container extraction, not just this one
  historical file.
- If the per-child gate wording is loose about "regardless of Created/Skip/Rename," a future
  reader could still misread it as inheriting the shared Created-only gate by proximity to the
  container-link bullet directly above it in the Rules list — the split into two clearly
  separate, explicitly-labeled bullets (step 3 above) is required, not optional, to prevent this.
- If the "child heading" scope is too loose, a future run could misattribute a leaf link to the
  wrong occurrence when heading text repeats — the existing "duplicate heading texts" narrowing
  rule must be explicitly extended to the per-child case (covered by step 3's fourth bullet).
