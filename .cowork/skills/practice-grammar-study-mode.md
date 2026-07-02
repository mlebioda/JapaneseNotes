---
name: practice-grammar-study-mode
description: >
  Sub-skill for practice-grammar. Handles the Study Mode section: topic selection,
  per-topic explanation, optional practice exercises, and post-Study-Mode routing.
  Loaded on demand by practice-grammar.md on first Study Mode invocation.
  Never write to grammar-state.json.
---

# Practice Grammar — Study Mode

## Context required (passed by practice-grammar.md)

- `batch_topics`: list of grammar headers + body_text for the completed batch
- `user_answers`: user's raw answers for each topic, keyed by grammar_header
- `batch_number` / `num_batches`: current batch position
- `is_last_batch`: boolean — controls whether Step 3 asks "Next batch" or proceeds to post-session
- `vocab_pool`: the session vocab pool (needed for Study Mode exercise generation)
- `weak_points`: per grammar_point_id weak_points from grammar-state.json (for bias in practice exercises)

---

### Trigger

Study Mode is entered only when the user selects "Study mode" from the between-batch prompt (see Workflow step 7e in practice-grammar.md). It cannot be entered from any other point in the session.

---

### Step 1 — Topic selection

Present the list of grammar points from the just-completed batch (numbered). Ask:

```
Which topics from this batch do you want to review?
  1. <grammar_header_1>
  2. <grammar_header_2>
  ...

Reply with number(s), topic name(s), or "none" to skip.
```

- The user may name any subset (e.g. "1 3", "Counter 本", "all").
- "None" or empty reply → treat as skipping the topic loop entirely and jump directly to Step 3. Step 3 already handles both cases (non-last batch: ask "Next batch / Finish"; last batch: proceed to post-session). Do not re-present the between-batch prompt.
- If the user names a topic not in the current batch list, reply: "That topic is not in this batch. Please choose from the numbered list." and re-present the prompt once. If still not recognized: skip silently.

Selected topics are processed in the order the user listed them (or in batch order if "all").

---

### Step 2 — For each selected topic

Process each topic in sequence. For each topic:

#### 2a. Explanation

Produce a detailed explanation of the grammar point using the following sources (in priority order):

1. Body text from the lesson file for this grammar point (structure blocks, examples, use cases) — always the primary source.
2. Claude's built-in Japanese grammar knowledge.
3. Web search (WebSearch / WebFetch) — only if the lesson body is thin (no structure block or fewer than 2 examples), or if the user explicitly requests "search for examples" or "find more online". If web tools fail or are unavailable, proceed with sources 1 and 2 without blocking.

**Crucially:** reference the user's actual answer from this batch when explaining. If the user answered correctly, call that out and note why it worked. If the user answered incorrectly or scored 1–2, quote their answer, show the correct form, and explain the specific error.

**Answer retrieval fallback:** If the user's answer for this grammar point cannot be retrieved from the session (e.g. the batch was stopped before this point was reached), fall back to: "Your answer was not recorded — here is the general explanation." Do not block or error.

Format:

```
## <grammar_header>

### Structure
...

### Meaning
...

### Examples
...

### Your answer this session
You wrote: <user's answer (plain Japanese, no furigana)>
<"Correct — because ..." or "Incorrect — <specific error explanation>">

### Common mistakes
<from weak_points if any, otherwise from known learner errors>
```

All kanji in the explanation must carry furigana (same furigana rule as exercise generation).

#### 2b. Choice prompt

After presenting the explanation, ask:

```
Practice / Next topic / Questions
```

#### 2c. Branch

- **"Questions"** → the user asks a follow-up question about this topic. Answer it using lesson content + Claude's knowledge. Use web search only if the lesson content and Claude's knowledge are insufficient to answer the question fully (same threshold as the explanation step). After answering, re-present: `Practice / Next topic / Questions` (or `Practice / Continue / Questions` if this is the last selected topic — "Continue" exits Study Mode).
- **"Next topic"** / **"Continue"** → if there is a next selected topic, move to it (skip to 2a); if this is the last selected topic, exit Study Mode and proceed to Step 3.
- **"Practice"** → go to Step 2d.

#### 2d. Study Mode practice

Attempt one exercise per exercise type (Types 1–6 as defined in `## Exercise generation` in practice-grammar.md). Each exercise targets this single grammar point. Apply all existing exercise generation rules (furigana rule, vocabulary rule, gate checks, confusability prerequisites, non-trivial exercise checklist). If a type cannot be validly constructed (fails its gate or a prerequisite such as Type 2 confusability), skip that type. Require at least 4 valid exercises; if fewer than 4 are valid, proceed with however many are valid — do not pad. Report any skipped types to the user after grading feedback.

**Session counter:** Study Mode uses its own local counter `study_counter` (resets to 1 at the start of each topic's practice block). The session-wide exercise counter is frozen on Study Mode entry and restored on exit. Study Mode prompts show `Exercise study_counter / total_study` where `total_study` is the number of valid exercises generated for this topic.

Present all valid exercises at once (batch layout, same as normal batch mode):

```
Study Mode — <grammar_header> (total_study exercises). Reply with all answers in one message.

Exercise 1 / total_study
...

Exercise 2 / total_study
...

...

Exercise total_study / total_study
...
```

User replies once with all answers. Grade all in one follow-up message (same grading display rules as batch mode: ✓/✗ lines, You/OK/error, plain Japanese, no furigana in diffs).

Do NOT ask for self-evaluation scores. Do NOT write any Study Mode results to grammar-state.json.

After grading, ask:

- If there are more selected topics remaining: `Next topic / Questions`
- If this is the last selected topic: `Continue / Questions`

Where "Continue" exits Study Mode and proceeds to Step 3.

- **"Questions"** → user asks a follow-up question. Answer it. Re-present the same prompt (`Next topic / Questions` or `Continue / Questions` — same context rule applies).
- **"Next topic"** → move to next selected topic (back to 2a).
- **"Continue"** → exit Study Mode and proceed to Step 3.

There is no self-evaluation step, no "Needs practice / Solid" summary for Study Mode exercises.

---

### Step 3 — After all selected topics are done

When all selected topics have been processed (or the user chose "none"):

- If not the last batch: ask `Next batch / Finish`
  - "Next batch" → continue to batch B+1.
  - "Finish" → proceed to post-session (write state + calendar) with all scores collected so far.
- If the last batch: proceed directly to post-session (write state + calendar).

The "Finish" option in Step 3 is a full early exit — load `practice-grammar-srs.md`, write grammar-state.json and .ics for all scores collected so far, print the session summary, and end.

---

## Never touch

- Lesson files under `JPLessons/` (read-only — never write)
- `<!--ID: -->` lines anywhere
- `TARGET DECK` lines
- Do NOT write to grammar-state.json — Study Mode exercises are excluded from SRS state
- Do not run `git push` or any remote git operation
