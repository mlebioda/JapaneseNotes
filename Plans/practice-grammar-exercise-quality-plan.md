# Plan: Practice Grammar — Exercise Quality & Use-Case Coverage

**Date:** 2026-06-06
**Target file:** `.cowork/skills/practice-grammar.md`
**Status:** ready for implementation

---

## Background

Two problems were identified with the current `practice-grammar` skill:

1. **Trivial exercises** — the skill already has one anti-trivial rule ("Avoid trivial fill-the-blank"), but it is narrow: it only bans single-obvious-particle fill-ins, and only for fill-the-blank type. In practice, exercises also fail in other ways: the prompt text restates the answer directly, or an exercise asks the user to conjugate a single character. These cases are not covered.

2. **One exercise per grammar point regardless of content** — a grammar point like `名詞 + 中（ちゅう・じゅう）` has three distinct use cases (N + ちゅう = ongoing state, N + ちゅう = time period, N + じゅう = whole area/place). Generating one exercise covers at most one use case and gives the user false confidence. The fix is to generate one exercise per use case defined in the source file.

The user has confirmed:
- No upper cap on exercises per grammar point — use all use cases found in the source.
- SM-2 tracking stays **one score per grammar point**, not per use case. All exercises for a point in a session feed one shared self-score.

---

## Change 1: Stronger anti-trivial rules

### Problem details

The current rule says:

> "If the answer could be guessed without knowing the grammar (e.g. filling in か when the surrounding sentence makes it the only possible word), switch to a translate-to-Japanese exercise instead."

This covers one specific failure mode. Two others are not covered:

**A. Prompt leaks the answer.** The prompt text contains the exact word, form, or pattern the user must produce. Example: asking the user to "use こと に する" in a sentence when the prompt says "use こと に する to express a decision." The user just copies the prompt text. This applies to all exercise types.

**B. Single-character conjugation target.** The blank (or the required change) is a single syllable where the challenge is near-zero. Example: for `ない形`, showing `食べ___` and asking the user to fill `ない`. The only possible answer for a known G2 verb is `ない`; this tests nothing. Same failure: showing a ます-stem and asking the user to add `ます`.

### Fix

Replace the current "Avoid trivial fill-the-blank" paragraph with a broader **Non-trivial exercise checklist** that applies before any exercise is output. The checklist has three gates, all of which must pass:

**Gate 1 — Prompt does not leak the answer.** The prompt must not contain, quote, or directly name the exact form the user must produce. A prompt like "Translate to Japanese: 'I decided to go to graduate school'" is fine — the grammar form (ことにしました) is not named. A prompt like "Use ことにする to say you decided to quit" fails because it names the form; rewrite as a neutral translation or context prompt.

**Gate 2 — Answer requires genuinely using the grammar point.** A native speaker who does not know this grammar point but knows vocabulary could not produce the answer by elimination or by copying surrounding text. If they could, the exercise type must be upgraded (e.g. fill-the-blank → translate-to-Japanese).

**Gate 3 — Conjugation target is not a single morpheme.** If the answer requires adding or changing only one particle or suffix (ない, ます, か) to a fully given stem, the exercise is too narrow. The exercise must require the user to produce the whole grammatical construction, not just append one character. Exception: exercises that are explicitly testing a single distinction (e.g. rendaku in counters, sound change in irregular forms like いっぽん) are allowed, because the tested knowledge is genuinely difficult and cannot be widened.

---

## Change 2: One exercise per use case, SM-2 per grammar point

### Problem details

The current skill says in step 6: "Generate the exercise set — one exercise per grammar point." This is a hard limit that ignores the internal structure of many grammar points.

Many grammar points have explicit use cases in the source:
- Listed as `### Use cases` sections with numbered items
- Distinct structural variants documented under `### Structure` (e.g. `V「dict」+ の`, `V「た」+ の`, `いadj + の`, `なadj + な + の` are four distinct uses of の名詞化)
- Sub-variants that differ in meaning (e.g. ちゅう vs じゅう reading of 中 with different semantics)

