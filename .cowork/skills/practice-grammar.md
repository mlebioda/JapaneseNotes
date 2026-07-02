---
name: practice-grammar
description: >
  Interactive grammar practice session driven by a single lesson file. Extracts
  grammar points from the 文法 section, generates exercises using vocabulary from
  the Summary section (plus N5-level fillers), grades answers, and writes results

to the spaced-repetition state file so they can be prioritized by practice-grammar.
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

Scope triggers (no lesson file needed — select from grammar-state.json):
- "practice today's topics" / "practice grammar due today" / "drill today's grammar"
  → scope = TODAY
- "practice overdue topics" / "practice overdue grammar" / "drill overdue topics"
  → scope = OVERDUE

Scope triggers are matched before lesson-code detection. If no scope phrase and no lesson reference are found, fall through to existing ambiguity handling.

---

## Scope resolution

This section runs when scope = TODAY or scope = OVERDUE. It produces `selected_entries` — a list of grammar point entries — which the session machinery then consumes exactly as if they came from a single lesson file.

### TODAY flow

1. Read `.cowork/progress/grammar-state.json`. If missing, treat state as empty.
2. Filter entries: keep only those where `next_review` is a valid ISO date (YYYY-MM-DD) AND `next_review == today` (exact string equality). Entries where `next_review < today` are NOT included. Entries where `next_review > today` are NOT included.
3. Apply edge-case skips (see **Edge cases** below).
4. If 0 entries remain: print `Nothing is scheduled for today.` and stop.
5. Print `count grammar points scheduled for today.` and proceed to session.

### OVERDUE flow

1. Read `.cowork/progress/grammar-state.json`. If missing, treat state as empty.
2. Filter entries: keep only those where `next_review` is a valid ISO date (YYYY-MM-DD) AND `next_review < today` (strictly less than — NOT <= and NOT ==). Entries where `next_review == today` are NOT included.
3. Apply edge-case skips (see **Edge cases** below).
4. If 0 entries remain: print `No overdue grammar points — you're up to date.` and stop.
5. Sort remaining entries by `next_review` ascending (oldest next_review first = most overdue first).
6. Print `count grammar points are overdue. How many do you want to practice? (most overdue first, or 'all')` and wait for user reply.
7. Parse user reply X — evaluated in this exact order:
   - X is `"all"` → use all count entries (no extra message).
   - X is a positive integer > count → use all count entries, print `Only count overdue points found — using all.`
   - X is a positive integer == count → use all count entries (no extra message).
   - X is a positive integer < count → use the first X entries (already sorted oldest first).
   - X is invalid (non-integer, negative, zero) → ask once more with identical prompt. If still invalid: print `Invalid selection — session cancelled.` and stop.
8. Print `Starting session with X grammar points.` and proceed to session.

### Multi-lesson file loading

Once `selected_entries` is resolved:

1. Collect unique `lesson_file` values from `selected_entries`.
2. For each lesson file, read content up to `# Summary` using:
   ```bash
   awk '/^# Summary$/{exit} {print}' "$LESSON_FILE"
   ```
   Load lazily — only read a file on first demand. Each path is read at most once.
3. For each selected entry, locate `grammar_header` in the loaded lesson slice by searching `# 文法` and `# Vocabulary` sections for a `## Heading` match. Strategy: exact → case-insensitive → whitespace-normalised. If no match: skip with warning. If more than one match (ambiguous): skip with warning.
4. Build merged vocab pool: union of all `# ごい` + `# ひょうげん` tagged lines from all loaded lesson files. Deduplicate by Japanese form (full kanji+reading string). When the same form appears in multiple lesson files, keep the first occurrence (session-list order).
5. If all lesson files fail to load: print `Error: no lesson files could be loaded — session cancelled.` and report all warnings. Stop.

**N (the count shown to the user) is derived solely from `grammar-state.json`** — it equals the number of entries passing the date filter. Lesson-file load failures and warned-and-skipped entries do NOT reduce N.

### Edge cases

The following cause an entry to be skipped **silently** (no output):
- `next_review` missing, null, empty, or not a parseable YYYY-MM-DD date.

