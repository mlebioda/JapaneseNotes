# Agent System Improvements

## Goal

Three targeted improvements to the ObsidianJP agent system, approved by the user. Item 3 (rationalise scribe calls — removing planner's scribe call and adding scribe ownership rule to orchestrator) has been explicitly excluded due to audit granularity risk. The approved work covers: splitting the monolithic lessons-learned.md into purpose-specific log files; adding a commit message suggestion step to skill-implementer; and adding a consistent error handling protocol to all five agent files.

## Approach

Changes are addressed in dependency order. Item 2 (scribe file split) goes first because it changes the routing table in scribe.md — the other items do not depend on it but it is the most structurally foundational. Item 1 (commit step in skill-implementer) is self-contained and goes second. Item 4 (error handling) touches all five agent files and goes last, since the error handling pattern can reference the already-updated scribe routing without ambiguity.

## Steps

### Item 2 — Split lessons-learned.md into 3 purpose-specific files

1. **Update scribe.md — Step 4 routing** — `.claude/agents/scribe.md`. Replace the single `Scribe/lessons-learned.md` append target in Mode: capture (Step 4) with conditional routing:
   - Captures from `skill-implementer` or `planner` → append to `Scribe/captures.md` (agent activity log)
   - Captures from `reviewer` (or with classification `bug-fix` / `missing-rule` / `design-oversight`) → append to `Scribe/issues-found.md` (reviewer findings)
   - Post generation events → append to `Scribe/posts-log.md` (generated posts index)
   Update Mode: post (Step 3) to also write an index entry to `Scribe/posts-log.md`.

2. **Update scribe.md — Mode: post source material** — `.claude/agents/scribe.md`. In Mode: post Step 1, replace the reference to `Scribe/lessons-learned.md` with references to all three new files (`captures.md`, `issues-found.md`, `posts-log.md`).

3. **Update scribe.md — Mode: retrospect** — `.claude/agents/scribe.md`. In Mode: retrospect Step 5, replace the append target `Scribe/lessons-learned.md` with `Scribe/issues-found.md` (retrospect findings are review-type content).

4. **Create seed files** — `Scribe/captures.md`, `Scribe/issues-found.md`, `Scribe/posts-log.md`. Create each with a minimal header comment so they exist as named files (empty files with a `# <title>` heading only). Do not migrate existing lessons-learned.md content — leave that file in place as an archive. Add a note at the top of `lessons-learned.md` marking it as superseded.

### Item 1 — Add commit message suggestion step to skill-implementer

5. **Add Step 5 — Suggest commit message** — `.claude/agents/skill-implementer.md`. After Step 4 (Notify Scribe), add a new Step 5: after all session tasks are complete and scribe has been called, skill-implementer proposes a git commit message. Format:
   - One-line summary in imperative mood, max 72 characters, describing the aggregate change (e.g. "add error handling protocol to all agent files")
   - Optionally a blank line followed by a brief body if multiple files were changed
   - Present this to the user as a suggestion with the label: "Suggested commit message:" — do not run git commit; just print the message for the user to copy.
   - Placement: after all scribe calls, before the final session report.

### Item 4 — Add error handling protocol to all 5 agent files

6. **Add error handling section to orchestrator.md** — `.claude/agents/orchestrator.md`. Add a new "Error handling" subsection under the Pipeline section (or as a standalone section before Hard rules). Rule: if any called sub-agent returns an error, an unexpected result structure, or fails silently (no output), the orchestrator must: (a) stop the pipeline immediately, (b) report the failure to the user with the agent name and the output received, (c) ask the user how to proceed (retry / skip / abort). Never silently continue past a failed sub-agent call.

7. **Add error handling section to reviewer.md** — `.claude/agents/reviewer.md`. Add equivalent rule: if a file read fails (file not found, permission error, empty content), report the specific path and error to the user and stop. Do not attempt to review a file that could not be read. If a called sub-agent (scribe, planner) fails, report and stop — do not silently skip the A2A call.

8. **Add error handling section to planner.md** — `.claude/agents/planner.md`. Add equivalent rule: if the target file read fails, report and ask the user to confirm the correct path. If the Plans/ directory cannot be written to, report the error immediately. If scribe A2A call fails, report it but do not block plan completion — the plan file is the primary output.

9. **Add error handling section to skill-implementer.md** — `.claude/agents/skill-implementer.md`. Add equivalent rule: if a plan file or task file cannot be read, report and stop. If a file write fails mid-task, report the failure, do not mark the task complete, and ask the user how to proceed. If the scribe A2A call fails, report it but do not block the session — note the missed capture in the session report.

10. **Add error handling section to scribe.md** — `.claude/agents/scribe.md`. Add equivalent rule: if a git command fails (e.g. not a git repo, no commits), report the error and proceed with whatever data is available. If a target file for append cannot be created or written, report the specific file path and error and stop that step. Never silently swallow errors.

## Risks

- The scribe file split (Item 2) changes where new entries are written. Existing `Scribe/lessons-learned.md` content is not migrated — it remains as an archive. Any external references to `lessons-learned.md` (e.g. in Mode: post source reading) must be updated to read from the three new files instead. Steps 2 and 3 above cover these references.
- The commit message suggestion step (Item 1) is display-only and does not run git commands — no data risk.
- The error handling additions (Item 4) are additive-only: new sections appended or inserted. No existing behaviour is removed. Low regression risk.
- No Anki plugin data (`<!--ID:-->`, `TARGET DECK`, `# Summary`) is affected — all changes are to agent definition files only.
