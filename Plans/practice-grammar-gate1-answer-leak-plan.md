# Practice Grammar — Gate 1 answer-leak fix

## Goal
Fix a real exercise-generation quality bug in `lesson-grammar-practice` /
`scheduled-grammar-practice`: Gate 1 of the shared "Non-trivial exercise
checklist" only checked that the grammar point's *name* wasn't mentioned in
the prompt. It never checked whether the prompt already contained the
*complete, fully-formed answer sentence* itself. A real session produced this
exercise for the `個` general-counter point (source:
`JPLessons/Udemy/N5/Grammar/UN5GL9.md`):

> 店（みせ）で卵（たまご）を8個（こ）買（か）いました。この文（ぶん）を完全（かんぜん）な文（ぶん）で言（い）ってください。

The prompt already contains the finished answer (卵を8個買いました) — there
is nothing left for the student to produce. This should have been a Type 3
(Description → production) exercise instead. The underlying rule ("don't
name what the student must produce") was too narrow — it covered naming the
*grammar form* but not handing over the *complete realized sentence*.

## Approach
Rewrite Gate 1 in `.cowork/skills/_practice-grammar-common.md` (currently
lines 286–295) to state two checks instead of one:

1. Keep the existing rule — grammar point name/form must not be named in the
   prompt (still a real, valid failure mode; unchanged in substance).
2. Add a new, precise, mechanically-checkable rule: extract the exact string
   the student must produce, and confirm it does not already appear
   complete and intact anywhere in the prompt, in any language (Japanese
   included) — scene-setting description is fine, a pre-stated finished
   answer is not. Includes a named banned template (complete sentence +
   "say/write/repeat this in complete form") as a concrete negative example
   the model can pattern-match against.

This wording is intentionally generic rather than enumerated per exercise
type — it applies uniformly to Types 1–6 (including discrimination blanks,
sentence ordering, passage grammar) without needing type-by-type callouts,
per the user's explicit "keep it precise, not long" requirement. Gates 2 and
3 are untouched — this is a single, scoped replacement of the Gate 1 block
only.

## Steps
1. Open `.cowork/skills/_practice-grammar-common.md`.
2. Replace the current Gate 1 block (lines 286–295, starting `**Gate 1 —
   Prompt does not leak the answer — grammar point name must not appear
   anywhere...**` through `...never before.`) with the following exact
   text, keeping the surrounding blank lines and the `**Gate 2 —
   ...**` block immediately after untouched:

   ```
   **Gate 1 — Prompt does not leak the answer.**

   1. Grammar-point name/form must not be named anywhere in the prompt. A
      prompt like "Translate to Japanese: 'I decided to go to graduate
      school'" is fine — the form (ことにしました) is not named. "Use
      ことにする to say you decided to quit" fails — rewrite as a neutral
      translation/context prompt.
   2. Extract the exact string the student must produce. Confirm it does not
      already appear complete and intact anywhere in the prompt, in any
      language — Japanese included. Describing or setting a scene (English,
      Polish, or Japanese) is fine; pre-stating the finished answer is not.
      **Banned template:** a complete target sentence followed by an
      instruction like "say/write/repeat this sentence in complete form" —
      this hands over the answer and always fails Gate 1.

   The grammar point name (and the answer itself) may appear in grading
   feedback after the student submits — never before.
   ```

3. Verify the "Non-trivial exercise checklist — mandatory" lead-in
   (immediately above Gate 1, currently lines 282–284) still reads correctly
   against the renamed/restructured Gate 1 heading — no change needed there,
   just confirm no dangling reference to the old single-paragraph Gate 1
   wording elsewhere in the file (none found in the current read; re-check
   after editing).
4. No other file changes. `lesson-grammar-practice.md` and
   `scheduled-grammar-practice.md` both load this shared file and inherit
   the fix automatically — no changes needed in either trigger skill.
5. No slash-command or agent changes — this is a content-only edit to an
   existing shared skill file, not a new skill.

## Risks
- Scope discipline: only lines 286–295 (the Gate 1 block) change. Gates 2
  and 3, the checklist lead-in, and everything else in the file must be
  byte-identical before/after except for the Gate 1 replacement.
- Stale dead file: `practice-grammar.md` at the vault root (pre-split legacy
  copy, ~45KB, last modified before the skill was split into
  `_practice-grammar-common.md` + `lesson-grammar-practice.md` +
  `scheduled-grammar-practice.md`) contains an identical, now-outdated Gate 1
  paragraph. It is not referenced by any current trigger skill and is not
  in scope for this plan — flagged here for awareness only. Cleaning it up
  is a separate decision the user has not yet made.
- No plugin-export risk — this edit touches only a `.cowork/skills/` file,
  never lesson files, `TARGET DECK` lines, or `<!--ID:-->` lines.
