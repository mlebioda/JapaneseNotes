# Lesson Coverage Table

Generated 2026-09-06. "Covered" = at least one `grammar-state.json` entry keyed with this lesson's code (i.e. practiced at least once via `lesson-grammar-practice`). "Extracted" = the lesson file contains at least one `→ [[grammar-index/grammar/...]]` link (i.e. `extract-grammar` has been run on it, at least partially).

| File        | Covered in grammar-state.json | Extracted to grammar-index |
| ----------- | ----------------------------- | -------------------------- |
| UN5GL1L2.md | Yes (8 points)                | Yes (10 links)             |
| UN5GL3.md   | Yes (7 points)                | Yes (10 links)             |
| UN5GL4.md   | Yes (6 points)                | Yes (15 links)             |
| UN5GL5.md   | Yes (5 points)                | Yes (8 links)              |
| UN5GL6.md   | Yes (12 points)               | Yes (13 links)             |
| UN5GL7.md   | Yes (12 points)               | No                         |
| UN5GL8.md   | Yes (8 points)                | No                         |
| UN5GL9.md   | Yes (17 points)               | No                         |
| UN5GL10.md  | Yes (23 points)               | No                         |
| UN5GL11.md  | Yes (17 points)               | **Ready to extract**       |
| UN5GL12.md  | **No**                        | Yes (9 links)              |
| UN5GL13.md  | Yes (9 points)                | **Ready to extract**       |
| UN5GL14.md  | Yes (20 points)               | Yes (21 links)             |
| UN5GL15.md  | Yes (8 points)                | **Ready to extract**       |
| UN4GL1.md   | Yes (17 points)               | Yes (20 links)             |
| UN4GL2.md   | Yes (10 points)               | Yes (11 links)             |
| UN4GL3.md   | Yes (10 points)               | Yes (11 links)             |
| UN4GL4.md   | Yes (11 points)               | Yes (11 links)             |
| UN4GL5.md   | Yes (20 points)               | Yes (10 links)             |
| UN4GL6.md   | Yes (9 points)                | Yes (11 links)             |
| UN4GL7.md   | Yes (9 points)                | Yes (9 links)              |
| UN4GL8.md   | Yes (8 points)                | Yes (9 links)              |
| UN4GL9.md   | Yes (8 points)                | Yes (9 links)              |
| UN4GL10.md  | Yes (7 points)                | Yes (7 links)              |
| UN4GL11.md  | Yes (5 points)                | Yes (5 links)              |
| UN4GL12.md  | Yes (8 points)                | Yes (8 links)              |
| UN4GL13.md  | Yes (17 points)               | Yes (22 links)             |
| UN4GL14.md  | Yes (8 points)                | Yes (10 links)             |
| UN4GL15.md  | Yes (11 points)               | Yes (13 links)             |

## Notes

- **Resolved since the last generation (2026-08-13)**:
  - **UN4GL1** was previously covered-but-unextracted (16 points, No). It's now both: extracted this session (12 grammar points + 2 containers → 20 wikilinks), and its `grammar-state.json` entries were repointed from the raw lesson file to the new `grammar-index/grammar/...` files — one entry (`konna-sonna-anna`) was split into two since that heading resolved to a container with two distinct child files, netting 17 covered points.
  - **UN4GL3** was previously extracted-but-uncovered by this table (No), but had actually already been extracted to 11 links in a prior session (commit `eac73ca`, "extraction and refinement of un4gl3, un4gl2") that predates this table's last generation — this refresh is just catching the table up, not new work.
- **UN5GL12** remains the sole exception in the other direction: extracted (9 links) but still zero `grammar-state.json` entries — still the best candidate to run `lesson-grammar-practice` on next, since it'll link straight to the already-extracted files.
- No lesson is currently untouched by *both* pipelines (No/No) — every file has at least one of the two.
- Link/point counts don't need to match 1:1 even for fully-extracted lessons: a container heading produces one wikilink but is never itself a drill point, and vice versa some drilled points may not (yet) be extracted.
- Row counts cross-checked against the raw file: sum of per-file "Covered" counts (310) matches the total key count in `grammar-state.json` (310) exactly — every entry is accounted for.
