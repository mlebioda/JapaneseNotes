# Practice Grammar — Persist Before Study Mode (last batch)

## Goal
In `.cowork/skills/practice-grammar.md`, the last-batch branch of the between-batch
gate (Workflow step 7e) currently gates persistence (writing `grammar-state.json`
and the `.ics` calendar file) behind the user's choice between "Study mode" and
"Save & finish" — persistence only happens once the user picks one of those and,
if Study Mode was chosen, only after it exits. The user wants the reverse: as soon
as self-evaluation scores are collected for the final batch, persist immediately
(unconditionally), and only then ask whether the user wants to enter Study Mode.
This makes session data durable earlier and turns Study Mode into a purely optional,
already-safe extra step rather than something that gates saving.

Scope is confirmed to be **only** the last-batch branch of step 7e (`B ==
num_batches`). The non-last-batch branch (`Next batch / Study mode`, lines
142–149) is unaffected — it has no persistence step to reorder around, since
grammar-state.json is only ever written once per session (at the end), and
that remains true.

## Approach
Restructure the last-batch branch so Workflow steps 8–10 (write session summary,
persist `grammar-state.json`, write the calendar `.ics`) execute unconditionally
immediately after self-evaluation scores are collected for the final batch —
before any prompt is shown. Then present a renamed two-option prompt, `Study mode
/ Finish` (replacing `Study mode / Save & finish` — "Save & finish" no longer
makes sense once saving has already happened). "Study mode" enters Study Mode as
supplementary practice only (session data is already saved, so exiting Study Mode
just ends the session — no further action needed). "Finish" ends the session
immediately. "Finish" is chosen over "Done" to match the existing continuation
label already used after Study Mode in the non-last-batch branch (line 147:
"Next batch / Finish").

A second, related fix: pin down where Study Mode's `weak_points` input (Study
Mode section, line 444: "per grammar_point_id weak_points from
grammar-state.json") comes from. After the reorder, `grammar-state.json` will
already contain this session's freshly-written weak_points by the time Study
Mode runs for the last batch (unlike the non-last-batch case, where the file is
still untouched at that point in the session). Left ambiguous, this could cause
Study Mode's bias data to silently diverge between the two invocation paths.
The plan clarifies the wording to explicitly mean the in-memory value
loaded once at Workflow step 5 (session start) / accumulated during the
session — never a fresh re-read of the persisted file — so Study Mode's
behavior stays identical regardless of when in the flow it's invoked.

**Revision note (reviewer audit):** an earlier draft of this plan incorrectly
declared `.cowork/skills/practice-grammar-study-mode.md` out of scope /
"no change." That was wrong — its Step 3 last-batch case still calls for a
second post-session persistence pass after Study Mode exits, which after the
reorder would double-invoke `practice-grammar-srs.md` on the same
`session_scores` (duplicate SM-2 advancement and a duplicate `.ics` file).
That sub-skill file is now explicitly in scope (Step 6 below), along with a
new guard against "stop"/"end" at the last-batch `Study mode / Finish` prompt
triggering the same double-persist bug via the Early-exit path (Step 1).

## Steps

1. **`.cowork/skills/practice-grammar.md` — Workflow step 7e, last-batch branch (currently lines 150–157)**
   Replace the existing bullet with:
   - On reaching `B == num_batches` (last batch), immediately after self-evaluation
     scores are collected for this batch: run Workflow steps 8–10 unconditionally
     (write the session summary, persist to `grammar-state.json`, write the
     calendar `.ics` — see **Session summary** and **Persistence and Calendar
     sync** sections). This happens before any prompt is shown; it is no longer
     gated behind a user choice.
   - Then ask:
     ```
     Study mode / Finish
     ```
     - "Study mode" → enter Study Mode for the topics in the last batch. Session
       data is already saved at this point — Study Mode is purely supplementary
       practice. After Study Mode exits, end the session (nothing further to
       persist).
     - "Finish" (or equivalent affirmative) → end the session immediately.
     - If the user asks an off-topic question, answer it and re-present the same
       prompt.
     - The prompt must always appear — never auto-finish without user
       confirmation, even though persistence has already occurred.
   - **New guard — "stop"/"end" at this specific prompt.** The general
     Early-exit sub-bullet (below) fires on "stop"/"end" "at any point
     mid-session" and unconditionally re-persists all scores collected so far.
     That rule must **not** apply verbatim at this specific prompt, because
     persistence for this batch (and the whole session, since this is the
     last batch) already happened one step above. Explicitly carve out this
     case: if the user types "stop" or "end" in reply to the `Study mode /
     Finish` prompt, treat it as a no-op alias for "Finish" — end the session
     immediately, do **not** re-invoke `practice-grammar-srs.md`, do not
     rewrite `grammar-state.json`, and do not write a second `.ics` file.
   - Leave the **Early exit** sub-bullet's behavior for all other mid-session
     points (before this prompt is reached) unchanged — it still persists
     immediately then stops there, which remains correct since persistence
     has not yet happened at those earlier points.

