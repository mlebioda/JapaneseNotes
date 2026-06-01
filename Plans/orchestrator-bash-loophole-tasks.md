# Tasks: orchestrator-bash-loophole

**Target file:** `.claude/agents/orchestrator.md`
**Plan:** `Plans/orchestrator-bash-loophole-plan.md`

---

## Checklist

- [x] **Task 1 — Replace the `Edit`/`Write` note in hard rules with the expanded three-bullet Bash write prohibition**
  - Location: lines 231–232 (end of hard rules block)
  - Remove: the two existing bullets about `Edit`/`Write` omission and the `Temp file (active use)` bullet
  - Add: the three new bullets from Change 1 in the plan (Edit/Write omission note + Bash write prohibition + temp file exception)
  - Confirm: the hard rules block now explicitly names `Bash` as write-prohibited and contains the sole canonical statement of the temp-file exception

- [x] **Task 2 — Fix "absolute path" to "relative path" in Stage 2 revision template**
  - Location: line 114 inside the `REVIEWER_BRIEF: true` code block under "Revise X"
  - Change: `TARGET: <same absolute path from Stage 1>` → `TARGET: <same relative path from Stage 1 — e.g. .cowork/skills/fill-templates.md>`
  - Confirm: all three `TARGET` references in Stage 1 and Stage 2 now consistently say "relative path"

- [x] **Task 3 — Remove "This is the only direct write the orchestrator performs" from Stage 3 intro**
  - Location: line 127, the Stage 3 intro paragraph
  - Change: remove the phrase "This is the only direct write the orchestrator performs:" — this claim now lives exclusively in the hard rules block (Task 1)
  - Confirm: sentence still reads naturally and the Bash write block below it is unchanged

- [x] **Task 4 — Fix handoff file overwrite timing note in Stage 3**
  - Location: line 142 (the `Important:` note after the Bash read-back block)
  - Change: "at the start of each Stage 2 call" → "each time Stage 3 begins"
  - Confirm: the overwrite note no longer says "Stage 2"

- [x] **Task 5 — Fix pipeline table row for "new" tasks**
  - Location: task classification table, the `new` row (line 37)
  - Change: `planner → implementer → scribe` → `reviewer (related file, quick) → planner → implementer → scribe`
  - Confirm: table now matches the prose at line 41

- [x] **Task 6 — Add scribe parenthetical to Stage 4 "no issues" path**
  - Location: Stage 4 section, line 182
  - Change: append `(Reviewer called scribe internally — no additional scribe call needed.)` after "close the pipeline."
  - Confirm: both "no issues" and "issues found" branches of Stage 4 now mention the scribe disposition
