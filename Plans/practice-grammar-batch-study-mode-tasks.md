# Practice Grammar — Batch Session Mode & Study Mode — Tasks

- [ ] Add scope-based triggers to the `## Trigger` section of `.cowork/skills/practice-grammar.md`
- [ ] Add `## Scope resolution` section: filter logic (due_today / overdue / most_overdue N), sorting by overdue_days descending, tie-breaking by ease ascending, empty-result message
- [ ] Add `## Lazy lesson-file loading` section: read lesson files up to `# Summary`, cache by lesson code, match grammar_header to heading, skip-with-warning on unreadable file
- [ ] Add `## Pre-session summary and batch split` section: user-facing summary of queued topics, prompt for number of batches, batch size computation (ceil), session scratch object definition
- [ ] Add `## Batch loop` section: exercise generation per batch (reuse existing logic), batch-scoped progress indicator (`Exercise N / T` within batch), batch header format
- [ ] Add `## Score buffering` rule: scores accumulated in session scratch object, NOT written to grammar-state.json until Step 7
- [ ] Add `## Batch summary and mode choice` section: compact batch summary format, [next] / [study] / [end] prompt
- [ ] Add `## Study Mode` section covering:
  - Topic selection prompt (numbered list from batch + free-form name entry)
  - Explanation format (Structure / Meaning / Examples / Common mistakes)
  - WebSearch / WebFetch as optional fallback (graceful degradation if unavailable)
  - Per-topic [practice] / [next] / [question] choice
  - Practice sub-loop: one-at-a-time exercises, no self-evaluation score collection, [next exercise] / [ask question] / [exit study] controls
  - Follow-up question handling
  - Exit Study Mode → return to batch loop
- [ ] Add `## Post-session` section: combined multi-batch summary, single-pass SM-2 write to grammar-state.json, calendar file generation (same Python script, key set = full score_buffer)
- [ ] Verify existing single-lesson trigger flow is untouched (no edits to existing workflow steps 1–10)
- [ ] Update skill frontmatter `description` field to mention scope-based triggers and Study Mode
