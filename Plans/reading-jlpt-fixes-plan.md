# reading-jlpt Skill — Targeted Fixes

## Goal
Apply five targeted fixes to the already-created `.cowork/skills/reading-jlpt.md` skill. The skill is functional but has gaps in its frontmatter, directory handling, fill-templates interface contract documentation, session filename uniqueness, and no-passage fallback behaviour.

## Approach
All five changes are confined to a single file: `.cowork/skills/reading-jlpt.md`. No other skill or configuration file needs to change. Changes are surgical edits — no structural rewrite. fill-templates already works correctly with `# Words to extract` (its script extracts all `#w`/`#wc`/`#wp` tags from anywhere in the file above `# Summary`), so the interface fix is documentation-only.

## Steps

1. **Add tools frontmatter** — `.cowork/skills/reading-jlpt.md`
   - The current frontmatter block has `name` and `description` but no `tools:` field.
   - Add `tools: [Read, Write, Bash]` as the third frontmatter line, after `description`.

2. **Add directory guard in Step 6** — `.cowork/skills/reading-jlpt.md`
   - Step 6 currently writes the session file with no pre-check.
   - Immediately before the write instruction, add: before writing, use Bash to run `mkdir -p` on the absolute vault path to `JPLessons/Reading/` so the directory is created if it does not yet exist.
   - Also remove the contradicting "Does not create the `JPLessons/Reading/` directory" line from the "What this skill does NOT do" section, since the guard now handles it.

3. **Document fill-templates chain interface** — `.cowork/skills/reading-jlpt.md`
   - Step 7's fill-templates chain sentence currently reads: "The `# Words to extract` section feeds the vocabulary; fill-templates outputs into `# Summary`."
   - Expand this with an explicit interface note: fill-templates uses `fill_extract.py` which scans for `#w`/`#wc`/`#wp` tags anywhere in the file above `# Summary`, so `# Words to extract` is already a valid source with no changes needed to fill-templates.

4. **Fix session filename to include time component** — `.cowork/skills/reading-jlpt.md`
   - All occurrences of the filename pattern `Reading-session-<YYYYMMDD>.md` must become `Reading-session-YYYYMMDDTHHMMSS.md` (ISO 8601 compact datetime, no angle-brackets in the pattern text).
   - Affected locations in the skill file: the Step 6 write instruction, the Step 6 confirmation message template, the Step 7 "if no" manual-call example sentence, and the "What this skill does NOT do" section.

5. **Add no-passage fallback instruction** — `.cowork/skills/reading-jlpt.md`
   - The Trigger section currently lists valid trigger phrases but gives no instruction for the case where the user invokes the skill without pasting a passage.
   - At the end of the Trigger section, add one sentence: "If the user triggers this skill but pastes no passage, ask them to provide one before proceeding."

## Risks
- The fill-templates interface note (Step 3) is documentation only — it does not change how fill-templates works, and the chain already functions correctly.
- Changing the filename pattern (Step 4) means old session files named `Reading-session-YYYYMMDD.md` will not match the new pattern in Step 7's manual-call example. This is acceptable — old files are unaffected; only new sessions use the new name.
- The `mkdir -p` guard (Step 2) is idempotent and will not overwrite any existing directory contents.
