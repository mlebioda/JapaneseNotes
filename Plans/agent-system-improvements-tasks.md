# Agent System Improvements — Tasks

## Item 2 — Split lessons-learned.md into 3 purpose-specific files

- [ ] Task 1: Update scribe.md Step 4 routing — replace single lessons-learned.md append with conditional routing to captures.md / issues-found.md / posts-log.md based on calling agent and classification
- [ ] Task 2: Update scribe.md Mode: post Step 1 — replace lessons-learned.md reference with all three new files (captures.md, issues-found.md, posts-log.md)
- [ ] Task 3: Update scribe.md Mode: retrospect Step 5 — replace lessons-learned.md append target with issues-found.md
- [ ] Task 4: Create Scribe/captures.md with header (agent activity log)
- [ ] Task 5: Create Scribe/issues-found.md with header (reviewer findings)
- [ ] Task 6: Create Scribe/posts-log.md with header (generated posts index)
- [x] Task 7: Add superseded notice to top of Scribe/lessons-learned.md (archive note, no content removal)

## Item 1 — Add commit message suggestion step to skill-implementer

- [x] Task 8: Add Step 5 to skill-implementer.md — after all scribe calls, propose a git commit message to the user (display-only, no git command execution)

## Item 4 — Add error handling protocol to all 5 agent files

- [x] Task 9: Add error handling section to orchestrator.md — stop pipeline, report failure, ask user on sub-agent error
- [x] Task 10: Add error handling section to reviewer.md — report file read failures and A2A failures, do not silently continue
- [x] Task 11: Add error handling section to planner.md — report file read failures and write failures; scribe failure non-blocking
- [x] Task 12: Add error handling section to skill-implementer.md — report plan/task read failures and write failures; scribe failure non-blocking
- [x] Task 13: Add error handling section to scribe.md — report git command failures and file write failures, never silently swallow errors
