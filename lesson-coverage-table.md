# Lesson Coverage Table

Generated 2026-08-05. "Covered" = at least one `grammar-state.json` entry keyed with this lesson's code (i.e. practiced at least once via `lesson-grammar-practice`). "Extracted" = the lesson file contains at least one `→ [[grammar-index/grammar/...]]` link (i.e. `extract-grammar` has been run on it, at least partially).

| File | Covered in grammar-state.json | Extracted to grammar-index |
|---|---|---|
| UN4GL1.md | Yes (16 points) | No |
| UN4GL2.md | Yes (10 points) | No |
| UN4GL3.md | Yes (10 points) | No |
| UN4GL4.md | Yes (11 points) | Yes (11 links) |
| UN4GL5.md | Yes (20 points) | Yes (10 links) |
| UN4GL6.md | Yes (9 points) | Yes (11 links) |
| UN4GL7.md | Yes (9 points) | Yes (9 links) |
| UN4GL8.md | Yes (8 points) | Yes (9 links) |
| UN4GL9.md | Yes (8 points) | Yes (9 links) |
| UN4GL10.md | Yes (7 points) | Yes (7 links) |
| UN4GL11.md | Yes (5 points) | Yes (5 links) |
| UN4GL12.md | Yes (8 points) | Yes (8 links) |
| UN4GL13.md | Yes (17 points) | Yes (22 links) |
| UN4GL14.md | Yes (8 points) | Yes (10 links) |
| UN4GL15.md | **No** | Yes (13 links) |
| UN5GL1L2.md | Yes (8 points) | Yes (10 links) |
| UN5GL3.md | Yes (7 points) | Yes (10 links) |
| UN5GL4.md | Yes (6 points) | Yes (15 links) |
| UN5GL5.md | Yes (5 points) | Yes (8 links) |
| UN5GL6.md | Yes (12 points) | Yes (13 links) |
| UN5GL7.md | Yes (12 points) | No |
| UN5GL8.md | Yes (8 points) | No |
| UN5GL9.md | Yes (17 points) | No |
| UN5GL10.md | Yes (23 points) | No |
| UN5GL11.md | Yes (17 points) | No |
| UN5GL12.md | **No** | No |
| UN5GL13.md | Yes (9 points) | No |
| UN5GL14.md | **No** | Yes (21 links) |
| UN5GL15.md | Yes (8 points) | No |

## Notes

- **UN4GL15** and **UN5GL14** are extracted but never practiced (drilled) — good candidates to run `lesson-grammar-practice` on, since a fresh session there will now link straight to the already-extracted files.
- **UN5GL12** is the only lesson neither practiced nor extracted at all — fully untouched by either pipeline.
- Link/point counts don't need to match 1:1 even for fully-extracted lessons: a container heading produces one wikilink but is never itself a drill point, and vice versa some drilled points may not (yet) be extracted.
- Row counts cross-checked against the raw file: sum of per-file "Covered" counts (278) matches the total key count in `grammar-state.json` (278) exactly — every entry is accounted for.
- **Correction from the first version of this table**: UN5GL13 and UN5GL15 were reported as uncovered in the version generated a few minutes earlier in this session — `grammar-state.json` genuinely changed in between (confirmed via `git diff --cached`, 17 new entries appeared under those two codes in the staged index that weren't in HEAD). This regenerated version reflects the file's current on-disk state.
