# Practice Grammar — Batch Mode — Tasks

- [ ] Read `.cowork/skills/practice-grammar.md` in full before making any edits
- [ ] Add step 6b — batch-split logic after scope topic assembly: if count > 5, divide into batches of 5 and notify the user; if count <= 5, proceed as before; direct-lesson sessions unaffected
- [ ] Replace single-pass drill-and-rate with a batch loop: display "Batch N / M" header, run drill-and-rate for each batch, prompt "Ready for next batch? (yes / stop)" between batches (skip prompt if only one batch)
- [ ] Move session summary printout to fire once after the batch loop ends, not per-batch
- [ ] Confirm SM-2 persistence write fires once after the full batch loop (no per-batch partial writes)
- [ ] Confirm `.ics` calendar export fires once after the full batch loop, covering all completed batches
- [ ] Create `.claude/commands/practice-grammar.md` slash command stub (if not already present)