The following cause an entry to be skipped **with a warning line**:
- `lesson_file` missing or empty.
- `grammar_header` missing or empty.
- Lesson file path not found on disk.
- `grammar_header` not found in lesson file after all match strategies.
- `grammar_header` matches more than one heading in the lesson file (ambiguous).

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
6. **Batch-split (scope sessions only — skip for lesson sessions)**
    After assembling `selected_entries`:
    - Ask: "X topics selected. How many batches would you like to split these into?" Wait for a positive integer `num_batches`.
    - If `num_batches` == 1 or the user says "none" / "no split": set `num_batches = 1` (no batch headers, no between-batch prompts).
    - If `num_batches` > total topics: inform the user "Only X topics available — running as a single batch." and set `num_batches = 1`.
    - If `num_batches` > 1: divide `selected_entries` evenly into `num_batches` ordered batches. First batch = entries 1 through ⌈total/num_batches⌉; last batch may be smaller. Do not reorder entries.
    - If the user gives an invalid answer (non-integer, negative, zero): ask once more with the same prompt. If still invalid: set `num_batches = 1`.
    - For lesson-triggered sessions: skip this step. Set `num_batches = 1`.
7. **Run the session — batch loop**
    For each batch B (1 to `num_batches`):
    a. **Generate exercises for this batch's topics only** (see **Exercise generation** and **Parsing — Use case extraction**). Apply weak_point bias per topic. `N` = total exercises across the full session (sum across all batches, fixed after the first batch).
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
         - "Study mode" → enter Study Mode for the topics in batch B (see **Study Mode** section). After Study Mode exits, ask again: `Next batch / Finish` (same rules as Step 3 of Study Mode).
         - If the user asks an off-topic question, answer it and re-present the same prompt.
         - The prompt must always appear — never auto-advance to the next batch.
       - If B == `num_batches` (last batch): ask:
         ```
         Study mode / Save & finish
         ```
         - "Study mode" → enter Study Mode for the topics in the last batch. After Study Mode exits, proceed to post-session (write state + calendar).
         - "Save & finish" (or equivalent) → proceed to post-session.
         - If the user asks an off-topic question, answer it and re-present the same prompt.
         - The prompt must always appear — never auto-finish without user confirmation.
       - **Early exit:** if the user types "stop" or "end" as a standalone message at any point mid-session, load `practice-grammar-srs.md` and write grammar-state.json and .ics for all scores collected so far, print the partial session summary, and end immediately. "stop" is no longer offered as a named option in the between-batch prompt.
    f. Never skip a batch automatically — always wait for user confirmation before advancing.
8. **After the last batch** — write the session summary (see **Session summary**).
9. **Persist results** — update `grammar-state.json` (see **Persistence and Calendar sync**).
10. **Write calendar file** — after writing `grammar-state.json`, write a new timestamped `japanese-grammar-review-<timestamp>.ics` file at the vault root (see **Persistence and Calendar sync**).

Don't skip any step. Start practicing immediately after the user triggers the skill.

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

- **Type 1 — Contextual production** — Situation described in English/Polish, no grammar named. Student writes natural Japanese. Claude internally knows the target grammar and grades on whether it was used correctly and naturally. Best for single nuanced words/expressions (ぜひ, きっと, etc.).
- **Type 2 — Discrimination fill-in-blank** — One gap, four choices — ALL four must be genuinely confusable. Confusability definition: all four choices must be grammatically plausible in the given sentence; the lesson must contain at least two forms that share a morphological relationship with the target (e.g. all conditionals, all て-forms, all aspect pairs). ONLY used when there is a group of similar forms in the lesson. Never used for a single grammar point where the choice is obvious. Best for groups of similar forms (conditionals, て-forms, aspect pairs).
- **Type 3 — Description → production** — Claude describes a concrete situation without naming or hinting at the grammar. Student must produce the correct form, counter, or structure. Best for counters, classifiers, specific constructions.
- **Type 4 — JLPT sentence ordering (文の組み立て)** — A sentence is broken into scrambled fragments. One position is marked ★. Student places the fragments in the correct order. The grammar form is never named. Best for complex sentence-pattern grammar.
- **Type 5 — JLPT passage grammar (文章の文法)** — A short natural paragraph (3–5 sentences) with one or two numbered blanks. Student picks which option fits the passage context. Surrounding sentences provide natural context clues, not grammar hints. Best for grammar points with rich context dependency.
- **Type 6 — Bolded form → explain** — Claude writes a sentence with the target grammar bolded. Student explains: what does this form mean here, and why is it used (not a different form). Best for nuanced contrasts (e.g. ことにした vs つもり) and grammar points already seen in a prior session.

