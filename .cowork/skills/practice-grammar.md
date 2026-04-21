---
name: practice-grammar
description: >
  Interactive grammar practice session driven by a single lesson file. Extracts
  grammar points from the 文法 section, generates exercises using vocabulary from
  the Summary section (plus N5-level fillers), grades answers, and writes results
  to the spaced-repetition state file so they can be prioritized by repeat-grammar.
  Trigger: user says "let's practice <filename>", "practice <lesson>",
  "exercise <lesson>", or similar.
---

# Practice Grammar Skill

## Trigger

User says any of:
- "Let's practice UN5GL14" / "Let's practice <filename>"
- "practice <lesson>"
- "exercise <lesson>"
- "drill grammar in <lesson>"

If user references a lesson by code only (e.g. `UN5GL14`), find the file under `JPLessons/Udemy/N<level>/Gramatyka/` — match by prefix, ignore trailing description in filename.

---

## Workflow

1. **Find the lesson file** — by code or filename
2. **Parse the 文法 section** — collect every grammar point (see **Parsing**)
3. **Parse the Summary section** — collect vocabulary (Japanese word + translation pairs)
4. **Load `.cowork/progress/grammar-state.json`** — if the file does not exist yet, treat state as empty. Pick up any prior `weak_points` for these grammar points so exercises can stress them.
5. **Generate the exercise set** — one exercise per grammar point (see **Exercise generation**). If a grammar point has recorded weak_points, bias that exercise toward the weak aspect.
6. **Run the session interactively** — present exercises one at a time. After each answer, grade it (see **Grading**), give brief feedback, ask the user to self-score 1–4 (fail / hard / good / easy). Accept the score, move to the next exercise.
7. **After the last exercise** — write a summary of what went well and what needs more practice.
8. **Persist results** — update `grammar-state.json` and append a session log (see **Persistence**).

No confirmation needed at any step — start practicing immediately after the user triggers the skill.

---

## Parsing

### 文法 section

Find the line matching `^# 文法` (exact `#` level — the section heading). Collect content until the next `#` heading of the same level (e.g. `# Vocabulary`, `# Summary`).

Inside this section:
- Every `## Heading` is a top-level grammar point — always include.
- Every `### Heading` under a `##` that contains only `###` subpoints (no prose of its own) becomes a grammar point on its own. If the `##` has both prose and `###` children, include the `##` only (same rule as grammar-summary skill).
- Preserve Japanese characters exactly.

Build a list of `{grammar_header, body_text}` pairs. The body text (Structure blocks, examples under the heading) is what you use to generate exercises.

### Summary section

Find the line matching `^# Summary`. Below it, every non-verb/non-adjective card is shaped:

```
<translation>  #card
Tłumaczenie: <Japanese>
<!--ID: ...-->
```

Collect `{translation, japanese}` pairs from these cards — this is the vocabulary pool for exercises. Skip verb-conjugation cards (`ほんやく:` + `ます形:` etc.) and adjective cards (they have `過去形:`) — those are useful as reference but not as exercise fillers.

### Grammar point ID

Build a stable ID: `<lesson-code>::<slug>` where slug is the grammar header romanized/simplified — lowercase, non-alphanumeric collapsed to `-`, trimmed. Keep the **original Japanese heading** in the state entry too (`grammar_header`), since the slug may not round-trip.

Example: header `Vないで ください` → slug `vnaide-kudasai` → id `UN5GL14::vnaide-kudasai`.

---

## Exercise generation

For each grammar point, produce **one** exercise. Pick the type that best tests the specific point:

- **Translate to Japanese** — Polish/English prompt, user writes Japanese. Best for sentence-pattern grammar (てください, なくてもいい, だけ, が-contrast).
- **Fill the blank** — Japanese sentence with a gap, user fills the grammar form. Best for verb conjugation and particle choice.
- **Choose the correct form** — two or three candidate forms shown, user picks. Best for contrasts (Vない vs なくても, が vs で).
- **Build from pieces** — scrambled words + particles, user assembles. Best for noun-modifying-verb patterns.

**Vocabulary rule** — the content words in the exercise must come from the Summary pool first. Only reach for outside vocabulary if the Summary pool cannot express the grammar point. Any outside vocabulary must be strict N5 level.

**Weak-point bias** — if the state entry for this grammar point has `weak_points`, design the exercise so the answer requires getting that aspect right (e.g. if the weak point is "particle placement," the exercise must have the particle in the target answer).

**Variety** — across the session, rotate exercise types; avoid running five "translate to Japanese" in a row.

---

## Interaction flow

Present exercises like this:

```
Exercise 3 / 7 — grammar point: Vない なくてもいいです

Translate to Japanese: "You don't have to book a reservation."

(use vocabulary from the lesson where possible)
```

Wait for the user's answer. Then:

```
Your answer:   予約しなくてもいいです
Expected:      予約しなくてもいいです
✓ correct

Score this one 1–4? (1=fail, 2=hard, 3=good, 4=easy)
```

If partially correct, point out the specific issue in one sentence — no lecture. Example: `missed the second に in 午後７時に` — not a paragraph of explanation.

Record for each exercise: grammar_id, score (1–4), weak_points (array of short strings — only if the user made a mistake or chose 1–2).

---

## Grading

Compare user's answer to the expected answer with tolerance:

- **Kanji vs kana** — accept either for words that have both forms, unless the exercise is specifically testing kanji.
- **Particle correctness** — strict. Wrong particle = mistake, note as weak point.
- **Verb conjugation** — strict. Wrong form = mistake.
- **Word order** — if the sentence is still grammatically valid and conveys the same meaning, accept with a note rather than mark wrong.
- **Spelling typos** — accept if the intent is clear and only one character is off.

Weak-point strings should be short and categorical: `particle に placement`, `て-form of godan verbs`, `だけ vs しか`. Not free-form sentences.

---

## Session summary

After the last exercise, show a compact summary:

```
Session complete — UN5GL14 (7 grammar points)

Solid:
  ✓ Vないで ください               score 4
  ✓ Subject + で + V              score 4
  ✓ Counter 回                     score 3

Needs practice:
  ✗ Vplain + N (noun modifier)     score 2 — N が/の particle choice
  ✗ が (but / topic intro)         score 2 — confused contrast vs topic use
  ✗ Counter 本                      score 1 — sound changes (いっぽん, さんぼん)

Next review dates written to grammar-state.json.
```

---

## Persistence

Two writes at the end of the session:

### 1. Update `.cowork/progress/grammar-state.json`

Read the file (create with `{"grammar_points": {}}` if missing). For each practiced grammar point:

- If no prior entry: create one with defaults — `interval_days: 1`, `ease: 2.5`, `streak: 0`, `total_reviews: 0`.
- Apply the algorithm based on the score the user gave:

| Score | interval_days update                         | ease update        | streak          |
|-------|----------------------------------------------|--------------------|-----------------|
| 1     | reset to 1                                   | `ease - 0.2` (min 1.3) | reset to 0  |
| 2     | `max(1, round(interval * 1.2))`              | `ease - 0.15` (min 1.3) | +1          |
| 3     | `max(1, round(interval * ease))`             | unchanged          | +1              |
| 4     | `max(1, round(interval * ease * 1.3))`       | `ease + 0.15`      | +1              |

- If it's the first review (streak was 0 before), force `interval_days = 1` regardless of score ≥ 2.
- Compute `next_review = today + interval_days` (ISO date, YYYY-MM-DD).
- Set `last_reviewed = today`, `last_score`, `total_reviews += 1`.
- Merge weak_points: union with existing `weak_points`, deduped, keep most recent 5.

Example entry shape:

```json
{
  "grammar_points": {
    "UN5GL14::vnaide-kudasai": {
      "lesson_file": "JPLessons/Udemy/N5/Gramatyka/UN5GL14.md",
      "grammar_header": "Vないで ください",
      "last_reviewed": "2026-04-21",
      "next_review": "2026-04-24",
      "interval_days": 3,
      "ease": 2.5,
      "streak": 1,
      "total_reviews": 1,
      "last_score": 3,
      "weak_points": []
    }
  }
}
```

Keep JSON pretty-printed with 2-space indent so diffs are readable.

### 2. Append session log

Write `.cowork/progress/sessions/<YYYY-MM-DD>-<lesson-code>.md`. If a file for the same day + lesson already exists, append with a `---` separator and a new timestamp heading.

```markdown
---
date: 2026-04-21
time: 19:32
lesson: UN5GL14
lesson_file: JPLessons/Udemy/N5/Gramatyka/UN5GL14.md
total_exercises: 7
average_score: 2.9
---

## Results

| Grammar point | Score | Weak points |
|---|---|---|
| Vないで ください | 4 | — |
| Vない なくてもいいです | 3 | — |
| Vplain + N | 2 | N が/の particle choice |
| が (but / topic) | 2 | contrast vs topic use |
| Subject + で + V | 4 | — |
| N + だけ | 3 | — |
| Counter 本 | 1 | sound changes (いっぽん, さんぼん) |

## Transcript

### Exercise 1 — Vないで ください
Prompt: Translate to Japanese — "Please don't use a cellphone in the hospital."
User:    病院で携帯電話を使わないでください
Correct: 病院で携帯電話を使わないでください
Result:  ✓ score 4

### Exercise 2 — Vない なくてもいいです
...
```

---

## Never touch
- TARGET DECK line
- `<!--ID: -->` lines
- Anything inside the lesson file — this skill is **read-only on lessons**
- Do not modify other skill files or the instructions file
