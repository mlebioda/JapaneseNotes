# Practice Grammar — Study Mode v2

## Goal

Update the `practice-grammar` skill to add a Study Mode that the user can enter between any two batches (or after the last batch). The current between-batch prompt ("Ready for next batch?") is replaced with a deliberate choice prompt. Study Mode lets the user select topics from the just-completed batch, get an explanation tied to their actual answers, optionally do targeted exercises (all 6 types at once), and ask follow-up questions — before resuming the main session. Self-evaluation scores from Study Mode practice are not persisted.

---

## Approach

Two sections of the skill need to change: the **batch loop** (step 5e and 5d in the current workflow) and a new **Study Mode** interlude section. The between-batch prompt is replaced with a two-option or three-option choice depending on whether it is the last batch. Study Mode is a blocking interlude — the batch loop does not advance until Study Mode exits and the user makes an explicit choice.

No changes to exercise generation, grading, persistence, or calendar sync logic.

---

## Sections of the skill that change

### 1. `## Workflow` — Step 7e (between-batch prompt)

**Current text (step 7e):**
> If B < `num_batches`: print `Batch B / num_batches complete.` then ask `Ready for the next batch? (yes / stop)`. Wait for the user. If "stop": write grammar-state.json with all self-scores collected so far, write the .ics file, print the session summary for drilled topics only, and end the session. If "yes" or any affirmative: continue to next batch. If user asks a question, answer it and then ask again before proceeding.

**Replace with:**

After self-evaluation scores are collected for batch B:

- If B < `num_batches` (non-last batch):
  Ask the user:
  ```
  Next batch / Study mode
  ```
  - "Next batch" (or equivalent affirmative) → continue to batch B+1.
  - "Study mode" → enter Study Mode for the topics in batch B (see **Study Mode** section below). After Study Mode exits, ask again: "Next batch / Finish" if not last batch.
  - If the user asks an off-topic question, answer it and re-present the same prompt.
  - The prompt must always appear — never auto-advance to the next batch.

- If B == `num_batches` (last batch):
  Ask the user:
  ```
  Study mode / Save & finish
  ```
  - "Study mode" → enter Study Mode for the topics in the last batch. After Study Mode exits, proceed to post-session (write state + calendar).
  - "Save & finish" (or equivalent) → proceed to post-session.
  - If the user asks an off-topic question, answer it and re-present the same prompt.
  - The prompt must always appear — never auto-finish without user confirmation.

**Stop / early exit rule:** Remove "stop" as a between-batch option. The only way to exit early is via "Save & finish" on the last batch prompt, or by the user explicitly typing "stop" or "end" as a standalone message at any point (existing implicit exit behavior). If the user types "stop" mid-session, write grammar-state.json and .ics for all scores collected so far, print the partial summary, and end.

---

### 2. New `## Study Mode` section (insert after `## Interaction flow`)

Add a new top-level section `## Study Mode` to the skill file. Full specification:

#### Trigger

Study Mode is entered only when the user selects "Study mode" from the between-batch prompt (see Workflow step 7e above). It cannot be entered from any other point in the session.

#### Step 1 — Topic selection

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

#### Step 2 — For each selected topic

Process each topic in sequence. For each topic:

**2a. Explanation**

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

**2b. Choice prompt**

After presenting the explanation, ask:

```
Practice / Next topic / Questions
```

**2c. Branch**

- **"Questions"** → the user asks a follow-up question about this topic. Answer it using lesson content + Claude's knowledge. Use web search only if the lesson content and Claude's knowledge are insufficient to answer the question fully (same threshold as the explanation step). After answering, re-present: `Practice / Next topic / Questions`.
- **"Next topic"** → move to the next selected topic (skip to 2a for the next topic, or exit Study Mode if this was the last topic).
- **"Practice"** → go to Step 2d.

**2d. Study Mode practice**

