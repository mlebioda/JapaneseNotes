￥# Practice Grammar Skill Split

## Goal

Split the monolithic `practice-grammar.md` (691 lines) into three files to reduce context loss during long sessions. The primary symptom is that Claude forgets the between-batch gate rule — the requirement to always pause after self-evaluation and ask the user for "Study mode / Next batch", never auto-advancing. Splitting the Study Mode and SRS/Calendar sections into dedicated sub-skills reduces the number of tokens the model must hold simultaneously, keeping the critical gate rule in focus throughout the session.

## Approach

Pure structural refactor — no functionality changes. The main skill keeps all session-driving logic (trigger, scope resolution, batch loop with between-batch gate, parsing, exercise generation, grading, session summary). Two new sub-skill files hold the Study Mode section and the Persistence + Calendar section respectively. The main skill loads each sub-skill on demand with an explicit in-text directive. The between-batch gate rule gets a prominent visual callout added directly in Workflow step 7e of the main skill.

## Steps

### Step 1 — Edit `.cowork/skills/practice-grammar.md`

This is the most sensitive step. Do not drop any content from the sections that remain.

**a) Remove Study Mode section (lines 358–492 in the current file).**
Delete the entire `## Study Mode` section from the main skill — from the `## Study Mode` heading through the end of `### Step 3`. Replace it with a single load directive block:

```
## Study Mode

On first Study Mode invocation, read `.cowork/skills/practice-grammar-study-mode.md`
(skip re-reading if already in context). Pass to it:
- `batch_topics`: list of grammar headers + body_text for topics in the just-completed batch
- `user_answers`: the user's raw answers for each topic in this batch (keyed by grammar_header)
- `batch_number` and `num_batches`: so Step 3 knows whether to ask "Next batch" or proceed to post-session
- `is_last_batch`: boolean

Follow the instructions in that file exactly.
```

**b) Remove Persistence section (lines 547–649) and Calendar sync section (lines 651–682).**
Delete both sections entirely. Replace with a single load directive block placed after `## Session summary`:

```
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
```

**c) Add a prominent between-batch gate callout in Workflow step 7e.**
Immediately before the bullet points in step 7e (the "After self-evaluation scores are collected for batch B" block), insert:

```
> **BETWEEN-BATCH GATE — MANDATORY. After collecting self-scores for any batch,
> ALWAYS present the Study mode / Next batch prompt and wait for user input.
> NEVER auto-advance to the next batch or to post-session. This is the most
> important interaction rule in this skill.**
```

This callout must appear on the same page as the Workflow section so it is read in the same context window pass as the batch loop logic.

**d) Verify nothing else was dropped.** The following sections must remain in full in the main skill after the edit:
- Frontmatter (lines 1–11)
- Trigger (lines 13–31)
- Scope resolution (lines 33–90)
- Workflow (lines 92–143, with callout added at step 7e and load directives replacing the two removed sections)
- Parsing (lines 145–197)
- Exercise generation (lines 199–235)
- Interaction flow (lines 237–348)
- Grading (lines 494–515)
- Session summary (lines 517–545)
- Never touch (lines 684–691)

---

### Step 2 — Create `.cowork/skills/practice-grammar-study-mode.md`

New file. Contains the full Study Mode section extracted verbatim from the current skill, plus a context header at the top.

**Context header (add at top of file):**

```
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
```

**Body:** Paste the full Study Mode content from the current skill verbatim (Steps 1–3, ~135 lines). No other changes.

---

### Step 3 — Create `.cowork/skills/practice-grammar-srs.md`

New file. Contains the Persistence and Calendar sync sections extracted verbatim, plus a context header.

**Context header (add at top of file):**

```
---
name: practice-grammar-srs
description: >
  Sub-skill for practice-grammar. Handles SM-2 state persistence and .ics calendar
  file generation. Loaded once at session end (or on "stop" early exit).
  Study Mode exercises are excluded — only self-evaluation scores from main batch exercises.
---

# Practice Grammar — Persistence and Calendar Sync

## Context required (passed by practice-grammar.md)

- `session_scores`: dict keyed by grammar_point_id →
    `{min_score, weak_points[], grammar_header, lesson_file, interval_days}`
- `session_grammar_ids`: ordered list of grammar_point_ids practiced this session
- `today`: ISO date (YYYY-MM-DD)
- `scope`: "lesson" | "TODAY" | "OVERDUE"
  - "lesson" → write next_review directly (today + interval_days), skip load-control.py
  - "TODAY" or "OVERDUE" → two-step write: SM-2 fields first, then load-control.py for next_review
```

**Body:** Paste the full Persistence and Calendar sync sections from the current skill verbatim (~135 lines). No other changes.

---

### Step 4 — No `.claude/commands/` stubs needed

The two new sub-skills are internal — they are invoked by `practice-grammar.md` via load directives, not by the user directly. No slash command stubs are created for them. The existing `.claude/commands/` entry for `practice-grammar` (if any) does not change.

---

### Step 5 — Smoke-check the split

After all three files are written, verify:

1. Main skill line count is in the 420–460 range (from 691 — minus ~270 removed + ~20 added for load directives and callout).
2. `practice-grammar-study-mode.md` contains all three Study Mode steps and the "Do NOT write to grammar-state.json" rule.
3. `practice-grammar-srs.md` contains both the SM-2 algorithm table and the `ics-export.py` shell command.
4. The between-batch gate callout block is present in Workflow step 7e of the main skill and uses the word "MANDATORY".
5. The main skill's Workflow section still references `## Study Mode` and `## Persistence and Calendar sync` by name (so Claude can find the load directives when it reaches those points).

---

## Risks

- **Content drop during main skill edit** — the edit touches three non-adjacent regions (Study Mode section, Persistence section, Calendar sync section). If the implementer uses find-and-replace it must match the full section boundaries exactly. The `## Grading` and `## Session summary` sections sit between the Study Mode and Persistence sections and must not be disturbed.
- **Study Mode still referenced in Workflow** — Workflow step 7e references "Study Mode" by name. After the edit the `## Study Mode` heading must still exist in the main skill (now containing only the load directive), otherwise the reference becomes a dead link in Claude's reasoning.
- **Context not passed correctly** — if the main skill's load directive omits a required field (e.g. `vocab_pool` for Study Mode exercise generation), the sub-skill will silently degrade. The context blocks in Steps 2 and 3 above are the authoritative lists.
- **Early-exit "stop" path** — the `practice-grammar-srs.md` load must also trigger on early exit. The main skill's Workflow step 7e early-exit bullet ("if the user types 'stop'") must explicitly say "load `practice-grammar-srs.md`" — not just "write grammar-state.json", which is a call to logic that no longer lives in the main file.
- **No functionality loss** — this is a structural refactor only. Any substantive change to grading, SM-2 formula, exercise types, or Study Mode rules is out of scope and must be deferred to a separate plan.
