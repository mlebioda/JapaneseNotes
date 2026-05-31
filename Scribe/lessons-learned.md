# Lessons Learned — Agent & Skill Design

This file accumulates best practices and rules derived from analysing changes to skills and agents in this project. It is maintained automatically by the `scribe capture` skill.

---

<!-- New entries are appended below by scribe capture -->

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
