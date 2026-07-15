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

## 2026-06-01 — orchestrator.md

**Classification**: bug-fix
**What happened**: The orchestrator's write-prohibition rules omitted Bash, leaving a loophole that allowed it to write vault files directly via Bash tool calls instead of delegating to skill-implementer. An explicit Bash write prohibition was added to the hard rules block.
**Rule**: **[Rule]** When prohibiting direct file writes in an orchestrator, name every write-capable tool explicitly — Bash, Write, Edit, and Read-with-write patterns — because a prohibition that omits one tool name leaves an exploitable loophole.
**Source**: uncommitted — skill-implementer

---
## 2026-06-08 — skill-implementer.md / scribe.md

**Classification**: design-oversight
**What happened**: skill-implementer cannot spawn scribe via A2A because the Agent tool is not available inside a spawned subagent; the parent orchestrator must call scribe directly after skill-implementer completes.
**Rule**: **[Rule]** Never design an A2A chain where a spawned subagent is expected to re-spawn another subagent — the Agent tool is unavailable inside subagents; any agent that needs to trigger a peer must be called from the top-level orchestrator, not from inside a delegate.
**Source**: uncommitted — skill-implementer

---

## 2026-06-12 — vault-system-diagram.puml

**Classification**: new-feature
**What happened**: The vault system diagram was regenerated after accumulating drift from multiple unrecorded additions: two new top-level skills (reading-jlpt, templates-update), a new references package, corrected directory names (Kaligrafia/ → Caligraphy/), missing .ics output node for practice-grammar, and tightened agent notes across all five agents.
**Rule**: **[Rule]** A documentation agent must be triggered after every skill or agent change, not only after major milestones — a diagram that accumulates multiple stale entries becomes misleading enough to cause misrouting in A2A design reviews.
**Source**: uncommitted — documentation

---

## 2026-06-14 — docs/vault-system-diagram.puml

**Classification**: new-feature
**What happened**: Diagram regenerated after kanji-headers rewrite and kanji-file addition; kanji-file was added as a new component, kanji-headers call-chain annotation corrected to show delegation to kanji-file per kanji, update-kanji-list marked DEPRECATED, and minor clarifications applied to update-grammar, commit, scribe, and extract-grammar notes.
**Rule**: **[Rule]** When a documentation agent regenerates a diagram, it must explicitly verify and correct all inter-skill chain annotations (not only component existence) — a diagram that lists a new skill but retains the old, incorrect call-chain annotation is more misleading than one with a missing node.
**Source**: uncommitted — documentation

---

## 2026-06-15 — docs/vault-system-diagram.puml

**Classification**: new-feature
**What happened**: Diagram fully regenerated to cover all 7 agents and 18 skills including lesson-to-web subskills, deprecated entries, A2A wiring, skill chains, and storage access rules — replacing a partial version that had accumulated drift.
**Rule**: **[Rule]** When regenerating a documentation diagram from scratch, always enumerate every component category explicitly (agents, skills, subskills, deprecated entries, storage nodes, A2A edges) — a diagram regenerated by diff-patching misses categories that were never touched but have drifted from reality.
**Source**: uncommitted — documentation

---

## 2026-06-15 — docs/vault-system-diagram.puml (second pass)

**Classification**: new-feature
**What happened**: Diagram refined after a second full re-extraction from all 7 agent files and 19 skill files; a count discrepancy (18 vs 19 skills) revealed silently omitted components from the first pass, along with missing storage nodes and stale agent-note text.
**Rule**: **[Rule]** After regenerating a documentation diagram, always cross-check the component count against the actual skill/agent directory listing — a count discrepancy signals that at least one component was silently omitted.
**Source**: uncommitted — documentation

---

## 2026-06-16 — docs/vault-system-diagram.puml

**Classification**: improvement
**What happened**: Orchestrator was found in the active Agents package despite being deprecated; the diagram was regenerated with orchestrator correctly placed in the Deprecated package, all A2A edge annotations refreshed against actual agent file contents, and 15 skills confirmed with accurate chain and storage annotations.
**Rule**: **[Rule]** When a diagram has both an active and a deprecated package, always verify the package placement of every component against the current agent/skill status — a deprecated agent listed in the active package is more misleading than a missing node, because it actively directs design reviews toward a component that should no longer be used.
**Source**: uncommitted — documentation

---

## 2026-06-16 — docs/vault-system-diagram.puml (storage node granularity)

**Classification**: improvement
**What happened**: Diagram refined to split Caligraphy/ into Kanji/ and Primitives/ database nodes, add JPLessons/Reading/ as a separate node, rename VaultRoot to ICSRoot, add lesson-to-web/_conventions and _patterns as reference components, remove .cowork/tmp/ (deprecated-agent artefact), add Planner→Reviewer A2A edge, and standardise note formatting across all agents and skills.
**Rule**: **[Rule]** When modelling storage access in a documentation diagram, split every directory that has meaningfully different read/write access patterns into separate database nodes — a single coarse node for a directory with distinct sub-directories hides which skill or agent touches which subtree, making access-rule audits unreliable.
**Source**: uncommitted — documentation

---

## 2026-07-01 — docs/vault-system-diagram.puml

**Classification**: bug-fix
**What happened**: Diagram was missing write edges from SkillImplementer to grammar-index/, Vocabulary/, and .cowork/instructions.md; skill-implementer.md explicitly permits confirmation-gated writes to these paths, but the diagram only showed read edges, understating the component's actual write surface.
**Rule**: **[Rule]** When a documentation diagram distinguishes read vs write access edges, always cross-check each edge against the source agent/skill file's explicit permission language (e.g. "confirm-gated write") — an access edge drawn as read-only when the source file grants confirm-gated write is a silent understatement of actual write surface, which undermines access-rule audits.
**Source**: uncommitted — documentation

---

## 2026-07-07 — docs/vault-system-diagram.puml

**Classification**: design-oversight
**What happened**: A full regeneration of the diagram shrank it from 607 to 305 lines, collapsing storage-node splits (Caligraphy/Kanji, Caligraphy/Primitives, JPLessons/Reading, dedicated ICS root) and per-skill trigger/chain/read-write detail that had been deliberately added in the 2026-06-15/06-16 passes, even while adding two genuinely new audit findings (an orphaned skill not in the instructions.md registry, and a hardcoded-path inconsistency in fill-templates).
**Rule**: **[Rule]** When regenerating a diagram or artifact "from scratch," diff the new version against the last committed version (and its own lessons-learned history) before finalizing — a regeneration should be a superset of prior improvements plus new findings, never a reset to a simpler baseline.
**Source**: uncommitted — documentation

---
