# Agent System — Precision Rule

## Goal

Add a precision enforcement rule across three agents — planner, skill-implementer, and reviewer — so that every skill written or reviewed in this vault is a precise specification: anyone reading it can predict exactly what will happen when it runs, step by step. The motivation is that skills currently can contain AI-generated filler that "says everything and nothing at the same time", making it impossible for the user to predict execution from a reading.

The rule has three components, one per agent:

- **Planner** — must not write a plan around vague intent. If the user's request contains underspecified details (e.g. "make exercises", "study mode", "generate exercises"), the planner must ask one focused clarifying question to pin down what exactly is meant before drafting the plan.
- **Skill-implementer** — when writing skill content, must produce instructions that are concrete and predictable. The self-review step gains an explicit precision check: are counts explicit, are types named, are steps unambiguous? If any step could be read multiple ways, it must be rewritten before the task is marked complete.
- **Reviewer** — when reviewing a skill, must check whether each step is predictable. A step that could be interpreted multiple ways, or that relies on the model's judgment about "what's applicable", is flagged as a moderate issue.

## Approach

Each agent file (`.claude/agents/planner.md`, `.claude/agents/skill-implementer.md`, `.claude/agents/reviewer.md`) gets a small targeted addition. No existing rules are removed; the precision rule is layered on top of the current workflow. The changes are surgical — one block per agent file.

## Steps

### 1. planner.md — add underspecified-intent gate

In the `## How to collaborate on a plan` → `### Conversation flow` section, add an explicit rule under **Step 1 (Understand the goal)**:

> **Precision gate:** Before writing any plan, check whether the user's request contains underspecified details — vague verbs like "make exercises", "generate questions", "study mode", "review", "practice" without a defined format. If any detail is underspecified, ask one focused clarifying question that pins it down. Do not write the plan until the answer resolves the ambiguity. Example: if the user says "add a study mode", ask "What exactly happens in study mode step by step? Specifically: how many exercises, what types, and how does the user advance?"

### 2. skill-implementer.md — add precision check to self-review (Step 3)

In the `## Workflow` → `### Step 3 — Self-review` section, extend the per-file check list with a precision check:

> - If it is a skill file: run the **precision check** — read each step and ask "if I follow this instruction literally, do I know exactly what to produce?" For each step that fails this test (vague counts, unnamed types, "as applicable", "where relevant", "if needed" without a defined condition), rewrite it before marking the task complete. Specific checks: are counts explicit (e.g. "3–5 sentences" not "a few sentences")? Are exercise types named (e.g. "Type 1 — Contextual production" not "an appropriate exercise")? Are conditions for branching stated precisely (e.g. "if overdue_days > 0" not "if overdue")?

### 3. reviewer.md — add predictability check to 2f Proactive suggestions and 2b Missing rules

In **Step 2b — Missing rules / edge cases**, add as a standing check item:

> - **Predictability** — for each step in the skill's workflow: can a reader follow it and predict the exact output without relying on model judgment about "what's applicable"? If a step says "generate appropriate exercises" or "explain as needed" or "add relevant examples", that is a moderate issue — the instruction relies on implicit knowledge rather than explicit rules. Flag each such step with the problematic phrase quoted.

In **Step 2f — Proactive suggestions**, add a standing note:

> - **Precision [standing check]** — separately from 2b, scan for soft language that survived correctness review: "as appropriate", "where relevant", "a few", "some", "several", "if needed" (without a defined condition), "naturally". Each occurrence is a candidate for [optional] precision improvement — flag only those where a more concrete rule is feasible.

## File paths

- `.claude/agents/planner.md` — add precision gate to Step 1 of conversation flow
- `.claude/agents/skill-implementer.md` — add precision check to Step 3 self-review
- `.claude/agents/reviewer.md` — add predictability check to Step 2b and standing precision scan to Step 2f

## Risks

- These are agent definition files in `.claude/agents/` — they control agent behaviour across the whole vault. Changes should be narrow and additive (no deletions).
- The precision gate in planner adds a blocking step before planning. This is intentional but could slow down well-specified requests. Mitigation: the gate fires only when the request actually contains underspecified details — a precise request should pass through without any extra question.
- The self-review precision check in skill-implementer extends an already-complex step. The check is explicit and mechanical (look for named patterns), so it should not add ambiguity.