**Furigana rule — mandatory.** Every kanji character that appears anywhere in the exercise output **must** have furigana — no exceptions. This applies to every location: question text, answer options, feedback lines, hint text, example sentences, grammar-point context, and vocabulary pool words. Use vault inline style: kanji immediately followed by the reading in full-width parentheses, e.g. `名刺（めいし）`, `病院（びょういん）`, `食（た）べる`. Compound words are the most common failure point — every kanji in the compound needs its own reading. ✗ `来年、日本語の試験（しけん）を…` — 来年 and 日本語 are missing furigana. ✓ `来年（らいねん）、日本語（にほんご）の試験（しけん）を…` — every kanji covered. Before outputting each exercise, scan every kanji in every line and verify furigana is present.

**Vocabulary rule** — content words in the exercise must come from the vocab pool (`# ごい` + `# ひょうげん`) first. Only reach for outside vocabulary if the pool cannot express the grammar point. Any outside vocabulary must be strict N5 level.

**Weak-point bias** — if the state entry for this grammar point has `weak_points`, design the exercise so the answer requires getting that aspect right (e.g. if the weak point is "particle placement," the exercise must have the particle in the target answer). For weak-point reinforcement (low SM-2 ease or recent failure), prefer Type 1 or Type 3. Avoid Types 5 and 6 when targeting known weak conjugations — those types test comprehension and meta-awareness, not production accuracy.

**Type selection rule** — pick the type that best fits what the grammar point needs:
- Single nuanced word/expression (ぜひ, きっと, etc.) → Type 1 or Type 6
- Group of similar forms (conditionals, て-forms, aspect pairs) → Type 2 or Type 4; Type 2 requires all four choices to be genuinely confusable (see confusability definition above) — never use it for a single grammar point where the choice is obvious
- Counters, classifiers, specific constructions → Type 3
- Grammar points with rich context dependency → Type 5
- Any grammar point the student has already seen in a prior session (recorded in grammar-state.json) → prefer Type 6

**Variety rule** — vary types only when multiple types are equally valid for a given grammar point. Never override the pedagogically correct type just for variety.

**Non-trivial exercise checklist — mandatory.** Before outputting any exercise, verify all three gates pass. If a gate fails, redesign the exercise (change type or rewrite the prompt) until it passes all three.

**Gate 1 — Prompt does not leak the answer — grammar point name must not appear anywhere in the exercise shown to the student before they answer.** The prompt must not contain, quote, or directly name the exact form the user must produce. A prompt like "Translate to Japanese: 'I decided to go to graduate school'" is fine — the grammar form (ことにしました) is not named in the prompt. A prompt like "Use ことにする to say you decided to quit" fails because it names the target form; rewrite as a neutral translation or context prompt instead. The grammar point name is held internally by Claude and may appear in grading feedback after the student submits their answer — never before.

**Gate 2 — Answer requires genuinely using the grammar point.** A native speaker who does not know this grammar point but knows vocabulary could not produce the answer by elimination or by copying surrounding text. If they could, upgrade the exercise type (e.g. fill-the-blank → translate-to-Japanese).

**Gate 3 — Conjugation target is not a single morpheme.** If the answer requires adding or changing only one particle or suffix (ない, ます, か) to a fully given stem, the exercise is too narrow. The exercise must require the user to produce the whole grammatical construction, not just append one character to a given stem. Exception: exercises explicitly testing a single difficult distinction (e.g. rendaku in counters, sound changes in irregular forms like いっぽん, さんぼん) are allowed, because the tested knowledge is genuinely difficult and cannot be meaningfully widened.

---

## Interaction flow

There are two modes — **batch** (default) and **interactive**. Pick batch unless the user explicitly asks for one-at-a-time.

**Progress indicator — required.** Every exercise prompt MUST start with `Exercise <current> / <total>` so the user always knows where they are in the session. `<current>` is 1-based (first exercise is `1 / N`, last is `N / N`). The total is fixed at the start of the session and does not change mid-session. The exercise title shows only the number — never the grammar point name. Study Mode exercises use a local `study_counter` and are excluded from the session-wide progress indicator.

### Batch mode (default — works on flaky connections)

Print **all** exercises at once in a single message. Number them, include the grammar point header, and put the prompt on its own. No expected answers, no hints that reveal the form. The user replies once with all answers (numbered or in order). Then grade everything in one follow-up message and ask for self-scores in one batch.

The session header must show both the exercise count and the grammar point count. The `Exercise N / T` progress indicator uses the exercise count (total use cases), not the grammar point count.

For scope sessions (TODAY / OVERDUE), use these header and footer formats instead of the single-lesson variants:

**Session header — Today:**
```
Session: today's topics — N exercises across M grammar points (K lessons). Reply with all answers in one message.
```

