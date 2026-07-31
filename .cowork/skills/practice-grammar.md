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
2. **Source-type branch** — for each `lesson_file` path, determine its source type before loading. Load lazily in both flows — only read a file on first demand. Each path is read at most once.
   - Path starts with `grammar-index/grammar/` → **extracted-file flow** (2a below).
   - Otherwise → **lesson-file flow, unchanged from prior behavior** (2b below).

   **2a. Extracted-file flow:**
   - Read the whole file directly (no awk slice — these files have no `# Summary`).
   - Parse the YAML frontmatter for `pattern`, `register`, `confused_with`, `function`, `topic_slug`, `level`. Attach these to the entry for use in **Metadata-driven exercise generation**.
   - **Container-file guard**: if the file contains a `## Sub-topics` heading, it is a container file — skip the entry with a warning naming the file (e.g. `Skipped <file> — container file, no drillable content.`). Container files are never drilled.
   - `grammar_header` = the file's H1 (`# <pattern>` line). If the H1 text differs from the entry's stored `grammar_header`, print a warning (e.g. `grammar_header mismatch for <file> — using file H1.`) but continue using the H1 — do **not** skip the entry.
   - `body_text` = the gloss blockquote (the `>` line under the H1) + `## Structure` + `## Examples` + `## Use Cases` (if present) + `## Notes` (if present) + `## Register` (if present) + `## Often confused with` (if present). Exclude the YAML frontmatter block and `## See also`.

   **2b. Lesson-file flow (existing behavior, unchanged):**
   - Read content up to `# Summary` using:
     ```bash
     awk '/^# Summary$/{exit} {print}' "$LESSON_FILE"
     ```
   - For each selected entry, locate `grammar_header` in the loaded lesson slice by searching `# 文法` and `# Vocabulary` sections for a `## Heading` match. Strategy: exact → case-insensitive → whitespace-normalised. If no match: skip with warning. If more than one match (ambiguous): skip with warning.
3. Build merged vocab pool — see **Vocabulary base** (under Parsing) for how extracted-file topics contribute. For lesson-file entries the pool is unchanged: union of all `# ごい` + `# ひょうげん` tagged lines from all loaded lesson files. Deduplicate by Japanese form (full kanji+reading string). When the same form appears in multiple lesson files, keep the first occurrence (session-list order).
4. If all lesson/extracted files fail to load: print `Error: no lesson files could be loaded — session cancelled.` and report all warnings. Stop.

**N (the count shown to the user) is derived solely from `grammar-state.json`** — it equals the number of entries passing the date filter. Lesson/extracted-file load failures and warned-and-skipped entries do NOT reduce N.

### Edge cases

The following cause an entry to be skipped **silently** (no output):
- `next_review` missing, null, empty, or not a parseable YYYY-MM-DD date.

The following cause an entry to be skipped **with a warning line**:
- `lesson_file` missing or empty.
- `grammar_header` missing or empty.
- Lesson/extracted file path not found on disk.
- Lesson-file flow only: `grammar_header` not found in lesson file after all match strategies.
- Lesson-file flow only: `grammar_header` matches more than one heading in the lesson file (ambiguous).
- Extracted-file flow only: the file contains `## Sub-topics` (container file) — never drilled.

The following causes a warning line but does **not** skip the entry (extracted-file flow only):
- The entry's stored `grammar_header` differs from the file's H1 — the H1 is authoritative; continue using it.

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
       - If B == `num_batches` (last batch): immediately after self-evaluation scores are collected for this batch, run Workflow steps 8–10 unconditionally (write the session summary, persist to `grammar-state.json`, write the calendar `.ics` — see **Session summary** and **Persistence and Calendar sync** sections). This happens before any prompt is shown; it is no longer gated behind a user choice. Then ask:
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
8. **After the last batch** — write the session summary (see **Session summary**). For the last batch, steps 8–10 execute inline and automatically as part of step 7e's last-batch branch, immediately after self-evaluation scores are collected — not as a separate phase reached only after a user chooses to finish.
9. **Persist results** — update `grammar-state.json` (see **Persistence and Calendar sync**).
10. **Write calendar file** — after writing `grammar-state.json`, write a new timestamped `japanese-grammar-review-<timestamp>.ics` file at the vault root (see **Persistence and Calendar sync**).

