# Japanese Vault — Cowork Project Instructions

## Vault location
/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/

## Directory map
- `JPLessons/` — all lesson files, organized by course then JLPT level
- `grammar-index/` — grammar index: topic files (one per topic, managed by summarize-grammar/extract-grammar skills) and `grammar/` subdirectory (standalone grammar point files, one per pattern, created by extract-grammar)
- `Caligraphy/` — standalone kanji reference notes: Kanji/, Radicals/, Primitives/ — NOT lesson files
- `Vocabulary/` — standalone vocabulary lists by topic (not lesson files)
- `BanBanAkademi/` — notes from BanBanAkademi course (separate from Udemy)

## Lesson file locations
- Grammar: JPLessons/Udemy/NL/Grammar/UNGLX (where L = level, X = number)
- Calligraphy: JPLessons/Udemy/NL/Caligraphy/UNKLX
- Example: JPLessons/Udemy/N5/Grammar/UNGL14-Please-come-to-station-at-7-pm.md

## File naming
- N = JLPT level (N5, N4, N3...)
- X = lesson number
- Example: UN5GL14 = Udemy, N5, Grammar, Lesson 14

## Note tags
- #w — word, expression, sentence, adverb (everything except verbs and adjectives)
- #wc — verb
- #wp — adjective

## File structure
Every lesson file contains:
1. TARGET DECK line at the top — never modify
2. Content sections: ごい, ひょうげん, 文法, Vocabulary
3. A separator line: # Summary
4. Everything below # Summary is plugin-generated export — structure:
   - Rzeczowniki: — #w cards (never modify)
   - Czasowniki: — #wc verb cards (plugin generates empty Polish fields)
   - Przymiotniki: — #wp adjective cards (plugin generates empty Polish fields)

## General rules — always follow
- Never modify anything above Summary section
- Never modify # Summary
- Never modify or delete <!--ID: --> lines
- Git is the rollback mechanism — no `.bak` files. Before a destructive edit, ensure pending changes are committed (commit a "WIP" snapshot if needed), then edit; commit the change separately.
- When user references a lesson by number (e.g. "UNGL15"), find the file automatically
- Never create files directly in the vault root (`/ObsidianJP/`) unless explicitly asked
  - Approved exception: `.ics` calendar files written by the practice-grammar skill (`japanese-grammar-review-<timestamp>.ics`) and manage-holidays skill (`japanese-grammar-full-calendar-<timestamp>.ics`). These are intentionally placed at the vault root for easy drag-and-drop calendar import.

## Image extraction format
When the user sends an image and asks to "extract", output vocabulary lines in this format:

```
#w 明日(あした)の仕事(しごと) - english
#wc 出来る(でき) - english
#wp 難しい(むずか) - english
```

RULE: Always extract the full phrase/sentence exactly as it appears in the image.
Never split into individual words. One line per visual item on screen, not per word.
Exception: only split if the image is explicitly a word-by-word vocabulary list.

Rules:
- #w — nouns, expressions, sentences, adverbs
- #wc — verbs (G1/G2/G3); append (transitive) or (intransitive) after the English translation, e.g. `#wc 食べる(たべ) - to eat (transitive)`
- #wp — adjectives (い-adj / な-adj)
- Readings are inline after each kanji word using ASCII parentheses: `kanji(reading)` — e.g. `明日(あした)の仕事(しごと)`
- Katakana-only words have no reading in parentheses
- n./G3 entries (suru nouns) → use #w with (する) appended after the reading: e.g. `#w 入院(にゅういん)(する) - hospitalization / to be hospitalized + verb`
- n./な-adj entries → use #wp
- interj. / adv. with no kanji → use #w with no parentheses

## fill workflow (fastest path)
Load the `.cowork/skills/fill-templates.md` skill and follow its instructions.
Claude generates cards directly — no script execution needed.
Output structure: `# Summary` heading → ` --- ` → ` Rzeczowniki:` → cards.
No `Tłumaczenie:` keyword. No confirmation step required.

## Available skills
Skills are defined in .cowork/skills/ — load the relevant skill before acting.

