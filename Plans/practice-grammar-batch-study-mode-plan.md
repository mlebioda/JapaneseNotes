# Practice Grammar — Batch Session Mode & Study Mode

## Goal

Extend `practice-grammar` with two new capabilities:

1. **Scope-based triggers** — the user can now say "let's practice today's topics" or "practice 10 most overdue topics" and the skill resolves the grammar point list from `grammar-state.json` rather than from a single lesson file. This allows cross-lesson review sessions that respect the spaced-repetition schedule.

2. **Study Mode** — an optional pause between batches where the user can deep-dive into specific weak topics (explanation + targeted exercises) before resuming the main session. Self-evaluation scores are held in memory throughout and written to `grammar-state.json` only once, at the very end.

The existing single-lesson trigger (`let's practice UN5GL14`) must continue to work exactly as before.

---

## Approach

The skill gains a new top-level branch: **scope resolution** vs **lesson-file resolution**. Scope resolution reads `grammar-state.json` directly, sorts/filters by `next_review`, and builds the grammar point list without opening any lesson file. Lesson files are opened lazily — only when exercises for a grammar point are about to be generated.

Self-evaluation scores are buffered in a session-scoped scratch object throughout the session and written to `grammar-state.json` in a single pass at the very end, preserving the existing SM-2 logic.

Study Mode is an optional interlude between any two batches. It uses the same exercise generation machinery but wraps it in a tighter explain-first loop. Internet information (WebSearch / WebFetch) may be used during Study Mode explanations.

---

## Steps

### 1. Trigger detection (entry point)

Add scope-based triggers alongside the existing lesson-file triggers.

Lesson-file triggers (unchanged):
- "let's practice UN5GL14"
- "practice `<lesson>`"
- "exercise `<lesson>`"
- "drill grammar in `<lesson>`"

New scope triggers:
- "let's practice today's topics" → scope = `due_today`
- "let's practice overdue topics" → scope = `overdue`
- "let's practice N most overdue topics" → scope = `most_overdue`, limit = N
- Natural variants: "practice grammar due today", "drill overdue grammar", "practice my 5 most overdue grammar points", etc.

When a scope trigger is detected, go to Step 2. When a lesson-file trigger is detected, go to the existing workflow (Step 1 of the original skill) — no changes there.

---

### 2. Scope resolution from grammar-state.json

Read `.cowork/progress/grammar-state.json`. For each entry in `grammar_points`, compute how many days overdue it is:

```
overdue_days = today - next_review   (negative = not yet due)
```

Apply the scope filter:

| Scope | Filter |
|---|---|
| `due_today` | `overdue_days >= 0` (due today or overdue) |
| `overdue` | `overdue_days > 0` (strictly past due) |
| `most_overdue` N | top N by `overdue_days` descending (ties broken by `ease` ascending — lower ease = harder = higher priority) |

Sort the resulting list by `overdue_days` descending so the most overdue topics come first.

If the filtered list is empty, inform the user ("No grammar points are due today. Next review: `<earliest next_review date>` — `<N>` points.") and stop.

**Output of this step:** a flat list of grammar point IDs that will be practiced this session, in priority order.

---

### 3. Lazy lesson-file loading

Each grammar point ID is of the form `<lesson_code>::<slug>` and its `grammar-state.json` entry contains `"lesson_file": "<relative path>"`. Crucially, multiple grammar points from the same lesson share one lesson file — open each file at most once.

To load the content needed for exercise generation, for each unique `lesson_file` referenced by the session's grammar point list:

1. Read the lesson file up to `# Summary` (same `awk` pattern as existing skill).
2. Extract the full grammar section (`# 文法` + `# Vocabulary`) and the vocab pool (`# ごい` + `# ひょうげん`) once.
3. Cache under the lesson code key so subsequent grammar points from the same lesson reuse it.

Then, for each grammar point in the session list, locate its `## Heading` (or `### Heading`) in the cached grammar section by matching the `grammar_header` string from `grammar-state.json`. Extract the body text and use cases exactly as the existing parsing rules describe.

If a lesson file cannot be read (file moved, renamed, or deleted), log a warning to the user and skip that grammar point: "Skipping `<id>` — lesson file not found: `<path>`". Continue with the rest of the session.

---

### 4. Pre-session summary and batch split

After scope resolution and before generating any exercises, tell the user:

```
Found N grammar points due for review (scope: overdue topics).
  Most overdue: <grammar_header> — <overdue_days> days late
  ...up to 3 examples...

How many batches do you want to split these into?
(e.g. enter 1 for one long session, 2 for two halves, etc.)
```

Wait for the user's answer. Compute batch size: `ceil(N / num_batches)`. If N = 0 after filtering, stop. If the user does not specify a number, default to 1 batch (equivalent to the existing flow).

