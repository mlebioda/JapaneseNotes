# reading-jlpt — Tasks

- [x] Create `.cowork/skills/reading-jlpt.md` with all seven workflow steps, recommended sources block, and "what this skill does NOT do" section; ensure frontmatter tools list contains Write and Edit only (no Read)
- [x] Verify `JPLessons/Reading/` directory exists before writing; if missing, stop with error "JPLessons/Reading/ not found — check iCloud sync and create it manually" — do NOT use mkdir -p
- [x] Confirm with user before editing `.cowork/instructions.md`, then add reading-jlpt entry to the Available skills table
- [ ] Smoke-test the skill with a short (短文) passage: check passage-type detection, question count (1), above-N4 scan output, session file written to `JPLessons/Reading/Reading-session-<YYYYMMDDTHHMMSS>.md` with correct TARGET DECK line and empty # Summary
- [ ] Smoke-test with a medium (中文) passage: check 2–3 questions generated, explanations reference passage sentences, word suggestions only appear for wrong answers or above-N4 flags
- [ ] Verify fill-templates chain: confirm that when user says yes in Step 7, fill-templates runs correctly on the session file (# Words to extract feeds into # Summary output)
