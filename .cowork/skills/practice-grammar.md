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

If user references a lesson by code only (e.g. `UN5GL14`), find the file under `JPLessons/Udemy/N<level>/Grammar/` — match by prefix, ignore trailing description in filename.

---

## Workflow

1. **Find the lesson file** — by code or filename
2. **Extract everything before `# Summary`** — never read the whole lesson file. The Summary section (~70% of the file) is generated Anki cards and not needed for practice. Run:

   ```bash
   awk '/^# Summary$/{exit} {print}' "$LESSON"
   ```

   Pass only this slice to all subsequent parsing.
3. **Parse grammar topics** — from `# 文法` AND `# Vocabulary` sections (see **Parsing**)
4. **Parse vocab pool** — from `#w`, `#wc`, `#wp` lines in `# ごい` AND `# ひょうげん` (see **Parsing**)
5. **Load `.cowork/progress/grammar-state.json`** — if the file does not exist yet, treat state as empty. Pick up any prior `weak_points` for these grammar points so exercises can stress them.
6. **Generate the exercise set** — one exercise per use case per grammar point (see **Exercise generation** and **Parsing — Use case extraction**). If a grammar point has recorded weak_points, bias the exercise(s) for matching use cases toward the weak aspect. Session total = sum of all use cases across all grammar points.
7. **Run the session interactively** — present exercises one at a time. After each answer, grade it (see **Grading**), give brief feedback, ask the user to self-score 1–4 (fail / hard / good / easy). Accept the score, move to the next exercise.
8. **After the last exercise** — write a summary of what went well and what needs more practice.
9. **Persist results** — update `grammar-state.json` (see **Persistence**).

No confirmation needed at any step — start practicing immediately after the user triggers the skill.

---

## Parsing

### Grammar topics (`# 文法` and `# Vocabulary`)

Both top-level sections contain grammar points to drill. `# 文法` is core grammar; `# Vocabulary` covers more complex sentence-construction patterns that don't fit a single `#w`/`#wc`/`#wp` line. Treat them the same way.

For each section, find its `^# ` heading and collect content until the next `^# ` heading of the same level. Inside:

- Every `## Heading` is a top-level grammar point — always include.
- Every `### Heading` under a `##` that contains only `###` subpoints (no prose of its own) becomes a grammar point on its own. If the `##` has both prose and `###` children, include the `##` only (same rule as grammar-summary skill).
- Preserve Japanese characters exactly.

Build a list of `{grammar_header, body_text, source_section}` triples. The body text (Structure blocks, examples) is what generates exercises.

#### Use case extraction

After building each triple, identify the use cases within the body text:

1. **`### Use cases` section present** — each numbered item in that list is one use case. Extract the item number and its short description as the use case label (e.g. `"1. ongoing state"`, `"2. time period"`, `"3. whole area"`).
2. **`### Structure` section with multiple top-level bullet variants** — if the section contains two or more top-level bullet points each beginning with a structural pattern (`V「...」`, `N + ...`, `いadj`, `なadj`, etc.) with distinct structures, each top-level variant is one use case. Label with the pattern text (e.g. `"V「dict」+ の"`, `"V「た」+ の"`).
3. **Neither applies** — the grammar point is prose/examples only, no explicit structural variants. Treat the whole grammar point as one use case (label: the grammar header itself).

Minimum: every grammar point yields at least one use case; there is no maximum. The use case label is used only internally for exercise generation — it must **not** appear in the exercise prompt shown to the user (showing it would leak the tested structure).

### Vocab pool (`# ごい` and `# ひょうげん`)

Find both `^# ごい` and `^# ひょうげん`. Collect every `#w`, `#wc`, `#wp` line — these are the source vocabulary in the format defined by fill-templates:

```
日本語（よみ）- translation #w
日本語（よみ）- translation #wc
日本語（よみ）- translation #wp
```

Variants (same parsing rules as fill-templates):

- `日本語 (よみ) - translation` — half-width parens.
- `日本語 - translation` — no reading.
- Double-Japanese (`#wc 伝える（つた）- 伝える（つたえる）- Polish`) — use the second Japanese form.
- Strip `**` bold markers.

For each line, build `{japanese, reading, translation, type}` where `type ∈ {word, verb, adjective}` from the `#w`/`#wc`/`#wp` tag. Verb conjugations and adjective forms aren't pre-stored — derive them from rules at exercise-generation time using your Japanese knowledge.

All three types are first-class practice material — drill conjugations and form transformations, not just plain-word translation.

### Grammar point ID

Build a stable ID: `<lesson-code>::<slug>` where slug is the grammar header romanized/simplified — lowercase, non-alphanumeric collapsed to `-`, trimmed. Keep the **original Japanese heading** in the state entry too (`grammar_header`), since the slug may not round-trip.

Example: header `Vないで ください` → slug `vnaide-kudasai` → id `UN5GL14::vnaide-kudasai`.

---

## Exercise generation