Store the batch plan:
```
session = {
  grammar_point_ids: [...],    # full list in priority order
  batches: [[id, ...], ...],   # split into num_batches sub-lists
  current_batch_index: 0,
  score_buffer: {},            # keyed by grammar_point_id, written at end
  weak_point_buffer: {}        # keyed by grammar_point_id
}
```

---

### 5. Batch loop

Repeat for each batch:

#### 5a. Generate and present exercises

For each grammar point in the current batch, apply the existing exercise generation logic (one exercise per use case, all exercise types, furigana rule, vocabulary rule, gate checks, weak-point bias). Stack all exercises into a single batch message, as in the existing batch mode.

Session header for scope mode:
```
Batch 1 / 2 — 5 topics, 8 exercises. Reply with all answers in one message.

Exercise 1 / 8
...
```

The progress indicator (`Exercise N / T`) counts exercises within the current batch only (T = total exercises in this batch, not in the whole session). The batch header shows the batch number and the exercise total for that batch.

#### 5b. Collect answers and grade

Identical to existing batch mode: user replies once with all answers, skill grades in one follow-up message, then asks for self-scores.

#### 5c. Collect self-evaluation scores

User replies with scores (e.g. `4 2 3 1 3`).

**Do not write to `grammar-state.json` yet.** Instead, accumulate into `score_buffer` and `weak_point_buffer`. For multi-exercise grammar points, take the minimum score as the SM-2 input (same rule as existing skill).

#### 5d. Batch summary and mode choice

Show a compact batch summary (same format as the existing session summary, but titled "Batch N / M complete"):

```
Batch 1 / 2 complete — 5 topics

Solid:
  ✓ Vないで ください    score 4

Needs practice:
  ✗ Counter 本          score 1 — sound changes (いっぽん, さんぼん)
  ✗ て-form (godan)     score 2 — て vs って distinction

What next?
  [next]  — go to Batch 2
  [study] — enter Study Mode on one or more topics from this batch
  [end]   — end session and save scores
```

If the user types `next` (or equivalent): go to Step 5a for the next batch.
If the user types `end` or it is the last batch: go to Step 7 (post-session).
If the user types `study`: go to Step 6 (Study Mode).

---

### 6. Study Mode

Study Mode is an optional interlude, entered between batches (or after the last batch). It does NOT collect self-evaluation scores and does NOT update `grammar-state.json`. It is purely a learning aid.

#### 6a. Topic selection

```
Study Mode — which topics do you want to review?
Topics from this batch:
  1. Counter 本
  2. て-form (godan)
  3. (any topic you name)

Reply with topic number(s) or names.
```

The user may name topics not in the current batch by their grammar header. If a named topic is not recognized (not in `grammar-state.json` and not found in any loaded lesson file), reply: "I don't have a grammar point matching '`<name>`' — please check the name or enter a number from the list."

#### 6b. Topic explanation loop

For each selected topic:

**Explanation step:**

Prepare a detailed explanation of the grammar point. Sources to use, in priority order:

1. The body text from the lesson file (structure blocks, examples, use cases) — always the primary source.
2. Claude's built-in Japanese grammar knowledge.
3. WebSearch / WebFetch if the lesson body is thin (no structure block, fewer than 2 examples) or the user explicitly asks "search for examples" or "find more examples online". Note: WebSearch and WebFetch may not always be available; if they fail or are absent, proceed with sources 1 and 2.

Format of the explanation:
```
## <grammar_header>

### Structure
...

### Meaning
...

### Examples
...

### Common mistakes
(from the grammar point's weak_points if any, otherwise from known learner errors)
```

All kanji must carry furigana (same furigana rule as exercise generation).

After presenting the explanation, ask:
```
Practice this topic now, or move to the next one?
  [practice] — generate exercises for this topic
  [next]     — move to next topic
  [question] — ask a follow-up question about this topic
```

**Practice step (if user chooses [practice]):**

Generate all exercise types applicable to this grammar point (one per use case, as in the normal flow, but all of them rather than the pre-session set — Study Mode is intensive). The user may also suggest a custom exercise: "give me a Type 3 exercise" or "make me translate this sentence: …".

Present exercises one at a time (interactive mode, not batch). After each answer:
- Grade and give feedback (same grading logic).
- Do NOT ask for self-evaluation score (Study Mode scores are not persisted).
- Ask: `[next exercise]`, `[ask question]`, or `[exit study]`.

**Follow-up questions (if user chooses [question]):**

The user may ask any question about the topic or about a specific exercise. Answer using lesson file content + Claude knowledge + WebSearch/WebFetch if needed. Then return to the `[practice] / [next] / [question]` prompt.

