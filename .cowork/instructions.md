# Japanese Vault — Cowork Project Instructions

## Vault location
/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/

## Directory map
- `JPLessons/` — all lesson files, organized by course then JLPT level
- `grammar-index/` — grammar index: topic files (one per topic, managed by summarize-grammar/extract-grammar skills) and `grammar/` subdirectory (standalone grammar point files, one per pattern, created by extract-grammar)
- `Kaligrafia/` — standalone kanji reference notes: Kanji/, Radicals/, Primitives/ — NOT lesson files
- `Vocabulary/` — standalone vocabulary lists by topic (not lesson files)
- `BanBanAkademi/` — notes from BanBanAkademi course (separate from Udemy)

## Lesson file locations
- Grammar: JPLessons/Udemy/NL/Gramatyka/UNGLX (where L = level, X = number)
- Calligraphy: JPLessons/Udemy/NL/Kaligrafia/UNKLX
- Example: JPLessons/Udemy/N5/Gramatyka/UNGL14-Please-come-to-station-at-7-pm.md

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

## Image extraction format
When the user sends an image and asks to "extract", output vocabulary lines in this format:

```
#w japanese (reading1, reading2) - english
#wc japanese (reading) - english
#wp japanese (reading) - english
```

Rules:
- #w — nouns, expressions, sentences, adverbs
- #wc — verbs (G1/G2/G3)
- #wp — adjectives (い-adj / な-adj)
- Readings in parentheses are readings of kanji only, comma-separated, in order of appearance
- Katakana-only words have no reading in parentheses
- n./G3 entries (suru nouns) → use #w with (する) appended to the Japanese: e.g. `#w 入院(する) (にゅういん) - hospitalization / to be hospitalized + verb`
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
- practice-grammar — interactive grammar drill for a lesson file; reads only `# 文法` + `# Vocabulary` (grammar topics) and `# ごい` + `# ひょうげん` (vocab pool). Writes results to `.cowork/progress/grammar-state.json` (SM-2 lite). Trigger: "let's practice <lesson>"
- summarize-grammar — add a single lesson's grammar points to the topic-grouped index at `/grammar-index/`. One topic file per topic; entries are wikilinks (no copied text); a point may appear in multiple topics. Trigger: "summarize <lesson>"
- extract-grammar — extract grammar points from a lesson's 文法 section into standalone files under grammar-index/grammar/. Also classifies each file into grammar-index/ topic files. Trigger: "extract grammar from <lesson>"
- extract-vocabulary — extract vocabulary lines from a lesson into Vocabulary/words-extracted.md. Trigger: "extract vocabulary from <lesson>"

# Project rules
- Never modify files in .cowork/ without permission. Always ask and explain what do you want to modify.
- Never remove files without my permission
- Don't use git commands without permission