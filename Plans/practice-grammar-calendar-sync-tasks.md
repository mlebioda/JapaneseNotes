# Practice Grammar — Calendar Sync Fixes — Tasks

## File: `.cowork/skills/practice-grammar.md`

- [ ] **#1 (critical)** Fix `DTEND` — add `from datetime import date, timedelta`; derive `dt_date = date.fromisoformat(d[:10])` and `dt_end = (dt_date + timedelta(days=1)).strftime("%Y%m%d")`; replace `DTEND` line to use `dt_end`
- [ ] **#2 (critical)** Add `fold()` helper function before the `lines = [...]` block; wrap every line through `fold()` in the `f.write()` call; verify the `open()` call includes `encoding="utf-8"`
- [ ] **#3 (moderate)** Replace hardcoded `/sessions/stoic-jolly-noether/mnt/ObsidianJP/` paths with a `VAULT_ROOT` constant set to `/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP`; add the NOTE comment instructing Claude to translate to the active session mount at runtime
- [ ] **#4 (moderate)** Replace `d.replace("-","")` with `date.fromisoformat(d[:10])` + `.strftime("%Y%m%d")` (reuse `dt_date` from fix #1 — a single variable serves both)
- [ ] **#6 (design decision)** Switch from single overwrite file to timestamped file per session: add `session_ts = date.today().strftime("%Y%m%dT%H%M%S")`; set `ics_path = f"{VAULT_ROOT}/japanese-grammar-review-{session_ts}.ics"`; update `## Calendar sync` prose to describe per-session additive files and remove the "Always overwrite" bullet from the Rules list
- [ ] **#7 (minor)** Add `import uuid`; replace UID line with `f"UID:{dtstr}-{session_ts}-{str(uuid.uuid4())[:8]}@japanese-notes"` using the `session_ts` already computed for the filename
- [ ] **#8 (minor)** Remove stray `a` typo and orphaned `1. ` prefix on the line after the closing code fence; update the confirmation message filename reference from `japanese-grammar-review.ics` to `japanese-grammar-review-<timestamp>.ics`
- [ ] **#9 (minor)** In `## Session summary`, update the closing line of the summary block from `Next review dates written to grammar-state.json.` to `Next review dates written to grammar-state.json. Calendar file: japanese-grammar-review-<timestamp>.ics written to vault root.`
- [ ] Verify the complete script block matches the canonical fixed version in the plan's "Complete fixed Python script" section

## File: `.cowork/instructions.md`

> Note: both changes below touch a protected `.cowork/` file — obtain explicit user permission before editing.

- [ ] **#5 (moderate)** In `## General rules — always follow`, add an indented approved-exception note under the vault-root bullet documenting that `.ics` calendar files from the practice-grammar skill are an approved exception
- [ ] **#10 (minor)** In `## Available skills`, update the `practice-grammar` bullet to mention the timestamped `.ics` output alongside `grammar-state.json`

## Verification

- [ ] Confirm no other occurrence of the hardcoded `/sessions/stoic-jolly-noether/` path remains in the file
- [ ] Confirm `DTSTART` and `DTEND` are distinct dates (off-by-one check)
- [ ] Confirm `fold()` is actually called in the write path, not just defined
- [ ] Confirm the stray `a` on line 382 is gone
- [ ] Confirm `## Workflow` step 10 still references the calendar file (it already says "Regenerate calendar file" — verify the wording remains accurate after the overwrite→timestamped change)