#### 6c. Exit Study Mode

When the user has finished all selected topics (or says "exit study", "done", "back"), return to the batch loop:

```
Study Mode complete. Ready for Batch 2 / 2?
  [next] — continue to Batch 2
  [end]  — end session and save scores
```

---

### 7. Post-session: write state and calendar

This step runs after all batches are complete (and after any final Study Mode exit).

#### 7a. Final summary

Show a combined summary across all batches:

```
Session complete — N topics across M batches

Solid (will be reviewed in X days):
  ✓ ...

Needs practice (scheduled sooner):
  ✗ ...
```

#### 7b. Write grammar-state.json

Apply SM-2 updates to `grammar-state.json` for every grammar point in `score_buffer`. Use the same algorithm as the existing skill:

- Minimum score across multi-exercise grammar points (already computed per batch).
- First-review rule (force `interval_days = 4` on first review, score >= 2).
- Merge `weak_points` from `weak_point_buffer` with existing `weak_points` (union, max 5, most recent).
- Set `last_reviewed = today`, `next_review = today + interval_days`, `last_score`, `total_reviews += 1`.

This is a **single write** that covers all batches in one pass. Do not write intermediate results during the session.

#### 7c. Write calendar file

Same logic as existing skill: generate `japanese-grammar-review-<YYYYMMDDTHHMMSS>.ics` at the vault root. Include only grammar points from this session (i.e. the full `score_buffer` key set). Use the newly written `next_review` dates from `grammar-state.json`.

---

### 8. Trigger table update in skill file

Add the new triggers to the `## Trigger` section of `practice-grammar.md`:

```
New scope triggers:
- "let's practice today's topics"
- "let's practice overdue topics"
- "let's practice N most overdue topics"
- "practice grammar due today"
- "drill overdue grammar"
- "practice my N most overdue grammar points"
- Similar natural-language variants referring to a scope rather than a specific lesson
```

---

## Key design decisions

### Why lazy lesson-file loading (Step 3)?

Grammar points in `grammar-state.json` span many lessons. Loading all lesson files upfront for a session of 20 topics would read many files unnecessarily (e.g. a lesson with 10 topics but only 2 in scope). Loading per-lesson-file lazily (and caching within the session) means each file is read at most once and only when actually needed.

### Why hold scores until the end (Step 5c)?

Intermediate writes after each batch would create a window where a partial session (user abandons mid-session) results in some grammar points getting their intervals updated while others don't. Holding all scores until the final write ensures the state is consistent: either the whole session is committed or none of it is. The tradeoff is that if Claude's context is lost mid-session, the scores are lost — this is acceptable for the study use case.

### Study Mode and WebSearch

Study Mode explanations should prefer lesson file content first. WebSearch / WebFetch are a fallback for thin lesson bodies or explicit user requests. They must be treated as optional: if the tool call fails or is unavailable, the explanation must still be generated from lesson content and Claude's knowledge. Never block the Study Mode flow on a network call.

### Score isolation between Study Mode and batch sessions

Study Mode exercises do not produce self-evaluation scores. Only batch exercises do. This is intentional: Study Mode is re-learning under guided conditions, not a fair assessment. Mixing Study Mode performance into SM-2 would inflate ease ratings for material the user just reviewed with full explanation support.

### Grammar point matching by header string

When resolving a grammar point from `grammar-state.json` back to its body text in the lesson file, match by `grammar_header` string against the `##` / `###` headings found in the grammar section. The match is exact (same string). If no exact match is found, try a case-insensitive match, then a whitespace-normalized match. If still no match, skip with a warning (same as unreadable file).

---

## Risks

- **Stale `lesson_file` paths in grammar-state.json** — if a lesson file is renamed or moved after it was first practiced, the `lesson_file` path is stale. Step 3 handles this gracefully (skip with warning), but grammar points that can't be loaded will be silently dropped from the session. A future improvement could re-scan for the file by lesson code.
- **Score buffer lost on context window expiry** — for very long sessions (many batches, lots of Study Mode), Claude's context could fill up. Scores held in the session scratch object would be lost. Mitigation: encourage users to keep sessions to a reasonable number of batches; document this risk in the skill.
- **`grammar_header` matching fragility** — if the lesson file's heading is edited after the grammar point was first practiced (e.g. fixing a typo in the heading), the `grammar_header` in `grammar-state.json` won't match. This is a known limitation; no automatic fix is planned.
- **WebSearch / WebFetch availability** — Study Mode explanations that rely on internet search will silently degrade to lesson-only content if those tools are unavailable. This is acceptable.
- **No changes to `# Summary` or `<!--ID:-->` lines** — this skill remains read-only on lesson files. No risk to Anki export data.
