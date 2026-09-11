---
name: _practice-grammar-common
description: >
  Shared logic for grammar practice sessions — lesson-file slicing, grammar-topic
  and vocab-pool parsing, exercise generation (Types 1–6 and the 4 gates),
  interaction-flow mechanics, grading, and the Study Mode invocation hookup.
  Never triggered directly — loaded by `lesson-grammar-practice.md` and
  `scheduled-grammar-practice.md`.
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

---

## Loading an extracted grammar file

Given a target file path under `grammar-index/grammar/` (an extracted
grammar-point file), load it as follows. This routine is shared — any
caller passes in a file path and gets back `{grammar_header, body_text,
frontmatter}` (or a skip signal, per the container-file guard below).

- Read the whole file directly (no awk slice — these files have no
  `# Summary`).
- Parse the YAML frontmatter for `pattern`, `register`, `confused_with`,
  `function`, `topic_slug`, `level`. Attach these to the entry for use in
  **Metadata-driven exercise generation** (defined in
  `scheduled-grammar-practice.md`, the only current consumer of these
  fields).
- **Container-file guard**: if the file contains a `## Sub-topics` heading,
  it is a container file — skip the entry with a warning naming the file
  (e.g. `Skipped <file> — container file, no drillable content.`). Container
  files are never drilled.
- `grammar_header` = the file's H1 (`# <pattern>` line). If the H1 text
  differs from the entry's stored `grammar_header`, print a warning (e.g.
  `grammar_header mismatch for <file> — using file H1.`) but continue using
  the H1 — do **not** skip the entry.
- `body_text` = the gloss blockquote (the `>` line under the H1) +
  `## Structure` + `## Examples` + `## Use Cases` (if present) + `## Notes`
  (if present) + `## Register` (if present) + `## Often confused with` (if
  present). Exclude the YAML frontmatter block and `## See also`.

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

#### Extracted-file linkage (fresh-discovery detection)

This subsection runs only during `lesson-grammar-practice`'s fresh-discovery
pass over `# 文法`/`# Vocabulary`, not `scheduled-grammar-practice`'s
lesson-file flow.

For each **point**-role heading (never for container- or scaffolding-role
headings, since those never become point triples in the first place — see
`_heading-roles.md`), check the line immediately after the heading line,
before any other body content. extract-grammar step 6e guarantees the
wikilink is always inserted there when a point has been extracted, so this
is a single, committed positional check — not a "search the whole body"
fallback. Test the line against:

```
^→ \[\[(grammar-index/grammar/[^\]]+)\]\]\s*$
```

This regex covers both `grammar-index/grammar/<slug>.md` and
`grammar-index/grammar/vocabulary/<subdir>/<slug>.md` (vocabulary
extractions nest under the same prefix).

- **Match** → provisionally set `extracted_file_path = "<captured path>.md"`
  on the point's triple (append `.md` — the wikilink target omits the
  extension, the file on disk has it). This is provisional, subject to the
  container-file guard immediately below. Strip the matched wikilink line
  out of `body_text` — it's a bare navigation link, not example content, and
  must not be fed into exercise-generation prompts as if it were.
- **No match** → `extracted_file_path = null` on the triple. No further
  check needed.

**Container-file guard.** For any point where the check above found a
wikilink match, before finalizing `extracted_file_path`, open the target
file and check whether it contains a `## Sub-topics` heading — the exact
container-file signature already defined above for the "Loading an
extracted grammar file" routine (reuse that check verbatim; do not invent a
second one). This is a lightweight read — open the file and check for
heading presence only; it does **not** parse frontmatter or assemble
`body_text` (that heavier work is exclusive to "Loading an extracted
grammar file", used only when `scheduled-grammar-practice` actually drills
the point later).

- If `## Sub-topics` **is present**: discard the match — set
  `extracted_file_path = null` and fall back to ordinary lesson-file linking
  for that point, exactly as if no wikilink had been detected. Never leave
  the point silently unlinked.