Don't skip any step. Start practicing immediately after the user triggers the skill.

---

## Parsing

### Grammar topics (`# 文法` and `# Vocabulary`)

Both top-level sections contain grammar points to drill. `# 文法` is core grammar; `# Vocabulary` covers more complex sentence-construction patterns that don't fit a single `#w`/`#wc`/`#wp` line. Treat them the same way.

For each section, find its `^# ` heading and collect content until the next `^# ` heading of the same level.

Load `.cowork/skills/_heading-roles.md` and apply its rules to the section's heading tree — roles are content-based and apply at **any nesting depth** (real patterns appear at `##`, `###`, and `####`):

- **Point** headings become drill points — one `{grammar_header, body_text, source_section}` triple each. Scaffolding children (`Examples`, `Structure`, …) fold into the point's `body_text`.
- **Container** headings are never drilled themselves — their descendant points are drilled individually.
- **Scaffolding** headings are never drill points.
- practice-grammar applies these rules deterministically — no user gate. When a child heading is ambiguous (explanation-part vs sub-pattern), fold it into the parent point's body.
- Preserve Japanese characters exactly.

The body text (Structure blocks, examples) is what generates exercises.

**Migration note:** role-based parsing can change the drill-point set for lessons first drilled under the older level-based rules. `grammar-state.json` entries whose `grammar_header` no longer matches any heading are skipped with a warning (existing behavior) — when that warning fires, tell the user which entry was orphaned so they can re-practice the lesson or delete the stale entry.

#### Use case extraction

After building each triple, identify the use cases within the body text:

1. **`### Use cases` section present** — each numbered item in that list is one use case. Extract the item number and its short description as the use case label (e.g. `"1. ongoing state"`, `"2. time period"`, `"3. whole area"`).
2. **`### Structure` section with multiple top-level bullet variants** — if the section contains two or more top-level bullet points each beginning with a structural pattern (`V「...」`, `N + ...`, `いadj`, `なadj`, etc.) with distinct structures, each top-level variant is one use case. Label with the pattern text (e.g. `"V「dict」+ の"`, `"V「た」+ の"`).
3. **Neither applies** — the grammar point is prose/examples only, no explicit structural variants. Treat the whole grammar point as one use case (label: the grammar header itself).

**Extracted-file flow (`## Structure` / `## Use Cases` at H2 level)**: apply the same three-way logic, but keyed on **semantic content, not markdown heading level or bullet/heading style**:

1. **Multiple distinct structural sub-groups** — if `## Structure` (or `## Use Cases`) contains two or more genuinely distinct structural sub-groups (e.g. different verb-group conjugation patterns, different grammatical contexts, different registers of the same pattern), each sub-group is its own use case — regardless of whether the file expresses them as H3 subheadings, bold labels, bullets, or plain prose, and regardless of heading depth. Do not key this rule on any specific markdown construct (H3, numbered list, etc.) — those are incidental formatting choices that vary file to file. Label each use case with its sub-group's own heading/label text.
2. **Single unified pattern** — if `## Structure`/`## Use Cases` describes one pattern with no distinct sub-groups, the whole point is one use case (label: the grammar header / H1 itself). **This is the common case in current data** — verified against all 8 non-container files extracted so far (all from UN4GL14); only `o-go-v-masukudasai-respectful-request-form.md` has genuinely distinct sub-groups (Group 1/2 verbs vs. Group 3 vs. Exceptions — currently marked with H3 headings, but the rule above keys on the semantic grouping, not the H3 markup itself).

Same labels-stay-internal rule as above — the use case label must never appear in the exercise prompt.

**Unconfirmed against a second lesson**: this extracted-file rule set is derived from a single-lesson sample (all 8 extracted files come from UN4GL14). Re-validate against a second lesson's extracted files, which may use different formatting conventions, once one is available.

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

### Vocabulary base (`Vocabulary/*.md` — extracted-file topics only)

