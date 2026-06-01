# Plan: orchestrator-bash-loophole

**Target:** `.claude/agents/orchestrator.md`
**Slug:** `orchestrator-bash-loophole`
**Reviewer brief:** REVIEWER_BRIEF: true

---

## Problem summary

The orchestrator has `Bash` in its `tools:` list and used it to write vault files directly during a live session, bypassing skill-implementer and causing scribe to miss most captures. The hard rules block prohibits `Edit` and `Write` by name but is silent on `Bash` — leaving a usable loophole. Several related consistency issues compound the risk: the temp-file write restriction lives only in prose, Stage 2 revision templates reference "absolute path" while Stage 1 uses relative paths, and the handoff file write timing is stated in three places with contradictory wording.

---

## Issues addressed

| # | Severity | Issue |
|---|---|---|
| 1 | critical | Bash write loophole — hard rules don't mention Bash as prohibited for file writes |
| 2 | critical | Temp file write scope restriction is in prose only, not in the hard rules block |
| 3 | moderate | Stage 2 revision template says "absolute path" but Stage 1 uses relative paths |
| 4 | moderate | Handoff file write timing is stated in three places with contradictory wording |
| 5 | moderate | Pipeline table for "new" tasks omits reviewer (prose corrects it but table misleads) |
| 6 | minor | Stage 4 "no issues" path missing note that reviewer called scribe internally |

---

## Changes

### Change 1 — Add explicit Bash write prohibition to hard rules block (issues 1 + 2)

**Location:** Hard rules block, line 231 (the existing `Edit`/`Write` note)

**Current text (line 231–232):**
```
- The tools list intentionally omits `Edit` and `Write` — the orchestrator has no direct write access to vault files; all file changes are delegated to skill-implementer
- **Temp file (active use):** the orchestrator writes the planner slug to `.cowork/tmp/orchestrator-handoff.md` at Stage 2 completion and reads it back at Stage 3 start; this is the only permitted direct write by the orchestrator. Always overwrite, never append.
```

**Replace with:**
```
- The tools list intentionally omits `Edit` and `Write` — the orchestrator has no direct write access to vault files; all file changes are delegated to skill-implementer
- **Bash may not write files** — Bash is permitted for read-only lookups (`ls`, `cat`, `grep`) only. Never use Bash to write, overwrite, append to, or delete any file (no `echo >`, `tee`, `cat >`, heredocs, `rm`, `mv`, etc.) — not even `.cowork/tmp/` files, except for the single permitted handoff write below
- **Temp file exception (sole permitted write):** the orchestrator may write one file — `.cowork/tmp/orchestrator-handoff.md` — using a single `echo "SLUG: <slug>" > <path>` Bash call, once per pipeline run, at the moment Stage 3 begins (after planner confirms the plan is written, before calling skill-implementer). Always overwrite, never append. No other Bash write is permitted.
```

**Rationale:** Naming `Bash` explicitly closes the loophole. Collapsing the scattered temp-file references into one canonical hard-rule bullet gives skill-implementer a single authoritative statement to enforce.

---

### Change 2 — Fix "absolute path" inconsistency in Stage 2 revision template (issue 3)

**Location:** Stage 2 prose, line 114

**Current text:**
```
  - "Revise X" → call planner again using the standard `REVIEWER_BRIEF: true` format, carrying forward the same `TARGET`, `SUMMARY`, and `ISSUES`, and appending `REVISION_NOTES: <user feedback>` so planner knows this is a revision run:
    ```
    REVIEWER_BRIEF: true
    TARGET: <same absolute path from Stage 1>
    SUMMARY: <original summary>
    ISSUES:
    <original issues list>
    REVISION_NOTES: <user's revision feedback>
    ```
```

**Replace `TARGET` line with:**
```
    TARGET: <same relative path from Stage 1 — e.g. .cowork/skills/fill-templates.md>
```

**Rationale:** Stage 1 and the primary Stage 2 call template both use relative paths. Using "absolute path" here was an inconsistency that would cause the planner to receive a different path format on revision runs.

---

### Change 3 — Consolidate handoff file write timing (issue 4)

Three locations currently give contradictory write timing:

- Line 127: "write the slug to the handoff file immediately — before calling skill-implementer"
- Line 142: "always overwrite... the handoff file at the start of each Stage 2 call"
- Line 232 (hard rules): "at Stage 2 completion"

The canonical answer is: **write it once, at the start of Stage 3, after planner confirms the plan is written.** This is the most coherent reading (planner must have written the slug before you can record it).

**Fix line 127 — Stage 3 intro paragraph:**

Current:
```
After planner confirms the plan is written, write the slug to the handoff file immediately — before calling skill-implementer. This is the only direct write the orchestrator performs:
```

Replace with:
```
After planner confirms the plan is written, write the slug to the handoff file before calling skill-implementer:
```

(The "only direct write" claim moves to the hard rules block as the canonical statement — see Change 1.)

**Fix line 142 — the overwrite note:**

Current:
```
Important: always overwrite (never append) the handoff file at the start of each Stage 2 call, so a stale slug from a previous session cannot carry forward.
```

Replace with:
```
Important: always overwrite (never append) the handoff file each time Stage 3 begins, so a stale slug from a previous session cannot carry forward.
```

---

### Change 4 — Fix pipeline table for "new" tasks (issue 5)

**Location:** Task classification table, line 37

**Current row:**
```
| `new` | Creating a skill or agent that does not exist yet | planner → implementer → scribe |
```

**Replace with:**
```
| `new` | Creating a skill or agent that does not exist yet | reviewer (related file, quick) → planner → implementer → scribe |
```

**Rationale:** Line 41 already explains that reviewer still runs on `new` tasks (targeting a related existing file for consistency patterns), but the summary table contradicts this. Fix the table so it matches the prose.

---

### Change 5 — Add scribe note to Stage 4 "no issues" path (issue 6)

**Location:** Stage 4, line 182

**Current text:**
```
If reviewer reports **no issues**: inform the user and close the pipeline.
```

**Replace with:**
```
If reviewer reports **no issues**: inform the user and close the pipeline. (Reviewer called scribe internally — no additional scribe call needed.)
```

**Rationale:** The "issues found" path already notes that reviewer+scribe ran. The "no issues" path should say the same for completeness and to avoid the orchestrator making a redundant scribe call.

---

## What is NOT changing

- The `Bash` tool is **not being removed** from the `tools:` list. It is needed for read-only lookups (`ls`, `cat`, `grep`). Only write-mode Bash is being prohibited.
- No pipeline logic changes — all stage gates, agent calls, and A2A wiring remain the same.
- No changes to reviewer, planner, skill-implementer, or scribe agent files.
