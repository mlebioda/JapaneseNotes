# Practice Grammar — Exercise Type Redesign

## Goal

Replace the current four loose exercise types in `practice-grammar.md` with six well-defined, JLPT-aligned exercise types and a deterministic selection rule. The current design allows a single-point fill-in-blank pattern (e.g. "fill in ぜひ") that is too easy and does not resemble JLPT difficulty. The redesign also tightens grading feedback so errors are categorised precisely (e.g. "used つもり (intention) but the situation requires a completed decision → ことにした") rather than a generic "incorrect."

## Approach

The exercise type list and the selection rule both live in the `## Exercise generation` section of `.cowork/skills/practice-grammar.md` (lines 108–128). Those lines are the sole target of this change. No other section of the skill file changes: parsing, interaction flow, grading tolerance, persistence, and calendar sync are untouched. The six new types fully replace the four old types — no migration, clean replacement. The selection rule replaces the current "Variety" bullet. The hidden-target and grading rules are extended in their respective sections.

## Steps

1. **Replace the exercise type bullet list** — lines 108–119 in `.cowork/skills/practice-grammar.md`.

   Remove the four old type bullets entirely (no migration):
   - "Translate to Japanese"
   - "Fill the blank"
   - "Choose the correct form"
   - "Build from pieces"

   Replace with the six approved types (full descriptions in the Reference section below).

2. **Replace the selection rule** — replace the current "Variety" bullet with the deterministic selection rule.

   New rule:
   - Single nuanced word/expression (ぜひ, きっと, etc.) → Type 1 or Type 6
   - Group of similar forms (conditionals, て-forms, aspect pairs) → Type 2 or Type 4; Type 2 requires all four choices to be genuinely confusable (see confusability definition in Reference) — never use it for a single grammar point where the choice is obvious
   - Counters, classifiers, specific constructions → Type 3
   - Grammar points with rich context dependency → Type 5
   - Any grammar point the student has already seen in a prior session (recorded in grammar-state.json) → prefer Type 6

   Variety rule: type selection is driven by what the grammar point needs (see selection logic above). Vary types only when multiple types are equally valid for a given grammar point. Never override the pedagogically correct type just for variety.

3. **Add and tighten the hidden-target rule** — the existing Gate 1 ("Prompt does not leak the answer") must explicitly reference the grammar-name suppression rule:

   - Claude holds the target grammar point name internally and must never surface it before the student submits their answer.
   - Exercise title format is `Exercise N / T` only — no `— grammar point: X` appended.
   - The `[use case: …]` label is also suppressed from output (already noted in the skill — extend the note to cover the grammar point name too).
   - Grammar point name may appear in grading feedback after the student submits an answer. It must never appear in the exercise prompt.

   Update Gate 1 wording to: "Prompt does not leak the answer — grammar point name must not appear anywhere in the exercise shown to the student before they answer."

4. **Tighten grading feedback** — in the `## Grading` section (lines 229–240), add after the "Weak-point strings" rule:

   Feedback must name the specific semantic or grammatical mismatch, not just flag it as wrong. Format: `"you used X (meaning/use) but the situation requires Y (meaning/use)"`. Example: `"you used つもりです (future intention) but the situation calls for a completed decision → ことにした"`.

   Grammar point name is allowed in grading feedback (after submission) — this is pedagogically useful as it confirms what was being tested.

5. **Update the batch-mode layout example** — remove the `— grammar point: …` and `[use case: …]` labels from the exercise header line. The only visible header is `Exercise N / T`. Update the explanatory note below the example to state that both the grammar-point name and the use-case label are suppressed from the exercise prompt (Claude holds them internally only).

6. **Add grading rules for Types 5 and 6** — extend the `## Grading` section with type-specific grading rules:

   - **Type 5 (passage grammar)**: mark correct or incorrect AND explain why the chosen option does not fit the passage context, citing the surrounding sentences as evidence. Also explain why the correct option does fit.
   - **Type 6 (bolded form → explain)**: semantic evaluation, not right/wrong. Grade on (a) whether the student correctly identified the meaning of the bolded form, and (b) whether they explained the contrast with the obvious alternative. Evaluate the quality of the explanation rather than matching a fixed answer.

