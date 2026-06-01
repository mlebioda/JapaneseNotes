# Skill Lessons Learned

<!-- Entries appended by scribe capture — domain: skill authoring, skill structure, skill conventions, skill-file format -->

---
## 2026-06-01 — structure-grammar.md

**Classification**: improvement
**What happened**: Removed the `## Never touch` section from structure-grammar.md; rules now live in the shared _conventions.md.
**Rule**: **[Rule]** When the same constraint list appears verbatim in multiple skill files, consolidate to a shared conventions file and reference it — prevents silent constraint divergence as the system evolves.
**Source**: uncommitted

---
## 2026-06-01 — update-grammar.md

**Classification**: improvement
**What happened**: Added _conventions.md load instruction to the update-grammar workflow — the pipeline entry point now explicitly declares the shared-file dependency.
**Rule**: **[Rule]** A pipeline-entry skill that delegates to sub-skills must still declare shared-file dependencies explicitly — relying on sub-skills to load them silently makes the entry point's contract incomplete.
**Source**: uncommitted

---
