# Tasks: fill-templates kanji trainer links

**Date:** 2026-06-07
**Plan:** `Plans/fill-templates-kanji-links-plan.md`
**Target files:** `.cowork/skills/fill-templates.md`
**Status:** done

---

## Task list

| # | File | Change | Status |
|---|------|--------|--------|
| 1 | **fill-templates.md** | Add kanji link generation rule to Step 4 and Step 5 fill passes: after writing all conjugation/adjective rows for a template, collect CJK kanji (U+4E00–U+9FFF) from the completed template text, deduplicate by first occurrence, append one `<a href="...">X</a>` line per kanji, preserve trailing blank separator line | [x] |
| 2 | **fill-templates.md** | Update the `#wc` godan/ichidan card format reference example under `## Card format reference` to include the kanji link block | [x] |

---

## Notes

- Deduplication is per-template only (not cross-card).
- No HTTP calls — links are pure string construction.
- The blank line between cards must be preserved after the link block.
- Hiragana, katakana, romaji, and punctuation must NOT produce links.
