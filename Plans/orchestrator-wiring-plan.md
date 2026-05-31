# Orchestrator A2A Wiring — Second-pass Fixes

## Goal

The orchestrator's first-pass fixes (orchestrator-fixes-plan.md) left seven gaps in A2A wiring,
error handling, and interface contracts. These gaps include: no defined path when the reviewer
returns a clean result; a stale-slug risk introduced by the ls -t resolution approach; a field-name
mismatch in the scribe post-mode call (TOPIC vs TARGET); absolute-path inconsistency in
reviewer/scribe calls; the REVISION_NOTES field being undocumented in planner's A2A interface; a
Stage 4 reviewer that can autonomously invoke planner outside the orchestrator's confirmation gate;
and a duplicate scribe entry risk in the review-only path. Fixing these makes the orchestrator
reliable across all task types and consistent with the documented interfaces of every downstream
agent.

## Approach

All changes are confined to `.claude/agents/orchestrator.md` and `.claude/agents/planner.md`.
Each fix is surgical: replace or extend the affected block only. The temp-file mechanism already
present in the Hard rules (the `.cowork/tmp/orchestrator-handoff.md` exception) is promoted into
the active slug-resolution step to eliminate the stale-mtime risk. The clean-reviewer branch adds
an explicit "no issues found" exit path. The TOPIC/TARGET mismatch is a one-field rename. Relative
vs absolute path standardisation affects Stage 1, Stage 4, and Hard rules prose only. REVISION_NOTES
is documented as an accepted optional field in planner's A2A section.

## Steps

1. **Add clean-reviewer branch — `orchestrator.md` Stage 1 "After reviewer completes" block**

   When reviewer returns with no critical or moderate issues (an empty or issues-free result),
   the orchestrator currently has no defined path. Planner would receive a blank ISSUES list and
   may enter interactive discovery mode. Add an explicit branch after the summary presentation:

   - If reviewer reports no issues: present that finding to the user and ask:
     "No issues were found. Do you want to proceed to planning anyway (e.g. for a proactive
     improvement), or end the session?"
     - Yes, plan anyway → Stage 2 with `ISSUES:` left empty and `SUMMARY:` describing the intent
     - No → end session (reviewer already called scribe internally)

2. **Replace ls -t slug resolution with temp-file handoff — `orchestrator.md` Stage 3**

   The current `ls -t Plans/*-plan.md | head -1` approach returns a stale file if planner wrote
   nothing (or if iCloud mtime is behind). Replace the entire slug-resolution block with the
   temp-file approach already permitted by the Hard rules:

   - After planner confirms the plan is written, the orchestrator writes the slug to
     `.cowork/tmp/orchestrator-handoff.md` (one line: `SLUG: <slug>`).
   - Before calling skill-implementer, the orchestrator reads that file to recover the slug.
   - If the file is missing or empty, fall back to the `ls -t` heuristic and ask the user to
     confirm the slug before proceeding.
   - Remove the "Caveat" note about iCloud mtime from Stage 3 (it is resolved by this change).
   - Update the Hard rules temp-file exception note to say the file is actively used (not just
     permitted).

   File touched: `.claude/agents/orchestrator.md` (Stage 3 slug-resolution block).