For each grammar point, produce **one exercise per use case** (as extracted during parsing). Each exercise must target its specific use case — not a generic demonstration of the overall grammar point. The use case label must not appear in the prompt text. If the grammar point has recorded `weak_points`, prioritize the use case(s) that match the weak point in the exercises for that use case.

Pick the exercise type that best tests the specific use case:

- **Translate to Japanese** — Polish/English prompt, user writes Japanese. Best for sentence-pattern grammar (てください, なくてもいい, だけ, が-contrast).
- **Fill the blank** — Japanese sentence with a gap, user fills the grammar form. Best for verb conjugation and particle choice.
- **Choose the correct form** — two or three candidate forms shown, user picks. Best for contrasts (Vない vs なくても, が vs で).
- **Build from pieces** — scrambled words + particles, user assembles. Best for noun-modifying-verb patterns.

**Furigana rule — mandatory.** Every kanji character that appears in an exercise (sentence, prompt, choices, fragments, hint text) **must** have furigana. Use vault inline style: kanji immediately followed by the reading in full-width parentheses, e.g. `名刺（めいし）`, `病院（びょういん）`, `食（た）べる`. Before outputting each exercise, scan every kanji in it and verify furigana is present — no exceptions, including words from the vocab pool, example sentences, and grammar point context.

**Vocabulary rule** — content words in the exercise must come from the vocab pool (`# ごい` + `# ひょうげん`) first. Only reach for outside vocabulary if the pool cannot express the grammar point. Any outside vocabulary must be strict N5 level.

**Weak-point bias** — if the state entry for this grammar point has `weak_points`, design the exercise so the answer requires getting that aspect right (e.g. if the weak point is "particle placement," the exercise must have the particle in the target answer).

**Variety** — across the session, rotate exercise types; avoid running five "translate to Japanese" in a row.

**Non-trivial exercise checklist — mandatory.** Before outputting any exercise, verify all three gates pass. If a gate fails, redesign the exercise (change type or rewrite the prompt) until it passes all three.

**Gate 1 — Prompt does not leak the answer.** The prompt must not contain, quote, or directly name the exact form the user must produce. A prompt like "Translate to Japanese: 'I decided to go to graduate school'" is fine — the grammar form (ことにしました) is not named in the prompt. A prompt like "Use ことにする to say you decided to quit" fails because it names the target form; rewrite as a neutral translation or context prompt instead.

**Gate 2 — Answer requires genuinely using the grammar point.** A native speaker who does not know this grammar point but knows vocabulary could not produce the answer by elimination or by copying surrounding text. If they could, upgrade the exercise type (e.g. fill-the-blank → translate-to-Japanese).

**Gate 3 — Conjugation target is not a single morpheme.** If the answer requires adding or changing only one particle or suffix (ない, ます, か) to a fully given stem, the exercise is too narrow. The exercise must require the user to produce the whole grammatical construction, not just append one character to a given stem. Exception: exercises explicitly testing a single difficult distinction (e.g. rendaku in counters, sound changes in irregular forms like いっぽん, さんぼん) are allowed, because the tested knowledge is genuinely difficult and cannot be meaningfully widened.

---

## Interaction flow

There are two modes — **batch** (default) and **interactive**. Pick batch unless the user explicitly asks for one-at-a-time.

**Progress indicator — required.** Every exercise prompt MUST start with `Exercise <current> / <total>` so the user always knows where they are in the session. `<current>` is 1-based (first exercise is `1 / N`, last is `N / N`). The total is fixed at the start of the session and does not change mid-session.

### Batch mode (default — works on flaky connections)

Print **all** exercises at once in a single message. Number them, include the grammar point header, and put the prompt on its own. No expected answers, no hints that reveal the form. The user replies once with all answers (numbered or in order). Then grade everything in one follow-up message and ask for self-scores in one batch.

The session header must show both the exercise count and the grammar point count. The `Exercise N / T` progress indicator uses the exercise count (total use cases), not the grammar point count.

Layout for the batch prompt:

```
Session: UN4GL7 — 14 exercises across 9 grammar points. Reply with all answers in one message (numbered or in order).

Exercise 1 / 14 — grammar point: 名詞 + 中（ちゅう・じゅう）  [use case: ongoing state]
Translate to Japanese: "The meeting is currently in progress."

Exercise 2 / 14 — grammar point: 名詞 + 中（ちゅう・じゅう）  [use case: whole area / place]
Translate to Japanese: "I travelled all around Japan."

Exercise 3 / 14 — grammar point: Vないで ください
Translate to Japanese: "Please don't use a cellphone in the hospital."

…

Exercise 14 / 14 — grammar point: Counter 本
Fill the blank: ペンが ___ あります (3 pens).
```

Note: the `[use case: ...]` label in the example above is shown here for illustration only — **omit it from the actual exercise output** so the label does not leak the tested structure to the user.

Layout for the grading reply (single message):

```
✓ 1/7 — Vないで ください

✗ 2/7 — Vない なくてもいいです
  You: 予約しなくていいです
  OK:  予約しなくてもいいです
  missing も in なくても

…

Self-score each one 1–4 (1=fail, 2=hard, 3=good, 4=easy). Reply with the 7 scores in order, e.g. `4 2 3 4 2 3 1`.
```