Extracted-file topics have no lesson `# ごい`/`# ひょうげん` pool of their own (the file itself contains no vocab section). When a session includes at least one extracted-file topic, supplement the pool from `Vocabulary/*.md`:

- Source: every `.md` file directly under `Vocabulary/` (**top level only**) — skip the `Vocabulary/JLPT-decks/` subdirectory entirely.
- Collect only **plain tag lines** — never lines inside an Anki card-format block.
- **Block-boundary rule (explicit, mechanical)** — real files mix both formats, so apply this test to every `#w`/`#wc`/`#wp` line encountered:
  - A **card block** starts at a tag line whose next non-blank line is a card-field line (e.g. `ほんやく:`, `Przykład:`, `informal:`, `polite:`, `sonkeigo:`, `kenjougo:`, or any other `Label:` line). The block ends at the next `<!--ID:-->` line, **inclusive**, or at the next `---` separator line — whichever comes first. Never read past a card block's closing `<!--ID:-->` line back into plain-line collection; treat it strictly as the block's closing boundary.
  - A **plain usable line** is a `#w`/`#wc`/`#wp` tag line whose next non-blank line is **not** a card-field line — i.e. it is another tag line, a `---` separator, or end of file. Collect these into the pool.
  - Files vary in how the two formats mix: `Interview.md`/`Car.md` separate card blocks with `---`; `Bank-vocabulary.md`/`Post-vocabulary.md`/`Slownictwo-kolejowe.md` interleave plain tag lines directly between card blocks with no `---` separator; a file can also be 100% cards (e.g. `Interview.md`), yielding zero usable lines — that's fine, just move to the next file.
- For each usable line, parse `{japanese, reading, translation, type}` exactly as in the lesson vocab pool above, but the parsing must be **tag-position-agnostic**: the lesson-pool format documented above is tag-last (`日本語（よみ）- translation #w`), while real `Vocabulary/*.md` plain lines are tag-first (`#w 日本語（よみ）- translation`). Accept both orders.
- Prefer topically relevant words when drawing from this base for a given extracted-file topic (best-effort judgment — deterministic topic_slug-to-file matching is Phase 2, not implemented here).

**Mixed-session pool merge**: the final pool for a session = union of (lesson `# ごい`/`# ひょうげん` pools, from lesson-file entries) + (Vocabulary base, from extracted-file entries). Apply the existing dedup-by-Japanese-form rule across the merged pool (keep first occurrence, session-list order). The existing outside-vocab rule (strict N5, used only when the pool cannot express the grammar point) remains the final fallback and is unchanged.

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

**Weak-point bias** — if the state entry for this grammar point has `weak_points`, design the exercise so the answer requires getting that aspect right (e.g. if the weak point is "particle placement," the exercise must have the particle in the target answer). For weak-point reinforcement (low SM-2 ease or recent failure), prefer Type 1 or Type 3. Avoid Types 5 and 6 when targeting known weak conjugations — those types test comprehension and meta-awareness, not production accuracy. For extracted-file topics, if the weak_point names a pattern confusion (e.g. "だけ vs しか"), apply the **weak_points ↔ confused_with synergy** rule instead (see Metadata-driven exercise generation) — that takes priority over the generic bias above for that topic.

**Type selection rule** — pick the type that best fits what the grammar point needs:
- Single nuanced word/expression (ぜひ, きっと, etc.) → Type 1 or Type 6
- Group of similar forms (conditionals, て-forms, aspect pairs) → Type 2 or Type 4; Type 2 requires all four choices to be genuinely confusable (see confusability definition above) — never use it for a single grammar point where the choice is obvious
- Counters, classifiers, specific constructions → Type 3
- Grammar points with rich context dependency → Type 5
- Any grammar point the student has already seen in a prior session (recorded in grammar-state.json) → prefer Type 6
- Extracted-file topic with a resolvable `confused_with` entry → Type 2 is available even without in-lesson confusable forms (see Metadata-driven exercise generation → confused_with); a `register: polite` topic may take the plain↔keigo transformation flavor on one existing use-case exercise (see Metadata-driven exercise generation → register)

