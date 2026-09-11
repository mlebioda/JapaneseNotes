# Lesson Coverage Table

Generated 2026-09-06, last refreshed 2026-09-11. "Covered" = at least one `grammar-state.json` entry keyed with this lesson's code (i.e. practiced at least once via `lesson-grammar-practice`). "Extracted" = the lesson file contains at least one `→ [[grammar-index/grammar/...]]` link (i.e. `extract-grammar` has been run on it, at least partially).

| File        | Covered in grammar-state.json | Extracted to grammar-index |
| ----------- | ----------------------------- | -------------------------- |
| UN5GL1L2.md | Yes (8 points)                | Yes (9 links)               |
| UN5GL3.md   | Yes (5 points)                | Yes (7 links)               |
| UN5GL4.md   | Yes (6 points)                | Yes (14 links)              |
| UN5GL5.md   | Yes (6 points)                | Yes (9 links)               |
| UN5GL6.md   | Yes (13 points)               | Yes (13 links)              |
| UN5GL7.md   | Yes (12 points)               | Yes (16 links)              |
| UN5GL8.md   | Yes (10 points)               | Yes (16 links)              |
| UN5GL9.md   | Yes (15 points)               | Yes (21 links)              |
| UN5GL10.md  | Yes (23 points)               | Yes (26 links)              |
| UN5GL11.md  | Yes (19 points)               | Yes (22 links)              |
| UN5GL12.md  | Yes (9 points)                | Yes (10 links)              |
| UN5GL13.md  | Yes (9 points)                | Yes (11 links)              |
| UN5GL14.md  | Yes (20 points)               | Yes (21 links)              |
| UN5GL15.md  | Yes (7 points)                | Yes (10 links)              |
| UN4GL1.md   | Yes (17 points)               | Yes (20 links)              |
| UN4GL2.md   | Yes (10 points)               | Yes (11 links)              |
| UN4GL3.md   | Yes (10 points)               | Yes (11 links)              |
| UN4GL4.md   | Yes (11 points)               | Yes (11 links)              |
| UN4GL5.md   | Yes (20 points)               | Yes (10 links)              |
| UN4GL6.md   | Yes (9 points)                | Yes (11 links)              |
| UN4GL7.md   | Yes (9 points)                | Yes (9 links)               |
| UN4GL8.md   | Yes (8 points)                | Yes (9 links)               |
| UN4GL9.md   | Yes (8 points)                | Yes (9 links)               |
| UN4GL10.md  | Yes (7 points)                | Yes (7 links)               |
| UN4GL11.md  | Yes (5 points)                | Yes (5 links)               |
| UN4GL12.md  | Yes (8 points)                | Yes (8 links)               |
| UN4GL13.md  | Yes (17 points)               | Yes (22 links)              |
| UN4GL14.md  | Yes (8 points)                | Yes (10 links)              |
| UN4GL15.md  | Yes (11 points)               | Yes (13 links)              |

## Notes

- **Resolved since the last generation (2026-09-07 → 2026-09-10)**: this was the big batch — six of the seven remaining covered-but-unextracted N5 lessons got extracted, leaving only two rows unextracted in the whole table.
  - **UN5GL1L2** (commit `5a59212`, "un5gl1l2 extracted"), **UN5GL5** (`8299aae`), **UN5GL6** (`698ce49`), and **UN5GL7/8/9/10** (bulk-extracted in `0cb6b7a` "extract un5gl15", then individually refined in `2e15315` "extraction un5gl8" and `e8cfaf3` "extract un5gl9") all moved from **No** to extracted (9, 9, 13, 16, 16, 21, and 26 links respectively).
  - **UN5GL12** moved from **No** covered to **Yes (9 points)** — the sole covered/extracted mismatch from the last refresh is now resolved; its `grammar-state.json` entries were added in `ad35a1a` and touched again in the `cc82e6f` dedup refactor.
  - A broad "refactor of notes, lists of jlpt topics, removing duplicates" pass (`cc82e6f`, 2026-09-10) rewrote `grammar-state.json` and several lesson files to remove duplicate grammar points, which is why some per-lesson point counts moved *down* as well as up since the last refresh (e.g. UN5GL3 7→5, UN5GL9 17→15, UN5GL15 8→7) alongside the growth from newly-covered/extracted lessons. This pass also added `JLPT-N3/N4/N5-Grammar-List.md` at the vault root.
- **Resolved since the last refresh (2026-09-10 → 2026-09-11)**: **UN5GL3** (7 links) and **UN5GL4** (14 links) both moved from **No** to extracted, closing out the last two unextracted rows in the whole table. UN5GL4's `grammar-state.json` entries were also relinked from the raw lesson file to their new `grammar-index/grammar/` files (`years`, `nengappi-dates`, `time`, `directions`, `or-kaka`); UN5GL3's 5 entries were likewise relinked (`mai-counter-for-flat-thin-objects`, `koko-soko-asoko-...`, `kochira-sochira-achira-dochira-...`, `p-ni-n-ga-arimasu-imasu-...`, `something-is-somewhere`). Two files from each lesson's extraction (UN5GL3: `indicating-directions`, `location-of-the-objects-with-directions`; UN5GL4: `months`, `weeks`, `period-of-time`, `date-time`) have no SRS entry yet — they're correctly wikilinked from their lesson files but have never been drilled.
- Every lesson row is now **Yes/Yes** — no lesson is untouched by either pipeline, and none remain unextracted.
- Link/point counts don't need to match 1:1 even for fully-extracted lessons: a container heading produces one wikilink but is never itself a drill point, and vice versa some drilled points may not (yet) be extracted.
- Row counts cross-checked against the raw files as of 2026-09-11: sum of per-file "Covered" counts (320) matches the total key count in `grammar-state.json` (320) exactly.
