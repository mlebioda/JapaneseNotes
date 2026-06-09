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
## 2026-06-08 — templates-update.md

**Classification**: improvement
**What happened**: Repair numbering gap found (Repair 5 was absent while Repair 6 and 7 existed) after incremental authoring; corrected by renumbering and inserting the missing repair.
**Rule**: **[Rule]** When a skill is authored incrementally, audit all repair/step numbers explicitly before publishing — numbering gaps are invisible to readers and cause confusion when later steps are added.
**Source**: uncommitted — skill-implementer

---
## 2026-06-08 — kanji-links.py (new file) + references/kanji-links.md

**Classification**: new-feature / improvement
**What happened**: Mechanical Unicode scanning for kanji link generation was extracted from inline skill instructions into a dedicated stdlib-only Python script; the reference file was updated with the calling convention and furigana pre-processing responsibility.
**Rule**: **[Rule]** Delegate mechanical text-processing tasks (Unicode scanning, regex matching, deduplication) to a small stdlib script rather than performing them inline in a skill — the script is deterministic, testable, and frees LLM context for reasoning-heavy work.
**Source**: uncommitted — skill-implementer

---
## 2026-06-08 — references/kanji-links.md

**Classification**: improvement
**What happened**: "Script usage" section added to document how to call kanji-links.py, including the furigana-stripping responsibility that belongs to the caller.
**Rule**: **[Rule]** When a skill delegates a mechanical task to an external script, the reference file for that domain must document the script's calling convention and any pre-processing the caller is responsible for — never leave the interface implied.
**Source**: uncommitted — skill-implementer

---
## 2026-06-08 — instructions.md

**Classification**: improvement
**What happened**: templates-update skill entry added to Available skills list with all four trigger phrases after the skill was renamed from update-templates.md.
**Rule**: **[Rule]** Every time a skill is renamed or created, update instructions.md's Available skills list in the same change set — stale or missing entries make the skill invisible to both users and the orchestrator.
**Source**: uncommitted — skill-implementer

---
## 2026-06-08 — templates-update.md (reviewer finding)

**Classification**: missing-rule
**What happened**: Reviewer found no pre-execution git-commit guardrail in templates-update.md despite the skill being destructive — it can silently overwrite all conjugation and adjective form values across an entire lesson file.
**Rule**: **[Rule]** Any skill that overwrites existing values across a whole file must open with an explicit git-commit guardrail step: "Ensure all pending changes are committed before proceeding; if not, commit a WIP snapshot first."
**Source**: uncommitted — reviewer

---
## 2026-06-08 — templates-update.md (reviewer finding)

**Classification**: missing-rule
**What happened**: Step 4 of templates-update.md instructs "Apply changes using targeted Edit calls" with no provision for large files; when 130+ cards all need kanji-link repairs, the LLM silently deviates to a full-file rewrite because the permitted mechanism does not scale.
**Rule**: **[Rule]** When a skill specifies a repair mechanism, also state the threshold at which bulk alternatives are permitted (e.g. "if more than N blocks require the same repair, a single full-section rewrite is allowed") — an unqualified "use targeted Edits" instruction fails silently at scale.
**Source**: uncommitted — reviewer

---
## 2026-06-08 — templates-update.md (reviewer finding, design-oversight)

**Classification**: design-oversight
**What happened**: templates-update.md instructs the skill to read the full lesson file, but all its repair work targets only the post-Summary section — the pre-Summary content is never touched and should never be loaded.
**Rule**: **[Rule]** When a skill operates only on a known sub-section of a file (e.g. post-Summary), its read instruction must scope to that section explicitly — reading the full file wastes context budget and risks inadvertently exposing content the skill has no business touching.
**Source**: uncommitted — reviewer

---
## 2026-06-08 — templates-update.md (reviewer finding, design-oversight)

**Classification**: design-oversight
**What happened**: The block-parsing step in templates-update.md does not handle the legacy Rzeczowniki: label, which appears in some older lesson files as a section header rather than a card-type marker — this ambiguity causes the parser to misclassify blocks.
**Rule**: **[Rule]** When a skill parses structured content that has a known legacy format variant, explicitly document how to detect and handle each variant in the parsing step — silent misclassification is worse than a visible parsing error.
**Source**: uncommitted — reviewer

---