2. **`.cowork/skills/practice-grammar.md` — Workflow numbered list, steps 8–10 (currently lines 160–162)**
   Add a short clarifying note to step 8 ("After the last batch — write the
   session summary") that these three steps execute inline, automatically, as
   part of step 7e's last-batch branch — not as a separate phase the user
   reaches only after choosing "Save & finish" (that gate no longer exists).
   No change to the content of steps 8, 9, or 10 themselves, or their internal
   order (summary → persist → calendar stays the same).

3. **`.cowork/skills/practice-grammar.md` — Persistence and Calendar sync section (currently lines 502–513)**
   Update the opening line ("After the last batch completes (or when the user
   types 'stop'), read `.cowork/skills/practice-grammar-srs.md`...") to note
   this now happens immediately upon reaching the last batch's self-evaluation
   completion — before the `Study mode / Finish` prompt — not after a user
   chooses to finish. No change to the `session_scores` / `session_grammar_ids`
   / `today` / `scope` payload passed to `practice-grammar-srs.md`.

4. **`.cowork/skills/practice-grammar.md` — Study Mode section (currently lines 435–446)**
   Clarify the `weak_points` bullet (line 444) to read: "per grammar_point_id
   weak_points, as loaded once at Workflow step 5 (session start) and/or
   accumulated in memory during the session — never re-read from
   `grammar-state.json` after persistence." This keeps Study Mode's bias data
   identical whether it's invoked from the non-last-batch branch (state file
   not yet written) or the last-batch branch (state file already written, post
   reorder).

   Also fix the adjacent `is_last_batch` bullet (currently line 441 —
   "`is_last_batch` and `num_batches`: so Step 3 knows whether to ask 'Next
   batch' or proceed to post-session"). "Proceed to post-session" is stale for
   the last-batch case in the same way as the `practice-grammar-study-mode.md`
   fix in step 6 below — reword to: "so Step 3 knows whether to ask 'Next
   batch / Finish' (non-last batch) or simply end the session (last batch —
   the session was already saved before Study Mode was entered)."

5. **No change** to the non-last-batch branch (`Next batch / Study mode`, lines
   142–149) — confirm this explicitly during implementation review; it is out
   of scope per user confirmation.

6. **`.cowork/skills/practice-grammar-study-mode.md` — Step 3 (currently lines
   146–155) and Context required section (currently lines 12–19)**
   This file **is** in scope — correcting an earlier mistake in this plan
   that declared it unchanged. Two fixes required:

   a. **Step 3, last-batch case (currently line 153).** Currently reads:
      "If the last batch: proceed directly to post-session (write state +
      calendar)." Post-reorder, persistence for the last batch already
      happened in `practice-grammar.md` step 7e *before* Study Mode was even
      entered. If this line is left as-is, it triggers a **second** call to
      `practice-grammar-srs.md` with the same `session_scores` — double
      advancing SM-2 intervals/ease and writing a duplicate `.ics` calendar
      file. Rewrite to: "If the last batch: the session was already saved
      before Study Mode was entered — end the session now. Do **not**
      re-invoke `practice-grammar-srs.md`, do not rewrite
      `grammar-state.json`, and do not write a second `.ics` file. There is
      nothing further to persist."

      Note: the **non-last-batch** case immediately above it (currently line
      150–152, "If not the last batch: ask `Next batch / Finish`" → "Finish"
      → "proceed to post-session ... with all scores collected so far")
      stays unchanged — that path is a genuine early exit with real
      unsaved data, since persistence is still deferred to end-of-session
      for non-last batches. Do not apply the last-batch fix to this bullet.

      Also update the standalone sentence below the bullets (currently line
      155: "The 'Finish' option in Step 3 is a full early exit — load
      `practice-grammar-srs.md`...") to scope it explicitly to the
      non-last-batch case only, so it isn't misread as applying to the
      last-batch "end the session now" case too.

   b. **Context required section, `weak_points` bullet (currently line 19).**
      This is a duplicate of the wording fixed in step 4 above
      (`practice-grammar.md` line 444). Apply the identical clarification
      here so both files describe the input the same way: "per
      grammar_point_id weak_points, as loaded once at Workflow step 5
      (session start) and/or accumulated in memory during the session —
      never re-read from `grammar-state.json` after persistence."

      Also fix `is_last_batch` bullet (currently line 17 — "controls whether
      Step 3 asks 'Next batch' or proceeds to post-session") to match the
      step 4 fix in `practice-grammar.md`: reword to reference "Next batch /
      Finish" vs. "end the session (already saved)", not "post-session."

## Risks
- If the reorder wording is ambiguous, an implementer could accidentally make
  persistence conditional again (e.g. by leaving stale references to "proceed
  to post-session" that imply steps 8–10 only run after the prompt). Step 1's
  replacement bullet must be copied verbatim, not paraphrased, during
  implementation.
- **Double-persistence (critical, now guarded by Steps 1 and 6).** Two
  distinct triggers could otherwise cause `practice-grammar-srs.md` to run
  twice for the same last-batch session — once from step 7e's new
  unconditional persist, and again from either (a) `practice-grammar-study-
  mode.md` Step 3's stale "proceed directly to post-session" line, or (b) the
  general Early-exit sub-bullet firing on "stop"/"end" at the new `Study mode
  / Finish` prompt. Both are explicitly closed by Steps 6a and 1's new guard
  respectively — the implementer must verify both fixes land together, since
  either one alone leaves a live double-write path.
- Session-summary footer text ("Next review dates written to
  grammar-state.json. Calendar file: ... written to vault root.") is printed
  as part of step 8 and must remain accurate — since steps 8–10 now run before
  the Study mode/Finish prompt, this line is truthful (the state file really
  has been written by the time it's shown), which is actually an improvement
  over the current ordering's implied simultaneity.
- Does not touch `<!--ID:-->` lines, `TARGET DECK`, or any lesson file — this
  is a skill-file-only change, no risk to plugin export data.
- `.cowork/instructions.md`'s skill description for `practice-grammar` does
  not need updating for this change (it doesn't describe this level of
  internal ordering detail) — confirm during implementation review.
