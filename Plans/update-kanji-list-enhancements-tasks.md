# Tasks: update-kanji-list & kanji-headers Enhancements

**Date:** 2026-06-07
**Plan:** `Plans/update-kanji-list-enhancements-plan.md`
**Target files:** `.cowork/skills/update-kanji-list.md`, `.cowork/skills/kanji-headers.md`
**Status:** done

---

## Task list

| # | Section | Change | Status |
|---|---------|--------|--------|
| 1 | **update-kanji-list.md — Step 0** | Add web fetch step: fetch kanji-trainer.org page per kanji, extract Mnemonic (`id="idFeldErklar"`) and Explanation (`id="idFeldErlaeter"`); handle failure with warning | [x] |
| 2 | **update-kanji-list.md — Step 1/3: Component linking** | Parse Explanation text for CJK component characters; resolve each to existing file in Primitives/ or Kanji/; write `### Mnemonic` and `### Parts` sections to kanji file; de-duplicate links | [x] |
| 3 | **update-kanji-list.md — Step 2: Routing and naming** | Add component file routing rule (Primitives/ vs Kanji/); add rename rule `character - name.md` (spaces around hyphen); update new-file structure to match | [x] |
| 4 | **update-kanji-list.md — Step 4: Bare link migration** | When reading an existing kanji/primitive file, migrate any wikilinks that appear outside a named `##` section into `## Occurences` | [x] |
| 5 | **update-kanji-list.md — Step 5: Consistency check** | After all steps, verify every touched file has `## Occurences`; verify all links under `## Occurences` and `## Parts` are valid wikilinks; report warnings | [x] |
| 6 | **update-kanji-list.md — Completion report** | Update the completion report format to include web fetch stats, mnemonics written, bare links migrated, component files created | [x] |
| 7 | **kanji-headers.md — Cross-reference note** | Add note that `update-kanji-list` Step 3 handles `## Parts` component files; `kanji-headers` does not touch them | [x] |
| 8 | **kanji-headers.md — Wikilink re-derive note** | Add note that when `update-kanji-list` creates a new file, the wikilink must be re-derived from the actual filename (post-creation) | [x] |

---

## Notes

- Steps 0, 1/3, 2, 4, 5 all go into `update-kanji-list.md`; tasks 7–8 are minor notes to `kanji-headers.md`.
- Step 0 must run first (per kanji, before any file writing) — ordering within the skill is critical.
- Component file routing: Primitives/ for non-learnable primitives; Kanji/ for standalone JLPT kanji.
- Rename rule applies only to files created or modified during the current run — not pre-existing untouched files.
- SM-2 state is not affected; no changes to grammar-state.json or any practice skill.
- Do not break existing behavior: KanjiList.md update, occurrence appending, file creation in Kaligrafia/Kanji/ all remain unchanged.