- kanji-headers — format kanji tables from images into structured markdown headers
- kanji-file — process a single kanji into a standalone `Caligraphy/Kanji/<kanji>.md` file: reads existing file or creates new, inserts structured table (readings, strokes, meanings, mnemonics, examples), links radicals/primitives. Trigger: "kanji file <kanji>", "create kanji file <kanji>"
- practice-grammar — interactive grammar drill for a lesson file; reads only `# 文法` + `# Vocabulary` (grammar topics) and `# ごい` + `# ひょうげん` (vocab pool). Writes results to `.cowork/progress/grammar-state.json` (SM-2 lite) and generates a timestamped `.ics` calendar file (`japanese-grammar-review-<timestamp>.ics`) at the vault root for easy calendar import. Trigger: "let's practice <lesson>". Also supports scope-based triggers: "practice today's topics" (drills grammar points with next_review == today) and "practice overdue topics" (drills past-due points, user picks how many).
- summarize-grammar — add a single lesson's grammar points to the topic-grouped index at `/grammar-index/`. One topic file per topic; entries are wikilinks (no copied text); a point may appear in multiple topics. Trigger: "summarize <lesson>"
- templates-update — audit and repair already-filled Anki card templates in a lesson's `# Summary` section: normalize field names, fill missing forms, verify conjugation/adjective form correctness, fix kanji links, and reposition `<!--ID:-->` lines. Triggers: "templates-update [file]", "update templates [file]", "repair templates [file]", "fix templates [file]"
- reading-jlpt — JLPT N4 reading comprehension drill on user-pasted passages. Auto-detects passage type (短文/中文/情報検索), flags above-N4 vocab, generates multiple-choice questions, explains results, suggests vocabulary, writes session file to `JPLessons/Reading/`. Chains to fill-templates. Trigger: "practice reading [passage]", "reading drill", "jlpt reading [passage]"
- manage-holidays — manage holiday dates for the SRS load control system. Add/remove holidays (treated as blocked days like Saturdays), detect and redistribute colliding reviews, export a full-calendar .ics with all future review events and holidays. Reads/writes `.cowork/progress/holidays.json`. Trigger: "manage holidays", "add holiday <date>", "remove holiday <date>", "show holidays", "export calendar"
- update-kanji-list — **DEPRECATED**. Use `kanji-file` instead for per-kanji standalone file processing.

**lesson-to-web/** (skills for extracting lesson content into published grammar-index files):
- lesson-to-web/extract-grammar — extract grammar points from a lesson's 文法 section into standalone files under grammar-index/grammar/. Also classifies each file into grammar-index/ topic files. Trigger: "extract grammar from <lesson>"
- lesson-to-web/extract-vocabulary — extract vocabulary lines from a lesson into Vocabulary/words-extracted.md. Trigger: "extract vocabulary from <lesson>"
- lesson-to-web/update-grammar — full post-processing pipeline: chains all four steps below. Trigger: "update grammar <file>"
- lesson-to-web/preprocess-grammar — Step 1: tag removal, Polish detection, furigana, typos (mechanical, no user gates). Trigger: "preprocess grammar <file>"
- lesson-to-web/review-grammar — Step 2: correctness check + missing info suggestions (user-gated). Trigger: "review grammar <file>"
- lesson-to-web/structure-grammar — Step 3: structure enforcement, Structure 1 vs 2 (user confirmation). Trigger: "structure grammar <file>"
- lesson-to-web/see-also-grammar — Step 4: populate ## See also, set proofread: true. Trigger: "see-also grammar <file>"


## Agent system

Agents are defined in `.claude/agents/`. Start with **`reviewer`** for analysis tasks or **`planner`** if you already know what to build. Each agent presents a "which agent next?" menu at the end of its run — follow the prompts.

Pipeline: **reviewer → planner → skill-implementer → reviewer (optional)**

**`orchestrator`** — DEPRECATED. No longer the entry point. Use the pipeline above instead.

**`reviewer`** — read-only analysis. Finds bugs, missing rules, A2A wiring issues, consistency problems. Entry point for any change task. At the end, presents agent options and suggests planner.

**`planner`** — creates structured plans in `Plans/`. Accepts `REVIEWER_BRIEF` input for A2A use. Calls scribe (non-blocking), then presents agent options and suggests skill-implementer.

**`skill-implementer`** — executes plans. Reads `Plans/`, writes to `.cowork/skills/` and `.claude/agents/`. Calls documentation agent automatically. At the end, presents agent options and suggests reviewer.

**`scribe`** — logs captures and generates blog posts. Called automatically by planner only. Modes: `capture`, `git-sweep`, `retrospect`, `post`.

**`documentation`** — generates and updates the vault system diagram (`docs/vault-system-diagram.puml`). Called automatically by skill-implementer after any agent or skill file change. Trigger: "generate diagram" or "update diagram".

**`skill-updater`** — DEPRECATED. Use the reviewer → planner → skill-implementer pipeline instead.

# Project rules
- Never modify files in .cowork/ without permission. Always ask and explain what do you want to modify.
- Never remove files without my permission
- Don't use git commands without permission
- When the user says "run implementer", "use skill-implementer", or similar, always spawn the skill-implementer agent — never implement the changes directly yourself. If the first spawn gets stuck, re-spawn with a fully self-contained prompt.