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
## 2026-06-11 — practice-grammar.md (calendar sync bug-fix)

**Classification**: bug-fix
**What happened**: ICS all-day events in the Calendar sync section had DTEND equal to DTSTART, producing zero-duration events silently discarded by Apple Calendar; DTEND was corrected to DTSTART + 1 day per RFC 5545 §3.6.1.
**Rule**: **[Rule]** For ICS all-day events, DTEND must be the exclusive next day (DTSTART + 1 day) — DTEND equal to DTSTART is a zero-duration event that Apple Calendar silently discards without error.
**Source**: uncommitted — manual

---
## 2026-06-11 — practice-grammar.md (RFC 5545 line folding)

**Classification**: missing-rule
**What happened**: The generated ICS content had no line folding, exceeding the 75-octet per-line limit mandated by RFC 5545 §3.1; lenient clients (Apple Calendar) hide the bug until a strict client fails to import.
**Rule**: **[Rule]** Always fold ICS content lines at 75 octets (bytes, not characters) using a `fold()` helper — lenient clients mask this omission, so it will surface only when a stricter client encounters the file.
**Source**: uncommitted — manual

---
## 2026-06-11 — practice-grammar.md (furigana scope)

**Classification**: missing-rule
**What happened**: The furigana rule said "no exceptions" but omitted the named failure mode (compound words) and a concrete example; a real session produced 試験（しけん）with furigana while 来年 and 日本語 in the same sentence had none.
**Rule**: **[Rule]** Abstract "no exceptions" mandates invite selective compliance — name the specific failure mode and embed a concrete ✗/✓ example directly in the rule to make partial compliance visibly wrong.
**Source**: uncommitted — manual

---
## 2026-06-11 — practice-grammar.md + instructions.md (vault-root policy exception)

**Classification**: missing-rule
**What happened**: The practice-grammar skill writes `.ics` files to the vault root, which conflicts with the general "never create files in vault root" rule in instructions.md; the rule was updated with an approved-exception bullet for this skill.
**Rule**: **[Rule]** When a skill intentionally writes to the vault root as a user-convenience design decision, add an explicit approved-exception bullet to instructions.md in the same change set — without it, other agents will flag the output as a policy violation.
**Source**: uncommitted — manual

---
## 2026-06-12 — instructions.md

**Classification**: new-feature
**What happened**: `reading-jlpt` skill registered in instructions.md Available skills table with description, output path, and trigger phrases, as part of creating the skill.
**Rule**: **[Rule]** When a new skill file is created, register it in instructions.md's Available skills table in the same change set, including the output path and all trigger phrases — a skill that is not registered is invisible to the orchestrator and cannot be invoked by name.
**Source**: uncommitted — skill-implementer

---

## 2026-06-12 — reading-jlpt.md (fixes plan)

**Classification**: bug-fix
**What happened**: Five runtime gaps in the reading-jlpt skill were identified and planned as fixes: missing tools frontmatter, no mkdir guard for the output directory, undocumented fill-templates interface contract, date-only session filenames that collide within a day, and no fallback for the no-passage invocation case.
**Rule**: **[Rule]** Before marking a new skill as done, audit it against a standard gap checklist: tools frontmatter present, output directories guarded with mkdir -p, interface contracts with chained skills documented, filenames include a time component to avoid collisions, and all trigger variants (including empty invocation) have explicit fallback instructions.
**Source**: uncommitted — planner

---

## 2026-06-12 — reading-jlpt.md (classification threshold)

**Classification**: bug-fix
**What happened**: The same five-fix revision was initially captured as "improvement" but re-submitted by the caller as "bug-fix" — missing tools frontmatter, absent directory guard, undocumented chain interface, filename collision risk, and no no-passage fallback are runtime failures, not refinements.
**Rule**: **[Rule]** When five or more runtime gaps are patched in a single skill revision, classify it as bug-fix — "improvement" understates the severity and makes the change harder to triage in a git-sweep.
**Source**: uncommitted — skill-implementer

---

## 2026-06-12 — reading-jlpt.md (five targeted fixes implemented)

