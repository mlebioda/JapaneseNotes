# Agent Lessons Learned

<!-- Entries appended by scribe capture — domain: agent design, A2A wiring, orchestration, inter-agent routing -->

---

## 2026-05-31 — orchestrator.md (implementation)

**Classification**: bug-fix
**What happened**: Nine A2A wiring bugs fixed in orchestrator.md: synthetic TARGET notation replaced with real Bash file lookup, broken revision loop corrected, slug resolution step added, post task type removed as out-of-scope, DONE block attribution corrected, and explicit write-prohibition Hard rules added.
**Rule**: **[Rule]** Never pass synthetic or inferred path strings between pipeline stages — always resolve real filesystem paths via a Bash lookup before delegating to a sub-agent, and document the resolution step explicitly in the agent definition.
**Source**: uncommitted — skill-implementer

---

## 2026-05-31 — orchestrator.md

**Classification**: new-feature
**What happened**: Plan created to fix eight structural bugs in orchestrator.md: synthetic TARGET for `new` tasks, broken revision loop, missing slug resolution, absent post pipeline, inaccurate DONE block, and no explicit write-prohibition rules.
**Rule**: **[Rule]** When designing an orchestrator agent, explicitly prohibit write access in its hard rules and define a concrete mechanism for passing state (e.g. slug, reviewer output) between pipeline stages rather than relying on implicit context.
**Source**: uncommitted — orchestrator-fixes plan

---

## 2026-05-31 — planner.md

**Classification**: bug-fix
**What happened**: `REVISION_NOTES` was added as a documented optional field in planner's A2A input schema; the agent was instructed to apply it directly rather than re-asking the user, enabling the orchestrator's revision loop to work without user interruption.
**Rule**: **[Rule]** Always declare every optional A2A input field in an agent's expected-input format block and provide explicit handling instructions, so callers can pass structured data without the agent re-asking the user for information it has already received.
**Source**: uncommitted — skill-implementer

---

## 2026-05-31 — orchestrator.md (second pass)

**Classification**: bug-fix
**What happened**: Second-pass wiring fixes addressed five residual issues: unhandled no-issues reviewer outcome, fragile mtime-based slug resolution, absolute paths in call templates, Stage 4 reviewer bypassing the routing gate, and an ambiguously defined review-only scribe exception.
**Rule**: **[Rule]** In a multi-stage agent pipeline, handle every possible sub-agent outcome explicitly (including the no-issues branch), use a dedicated temp-file handoff for inter-stage state rather than filesystem mtime, and add a CONSTRAINT field to sub-agent calls to prevent them from issuing routing instructions that bypass the orchestrator.
**Source**: uncommitted — skill-implementer

---

## 2026-05-31 — orchestrator.md, reviewer.md, planner.md, skill-implementer.md, scribe.md

**Classification**: missing-rule
**What happened**: A standardised error-handling protocol was added to all five agent files, requiring each to stop and report (rather than silently continue) when a file cannot be read, an A2A call fails, or a sub-step produces unexpected output.
**Rule**: **[Rule]** Every agent definition must include an explicit Error handling section covering file-not-found, A2A call failure, and unexpected output, with "stop and report to the user" as the default response — never silent continuation.
**Source**: uncommitted — skill-implementer

---
