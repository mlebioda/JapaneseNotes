---
name: _practice-grammar-common
description: >
  Shared logic for grammar practice sessions — lesson-file slicing, grammar-topic
  and vocab-pool parsing, exercise generation (Types 1–6 and the 3 gates),
  interaction-flow mechanics, grading, session-summary formatting, the
  Persistence/Calendar-sync load-directive, the Study Mode invocation hookup,
  and the batch-loop mechanics. Never triggered directly — loaded by
  `lesson-grammar-practice.md` and `scheduled-grammar-practice.md`.
---

# Practice Grammar — Common

Shared sub-skill. Everything in this file is used identically by both
`lesson-grammar-practice.md` (single-lesson-file sessions) and
`scheduled-grammar-practice.md` (TODAY/OVERDUE multi-file sessions). Content
that only one of the two trigger paths can produce (scope resolution,
metadata-driven exercise generation for extracted-file topics, batch-split
prompt, etc.) lives in that skill's own file, not here.

---

## Loading a lesson file slice

Given a resolved lesson file path, extract everything before `# Summary` —
never read the whole lesson file. The Summary section (~70% of the file) is
generated Anki cards and not needed for practice. Run:

```bash
awk '/^# Summary$/{exit} {print}' "$LESSON_FILE"
```

Pass only this slice to all subsequent parsing (Grammar topics, Vocab pool).
Both trigger skills call this routine once per resolved lesson file path —
`lesson-grammar-practice.md` calls it once for its single resolved file;
`scheduled-grammar-practice.md` calls it once per `lesson_file` in its
Multi-lesson file loading loop.

---

## Parsing

### Grammar topics (`# 文法` and `# Vocabulary`)

Both top-level sections contain grammar points to drill. `# 文法` is core
grammar; `# Vocabulary` covers more complex sentence-construction patterns
that don't fit a single `#w`/`#wc`/`#wp` line. Treat them the same way.

For each section, find its `^# ` heading and collect content until the next
`^# ` heading of the same level.

Load `.cowork/skills/_heading-roles.md` and apply its rules to the section's
heading tree — roles are content-based and apply at **any nesting depth**
(real patterns appear at `##`, `###`, and `####`):

- **Point** headings become drill points — one `{grammar_header, body_text, source_section}` triple each. Scaffolding children (`Examples`, `Structure`, …) fold into the point's `body_text`.
- **Container** headings are never drilled themselves — their descendant points are drilled individually.
- **Scaffolding** headings are never drill points.
- This classification is applied deterministically — no user gate. When a child heading is ambiguous (explanation-part vs sub-pattern), fold it into the parent point's body.
- Preserve Japanese characters exactly.

The body text (Structure blocks, examples) is what generates exercises.

#### Use case extraction

After building each triple, identify the use cases within the body text:

1. **`### Use cases` section present** — each numbered item in that list is one use case. Extract the item number and its short description as the use case label (e.g. `"1. ongoing state"`, `"2. time period"`, `"3. whole area"`).
2. **`### Structure` section with multiple top-level bullet variants** — if the section contains two or more top-level bullet points each beginning with a structural pattern (`V「...」`, `N + ...`, `いadj`, `なadj`, etc.) with distinct structures, each top-level variant is one use case. Label with the pattern text (e.g. `"V「dict」+ の"`, `"V「た」+ の"`).
3. **Neither applies** — the grammar point is prose/examples only, no explicit structural variants. Treat the whole grammar point as one use case (label: the grammar header itself).

Minimum: every grammar point yields at least one use case; there is no
maximum. The use case label is used only internally for exercise generation
— it must **not** appear in the exercise prompt shown to the user (showing
it would leak the tested structure).