3. **Fix TOPIC → TARGET field name in scribe post-mode call — `orchestrator.md` post pipeline**

   The scribe A2A interface (scribe.md retrospect mode and capture mode) defines `TARGET` for
   file-path-style fields. The orchestrator's post-mode call template uses `TOPIC: <user's topic>`
   but scribe's post mode reads `TARGET` (via the retrospect invocation pattern) or a free `TOPIC`
   field. Cross-check: scribe.md Step 2 says "If the caller specified a topic, use it" — but the
   field name it uses for A2A invocation in retrospect mode is `TARGET`. The safe fix is to rename
   the field in the orchestrator's post-mode template from `TOPIC` to `TARGET` to match the
   retrospect interface, and add a comment that this carries the user's topic string (not a file
   path) when invoked from the post pipeline.

   File touched: `.claude/agents/orchestrator.md` (post pipeline call template).

4. **Standardise on relative paths in reviewer and scribe calls — `orchestrator.md` Stages 1, 4**

   Reviewer's A2A interface documents `TARGET` as a relative path
   (`e.g. .cowork/skills/fill-templates.md`). Orchestrator currently passes absolute paths.
   Scribe log entries then contain absolute paths, making them non-portable.

   Change:
   - Stage 1 reviewer call template: replace `<absolute file path>` instruction with
     `<path relative to vault root, e.g. .cowork/skills/fill-templates.md>`.
   - Stage 2 planner call template: same — relative path in `TARGET`.
   - Stage 4 reviewer call template: same.
   - Add a note in Stage 1: "Derive the relative path by stripping the vault root prefix
     `/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/`."

   File touched: `.claude/agents/orchestrator.md` (Stage 1, Stage 2, Stage 4 call templates and
   surrounding prose).

5. **Document REVISION_NOTES in planner's A2A interface — `planner.md`**

   The orchestrator's Stage 2 revision branch appends `REVISION_NOTES: <user feedback>` to the
   planner call. This field is not listed in planner's "Expected input format" block, so planner
   treats it as unrecognised free text. Formalise it:

   - In planner.md's "A2A — Receiving briefs from Reviewer" section, add `REVISION_NOTES` as an
     optional field to the expected input format block, with a note:
     "Optional. Present only on revision runs. Contains the user's feedback from the plan review
     step. If present, incorporate this feedback into the revised plan rather than re-asking the
     user."

   File touched: `.claude/agents/planner.md` (A2A interface expected input format block).

6. **Add constraint to Stage 4 reviewer call — `orchestrator.md` Stage 4**

   The Stage 4 reviewer currently receives no instruction preventing it from autonomously asking
   the user to call planner. If it does, a new plan is created outside the current orchestrator
   session, bypassing the Stage 2 confirmation gate.

   Add a `CONSTRAINT:` field to the Stage 4 reviewer call template:
   ```
   CONSTRAINT: Report findings only. Do NOT ask the user to call planner or route to any other
   agent. If issues are found, present them and stop — the orchestrator will handle routing.
   ```

   Also update the "If issues found" prose in Stage 4 to make the confirmation gate explicit:
   after reviewer presents findings, the orchestrator (not the reviewer) asks the user whether to
   route back to planner.

   File touched: `.claude/agents/orchestrator.md` (Stage 4 reviewer call template and surrounding
   prose).

7. **Clarify scribe responsibility in review-only path — `orchestrator.md` Hard rules**

   The Hard rules state orchestrator may call scribe in the `review-only` end-of-session path.
   But reviewer.md Step 4 says reviewer always calls scribe after completing an analysis. Both
   paths run in a review-only session, so scribe is called twice.

   Fix: add an explicit rule in the Hard rules section:
   "In the review-only path, never call scribe directly — reviewer calls scribe internally at
   Step 4. The orchestrator's Hard rules exception for direct scribe calls covers only the `post`
   pipeline."

   Also update the Hard rules sentence that currently reads "Never call scribe directly except in
   the `post` pipeline or the `review-only` end-of-session path" to remove the `review-only`
   exception.

   File touched: `.claude/agents/orchestrator.md` (Hard rules section).

## Risks

- The temp-file write in Step 2 is the only direct write the orchestrator makes. The file
  `.cowork/tmp/orchestrator-handoff.md` already has a Hard rules exception — no new permission
  change needed. Risk: if planner is called but writes no plan (user cancels), the temp file may
  contain a stale slug from a previous session. Mitigation: the orchestrator must clear or
  overwrite the file at the start of each Stage 2 call, or validate the slug against the current
  Plans/ listing before passing it to implementer.
- Relative-path standardisation (Step 4) affects how reviewer and scribe receive paths. If any
  downstream agent resolves paths relative to cwd rather than vault root, the relative path will
  resolve incorrectly. Both reviewer.md and scribe.md include an explicit vault root constant —
  low risk.
- Adding REVISION_NOTES to planner's interface (Step 5) is additive only. No existing behaviour
  changes. The field is optional, so existing orchestrator-to-planner calls without it remain
  valid.
- The CONSTRAINT field added to the Stage 4 reviewer call (Step 6) is a prompt-level instruction,
  not an interface change in reviewer.md. The reviewer agent may not honour it if its own Step 5
  rule ("route to planner if user says yes") takes precedence. A follow-up could add a matching
  hard rule in reviewer.md for calls with CONSTRAINT set, but that is out of scope for this plan.
- No plugin export data (<!--ID:-->, TARGET DECK, # Summary) is touched — all changes are to
  agent definition files only.