Attempt one exercise per exercise type (Types 1–6 as defined in `## Exercise generation`). Each exercise targets this single grammar point. Apply all existing exercise generation rules (furigana rule, vocabulary rule, gate checks, confusability prerequisites, non-trivial exercise checklist). If a type cannot be validly constructed (fails its gate or a prerequisite such as Type 2 confusability), skip that type. Require at least 4 valid exercises; if fewer than 4 are valid, proceed with however many are valid — do not pad. Report any skipped types to the user after grading feedback.

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

```
Next topic / Questions
```

- **"Questions"** → user asks a follow-up question. Answer it. Re-present: `Next topic / Questions`.
- **"Next topic"** → move to next selected topic (back to 2a), or exit Study Mode if this was the last topic.

There is no self-evaluation step, no "Needs practice / Solid" summary for Study Mode exercises.

#### Step 3 — After all selected topics are done

When all selected topics have been processed (or the user chose "none"):

- If not the last batch: ask `Next batch / Finish`
  - "Next batch" → continue to batch B+1.
  - "Finish" → proceed to post-session (write state + calendar) with all scores collected so far.
- If the last batch: proceed directly to post-session (write state + calendar).

The "Finish" option in Step 3 is a full early exit — write grammar-state.json and .ics for all scores collected so far, print the session summary, and end.

---

### 3. `## Interaction flow` — progress indicator exception

Add one sentence to the `## Interaction flow` section: "Study Mode exercises use a local `study_counter` and are excluded from the session-wide progress indicator."

### 4. `## Session summary` — no change needed

The session summary covers only grammar points that were drilled in the main batch exercises (those with self-evaluation scores). Study Mode exercises do not appear in the summary. The existing summary rules are unchanged.

### 5. `## Persistence` — minor addition

Add one sentence: "Study Mode exercises do not contribute to `score_buffer` or `weak_point_buffer`. Only main batch exercises produce scores that are written to `grammar-state.json`."

---

## Steps

1. Edit `## Workflow`, step 7e — replace the current "Ready for next batch?" prompt with the two-prompt spec (non-last: "Next batch / Study mode"; last: "Study mode / Save & finish"). Preserve the early-exit-on-"stop" behavior as a standalone escape.
2. Insert new `## Study Mode` section into the skill file immediately after `## Interaction flow`. Cover: trigger, topic selection (Step 1), per-topic loop (Steps 2a–2d), and post-study prompt (Step 3).
3. Edit `## Interaction flow` — add one sentence: "Study Mode exercises use a local `study_counter` and are excluded from the session-wide progress indicator."
4. Edit `## Persistence` — add the Study Mode exclusion sentence.
5. Do NOT change `## Exercise generation`, `## Grading`, `## Parsing`, `## Calendar sync`, `## Session summary`, or `## Scope resolution`. Those sections are unchanged.

---

## Risks

- **Session-wide exercise counter** — Study Mode uses its own `study_counter` (`Exercise study_counter / total_study`). The main session counter is frozen on Study Mode entry and restored on exit. If the skill tracks a single running counter, it needs a guard to enforce this.
- **User's actual answer referencing** — the explanation step (2a) must quote the user's answer from earlier in the same session. Claude must retain all batch answers in context. For long sessions with many batches, this may push earlier answers out of context. If a specific answer is no longer retrievable, fall back to "Your answer was not recorded — here is the general explanation."
- **No changes to lesson files** — the skill remains read-only on lesson files. No risk to Anki export data or `<!--ID:-->` lines.
- **Study Mode does not change SM-2 state** — by design, no Study Mode exercise contributes to persistence. If the user practices 6 exercises in Study Mode and then "Finishes" without completing the next batch, the SM-2 entry for that topic is based only on the earlier batch score, not on Study Mode performance. This is intentional.
- **"None" exit from topic selection** — when the user picks "none", Study Mode skips the topic loop and lands directly at Step 3. Step 3 handles both cases (non-last batch: "Next batch / Finish"; last batch: proceed to post-session). The between-batch prompt must not be re-presented from the top; doing so would create a loop.