**Variety rule** — vary types only when multiple types are equally valid for a given grammar point. Never override the pedagogically correct type just for variety.

**Non-trivial exercise checklist — mandatory.** Before outputting any exercise, verify all three gates pass. If a gate fails, redesign the exercise (change type or rewrite the prompt) until it passes all three.

**Gate 1 — Prompt does not leak the answer — grammar point name must not appear anywhere in the exercise shown to the student before they answer.** The prompt must not contain, quote, or directly name the exact form the user must produce. A prompt like "Translate to Japanese: 'I decided to go to graduate school'" is fine — the grammar form (ことにしました) is not named in the prompt. A prompt like "Use ことにする to say you decided to quit" fails because it names the target form; rewrite as a neutral translation or context prompt instead. The grammar point name is held internally by Claude and may appear in grading feedback after the student submits their answer — never before.

**Gate 2 — Answer requires genuinely using the grammar point.** A native speaker who does not know this grammar point but knows vocabulary could not produce the answer by elimination or by copying surrounding text. If they could, upgrade the exercise type (e.g. fill-the-blank → translate-to-Japanese).

**Gate 3 — Conjugation target is not a single morpheme.** If the answer requires adding or changing only one particle or suffix (ない, ます, か) to a fully given stem, the exercise is too narrow. The exercise must require the user to produce the whole grammatical construction, not just append one character to a given stem. Exception: exercises explicitly testing a single difficult distinction (e.g. rendaku in counters, sound changes in irregular forms like いっぽん, さんぼん) are allowed, because the tested knowledge is genuinely difficult and cannot be meaningfully widened.

---

## Metadata-driven exercise generation (extracted-file topics)

This section applies only to grammar points loaded via the **extracted-file flow** (Multi-lesson file loading, step 2a). Their frontmatter fields (`confused_with`, `register`, `function`, `topic_slug`) unlock additional exercise-generation options beyond the base rules in **Exercise generation** above. Lesson-file topics are unaffected — nothing in this section changes their behavior.

### confused_with — Type 2 sourcing and minimal-pair contrast