**Session header — Overdue:**
```
Session: overdue topics — N exercises across M grammar points (K lessons). Reply with all answers in one message.
```

**Session summary footer — Today:**
```
Session complete — today's topics (N exercises across M grammar points)
```

**Session summary footer — Overdue:**
```
Session complete — overdue topics (N exercises across M grammar points)
```

K lessons = count of distinct lesson files successfully loaded. M = count of grammar points for which at least one exercise will be generated.

Layout for the batch prompt:

```
Session: UN4GL7 — 14 exercises across 9 grammar points. Reply with all answers in one message (numbered or in order).

Exercise 1 / 14
Translate to Japanese: "The meeting is currently in progress."

Exercise 2 / 14
Translate to Japanese: "I travelled all around Japan."

Exercise 3 / 14
Translate to Japanese: "Please don't use a cellphone in the hospital."

…

Exercise 14 / 14
Fill the blank: ペンが ___ あります (3 pens).
```

Note: both the grammar point name and the `[use case: ...]` label are suppressed from all exercise output — Claude holds them internally only. The only visible header is `Exercise N / T`. Grammar point names are permitted in the post-session summary (session is over; exposure is appropriate for review).

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

(Same display rules apply: plain Japanese only, no furigana, no partial-match fragment line.)

### Both modes

If partially correct, point out the specific issue in one sentence — no lecture. Example: `missed the second に in 午後７時に` — not a paragraph of explanation.

Record for each exercise: grammar_id, score (1–4), weak_points (array of short strings — only if the user made a mistake or chose 1–2).

---

## Study Mode

On first Study Mode invocation, read `.cowork/skills/practice-grammar-study-mode.md`
(skip re-reading if already in context). Pass to it:
- `batch_topics`: list of grammar headers + body_text for topics in the just-completed batch
- `user_answers`: the user's raw answers for each topic in this batch (keyed by grammar_header)
- `batch_number` and `num_batches`: so Step 3 knows whether to ask "Next batch" or proceed to post-session
- `is_last_batch`: boolean
- `vocab_pool`: the session vocab pool (needed for Study Mode exercise generation)
- `weak_points`: per grammar_point_id weak_points from grammar-state.json (for bias in practice exercises)

Follow the instructions in that file exactly.

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

**Feedback format** — feedback must name the specific semantic or grammatical mismatch, not just flag the answer as wrong. Format: `"you used X (meaning/use) but the situation requires Y (meaning/use)"`. Example: `"you used つもりです (future intention) but the situation calls for a completed decision → ことにした"`. Grammar point name is permitted in grading feedback after the student submits their answer.

**Type 5 grading (passage grammar)** — mark correct or incorrect AND explain why the chosen option does not fit the passage context, citing the surrounding sentences as evidence. Also explain why the correct option does fit.

**Type 6 grading (bolded form → explain)** — semantic evaluation, not right/wrong. Grade on: (a) whether the student correctly identified the meaning of the bolded form, and (b) whether they explained the contrast with the obvious alternative. Evaluate quality of explanation rather than matching a fixed answer.

---

## Session summary

**Batch sessions:** print the session summary once — after the last batch completes, or when the user types "stop". The summary covers only the grammar points that were actually drilled. Do not print a summary after each individual batch.

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

Next review dates written to grammar-state.json. Calendar file: japanese-grammar-review-<timestamp>.ics written to vault root.
```

Rules:
- If any exercise for a grammar point scored 1–2, the grammar point goes to "Needs practice."
- For points with multiple exercises, show all scores (e.g. `scores 4 / 2 / 1`) and name the use case that failed.
- For points with a single exercise, show `score N` as before.

---

## Persistence and Calendar sync

After the last batch completes (or when the user types "stop"), read
`.cowork/skills/practice-grammar-srs.md` and follow its instructions.
Pass to it:
- `session_scores`: dict keyed by grammar_point_id → `{min_score, weak_points, grammar_header, lesson_file}`
- `session_grammar_ids`: ordered list of grammar_point_ids practiced this session
- `today`: ISO date (YYYY-MM-DD)
- `scope`: one of "lesson", "TODAY", "OVERDUE"

Study Mode exercises are excluded — only include grammar points that received
self-evaluation scores from the main batch exercises.

---

## Never touch
- TARGET DECK line
- `<!--ID: -->` lines
- Anything inside the lesson file — this skill is **read-only on lessons**
- Do not modify other skill files or the instructions file
- `.cowork/instructions.md` trigger list needs updating after this implementation (requires explicit user permission before modifying)