7. **Add weak-point bias rule** — in the selection rule or a dedicated note in `## Exercise generation`:

   For weak-point reinforcement (a point with low SM-2 ease or recent failure), prefer Type 1 or Type 3. Avoid Types 5 and 6 when targeting known weak conjugations — those types test comprehension and meta-awareness, not production accuracy.

8. **Add session summary exemption note** — add an explicit note near the hidden-target rule:

   Grammar point headers are permitted in the post-session summary. The session is over at that point and exposure is appropriate for review.

## File paths

- `.cowork/skills/practice-grammar.md` — only file modified

## Risks

- The skill file is in `.cowork/skills/` — it is protected by the vault rule "Never modify files in .cowork/ without permission." This plan has user approval.
- No Anki export data, `<!--ID:-->` lines, or `# Summary` sections are involved — risk is low.
- The batch-mode layout change (step 5) removes information that was previously shown to the user (the grammar point name in the exercise header). This is intentional: the grammar point name leaked the tested structure. The session header still announces the grammar point count and lesson code, so the user retains orientation.
- The grading extension for Types 5 and 6 (step 6) adds evaluation criteria that did not exist before. If the grading section is long, verify the new rules do not create conflicts with the existing tolerance/leniency guidelines.

---

## Reference — Six approved exercise types

### Type 1 — Contextual production
Situation described in English/Polish, no grammar named. Student writes natural Japanese. Claude internally knows the target grammar and grades on whether it was used correctly and naturally.
Example prompt: "A new ramen restaurant opened near the station. Write a natural Japanese sentence strongly encouraging your friend to come try it." (internal target: ぜひ)

### Type 2 — Discrimination fill-in-blank
One gap, four choices — ALL four must be genuinely confusable. Confusability definition: all four choices must be grammatically plausible in the given sentence; the lesson must contain at least two forms that share a morphological relationship with the target (e.g. all conditionals, all て-forms, all aspect pairs). ONLY used when there is a group of similar forms in the lesson. Never used for a single grammar point where the choice is obvious.
Example: もっと練習（れんしゅう）する（　　）、上手（じょうず）になりますよ。 1.と 2.ば 3.たら 4.なら

### Type 3 — Description → production
Claude describes a concrete situation without naming or hinting at the grammar. Student must produce the correct form, counter, or structure.
Example A (counters): "You went shopping: three apples, two books, and one dog. Tell me what you bought in Japanese."
Example B (noun-modifying): "Your friend asks which café you want to go to. Describe it in one sentence without using its name."

### Type 4 — JLPT sentence ordering (文の組み立て)
A sentence is broken into scrambled fragments. One position is marked ★. Student places the fragments in the correct order. The grammar form is never named.
Example: 田中（たなか）さんは __ ★ __ しました。fragments: [ジムに通（かよ）う / ことに / 来年（らいねん）から]

### Type 5 — JLPT passage grammar (文章の文法)
A short natural paragraph (3–5 sentences) with one or two numbered blanks. Student picks which option fits the passage context. Surrounding sentences provide natural context clues, not grammar hints.
Grading: correct or incorrect + explain why the chosen option does not fit the passage context (use surrounding sentences as evidence) + explain why the correct option does fit.

### Type 6 — Bolded form → explain
Claude writes a sentence with the target grammar bolded. Student explains: what does this form mean here, and why is it used (not a different form).
Example: "田中（たなか）さんはジムに通（かよ）う**ことにしました**。 — What does the bolded part express, and why not つもりです here?"
Grading: semantic evaluation — grade on (a) whether the student correctly identified the meaning of the bolded form, and (b) whether they explained the contrast with the obvious alternative. Evaluate quality of explanation, not a fixed answer match.
