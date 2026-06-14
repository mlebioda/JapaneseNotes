# reading-jlpt

## Goal
Add a new skill that runs JLPT N4 reading comprehension drills on real passages pasted by the user. The user sources authentic texts (jlpt.jp, NHK Web Easy, Shin Kanzen Master N4, So-Matome N4) and Claude runs a structured drill: detect passage type, flag above-N4 content, generate multiple-choice questions, explain results, suggest vocabulary, and write a session file to `JPLessons/Reading/`. No generated passages — authentic material only.

## Approach
Single skill file at `.cowork/skills/reading-jlpt.md`. The skill is self-contained: it has no persistent state JSON (session files serve as the record). It chains to the existing `fill-templates` skill for Anki card generation at the end of each session. All output conventions (TARGET DECK, #w/#wc/#wp format, # Summary section) follow existing vault standards so fill-templates can operate on reading session files without modification.

## Steps

1. Create `.cowork/skills/reading-jlpt.md`
   - **Trigger section**: matches "practice reading", "reading drill", "jlpt reading [passage]", or equivalent phrasing.
   - **Recommended sources** block (printed on request): jlpt.jp, NHK Web Easy, Shin Kanzen Master N4 読解, So-Matome N4 読解 — with one-line descriptions.
   - **Step 1 — Auto-detect passage type**: classify pasted content as Short (短文, ~100–200 chars, 1 question), Medium (中文, ~300–400 chars, 2–3 questions), or Information retrieval (情報検索, document-like layout).
   - **Step 2 — Scan for above-N4 content**: before showing questions, identify vocabulary and kanji likely above N4. List each with reading and meaning. Present to user; user decides whether to proceed. Flagged words are carried forward to Step 5.
   - **Step 3 — Generate all questions at once** (batch mode, mirrors practice-grammar): all questions in a single message, no answers, no hints, no furigana. Multiple choice, 4 options (A/B/C/D). Question type varies by passage type (detail/main idea/inference/author intent/information retrieval).
   - **Step 4 — Explain all answers**: after user submits all answers, show per-question results. Correct: one-line confirmation plus key sentence from passage. Wrong: explain why chosen option is wrong and why correct option is right, quote specific passage sentences as evidence.
   - **Step 5 — Word suggestions**: suggest #w/#wc/#wp candidates from (a) words linked to wrong answers, (b) above-N4 words flagged in Step 2. Skip entirely if user got everything right and Step 2 found nothing. User confirms which to keep. Format confirmed words as standard vault vocabulary lines with furigana inline.
   - **Step 6 — Write session file** to `JPLessons/Reading/Reading-session-<YYYYMMDDTHHMMSS>.md` BEFORE asking about fill-templates. Before writing, check that `JPLessons/Reading/` exists; if it does not, stop with the error message: "JPLessons/Reading/ not found — check iCloud sync and create it manually." Do NOT create the directory. File must be written even if user declines fill-templates. File structure (exact field order): `TARGET DECK: JLPT-Reading` (line 1), `# Passage` (passage as pasted, no furigana), `# Questions` (questions as shown in Step 3), `# Results` (explanations from Step 4), `# Words to extract` (confirmed #w/#wc/#wp lines, or empty section), `# Summary` (always present, always empty — for fill-templates).
   - **Step 7 — Offer fill-templates**: ask user if they want fill-templates run on the session file. If yes, load `.cowork/skills/fill-templates.md` and follow its instructions. If no, inform user the file is saved and fill-templates can be called manually later.
   - **Skill frontmatter tools list**: must include Write and Edit only. Do NOT include Read — this skill never reads files.
   - **What this skill does NOT do** section: no generated passages, no persistent state JSON, no furigana in passage/questions/results, no word suggestions when user scored 100% with no above-N4 flags.

2. Register the skill in `.cowork/instructions.md` under the Available skills table.
   - Entry: `reading-jlpt — JLPT N4 reading comprehension drill on user-pasted passages. Auto-detects type, flags above-N4 vocab, generates multiple-choice questions, explains results, suggests vocabulary, writes session file to JPLessons/Reading/. Chains to fill-templates. Trigger: "practice reading [passage]", "reading drill", "jlpt reading [passage]"`

## Risks
- `JPLessons/Reading/` directory must already exist. The skill must check for its existence before writing and stop with a clear error message if it is missing: "JPLessons/Reading/ not found — check iCloud sync and create it manually." Do NOT use mkdir -p or any directory creation — fail loudly so iCloud sync problems are surfaced, not silently hidden.
- `TARGET DECK: JLPT-Reading` must be exactly line 1 — no blank line before it — so the Obsidian-to-Anki plugin picks it up the same way as all other lesson files.
- The `# Summary` section must be present but empty. fill-templates looks for this section; any content in it could confuse the plugin's ID tracking.
- No `<!--ID:-->` lines will exist in a new session file. That is expected and correct; the plugin generates them on first export.
- Modifying `.cowork/instructions.md` requires user permission per vault rules. The skill-implementer must ask before editing that file.