Currently a grammar point with three use cases gets one exercise — meaning two of the three use cases are never drilled.

### Fix

#### Use case extraction (parsing step)

During parsing, after building the `{grammar_header, body_text, source_section}` triple for each grammar point, identify the use cases within it:

1. If the grammar point body contains a `### Use cases` section, each numbered item in that list is one use case. Extract the item number and its description as the use case label.
2. If the grammar point body contains a `### Structure` section with multiple bullet variants (each starting with `V「...」` or `N + ...` or `いadj`/`なadj` with distinct structures), each top-level variant is one use case.
3. If neither applies — the grammar point body is prose/examples only with no explicit structural variants — treat the whole grammar point as one use case.
4. Minimum: every grammar point yields at least one use case. There is no maximum.

The use case label is used only for internal exercise generation — it is not shown to the user in the exercise prompt (showing it would leak the answer).

#### Exercise generation change

Replace the single "one exercise per grammar point" rule with:

> For each grammar point, generate one exercise per use case. The exercise must target that specific use case — not a generic demonstration of the grammar point. Use case label must not appear in the prompt text. If the grammar point has recorded `weak_points`, prioritize the use case(s) that match the weak point in exercises for that use case.

Session total is now the sum of all exercises across all grammar points (sum of use cases, not count of grammar points).

The `Exercise N / T` progress indicator still uses the total exercise count (not the grammar point count), so the user always sees the correct position.

#### Session summary change

The summary currently lists one row per grammar point. With multiple exercises per grammar point, a single grammar point may now contribute multiple exercises, each potentially graded differently. Summarize at the **grammar point level**, not the exercise level, since SM-2 tracks at that level. If any exercise for a grammar point scored 1–2, the grammar point goes to "Needs practice."

The summary format stays the same except replace the single score with the range or worst score:

```
Needs practice:
  ✗ 名詞 + 中（ちゅう・じゅう）     scores 4 / 2 / 1 — じゅう whole-area reading
```

Show individual exercise scores for points that had multiple exercises, to help the user see which use case failed.

#### Persistence change

SM-2 state remains one entry per grammar point. The score used for the SM-2 update after a multi-exercise session is the **minimum** self-score given across all exercises for that grammar point. Rationale: if the user aced two of three use cases but failed one, they have not mastered the grammar point and should review it sooner.

The `weak_points` merge logic is unchanged — aggregate all weak points from all exercises for the grammar point.

---

## Sections of the skill file to modify

| Section | What changes |
|---------|--------------|
| **Workflow, step 6** | Change "one exercise per grammar point" → "one exercise per use case per grammar point" |
| **Parsing — Grammar topics** | Add use case extraction sub-step after building the triple |
| **Exercise generation** | Replace "Avoid trivial fill-the-blank" paragraph with the three-gate non-trivial checklist; replace the single-exercise-per-point rule with per-use-case rule |
| **Interaction flow — Batch mode** | Update session header format: `Session: UN4GL7 — 14 exercises across 9 grammar points` (show both counts); `Exercise N / T` total is exercise count |
| **Session summary** | Update to show per-grammar-point roll-up with per-use-case scores when multiple exercises exist |
| **Persistence** | Add rule: when a grammar point had multiple exercises in the session, use the minimum self-score as the SM-2 input score |

No changes to: SM-2 algorithm, JSON schema, grading logic, furigana rule, vocabulary rule, interactive mode (same exercise-level flow applies), or any other section not listed above.

---

## Implementation notes for skill-implementer

- Do not add a new field to `grammar-state.json` for use cases — state stays at grammar point granularity.
- The use case extraction logic should be a clearly labelled sub-step under **Parsing**, not a separate top-level section.
- The three-gate checklist must replace (not supplement) the current "Avoid trivial fill-the-blank" paragraph — keep the file tidy.
- The batch mode session header example in the skill should show a realistic example like `Session: UN4GL7 — 14 exercises across 9 grammar points` to make the change concrete for the model.
- Gate 3's exception for explicit single-distinction tests (rendaku, sound changes) is important — do not drop it.