**Grading display rules:**
- **Correct:** one line — `✓ N/T — <grammar point>`. No answer text needed.
- **Wrong / partial:** three lines — the `✗ N/T — <grammar point>` header, then `You:` and `OK:` on their own lines, then the error on its own line. No extra label lines.
- Strip all furigana from `You:` and `OK:` lines before printing — plain Japanese only. Furigana is for exercises, not diffs.
- Do **not** print a partial-match fragment line (e.g. `✓ frag ✓, frag ✓`).

### Interactive mode (only if user asks)

Present one exercise, wait for the answer, grade, ask for the self-score, then move to the next.

```
Exercise 3 / 7 — grammar point: Vない なくてもいいです

Translate to Japanese: "You don't have to book a reservation."

(use vocabulary from the lesson where possible)
```

After the answer:

```
✓ 3/7 — Vない なくてもいいです

Score this one 1–4? (1=fail, 2=hard, 3=good, 4=easy)
```

Or if wrong:

```
✗ 3/7 — Vない なくてもいいです
  You: 予約しなくていいです
  OK:  予約しなくてもいいです
  missing も in なくても

Score this one 1–4? (1=fail, 2=hard, 3=good, 4=easy)
```

(Same display rules apply: plain Japanese only, no furigana, no partial-match fragment line.)

### Both modes

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

**Furigana in answers** — if the user writes furigana (e.g. 食べる(たべる) or 食べる【たべる】), strip the furigana before comparing to the expected answer. Do not penalise for its presence or absence.

Weak-point strings should be short and categorical: `particle に placement`, `て-form of godan verbs`, `だけ vs しか`. Not free-form sentences.

---

## Session summary

After the last exercise, show a compact summary. Summarize at the **grammar point level** — SM-2 tracks per grammar point, not per exercise. If a grammar point had multiple exercises (multiple use cases), show the individual scores and the worst-case outcome determines the "Solid" vs "Needs practice" classification.

```
Session complete — UN4GL7 (14 exercises across 9 grammar points)

Solid:
  ✓ Vないで ください               score 4
  ✓ Subject + で + V              score 4
  ✓ Counter 回                     score 3

Needs practice:
  ✗ 名詞 + 中（ちゅう・じゅう）     scores 4 / 2 / 1 — じゅう whole-area reading failed
  ✗ Vplain + N (noun modifier)     score 2 — N が/の particle choice
  ✗ Counter 本                      score 1 — sound changes (いっぽん, さんぼん)

Next review dates written to grammar-state.json.
```

Rules:
- If any exercise for a grammar point scored 1–2, the grammar point goes to "Needs practice."
- For points with multiple exercises, show all scores (e.g. `scores 4 / 2 / 1`) and name the use case that failed.
- For points with a single exercise, show `score N` as before.

---

## Persistence

One write at the end of the session: update `.cowork/progress/grammar-state.json`.

Read the file (create with `{"grammar_points": {}}` if missing). For each practiced grammar point:

- If no prior entry: create one with defaults — `interval_days: 1`, `ease: 2.5`, `streak: 0`, `total_reviews: 0`.
- Apply the algorithm based on the score the user gave:

| Score | interval_days update                         | ease update        | streak          |
|-------|----------------------------------------------|--------------------|-----------------|
| 1     | reset to 1                                   | `ease - 0.2` (min 1.3) | reset to 0  |
| 2     | `max(1, round(interval * 1.2))`              | `ease - 0.15` (min 1.3) | +1          |
| 3     | `max(1, round(interval * ease))`             | unchanged          | +1              |
| 4     | `max(1, round(interval * ease * 1.3))`       | `ease + 0.15`      | +1              |

- **Multi-exercise grammar points** — if a grammar point had more than one exercise in the session (multiple use cases), use the **minimum** self-score across all its exercises as the SM-2 input score. Rationale: if the user aced two of three use cases but failed one, they have not mastered the grammar point and should review it sooner. The `weak_points` are the union of all exercises' weak points for that grammar point.
- If it's the first review (streak was 0 before), force `interval_days = 4` regardless of score (score ≥ 2 only; a score-1 first review still resets to 1 per the table).
- Compute `next_review = today + interval_days` (ISO date, YYYY-MM-DD).
- Set `last_reviewed = today`, `last_score`, `total_reviews += 1`.
- Merge weak_points: union with existing `weak_points`, deduped, keep most recent 5.

Example entry shape:

```json
{
  "grammar_points": {
    "UN5GL14::vnaide-kudasai": {
      "lesson_file": "JPLessons/Udemy/N5/Grammar/UN5GL14.md",
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

No transcript file is written — the state JSON is the only output of a session.

---

## Never touch
- TARGET DECK line
- `<!--ID: -->` lines
- Anything inside the lesson file — this skill is **read-only on lessons**
- Do not modify other skill files or the instructions file