**Classification**: improvement
**What happened**: All five planned fixes applied: tools frontmatter added, mkdir -p guard inserted before session file write, contradicting "Does not create JPLessons/Reading/" disclaimer removed, fill_extract.py interface contract documented in Step 7, and all date-only filename references replaced with YYYYMMDDTHHMMSS timestamp format.
**Rule**: **[Rule]** When implementing a skill fixes plan, update all three surfaces atomically — the procedural steps, any "does not do X" disclaimer list, and all example filenames in prose — a fix applied to only one surface leaves the skill internally inconsistent.
**Source**: uncommitted — skill-implementer

---

## 2026-06-12 — Plans/reading-jlpt-plan.md, Plans/reading-jlpt-tasks.md

**Classification**: bug-fix
**What happened**: Four implementation issues corrected in the reading-jlpt plan: session filename upgraded to YYYYMMDDTHHMMSS, mkdir -p replaced with a fail-loud existence check, Read removed from skill tools frontmatter, and Step 7 fill-templates invocation made explicit.
**Rule**: **[Rule]** When a skill must not create a directory (e.g. because absence signals an iCloud sync failure), replace any mkdir -p guard with a fail-loud existence check that stops and surfaces the error — silent directory creation masks infrastructure problems the user needs to know about.
**Source**: uncommitted — planner

---

## 2026-06-14 — fix-kanji-headers-plan.md

**Classification**: new-feature
**What happened**: A plan was created to replace the kanji-headers skill's destructive from-scratch block-write step with a targeted in-place correction pass that only fixes `##` header formatting and wikilinks, leaving all block content and everything at or below `# Summary` untouched.
**Rule**: **[Rule]** When a skill's job is to format or annotate existing content, implement it as an in-place correction pass — never replace whole sections from a boundary line onward, because that silently destroys user content built up since the last git snapshot.
**Source**: uncommitted — planner

---

## 2026-06-14 — fix-kanji-headers-plan.md, fix-kanji-headers-tasks.md

**Classification**: improvement
**What happened**: Plan revised to split kanji-headers into two skills (kanji-headers for lesson-file concerns, kanji-file for per-kanji-reference-file concerns), with kanji-file independently invocable and callable by kanji-headers; update-kanji-list receives a deprecation notice and is retained rather than deleted.
**Rule**: **[Rule]** When deprecating a skill whose logic is being absorbed by two new skills, insert a deprecation notice at the top of the old file and retain it — never delete it in the same change set that introduces the replacements, so a rollback path exists until the new skills are confirmed stable.
**Source**: uncommitted — planner

---

## 2026-06-14 — kanji-headers.md

**Classification**: improvement
**What happened**: kanji-headers rewritten with a 5-step workflow that delegates all per-kanji-file work to the new kanji-file skill; the primary skill now explicitly owns only lesson-file operations (header format correction, wikilink placement, KanjiList.md update) and calls kanji-file for everything inside individual kanji reference files.
**Rule**: **[Rule]** When a skill is split into a primary skill and a delegated skill, the primary skill's workflow must explicitly state which steps it performs itself and which it delegates — an ambiguous boundary causes implementers to duplicate logic or skip responsibilities.
**Source**: uncommitted — skill-implementer

---

## 2026-06-14 — kanji-file.md

**Classification**: new-feature
**What happened**: New standalone skill created to handle all per-kanji-reference-file work (web fetch, mnemonic, parts, link verification, bare-link migration, consistency check), invocable both directly by the user ("kanji-file [character]") and programmatically by kanji-headers; neither the user-facing triggers nor the A2A interface were documented in the skill file initially, which was corrected.
**Rule**: **[Rule]** When a new skill is designed to be callable both directly by the user and programmatically by another skill, its invocation triggers and its A2A interface must both be documented in the skill file itself — without this, callers cannot determine the correct invocation form and user discovery fails.
**Source**: uncommitted — skill-implementer

---

## 2026-06-14 — .claude/commands/kanji-file.md

**Classification**: new-feature
**What happened**: Slash command stub created for the kanji-file skill, enabling direct invocation from the Claude command palette with "kanji-file [character]"; without the stub the skill existed but was not discoverable or triggerable from the palette.
**Rule**: **[Rule]** When a skill is designed to be directly user-invocable (not just called by other skills), create a matching `.claude/commands/<skill-name>.md` stub in the same change set — a skill without its command stub cannot be discovered or triggered from the command palette.
**Source**: uncommitted — skill-implementer

---

## 2026-06-14 — .cowork/instructions.md

