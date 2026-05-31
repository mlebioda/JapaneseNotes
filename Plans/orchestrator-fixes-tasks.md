# Orchestrator Agent Fixes — Tasks

- [x] Confirm `Edit` and `Write` are absent from the frontmatter `tools:` list in `.claude/agents/orchestrator.md` — no change needed if already absent
- [x] Fix Stage 1 call template: replace `"related: <topic>"` notation with instructions to resolve a real file path via Bash before calling reviewer (issue 1)
- [x] Fix Stage 2 planner call template: ensure `TARGET` is always a real path, not a synthetic string (issue 2)
- [x] Fix Stage 2 revision branch: drop `REVISE: true`; replace with a second `REVIEWER_BRIEF: true` call that appends `REVISION_NOTES: <user feedback>` (issue 3)
- [x] Add post-Stage-2 slug resolution step: document Bash one-liner `ls -t Plans/*-plan.md | head -1` and extraction logic; use resolved slug in Stage 3 call template (issue 4)
- [x] Add `post` pipeline stage: call scribe in `MODE: post` with user's topic; present output to user (issue 5)
- [x] Update DONE block `Scribe:` line to use conditional language per task type instead of hardcoded "captured by skill-implementer" (issue 6)
- [x] Add Hard rules entries: no Edit/Write tools; no implementer without a plan; no direct scribe except post/review-only; no stage-skipping; temp file exception at `.cowork/tmp/orchestrator-handoff.md` (issue 7 + USER_CONSTRAINT)
- [x] Update DONE block to include Stage 4 reviewer capture as a conditional entry in Stages completed (issue 8)
- [x] Add `skill-updater` row to agent roster table marked DEPRECATED (issue 9)