- **On-demand distractor sourcing.** For an extracted-file topic, Type 2 distractors may be drawn from its `confused_with`-linked patterns **even when those patterns are not part of the current session**. Load `grammar-index/grammar/<slug>.md` on demand, read-only, solely to retrieve its pattern name (H1, or frontmatter `pattern` if the H1 is unavailable). This relaxes, for extracted-file topics only, the base Type 2 constraint that confusable forms must come from within the lesson itself.
- **Test-line seeding.** The pre-authored `— test: <question>` line under `## Often confused with` seeds Type 2 / Type 6 prompts — build the discrimination the exercise tests from that contrast question. Wrong-answer feedback quotes or derives from the test line.
- **Broken reference fallback.** If a `confused_with` slug does not resolve to an existing file under `grammar-index/grammar/` (confirmed live example: `o-go-v-masushimasu.md` lists `o-go-v-masukudasai`, but the real file is `o-go-v-masukudasai-respectful-request-form.md`), silently skip that specific pairing and fall back to ordinary Type 2 distractor selection for the topic. Never print a warning for this — it is a data-quality issue in the extract-grammar pipeline's output, outside this skill's control, and must never block or interrupt a session.
- **Minimal-pair contrast exercise.** When both halves of a `confused_with` pair are due in the same session **and land in the same generation batch** (Workflow step 6/7a — batches are formed by even-count split with no `confused_with`-awareness), generate one contrast exercise (built from the pair's test line) that **replaces** one exercise slot for each of the two topics. It does not add to the session — the total exercise count stays exactly as it would without the pair merge. The self-evaluation score from this one exercise counts toward SM-2 for **both** topics (both grammar_point_ids receive the same min_score/weak_points contribution from it).
  - **Phase-1 batching constraint (known limitation).** If both halves of a pair land in the **same** batch, apply the minimal-pair replacement above. If they land in **different** batches, do **not** attempt a cross-batch merge — treat each topic independently with ordinary Type 2 distractors (using the on-demand lookup above, which works regardless of batching). This gap is fully resolved by Task C's `topic_slug`-based batching (Phase 2, deferred) and is out of scope for Phase 1.
  - **`Exercise N / T` total.** `T` must be computed **after** pair-merging is applied, at session start — the progress indicator must reflect the merged (post-replacement) count, not the pre-merge count.

### register — situation matching and transformation flavor

- Exercise situations for an extracted-file topic must match its `register` frontmatter value **and** the prose in its own `## Register` section — never default to a generic "polite" or "formal" flavor without reading that section.
- **`register: polite`** — situations should be business/service/customer scenarios. One of the topic's existing use-case exercises may take a **plain ↔ keigo transformation** form (student converts a given plain-register sentence to the keigo pattern, or vice versa) as an **alternative form** — this does not add an exercise, it replaces the form of one that would exist anyway; session length is unchanged.
- **`register: tiered`** (confirmed live examples due day one: `teineigo-polite-expressions.md`, `uchi-soto-in-group-out-group.md`) — do **not** apply the polite-transformation flavor above. Instead, build situations that exercise the register-**selection** logic itself: e.g. the ウチ・ソト (in-group/out-group) boundary decision, or tier-escalation across a formality scale (ます／です → ございます／でございます). Read the pattern's own `## Register` section prose for the specific selection rule to drill — which parties, which contexts trigger which tier — rather than inferring a generic transformation.

### weak_points ↔ confused_with synergy

When a stored `weak_point` string for an extracted-file topic names a pattern confusion (e.g. `"だけ vs しか"`), look up that topic's `confused_with` list, load the counterpart file (same on-demand, read-only rule as above), and build a targeted discrimination drill from its test line and pattern name — this takes priority over a generic weak-point-biased exercise for that topic.

---

## Interaction flow

There are two modes — **batch** (default) and **interactive**. Pick batch unless the user explicitly asks for one-at-a-time.

**Progress indicator — required.** Every exercise prompt MUST start with `Exercise <current> / <total>` so the user always knows where they are in the session. `<current>` is 1-based (first exercise is `1 / N`, last is `N / N`). The total is fixed at the start of the session and does not change mid-session. If the session includes a `confused_with` minimal-pair merge, `<total>` already reflects the post-merge count (see Metadata-driven exercise generation → confused_with) — merging happens before the total is fixed, not after. The exercise title shows only the number — never the grammar point name. Study Mode exercises use a local `study_counter` and are excluded from the session-wide progress indicator.

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
- `batch_number` and `num_batches`: so Step 3 knows whether to ask "Next batch / Finish" (non-last batch) or simply end the session (last batch — the session was already saved before Study Mode was entered)
- `is_last_batch`: boolean
- `vocab_pool`: the session vocab pool (needed for Study Mode exercise generation)
- `weak_points`: per grammar_point_id weak_points, as loaded once at Workflow step 5 (session start) and/or accumulated in memory during the session — never re-read from `grammar-state.json` after persistence

Follow the instructions in that file exactly.

---

## Grading

Compare user's answer to the expected answer with tolerance:

- **Kanji vs kana** — accept either for words that have both forms, unless the exercise is specifically testing kanji.
- **Particle correctness** — strict. Wrong particle = mistake, note as weak point.
- **Verb conjugation** — strict. Wrong form = mistake.
- **Word order** — if the sentence is still grammatically valid and conveys the same meaning, accept with a note rather than mark wrong.
- **Spelling typos** — accept if the intent is clear and only one character is off.
- **Register match (extracted-file topics only)** — a grammatically correct answer in the wrong register is a mistake. Name the register mismatch and cite the `## Register` guidance in feedback; for `register: tiered` patterns, cite the specific selection rule that was violated (e.g. which party/context should have triggered the other tier), not a generic politeness note.

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

For the last batch, this happens immediately upon reaching self-evaluation
completion for that batch — before the `Study mode / Finish` prompt is shown
— not after the user chooses to finish. (For an early "stop"/"end" at any
other point mid-session, this also runs immediately with scores collected so
far.) Read `.cowork/skills/practice-grammar-srs.md` and follow its instructions.
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