**Classification**: improvement
**What happened**: Available skills table updated with a new `kanji-file` entry and a `update-kanji-list` DEPRECATED notice; without these entries the new skill was invisible to users and the orchestrator, and the deprecated skill appeared to still be the correct choice.
**Rule**: **[Rule]** When a skill is deprecated (not deleted), add a DEPRECATED notice to its instructions.md entry in the same change set — a stale entry with no deprecation marker will continue to be invoked by users and agents that rely on the table for discovery.
**Source**: uncommitted — skill-implementer

---

## 2026-06-14 — kanji-file.md

**Classification**: improvement
**What happened**: The always-fetch + positional-keyword component parser (Steps 1–3) in kanji-file was replaced with a conditional mnemonic-driven flow (Steps A–D): skip the web fetch when ### Mnemonic already has content, and scan the settled mnemonic text for CJK codepoints to populate ### Parts instead of parsing Left:/Right:/Top: keywords.
**Rule**: **[Rule]** When a skill step produces data that is also expressed as Unicode characters in a text field already written to the file, scan that text field for the relevant codepoints instead of parsing positional keywords — scanning codepoints is robust to phrasing variation; keyword parsing is not.
**Source**: uncommitted — skill-implementer

---

## 2026-06-15 — practice-grammar.md

**Classification**: improvement
**What happened**: Replaced four vague exercise types with six JLPT-aligned types (Contextual production, Discrimination fill-in-blank, Description→production, Sentence ordering, Passage grammar, Bolded form→explain), and added a deterministic type-selection algorithm, weak-point bias rule, hidden-target rule, and grading rules for the new types.
**Rule**: **[Rule]** When designing a drill skill, define exercise types as a closed, named set aligned with the target exam format, and specify a deterministic selection algorithm — open-ended exercise variety produces inconsistent sessions and makes grading rules impossible to specify precisely.
**Source**: uncommitted — skill-implementer

---

## 2026-06-15 — practice-grammar.md (scope-based batch extension)

**Classification**: new-feature
**What happened**: Practice-grammar extended with scope-based triggers, lazy lesson-file loading, batch split negotiation, a session-wide score buffer, and an optional Study Mode interlude — transforming the skill from a single-lesson driller into a full cross-lesson spaced-repetition engine.
**Rule**: **[Rule]** When a drill skill grows to support cross-lesson scope queries, buffer all self-evaluation scores in a session scratch object and write the state file once at the very end — mid-session writes create partial state that is inconsistent if the session is interrupted.
**Source**: uncommitted — skill-implementer

---

## 2026-06-15 — Plans/sequential-kanji-fetch-plan.md

**Classification**: new-feature
**What happened**: kanji-file and kanji-headers had no explicit instruction to serialize web fetches to kanji-trainer.org; a plan was created to add a rate-limit rule at the fetch step of each skill, preventing HTTP 429 errors when multiple kanji are processed in a single run.
**Rule**: **[Rule]** When a skill fetches from an external site that enforces rate limits, add an explicit sequential-processing rule at the exact fetch step — never leave the serialization requirement implicit, as concurrent requests will be issued by default when multiple items are processed in a single run.
**Source**: uncommitted — planner

---

## 2026-06-15 — kanji-headers.md

**Classification**: missing-rule
**What happened**: kanji-headers had no rule requiring sequential calls to kanji-file; without it parallel calls triggered HTTP 429 rate-limit errors from kanji-trainer.org when a lesson header contained multiple kanji.
**Rule**: **[Rule]** When a skill calls a sub-skill that performs external web fetches, add an explicit sequential-call rule at the invocation step — "call one at a time, wait for completion before the next" — because parallel invocation is the default and will trigger rate-limit errors without this guard.
**Source**: uncommitted — skill-implementer

---

## 2026-06-15 — Plans/kanji-file-bare-link-fix-plan.md

**Classification**: bug-fix
**What happened**: kanji-file's Step 5 sent all bare wikilinks to ## Occurences regardless of whether they were structural component links (should go to ### Parts) or lesson occurrence links; Step 4 kept broken bare links with only a warning instead of removing them.
**Rule**: **[Rule]** When a skill migrates stale content into sections, it must classify each item's destination before migrating — a single-destination migration step silently misplaces items that belong to different sections, and broken items must be removed rather than preserved with a warning.
**Source**: uncommitted — planner

---