(Extracted-file topics use a different use-case-extraction variant, keyed on
semantic content rather than markdown heading level — see
`scheduled-grammar-practice.md`'s own Use case extraction subsection.)

### Vocab pool (`# ごい` and `# ひょうげん`)

Find both `^# ごい` and `^# ひょうげん`. Collect every `#w`, `#wc`, `#wp`
line — these are the source vocabulary in the format defined by
fill-templates:

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

For each line, build `{japanese, reading, translation, type}` where
`type ∈ {word, verb, adjective}` from the `#w`/`#wc`/`#wp` tag. Verb
conjugations and adjective forms aren't pre-stored — derive them from rules
at exercise-generation time using your Japanese knowledge.

All three types are first-class practice material — drill conjugations and
form transformations, not just plain-word translation.

(Extracted-file topics have no lesson vocab pool of their own; sessions that
include one supplement the pool from `Vocabulary/*.md` and merge it with a
cross-file dedup rule — see `scheduled-grammar-practice.md`'s Vocabulary base
subsection.)

### Grammar point ID

Build a stable ID: `<lesson-code>::<slug>` where slug is the grammar header
romanized/simplified — lowercase, non-alphanumeric collapsed to `-`, trimmed.
Keep the **original Japanese heading** in the state entry too
(`grammar_header`), since the slug may not round-trip.

Example: header `Vないで ください` → slug `vnaide-kudasai` → id
`UN5GL14::vnaide-kudasai`.

---

## Exercise generation

For each grammar point, produce **one exercise per use case** (as extracted
during parsing). Each exercise must target its specific use case — not a
generic demonstration of the overall grammar point. The use case label must
not appear in the prompt text. If the grammar point has recorded
`weak_points`, prioritize the use case(s) that match the weak point in the
exercises for that use case.

Pick the exercise type that best tests the specific use case:

- **Type 1 — Contextual production** — Situation described in English/Polish, no grammar named. Student writes natural Japanese. Claude internally knows the target grammar and grades on whether it was used correctly and naturally. Best for single nuanced words/expressions (ぜひ, きっと, etc.).
- **Type 2 — Discrimination fill-in-blank** — One gap, four choices — ALL four must be genuinely confusable. Confusability definition: all four choices must be grammatically plausible in the given sentence; the lesson must contain at least two forms that share a morphological relationship with the target (e.g. all conditionals, all て-forms, all aspect pairs). ONLY used when there is a group of similar forms in the lesson. Never used for a single grammar point where the choice is obvious. Best for groups of similar forms (conditionals, て-forms, aspect pairs).
- **Type 3 — Description → production** — Claude describes a concrete situation without naming or hinting at the grammar. Student must produce the correct form, counter, or structure. Best for counters, classifiers, specific constructions.
- **Type 4 — JLPT sentence ordering (文の組み立て)** — A sentence is broken into scrambled fragments. One position is marked ★. Student places the fragments in the correct order. The grammar form is never named. Best for complex sentence-pattern grammar.
- **Type 5 — JLPT passage grammar (文章の文法)** — A short natural paragraph (3–5 sentences) with one or two numbered blanks. Student picks which option fits the passage context. Surrounding sentences provide natural context clues, not grammar hints. Best for grammar points with rich context dependency.
- **Type 6 — Bolded form → explain** — Claude writes a sentence with the target grammar bolded. Student explains: what does this form mean here, and why is it used (not a different form). Best for nuanced contrasts (e.g. ことにした vs つもり) and grammar points already seen in a prior session.

**Furigana rule — mandatory.** Every kanji character that appears anywhere
in the exercise output **must** have furigana — no exceptions. This applies
to every location: question text, answer options, feedback lines, hint text,
example sentences, grammar-point context, and vocabulary pool words. Use
vault inline style: kanji immediately followed by the reading in full-width
parentheses, e.g. `名刺（めいし）`, `病院（びょういん）`, `食（た）べる`.
Compound words are the most common failure point — every kanji in the
compound needs its own reading. ✗ `来年、日本語の試験（しけん）を…` — 来年
and 日本語 are missing furigana. ✓
`来年（らいねん）、日本語（にほんご）の試験（しけん）を…` — every kanji
covered. Before outputting each exercise, scan every kanji in every line and
verify furigana is present.

**Vocabulary rule** — content words in the exercise must come from the vocab
pool (`# ごい` + `# ひょうげん`) first. Only reach for outside vocabulary if
the pool cannot express the grammar point. Any outside vocabulary must be
strict N5 level.

**Weak-point bias** — if the state entry for this grammar point has
`weak_points`, design the exercise so the answer requires getting that
aspect right (e.g. if the weak point is "particle placement," the exercise
must have the particle in the target answer). For weak-point reinforcement
(low SM-2 ease or recent failure), prefer Type 1 or Type 3. Avoid Types 5
and 6 when targeting known weak conjugations — those types test
comprehension and meta-awareness, not production accuracy.

**Type selection rule** — pick the type that best fits what the grammar
point needs:
- Single nuanced word/expression (ぜひ, きっと, etc.) → Type 1 or Type 6
- Group of similar forms (conditionals, て-forms, aspect pairs) → Type 2 or Type 4; Type 2 requires all four choices to be genuinely confusable (see confusability definition above) — never use it for a single grammar point where the choice is obvious
- Counters, classifiers, specific constructions → Type 3
- Grammar points with rich context dependency → Type 5
- Any grammar point the student has already seen in a prior session (recorded in grammar-state.json) → prefer Type 6

**Variety rule** — vary types only when multiple types are equally valid for
a given grammar point. Never override the pedagogically correct type just
for variety.

**Non-trivial exercise checklist — mandatory.** Before outputting any
exercise, verify all three gates pass. If a gate fails, redesign the
exercise (change type or rewrite the prompt) until it passes all three.

**Gate 1 — Prompt does not leak the answer — grammar point name must not
appear anywhere in the exercise shown to the student before they answer.**
The prompt must not contain, quote, or directly name the exact form the user
must produce. A prompt like "Translate to Japanese: 'I decided to go to
graduate school'" is fine — the grammar form (ことにしました) is not named
in the prompt. A prompt like "Use ことにする to say you decided to quit"
fails because it names the target form; rewrite as a neutral translation or
context prompt instead. The grammar point name is held internally by Claude
and may appear in grading feedback after the student submits their answer —
never before.

**Gate 2 — Answer requires genuinely using the grammar point.** A native
speaker who does not know this grammar point but knows vocabulary could not
produce the answer by elimination or by copying surrounding text. If they
could, upgrade the exercise type (e.g. fill-the-blank → translate-to-Japanese).

**Gate 3 — Conjugation target is not a single morpheme.** If the answer
requires adding or changing only one particle or suffix (ない, ます, か) to
a fully given stem, the exercise is too narrow. The exercise must require
the user to produce the whole grammatical construction, not just append one
character to a given stem. Exception: exercises explicitly testing a single
difficult distinction (e.g. rendaku in counters, sound changes in irregular
forms like いっぽん, さんぼん) are allowed, because the tested knowledge is
genuinely difficult and cannot be meaningfully widened.

(Extracted-file topics unlock additional exercise-generation options driven
by their `confused_with`/`register` frontmatter — see
`scheduled-grammar-practice.md`'s Metadata-driven exercise generation
section. That section's rules take priority over the generic Weak-point bias
and Type selection rules above for extracted-file topics specifically.)

---

## Interaction flow

There are two modes — **batch** (default) and **interactive**. Pick batch
unless the user explicitly asks for one-at-a-time.

**Progress indicator — required.** Every exercise prompt MUST start with
`Exercise <current> / <total>` so the user always knows where they are in
the session. `<current>` is 1-based (first exercise is `1 / N`, last is
`N / N`). The total is fixed at the start of the session and does not change
mid-session. The exercise title shows only the number — never the grammar
point name. Study Mode exercises use a local `study_counter` and are
excluded from the session-wide progress indicator.

### Batch mode (default — works on flaky connections)

Print **all** exercises at once in a single message. Number them, include
the grammar point header, and put the prompt on its own line. No expected
answers, no hints that reveal the form. The user replies once with all
answers (numbered or in order). Then grade everything in one follow-up
message and ask for self-scores in one batch.

The session header must show both the exercise count and the grammar point
count. The `Exercise N / T` progress indicator uses the exercise count
(total use cases), not the grammar point count.

Generic layout for the batch prompt (each trigger skill supplies its own
concrete session header text — see that skill's own Session header/example):

```
<session header — supplied by the calling trigger skill>

Exercise 1 / T
<prompt>

Exercise 2 / T
<prompt>

…

Exercise T / T
<prompt>
```

Note: both the grammar point name and the `[use case: ...]` label are
suppressed from all exercise output — Claude holds them internally only. The
only visible header is `Exercise N / T`. Grammar point names are permitted
in the post-session summary (session is over; exposure is appropriate for
review).

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

Present one exercise, wait for the answer, grade, ask for the self-score,
then move to the next.

```
Exercise 3 / 7

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

(Same display rules apply: plain Japanese only, no furigana, no
partial-match fragment line.)

### Both modes

If partially correct, point out the specific issue in one sentence — no
lecture. Example: `missed the second に in 午後７時に` — not a paragraph of
explanation.

Record for each exercise: grammar_id, score (1–4), weak_points (array of
short strings — only if the user made a mistake or chose 1–2).

---

## Grading

Compare user's answer to the expected answer with tolerance:

- **Kanji vs kana** — accept either for words that have both forms, unless the exercise is specifically testing kanji.
- **Particle correctness** — strict. Wrong particle = mistake, note as weak point.
- **Verb conjugation** — strict. Wrong form = mistake.
- **Word order** — if the sentence is still grammatically valid and conveys the same meaning, accept with a note rather than mark wrong.
- **Spelling typos** — accept if the intent is clear and only one character is off.
- **Register match (extracted-file topics only)** — a grammatically correct answer in the wrong register is a mistake. Name the register mismatch and cite the `## Register` guidance in feedback; for `register: tiered` patterns, cite the specific selection rule that was violated (e.g. which party/context should have triggered the other tier), not a generic politeness note.

**Furigana in answers** — if the user writes furigana (e.g. 食べる(たべる)
or 食べる【たべる】), strip the furigana before comparing to the expected
answer. Do not penalise for its presence or absence.

Weak-point strings should be short and categorical: `particle に placement`,
`て-form of godan verbs`, `だけ vs しか`. Not free-form sentences.

**Feedback format** — feedback must name the specific semantic or
grammatical mismatch, not just flag the answer as wrong. Format:
`"you used X (meaning/use) but the situation requires Y (meaning/use)"`.
Example: `"you used つもりです (future intention) but the situation calls
for a completed decision → ことにした"`. Grammar point name is permitted in
grading feedback after the student submits their answer.

**Type 5 grading (passage grammar)** — mark correct or incorrect AND explain
why the chosen option does not fit the passage context, citing the
surrounding sentences as evidence. Also explain why the correct option does
fit.

**Type 6 grading (bolded form → explain)** — semantic evaluation, not
right/wrong. Grade on: (a) whether the student correctly identified the
meaning of the bolded form, and (b) whether they explained the contrast with
the obvious alternative. Evaluate quality of explanation rather than
matching a fixed answer.

---

## Session summary

**Batch sessions:** print the session summary once — after the last batch
completes, or when the user types "stop". The summary covers only the
grammar points that were actually drilled. Do not print a summary after each
individual batch.

After the last exercise, show a compact summary. Summarize at the
**grammar point level** — SM-2 tracks per grammar point, not per exercise.
If a grammar point had multiple exercises (multiple use cases), show the
individual scores and the worst-case outcome determines the "Solid" vs
"Needs practice" classification.

```
Session complete — <header> (N exercises across M grammar points)

Solid:
  ✓ Vないで ください               score 4
  ✓ Subject + で + V              score 4
  ✓ Counter 回                     score 3

Needs practice:
  ✗ 名詞 + 中（ちゅう・じゅう）     scores 4 / 2 / 1 — じゅう whole-area reading failed
  ✗ Vplain + N (noun modifier)     score 2 — N が/の particle choice
  ✗ Counter 本                      score 1 — sound changes (いっぽん, さんぼん)

Next review dates written to grammar-state.json. Calendar file: japanese-grammar-review-<timestamp>.ics written to vault root.
```

`<header>` is supplied by the calling trigger skill — see that skill's own
session-summary footer text for the exact wording it plugs in here.

Rules:
- If any exercise for a grammar point scored 1–2, the grammar point goes to "Needs practice."
- For points with multiple exercises, show all scores (e.g. `scores 4 / 2 / 1`) and name the use case that failed.
- For points with a single exercise, show `score N` as before.

---

## Persistence and Calendar sync

For the last batch, this happens immediately upon reaching self-evaluation
completion for that batch — before the `Study mode / Finish` prompt is shown
— not after the user chooses to finish. (For an early "stop"/"end" at any
other point mid-session, this also runs immediately with scores collected so
far.) Read `.cowork/skills/practice-grammar-srs.md` and follow its
instructions. Pass to it:
- `session_scores`: dict keyed by grammar_point_id → `{min_score, weak_points, grammar_header, lesson_file}`
- `session_grammar_ids`: ordered list of grammar_point_ids practiced this session
- `today`: ISO date (YYYY-MM-DD)
- `scope`: one of `"lesson"`, `"TODAY"`, `"OVERDUE"` — set by whichever trigger skill calls this directive (`lesson-grammar-practice.md` always passes `"lesson"`; `scheduled-grammar-practice.md` passes `"TODAY"` or `"OVERDUE"` depending on which flow resolved the session)

Study Mode exercises are excluded — only include grammar points that
received self-evaluation scores from the main batch exercises.

---

## Study Mode

On first Study Mode invocation, read
`.cowork/skills/practice-grammar-study-mode.md` (skip re-reading if already
in context). Pass to it:
- `batch_topics`: list of grammar headers + body_text for topics in the just-completed batch
- `user_answers`: the user's raw answers for each topic in this batch (keyed by grammar_header)
- `batch_number` and `num_batches`: so Step 3 knows whether to ask "Next batch / Finish" (non-last batch) or simply end the session (last batch — the session was already saved before Study Mode was entered)
- `is_last_batch`: boolean
- `vocab_pool`: the session vocab pool (needed for Study Mode exercise generation)
- `weak_points`: per grammar_point_id weak_points, as loaded once at session start (see **Batch-loop mechanics** below) and/or accumulated in memory during the session — never re-read from `grammar-state.json` after persistence

Follow the instructions in that file exactly.

---

## Never touch

- TARGET DECK line
- `<!--ID: -->` lines
- Anything inside the lesson file — this skill is **read-only on lessons**
- Do not modify other skill files or the instructions file
- Edits to `.cowork/instructions.md` require explicit user permission before modifying — this is a standing project rule, not specific to any one implementation

---

## Batch-loop mechanics

**Load weak points.** At session start (before generating any exercises),
load `.cowork/progress/grammar-state.json` — if the file does not exist yet,
treat state as empty. Pick up any prior `weak_points` for the session's
grammar points so exercises can stress them.

Run the session as a loop over batches, parameterized by `num_batches` (the
lesson trigger always fixes `num_batches = 1` with no batch-split prompt;
the scheduled trigger resolves `num_batches` via its own batch-split prompt
before calling this loop):

For each batch B (1 to `num_batches`):

a. **Generate exercises for this batch's topics only** (see **Exercise generation** and the Use case extraction subsections under **Parsing**). Apply weak_point bias per topic. `N` = total exercises across the full session (sum across all batches, fixed after the first batch).
b. If `num_batches` > 1: print `Batch B / num_batches` before presenting exercises.
c. Present exercises for this batch (see **Interaction flow**). Collect user answers and self-scores.
d. Record self-scores and weak_points for this batch in memory. Do NOT write grammar-state.json yet.
e. After self-evaluation scores are collected for batch B:

   > **BETWEEN-BATCH GATE — MANDATORY. After collecting self-scores for any batch,
   > ALWAYS present the Study mode / Next batch prompt and wait for user input.
   > NEVER auto-advance to the next batch or to post-session. This is the most
   > important interaction rule in this skill.**

   - If B < `num_batches` (non-last batch): print `Batch B / num_batches complete.` then ask:
     ```
     Next batch / Study mode
     ```
     - "Next batch" (or equivalent affirmative) → continue to batch B+1.
     - "Study mode" → enter Study Mode for the topics in batch B (see **Study Mode** section). After Study Mode exits, ask again: `Next batch / Finish` (same rules as Step 3 of `practice-grammar-study-mode.md`).
     - If the user asks an off-topic question, answer it and re-present the same prompt.
     - The prompt must always appear — never auto-advance to the next batch.
   - If B == `num_batches` (last batch): immediately after self-evaluation scores are collected for this batch, run the session-summary, persistence, and calendar-sync steps unconditionally (write the session summary, persist to `grammar-state.json`, write the calendar `.ics` — see **Session summary** and **Persistence and Calendar sync** sections). This happens before any prompt is shown; it is no longer gated behind a user choice. Then ask:
     ```
     Study mode / Finish
     ```
     - "Study mode" → enter Study Mode for the topics in the last batch. Session data is already saved at this point — Study Mode is purely supplementary practice. After Study Mode exits, end the session (nothing further to persist).
     - "Finish" (or equivalent affirmative) → end the session immediately.
     - If the user asks an off-topic question, answer it and re-present the same prompt.
     - The prompt must always appear — never auto-finish without user confirmation, even though persistence has already occurred.
     - **Guard — "stop"/"end" at this prompt.** If the user types "stop" or "end" in reply to this `Study mode / Finish` prompt, treat it as a no-op alias for "Finish" — end the session immediately. Do **not** re-invoke `practice-grammar-srs.md`, do not rewrite `grammar-state.json`, and do not write a second `.ics` file. This overrides the general Early-exit rule below for this specific prompt only, since persistence for this batch (and the whole session) already happened one step above.
   - **Early exit:** if the user types "stop" or "end" as a standalone message at any other point mid-session (i.e. not in reply to the last-batch `Study mode / Finish` prompt above), load `practice-grammar-srs.md` and write grammar-state.json and .ics for all scores collected so far, print the partial session summary, and end immediately. "stop" is no longer offered as a named option in the between-batch prompt.

f. Never skip a batch automatically — always wait for user confirmation before advancing.

Don't skip any step in this loop. Start practicing immediately after the
user triggers the calling skill.