- If `## Sub-topics` **is absent**: keep `extracted_file_path` as captured.

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
exercise, verify all four gates pass. If a gate fails, redesign the
exercise (change type or rewrite the prompt) until it passes all four.

> **GATE 1 — ANSWER-LEAK GATE — MANDATORY. Before printing any exercise
> prompt, verify it passes both checks below. NEVER print a prompt that
> fails either one.**

1. Grammar-point name/form must not be named anywhere in the prompt. A
   prompt like "Translate to Japanese: 'I decided to go to graduate school'"
   is fine — the form (ことにしました) is not named. "Use ことにする to say
   you decided to quit" fails — rewrite as a neutral translation/context
   prompt.
2. Extract the exact string the student must produce. Confirm it does not
   already appear complete and intact anywhere in the prompt, in any
   language — Japanese included. Describing or setting a scene (English,
   Polish, or Japanese) is fine; pre-stating the finished answer is not.
   **Banned template:** a complete target sentence followed by an
   instruction like "say/write/repeat this sentence in complete form" — this
   hands over the answer and always fails Gate 1.

The grammar point name (and the answer itself) may appear in grading
feedback after the student submits — never before.

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

**Gate 4 — Prompt language complexity matches the grammar point's JLPT
level.** Derive the level from the lesson-code prefix already in hand (e.g.
`UN5GL9` → `N5`, `UN4GL7` → `N4`) — no extra file read needed, even for
extracted-file topics (their `level` frontmatter is itself derived from the
same lesson-code digit, never independently researched).

| Level | Prompt complexity |
|---|---|
| N5 | Short, everyday-vocabulary sentences. No idioms, no abstract phrasing. |
| N4 | Slightly richer but still plain, concrete language. |
| N3 | Moderate complexity — some abstract phrasing okay. |
| N2/N1 | Natural native-level prompts are fine. |

Example (N5): ✗ "You're complimenting a coworker. Point out that his
serious, hardworking nature is one of his good qualities." → ✓ "Tell your
coworker: 'You're always serious about work — that's a good thing.'"

Unlike Gate 1's mechanical string check, there's no mechanical test for
prompt sophistication — this is a judgment call the table and example
anchor but can't guarantee against.

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

Every exercise below must already pass Gate 1 — re-check before printing.

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
- **Wrong / partial:** the `✗ N/T — <grammar point>` header, then `You:` and `OK:` on their own lines, then the error explanation. A single mistake stays on one line. When the answer has two or more genuinely distinct mistakes, give each its own short line instead of joining them with semicolons — no "Error:" labels, no numbering, just one line per issue. No extra label lines otherwise.
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

If partially correct, point out the specific issue in one sentence per
distinct issue — no lecture. A single mistake gets one sentence, e.g.
`missed the second に in 午後７時に`. Two or more genuinely distinct mistakes
each get their own short line rather than being joined into one — never a
paragraph of explanation.

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

## Study Mode

On first Study Mode invocation, read
`.cowork/skills/practice-grammar/practice-grammar-study-mode.md` (skip re-reading if already
in context). Pass to it:
- `batch_topics`: list of grammar headers + body_text for topics in the just-completed batch
- `user_answers`: the user's raw answers for each topic in this batch (keyed by grammar_header)
- `batch_number` and `num_batches`: so Step 3 knows whether to ask "Next batch / Finish" (non-last batch) or simply end the session (last batch — the session was already saved before Study Mode was entered)
- `is_last_batch`: boolean
- `vocab_pool`: the session vocab pool (needed for Study Mode exercise generation)
- `weak_points`: per grammar_point_id weak_points, as loaded once at session start (see `scheduled-grammar-practice.md`'s **Batch-loop mechanics** section) and/or accumulated in memory during the session — never re-read from `grammar-state.json` after persistence

Follow the instructions in that file exactly.

---

## Never touch

- TARGET DECK line
- `<!--ID: -->` lines
- Anything inside the lesson file — this skill is **read-only on lessons**
- Do not modify other skill files or the instructions file
- Edits to `.cowork/instructions.md` require explicit user permission before modifying — this is a standing project rule, not specific to any one implementation
