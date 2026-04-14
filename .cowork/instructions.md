# Japanese Vault — Cowork Project Instructions

## Vault location
/Users/michallebioda/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianJP/

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
- Always create a .bak backup before modifying any file (no confirmation needed — backup is automatic)
- When user references a lesson by number (e.g. "UNGL15"), find the file automatically

## fill workflow (fastest path)
Load the `.cowork/skills/fill-templates.md` skill and follow its instructions.
Claude generates cards directly — no script execution needed.
Output structure: `# Summary` heading → ` --- ` → ` Rzeczowniki:` → cards.
No `Tłumaczenie:` keyword. No confirmation step required.

## Available skills
Skills are defined in .cowork/skills/ — load the relevant skill before acting.

- kanji-headers — format kanji tables from images into structured markdown headers
